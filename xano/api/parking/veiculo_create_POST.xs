query "veiculo" verb=POST {
  api_group = "Estacionamento"
  input {
    text plate filters=trim|upper
    text model filters=trim
    text color filters=trim
    text type
    int? mensalista_id?
  }
  stack {
    db.add veiculo {
      data = {
        plate: $input.plate
        model: $input.model
        color: $input.color
        type: $input.type
        mensalista_id: $input.mensalista_id
      }
    } as $veiculo
  }
  response = $veiculo
  guid = "P_cq0qWRBkRrJvD_KCctW7_Qsv8"
}
