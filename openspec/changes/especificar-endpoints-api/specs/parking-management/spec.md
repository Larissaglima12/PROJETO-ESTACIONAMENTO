# Spec Delta

## ADDED Requirements

### Requirement: Endpoints CRUD para Entidades
O sistema SHALL fornecer endpoints RESTful no Xano para operações CRUD (Criar, Ler, Atualizar e Deletar) nas tabelas `usuario`, `mensalista`, `veiculo` e `vaga`.

#### Scenario: Consulta de registros
- **WHEN** uma requisição GET é feita para listar registros de uma entidade
- **THEN** o sistema retorna a lista paginada dos registros correspondentes

#### Scenario: Criação de registro
- **WHEN** uma requisição POST é enviada com dados válidos para uma entidade
- **THEN** o sistema valida os dados, persiste o registro e retorna o objeto criado

### Requirement: Registro de Entrada de Veículo via API
O sistema SHALL fornecer um endpoint POST para registrar a entrada de um veículo, associando-o a uma vaga livre e validando se a placa já possui permanência ativa.

#### Scenario: Entrada bem-sucedida
- **WHEN** uma requisição de entrada é enviada com placa válida e há vaga disponível
- **THEN** o sistema cria o registro de movimentação, atualiza o status da vaga para ocupada e retorna os dados da entrada

#### Scenario: Vaga indisponível
- **WHEN** uma entrada é solicitada e todas as vagas compatíveis estão ocupadas
- **THEN** o sistema rejeita a operação com erro informando a indisponibilidade de vagas

### Requirement: Consulta de Ocupação de Vagas via API
O sistema SHALL fornecer um endpoint GET para consultar o status atual de ocupação das vagas do estacionamento.

#### Scenario: Consultar sumário de vagas
- **WHEN** o endpoint de ocupação é consultado
- **THEN** o sistema retorna a quantidade total, vagas livres e vagas ocupadas

### Requirement: Registro de Saída de Veículo via API
O sistema SHALL fornecer um endpoint POST para registrar a saída de um veículo, calcular o valor devido com base no tempo de permanência e liberar a vaga associada.

#### Scenario: Saída e cálculo de tarifa
- **WHEN** uma solicitação de saída é feita para uma placa com permanência ativa
- **THEN** o sistema calcula a permanência (arredondando para a próxima hora), determina o valor, encerra a movimentação e libera a vaga
