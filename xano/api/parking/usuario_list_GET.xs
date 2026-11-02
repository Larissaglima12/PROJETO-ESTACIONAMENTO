query "usuario" verb=GET {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
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

    db.query usuario {
      return = {type: "list"}
      output = ["id", "created_at", "name", "email", "type"]
    } as $usuarios
  }
  response = $usuarios
}
