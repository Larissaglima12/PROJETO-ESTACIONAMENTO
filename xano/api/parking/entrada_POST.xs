query "parking/entrada" verb=POST {
  api_group = "Estacionamento"
  input {
    int veiculo_id { table = "veiculo" }
    int vaga_id { table = "vaga" }
    int usuario_id { table = "usuario" }
  }
  stack {
    db.add movimentacao {
      data = {
        veiculo_id: $input.veiculo_id
        vaga_id: $input.vaga_id
        usuario_id: $input.usuario_id
        entry_time: "now"
      }
    } as $mov
    db.patch vaga {
      field_name = "id"
      field_value = $input.vaga_id
      data = {
        status: "ocupada"
      }
    } as $vaga_atualizada
  }
  response = {
    movimentacao: $mov,
    vaga: $vaga_atualizada
  }
  guid = "AFyckYEmWO7eu-z82JyYL2FpnpQ"
}
