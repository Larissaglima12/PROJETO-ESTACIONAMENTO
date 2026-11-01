query "usuario" verb=POST {
  api_group = "Estacionamento"
  input {
    text name filters=trim
    email email filters=trim|lower
    password password
    text type
  }
  stack {
    db.add usuario {
      data = {
        name: $input.name
        email: $input.email
        password: $input.password
        type: $input.type
      }
    } as $usuario
  }
  response = $usuario
  guid = "mTF2B0UvPOYsSzj7bhJphjnWT38"
}
