# parking-management Specification

## Purpose
Define a estrutura de dados e tabelas relacionais no Xano necessárias para o funcionamento do sistema de estacionamento (usuários, mensalistas, veículos, vagas e movimentações).

## Requirements

### Requirement: Tabela USUARIO
O sistema SHALL possuir uma tabela USUARIO para armazenar os dados de autenticação e perfil dos usuários do sistema com os campos nome, email, senha e tipo.

#### Scenario: Cadastro de usuário
- **WHEN** um novo usuário é cadastrado com nome, email, senha e tipo
- **THEN** o sistema armazena o registro na tabela USUARIO

### Requirement: Tabela MENSALISTA
O sistema SHALL possuir uma tabela MENSALISTA para gerenciar os clientes mensalistas com os campos nome, telefone, valor_mensalidade, data_inicio, data_fim e status.

#### Scenario: Cadastro de mensalista
- **WHEN** um mensalista é cadastrado com dados válidos e período de vigência
- **THEN** o sistema registra o mensalista na tabela MENSALISTA com status ativo

### Requirement: Tabela VEICULO
O sistema SHALL possuir uma tabela VEICULO para cadastrar os veículos com placa, modelo, cor, tipo e vinculo opcional com um mensalista (mensalista_id).

#### Scenario: Cadastro de veículo vinculado
- **WHEN** um veículo é cadastrado associado a um mensalista existente
- **THEN** o sistema registra a placa, modelo, cor, tipo e mensalista_id

### Requirement: Tabela VAGA
O sistema SHALL possuir uma tabela VAGA para gerenciar as vagas de estacionamento com os campos numero, tipo e status.

#### Scenario: Cadastro de vaga
- **WHEN** uma nova vaga é criada com número, tipo e status inicial livre
- **THEN** o sistema registra a vaga na tabela VAGA

### Requirement: Tabela MOVIMENTACAO
O sistema SHALL possuir uma tabela MOVIMENTACAO para registrar as entradas e saídas de veículos associando veiculo_id, vaga_id, usuario_id, entrada, saida e valor.

#### Scenario: Registro de movimentação
- **WHEN** uma entrada ou saída de veículo é processada
- **THEN** o sistema registra a movimentação relacionando veículo, vaga, usuário operador, horários e valores

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
