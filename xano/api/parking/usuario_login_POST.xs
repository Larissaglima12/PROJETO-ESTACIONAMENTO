query "usuario/login" verb=POST {
  api_group = "Estacionamento"
  input {
    email email? filters=trim|lower
    text password?
  }
  stack {
    db.get usuario {
      field_name = "email"
      field_value = $input.email
      output = ["id", "name", "email", "password", "type"]
    } as $user

    precondition ($user != null) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }

    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $pass_result

    precondition ($pass_result) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }

    security.create_auth_token {
      table = "usuario"
      extras = {type: $user.type}
      expiration = 86400
      id = $user.id
    } as $authToken
  }
  response = {
    authToken: $authToken,
    user: {
      id: $user.id,
      name: $user.name,
      email: $user.email,
      type: $user.type
    }
  }
  guid = "XpeZTlCdSJ0XgAtPnoArUSoQ9BY"
}
