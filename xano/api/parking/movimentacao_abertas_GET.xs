query "parking/movimentacao/abertas" verb=GET {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
  }
  stack {
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
        movimentacao_id: $db.movimentacao.id,
        veiculo_id: $db.movimentacao.veiculo_id,
        vaga_id: $db.movimentacao.vaga_id,
        plate: $db.veiculo.plate,
        model: $db.veiculo.model,
        vaga_number: $db.vaga.number,
        entry_time: $db.movimentacao.entry_time
      }
      where = $db.movimentacao.exit_time == null && $db.movimentacao.cancelled == false
      sort = { entry_time: "asc" }
      return = { type: "list" }
    } as $movimentacoes_abertas
  }
  response = $movimentacoes_abertas
  guid = "MovimentacaoAbertasGetEndpoint01"
}
