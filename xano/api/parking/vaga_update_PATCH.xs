query "vaga/{vaga_id}" verb=PATCH {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
    int vaga_id { table = "vaga" }
    int? number? filters=min:1
    enum? type? { values = ["carro", "moto", "idoso", "deficiente"] }
    bool? active?
  }
  stack {
    db.transaction {
      stack {
        // 1. Validar e buscar usuário administrador
        db.get usuario {
          field_name = "id"
          field_value = $auth.id
        } as $current_user

        precondition ($current_user != null && $current_user.type == "admin") {
          error_type = "accessdenied"
          error = "Admin access required"
        }

        // 2. Buscar e validar existência da vaga
        db.get vaga {
          field_name = "id"
          field_value = $input.vaga_id
        } as $vaga

        precondition ($vaga != null) {
          error_type = "notfound"
          error = "Vaga não encontrada."
        }

        // 3. Validar unicidade do número da vaga caso tenha sido alterado
        conditional {
          if (($input.number != null) && ($input.number != $vaga.number)) {
            db.has vaga {
              field_name = "number"
              field_value = $input.number
            } as $exists

            precondition (!$exists) {
              error_type = "inputerror"
              error = "Já existe uma vaga cadastrada com este número."
            }
          }
        }

        // 4. Validar regras de segurança ao desativar a vaga (active = false)
        conditional {
          if (($input.active != null) && ($input.active == false) && ($vaga.active == true)) {
            precondition ($vaga.status != "ocupada") {
              error_type = "inputerror"
              error = "Não é possível desativar uma vaga que está ocupada."
            }

            db.query movimentacao {
              where = $db.movimentacao.vaga_id == $input.vaga_id && $db.movimentacao.exit_time == null && $db.movimentacao.cancelled == false
              return = { type: "exists" }
            } as $mov_aberta

            precondition (!$mov_aberta) {
              error_type = "inputerror"
              error = "Não é possível desativar uma vaga com movimentação em aberto."
            }
          }
        }

        // 5. Construir objeto de atualização dinamicamente
        var $updates { value = {} }

        conditional {
          if ($input.number != null) {
            var.update $updates.number { value = $input.number }
          }
        }
        conditional {
          if ($input.type != null) {
            var.update $updates.type { value = $input.type }
          }
        }
        conditional {
          if ($input.active != null) {
            var.update $updates.active { value = $input.active }
          }
        }

        precondition (($updates|is_empty) == false) {
          error_type = "inputerror"
          error = "Nenhuma alteração informada."
        }

        // 6. Executar patch na vaga
        db.patch vaga {
          field_name = "id"
          field_value = $input.vaga_id
          data = $updates
        } as $vaga_atualizada
      }
    }
  }
  response = $vaga_atualizada
  guid = "VagaUpdatePatchEndpoint001"
}
