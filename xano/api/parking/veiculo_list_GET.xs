query "veiculo" verb=GET {
  api_group = "Estacionamento"
  input {
  }
  stack {
    db.query veiculo {
      return = {type: "list"}
    } as $veiculos
  }
  response = $veiculos
  guid = "nztk09_PkGZXMR7JXxm7SzbhmUc"
}
