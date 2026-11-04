query "parking/saida" verb=POST {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
    int movimentacao_id { table = "movimentacao" }
  }
  stack {
    db.get movimentacao {
      field_name = "id"
      field_value = $input.movimentacao_id
    } as $mov
    db.patch movimentacao {
      field_name = "id"
      field_value = $input.movimentacao_id
      data = {
        exit_time: "now"
        amount: 15.00
      }
    } as $mov_atualizada
    db.patch vaga {
      field_name = "id"
      field_value = $mov.vaga_id
      data = {
        status: "livre"
      }
    } as $vaga_atualizada
  }
  response = {
    movimentacao: $mov_atualizada,
    vaga: $vaga_atualizada
  }
  guid = "U8nLTJodQBXd4awKf5wJodzg1Uo"
}
