query "vaga/ocupacao" verb=GET {
  api_group = "Estacionamento"
  input {
  }
  stack {
    db.query vaga {
      where = $db.vaga.status == "livre"
      return = {type: "count"}
    } as $livres
    db.query vaga {
      where = $db.vaga.status == "ocupada"
      return = {type: "count"}
    } as $ocupadas
  }
  response = {
    livres: $livres,
    ocupadas: $ocupadas
  }
  guid = "mNM00ewqwL0Sp5GcXfWxlBzhTFk"
}
