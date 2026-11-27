query "vaga" verb=POST {
  api_group = "Estacionamento"
  auth = "usuario"
  input {
    int number filters=min:1
    enum type?="carro" { values = ["carro", "moto", "idoso", "deficiente"] }
  }
  stack {
    db.get usuario {
      field_name = "id"
      field_value = $auth.id
    } as $current_user

    precondition ($current_user != null && $current_user.type == "admin") {
      error_type = "accessdenied"
      error = "Admin access required"
    }

    db.has vaga {
      field_name = "number"
      field_value = $input.number
    } as $exists

    precondition (!$exists) {
      error_type = "inputerror"
      error = "Já existe uma vaga cadastrada com este número."
    }

    db.add vaga {
      data = {
        number: $input.number
        type: $input.type
        status: "livre"
        active: true
      }
    } as $vaga
  }
  response = $vaga
  guid = "Yli-02vCHdHfcB3iupqSVkSoWkw"
}
