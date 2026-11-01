table "mensalista" {
  auth = false
  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    text phone filters=trim
    decimal monthly_fee filters=min:0
    date start_date
    date end_date
    enum status?="ativo" { values = ["ativo", "inativo", "suspenso"] }
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "status"}]}
  ]
}
