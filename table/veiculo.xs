table veiculo {
  auth = false

  schema {
    int id
    timestamp created_at?=now
  
    // Placa do veículo
    text plate filters=trim|upper
  
    text model filters=trim
    text color filters=trim
    enum type {
      values = ["carro", "moto", "outro"]
    }
  
    // Referência opcional ao mensalista
    int mensalista_id? {
      table = "mensalista"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "plate"}]}
    {type: "btree", field: [{name: "mensalista_id"}]}
  ]

  guid = "tih54v3AwkdF-eInK1TzeJZN3rY"
}