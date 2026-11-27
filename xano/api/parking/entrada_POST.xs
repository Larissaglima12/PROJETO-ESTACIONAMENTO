query "parking/entrada" verb=POST {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
    int veiculo_id { table = "veiculo" }
    int vaga_id { table = "vaga" }
  }
  stack {
    db.transaction {
      stack {
        // 1. Validar e buscar veículo
        db.get veiculo {
          field_name = "id"
          field_value = $input.veiculo_id
        } as $veiculo

        precondition ($veiculo != null) {
          error_type = "notfound"
          error = "Veículo não encontrado."
        }

        // 2. Validar e buscar vaga
        db.get vaga {
          field_name = "id"
          field_value = $input.vaga_id
        } as $vaga

        precondition ($vaga != null) {
          error_type = "notfound"
          error = "Vaga não encontrada."
        }

        precondition ($vaga.active == true) {
          error_type = "inputerror"
          error = "A vaga selecionada está desativada."
        }

        precondition ($vaga.status == "livre") {
          error_type = "inputerror"
          error = "A vaga selecionada não está livre."
        }

        // 3. Bloquear movimentação aberta para o mesmo veículo
        db.query movimentacao {
          where = $db.movimentacao.veiculo_id == $input.veiculo_id && $db.movimentacao.exit_time == null && $db.movimentacao.cancelled == false
          return = { type: "exists" }
        } as $veiculo_ocupado

        precondition (!$veiculo_ocupado) {
          error_type = "inputerror"
          error = "O veículo já possui uma movimentação em aberto."
        }

        // 4. Bloquear movimentação aberta para a mesma vaga
        db.query movimentacao {
          where = $db.movimentacao.vaga_id == $input.vaga_id && $db.movimentacao.exit_time == null && $db.movimentacao.cancelled == false
          return = { type: "exists" }
        } as $vaga_ocupada

        precondition (!$vaga_ocupada) {
          error_type = "inputerror"
          error = "A vaga já possui uma movimentação em aberto."
        }

        // 5. Criar a movimentação com cancelled = false e usuario_id do auth
        db.add movimentacao {
          data = {
            veiculo_id: $input.veiculo_id
            vaga_id: $input.vaga_id
            usuario_id: $auth.id
            entry_time: "now"
            cancelled: false
          }
        } as $mov

        // 6. Atualizar a vaga para status = "ocupada"
        db.patch vaga {
          field_name = "id"
          field_value = $input.vaga_id
          data = {
            status: "ocupada"
          }
        } as $vaga_atualizada
      }
    }
  }
  response = {
    movimentacao: $mov,
    vaga: $vaga_atualizada
  }
  guid = "AFyckYEmWO7eu-z82JyYL2FpnpQ"
}
