query "mensalista" verb=GET {
  api_group = "Estacionamento"
  input {
  }
  stack {
    db.query mensalista {
      return = {type: "list"}
    } as $mensalistas
  }
  response = $mensalistas
  guid = "tRD3_nv3sW_0rJPlJpTR3ADWQfI"
}
