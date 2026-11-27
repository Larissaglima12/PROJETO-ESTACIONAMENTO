query "parking/saida" verb=POST {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
    int movimentacao_id { table = "movimentacao" }
  }
  stack {
    db.transaction {
      stack {
        // 1. Buscar e validar movimentação
        db.get movimentacao {
          field_name = "id"
          field_value = $input.movimentacao_id
        } as $mov

        precondition ($mov != null) {
          error_type = "notfound"
          error = "Movimentação não encontrada."
        }

        precondition ($mov.exit_time == null && $mov.cancelled == false) {
          error_type = "inputerror"
          error = "Esta movimentação já foi encerrada ou cancelada."
        }

        precondition ($mov.entry_time != null) {
          error_type = "inputerror"
          error = "Horário de entrada da movimentação inválido ou ausente."
        }

        // 2. Buscar veículo vinculado
        db.get veiculo {
          field_name = "id"
          field_value = $mov.veiculo_id
        } as $veiculo

        precondition ($veiculo != null) {
          error_type = "notfound"
          error = "Veículo associado não encontrado."
        }

        // 3. Buscar e validar vaga associada (garantindo que existe e está ocupada)
        db.get vaga {
          field_name = "id"
          field_value = $mov.vaga_id
        } as $vaga

        precondition ($vaga != null) {
          error_type = "notfound"
          error = "Vaga associada não encontrada."
        }

        precondition ($vaga.status == "ocupada") {
          error_type = "inputerror"
          error = "A vaga associada não está com status ocupada."
        }

        // 4. Definir instante de saída único (referência estática para cálculo e persistência)
        var $exit_now { value = "now" }
        var $exit_ms { value = $exit_now|to_ms }

        // 5. Calcular tempo de permanência em minutos
        var $duration_ms { value = $exit_ms - $mov.entry_time }

        precondition ($duration_ms >= 0) {
          error_type = "inputerror"
          error = "Horário de entrada inválido ou futuro."
        }

        var $duration_mins { value = $duration_ms / 60000 }

        // 6. Verificar se é mensalista ativo e válido (com fuso horário America/Sao_Paulo)
        var $is_mensalista_ativo { value = false }
        conditional {
          if ($veiculo.mensalista_id != null) {
            db.get mensalista {
              field_name = "id"
              field_value = $veiculo.mensalista_id
            } as $mensalista

            conditional {
              if (($mensalista != null) && ($mensalista.status == "ativo")) {
                var $today { value = "now"|to_timestamp|format_timestamp:"Y-m-d":"America/Sao_Paulo" }
                conditional {
                  if (($today >= $mensalista.start_date) && ($today <= $mensalista.end_date)) {
                    var.update $is_mensalista_ativo { value = true }
                  }
                }
              }
            }
          }
        }

        // 7. Calcular valor da cobrança (Tolerância de 10 minutos, R$ 5 por fração de 15 min, teto de R$ 50)
        var $amount { value = 0.00 }

        conditional {
          if (($is_mensalista_ativo == false) && ($duration_mins > 10)) {
            var $fracoes { value = ($duration_mins / 15)|ceil }
            var $calculated { value = $fracoes * 5.00 }
            var.update $amount { value = $calculated|min:50.00 }
          }
        }

        // 8. Atualizar movimentação
        db.patch movimentacao {
          field_name = "id"
          field_value = $input.movimentacao_id
          data = {
            exit_time: $exit_now
            amount: $amount
          }
        } as $mov_atualizada

        // 9. Atualizar vaga para livre
        db.patch vaga {
          field_name = "id"
          field_value = $mov.vaga_id
          data = {
            status: "livre"
          }
        } as $vaga_atualizada
      }
    }
  }
  response = {
    movimentacao: $mov_atualizada,
    vaga: $vaga_atualizada
  }
  guid = "U8nLTJodQBXd4awKf5wJodzg1Uo"
}
