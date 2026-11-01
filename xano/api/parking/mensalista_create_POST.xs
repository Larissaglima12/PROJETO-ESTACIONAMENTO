query "mensalista" verb=POST {
  api_group = "Estacionamento"
  input {
    text name filters=trim
    text phone filters=trim
    decimal monthly_fee filters=min:0
    date start_date
    date end_date
  }
  stack {
    db.add mensalista {
      data = {
        name: $input.name
        phone: $input.phone
        monthly_fee: $input.monthly_fee
        start_date: $input.start_date
        end_date: $input.end_date
        status: "ativo"
      }
    } as $mensalista
  }
  response = $mensalista
  guid = "gqs6S477irTRb9WRowMC1CPT6qE"
}
