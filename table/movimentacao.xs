table movimentacao {
  auth = false

  schema {
    int id
    timestamp created_at?=now
  
    // Referência ao veículo
    int veiculo_id {
      table = ""
    }
  
    // Referência à vaga
    int vaga_id {
      table = ""
    }
  
    // Referência ao usuário operador
    int usuario_id {
      table = "usuario"
    }
  
    // Horário de entrada
    timestamp entry_time?=now
  
    // Horário de saída
    timestamp? exit_time?
  
    // Valor cobrado
    decimal? amount? filters=min:0
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "veiculo_id"}]}
    {type: "btree", field: [{name: "vaga_id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "entry_time", op: "desc"}]}
  ]

  guid = "xMduFiYO65GsXuKGU36i8h7OtwQ"
}