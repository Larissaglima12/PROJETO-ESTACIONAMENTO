query "parking/financeiro" verb=GET {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
    timestamp? start_date?
    timestamp? end_date?
  }
  stack {
    // 1. Validar se o usuário é administrador
    db.get usuario {
      field_name = "id"
      field_value = $auth.id
    } as $current_user

    precondition ($current_user != null && $current_user.type == "admin") {
      error_type = "accessdenied"
      error = "Acesso exclusivo para administradores."
    }

    // 2. Buscar movimentações finalizadas com join para detalhes do veículo
    db.query movimentacao {
      join = {
        veiculo: {
          table: "veiculo",
          type: "inner",
          where: $db.movimentacao.veiculo_id == $db.veiculo.id
        },
        vaga: {
          table: "vaga",
          type: "inner",
          where: $db.movimentacao.vaga_id == $db.vaga.id
        }
      }
      eval = {
        id: $db.movimentacao.id,
        plate: $db.veiculo.plate,
        vaga_number: $db.vaga.number,
        entry_time: $db.movimentacao.entry_time,
        exit_time: $db.movimentacao.exit_time,
        amount: $db.movimentacao.amount
      }
      where = $db.movimentacao.exit_time != null && $db.movimentacao.cancelled == false && $db.movimentacao.exit_time >=? $input.start_date && $db.movimentacao.exit_time <=? $input.end_date
      sort = { exit_time: "desc" }
      return = { type: "list" }
    } as $movs

    // 3. Inicializar variáveis para agregação
    var $total_faturado { value = 0.0 }
    var $total_dia { value = 0.0 }
    var $total_mes { value = 0.0 }
    var $count { value = $movs|count }
    var $today { value = "now"|to_timestamp|format_timestamp:"Y-m-d":"America/Sao_Paulo" }
    var $this_month { value = "now"|to_timestamp|format_timestamp:"Y-m":"America/Sao_Paulo" }

    // 4. Processar movimentações para calcular totais
    foreach ($movs) {
      each as $m {
        var.update $total_faturado { value = $total_faturado + ($m.amount ?? 0.0) }

        var $m_day { value = $m.exit_time|to_timestamp|format_timestamp:"Y-m-d":"America/Sao_Paulo" }
        var $m_month { value = $m.exit_time|to_timestamp|format_timestamp:"Y-m":"America/Sao_Paulo" }

        conditional {
          if ($m_day == $today) {
            var.update $total_dia { value = $total_dia + ($m.amount ?? 0.0) }
          }
        }

        conditional {
          if ($m_month == $this_month) {
            var.update $total_mes { value = $total_mes + ($m.amount ?? 0.0) }
          }
        }
      }
    }

    // 5. Calcular ticket médio
    var $ticket_medio { value = 0.0 }
    conditional {
      if ($count > 0) {
        var.update $ticket_medio { value = $total_faturado / $count }
      }
    }
  }
  response = {
    total_faturado: $total_faturado,
    faturamento_dia: $total_dia,
    faturamento_mes: $total_mes,
    movimentacoes_concluidas: $count,
    ticket_medio: $ticket_medio,
    historico: $movs
  }
  guid = "FinanceiroGetEndpoint01"
}
