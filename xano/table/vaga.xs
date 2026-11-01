table "vaga" {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    int number
    enum type?="carro" { values = ["carro", "moto", "idoso", "deficiente"] }
    enum status?="livre" { values = ["livre", "ocupada", "manutencao"] }
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "number"}]}
    {type: "btree", field: [{name: "status"}]}
  ]
}
