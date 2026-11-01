table "usuario" {
  auth = true
  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    email email filters=trim|lower { sensitive = true }
    password password { sensitive = true }
    enum type?="operador" { values = ["admin", "operador"] }
  }
  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "email"}]}
  ]
}
