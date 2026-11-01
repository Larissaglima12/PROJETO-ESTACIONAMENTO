query "vaga" verb=GET {
  api_group = "Estacionamento"
  input {
  }
  stack {
    db.query vaga {
      return = {type: "list"}
    } as $vagas
  }
  response = $vagas
  guid = "ZO9MImtsvA79R3IsRHlGHlZnWmY"
}
