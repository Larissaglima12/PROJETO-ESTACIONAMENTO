// Query all TESTE records
query teste verb=GET {
  api_group = "Event Logs"

  input {
  }

  stack {
    db.query "" {
      return = {type: "list"}
    } as $teste
  }

  response = $teste
  guid = "5EfK-QiPY7M4ancdMf_rgRGFx4M"
}