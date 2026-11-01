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

### Requirement: Referências da tabela movimentacao (estado atual)
A tabela `movimentacao` SHALL referenciar `veiculo` por `veiculo_id`, `vaga` por `vaga_id` e `usuario` por `usuario_id`, em `xano/table/movimentacao.xs`.

#### Scenario: Referências conferidas no workspace
- **WHEN** o arquivo `xano/table/movimentacao.xs` é verificado
- **THEN** os três campos apontam para as tabelas `veiculo`, `vaga` e `usuario`, e o Xano está igual ao arquivo (o dry-run não lista diferença nas tabelas do projeto).

### Requirement: Comportamento atual dos endpoints de estacionamento (as-is)
Os endpoints do grupo Estacionamento SHALL permanecer com a lógica atual nesta Change, que apenas a documenta.

#### Scenario: Entrada de veículo
- **WHEN** `entrada_POST` é chamado
- **THEN** o endpoint grava uma movimentação com `entry_time` agora e marca a vaga como ocupada
- **AND** não verifica se a vaga está livre, se o veículo já está estacionado nem se veículo e vaga existem
- **AND** recebe `usuario_id` no corpo da requisição.

#### Scenario: Saída de veículo
- **WHEN** `saida_POST` é chamado
- **THEN** o endpoint grava `exit_time` agora, define o valor fixo de R$ 15,00 e libera a vaga
- **AND** não calcula tarifa pelo tempo de permanência e não bloqueia saída duplicada.

#### Scenario: Cadastros e consultas
- **WHEN** `veiculo_create_POST`, `mensalista_create_POST`, `usuario_create_POST` ou os endpoints de listagem são chamados
- **THEN** os endpoints cadastram ou listam os registros
- **AND** `veiculo_create_POST` grava a placa em maiúsculas sem bloquear placa duplicada
- **AND** `mensalista_create_POST` cria o mensalista com status ativo sem validar vigência.

#### Scenario: Ocupação das vagas
- **WHEN** `vaga_ocupacao_GET` é chamado
- **THEN** o endpoint retorna a contagem de vagas livres e ocupadas.

### Requirement: Regras alvo de cobrança e operação (alvo)
O sistema SHALL, em Change futura, implementar as regras de negócio de referência:
- Cobrança de saída de veículos avulsos em frações de 15 minutos (R$ 3,00 por fração), com até 15 minutos gratuitos e teto diário de R$ 25,00.
- Isenção de cobrança para mensalistas ativos.
- Validação de vaga livre na entrada e bloqueio de entradas/saídas duplicadas.
- Validação de placas duplicadas e `usuario_id` obtido diretamente do token de autenticação.

#### Scenario: Planejamento das regras alvo
- **WHEN** o sistema for evoluído em Changes futuras
- **THEN** as regras de cobrança por fração de 15 min, isenção de mensalistas e validações de unicidade serão aplicadas.

### Requirement: Pendências e lacunas identificadas
O sistema SHALL registrar todas as pendências identificadas para tratamento em andamentos futuros do projeto:
1. Validação de vaga livre na entrada.
2. Prevenção de entrada duplicada para o mesmo veículo.
3. Prevenção de saída duplicada.
4. Substituição da tarifa fixa de R$ 15,00 pelo cálculo dinâmico baseado no tempo.
5. Verificação de placa duplicada no cadastro de veículos.
6. Obtenção do `usuario_id` a partir do token de autenticação em vez do corpo da requisição.
7. Validação de status do usuário no login.
8. Ausência de endpoint de criação de vaga (`vaga_create_POST`).
9. `usuario_create_POST` e `usuario_list_GET` sem autenticação adequada.
10. Login fora do grupo Estacionamento (atualmente no grupo `Authentication` usando a tabela `user`).
11. Existência de duas tabelas de usuário (`user` do template e `usuario` do projeto).
12. Bloqueio de push (`xano workspace push`) devido aos endpoints `auth/` do template.
13. Registro de teste em `movimentacao` contendo campos vazios.

#### Scenario: Listagem de pendências técnicas
- **WHEN** o projeto for auditado para novas implementações
- **THEN** as pendências de validação de vagas, duplicidade e autenticação estarão mapeadas.
