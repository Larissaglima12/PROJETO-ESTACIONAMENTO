query "vaga" verb=GET {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
  }
  stack {
    db.query vaga {
      where = $db.vaga.active == true
      sort = { number: "asc" }
      return = {type: "list"}
    } as $vagas
  }
  response = $vagas
  guid = "ZO9MImtsvA79R3IsRHlGHlZnWmY"
}
