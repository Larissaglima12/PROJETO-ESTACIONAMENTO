table "movimentacao" {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int veiculo_id {
      table = "veiculo"
      description = "Referência ao veículo"
    }
    int vaga_id {
      table = "vaga"
      description = "Referência à vaga"
    }
    int usuario_id {
      table = "usuario"
      description = "Referência ao usuário operador"
    }
    timestamp entry_time?=now {
      description = "Horário de entrada"
    }
    timestamp? exit_time? {
      description = "Horário de saída"
    }
    decimal? amount? filters=min:0 {
      description = "Valor cobrado"
    }
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "veiculo_id"}]}
    {type: "btree", field: [{name: "vaga_id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "entry_time", op: "desc"}]}
  ]
}
