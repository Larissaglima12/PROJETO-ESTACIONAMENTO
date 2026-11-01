table "veiculo" {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    text plate filters=trim|upper { description = "Placa do veículo" }
    text model filters=trim
    text color filters=trim
    enum type { values = ["carro", "moto", "outro"] }
    int mensalista_id? {
      table = "mensalista"
      description = "Referência opcional ao mensalista"
    }
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "plate"}]}
    {type: "btree", field: [{name: "mensalista_id"}]}
  ]
}
