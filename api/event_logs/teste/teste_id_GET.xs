// Get TESTE record
query "teste/{teste_id}" verb=GET {
  api_group = "Event Logs"

  input {
    int teste_id? filters=min:1
  }

  stack {
    db.get "" {
      field_name = "id"
      field_value = $input.teste_id
    } as $teste
  
    precondition ($teste != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $teste
  guid = "7WgrkecU4h2UyMfUuonE3sLBA7k"
}