query "usuario" verb=GET {
  api_group = "Estacionamento"
  input {
  }
  stack {
    db.query usuario {
      return = {type: "list"}
    } as $usuarios
  }
  response = $usuarios
  guid = "Yw0wWhRdBpu6BTsQaVyqCRJt0xE"
}
