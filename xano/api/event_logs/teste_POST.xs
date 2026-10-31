// Add TESTE record
query teste verb=POST {
  api_group = "Event Logs"

  input {
    dblink {
      table = "TESTE"
    }
  }

  stack {
    db.add TESTE {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $teste
  }

  response = $teste
  guid = "UcGR0nRhEzOI58yXTyEQhlp_nKw"
}