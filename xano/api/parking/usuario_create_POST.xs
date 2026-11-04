query "usuario" verb=POST {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
    text name filters=trim
    email email filters=trim|lower
    password password
    text type
  }
  stack {
    db.get usuario {
      field_name = "id"
      field_value = $auth.id
    } as $current_user

    precondition ($current_user != null && $current_user.type == "admin") {
      error_type = "accessdenied"
      error = "Admin access required"
    }

    db.add usuario {
      data = {
        name: $input.name
        email: $input.email
        password: $input.password
        type: $input.type
      }
    } as $usuario
  }

  response = {
    id: $usuario.id
    name: $usuario.name
    email: $usuario.email
    type: $usuario.type
  }
  guid = "mTF2B0UvPOYsSzj7bhJphjnWT38"
}
