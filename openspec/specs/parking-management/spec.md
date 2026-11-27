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

### Requirement: Login sobre a tabela usuario
O sistema SHALL autenticar operadores e administradores exclusivamente pela tabela `usuario`, por meio do endpoint `usuario_login_POST`, que emite um token de autenticação.

#### Scenario: Login válido
- **WHEN** um usuário envia e-mail e senha corretos
- **THEN** o sistema verifica a senha em hash, emite o token e retorna o token e o `type` do usuário

#### Scenario: Login inválido
- **WHEN** o e-mail não existe ou a senha está incorreta
- **THEN** o sistema rejeita com uma mensagem genérica, sem revelar qual dos dois falhou

### Requirement: Sem cadastro público de usuários
O sistema SHALL NOT oferecer cadastro público (signup). O primeiro administrador é criado manualmente no painel do Xano, e depois somente administradores criam usuários.

#### Scenario: Tentativa de criação sem autenticação
- **WHEN** `usuario_create_POST` é chamado sem token
- **THEN** o sistema rejeita a requisição

### Requirement: Operador da movimentação vem do token
Os endpoints `entrada_POST` e `saida_POST` SHALL exigir autenticação e SHALL obter o `usuario_id` da movimentação de `$auth.id`, sem ler esse valor do corpo da requisição. Nenhuma outra regra desses endpoints é alterada nesta Change.

#### Scenario: Entrada com token válido
- **WHEN** `entrada_POST` é chamado com token válido
- **THEN** a movimentação é gravada com o `usuario_id` do token

#### Scenario: Saída com token válido
- **WHEN** `saida_POST` é chamado com token válido
- **THEN** a movimentação é encerrada e o operador registrado é o do token

#### Scenario: Chamada sem token
- **WHEN** `entrada_POST` ou `saida_POST` é chamado sem token
- **THEN** o sistema rejeita a requisição como não autenticada

#### Scenario: usuario_id enviado no corpo
- **WHEN** o corpo da requisição traz um `usuario_id`
- **THEN** o valor é ignorado e prevalece o do token

### Requirement: Gerenciamento de usuários restrito a administradores
`usuario_create_POST` e `usuario_list_GET` SHALL exigir autenticação e permitir acesso somente a usuários com `type = "admin"`.

#### Scenario: Administrador cria ou lista usuários
- **WHEN** um administrador autenticado chama um desses endpoints
- **THEN** a operação é executada

#### Scenario: Operador tenta gerenciar usuários
- **WHEN** um operador autenticado chama um desses endpoints
- **THEN** o sistema responde 403 (acesso negado)

### Requirement: Proteção da senha
O sistema SHALL gravar a senha em hash em `usuario_create_POST` e SHALL NOT retornar o campo `password` em nenhuma resposta.

#### Scenario: Criação de usuário
- **WHEN** um administrador cria um usuário
- **THEN** a senha é gravada em hash

#### Scenario: Listagem de usuários
- **WHEN** `usuario_list_GET` é chamado por um administrador
- **THEN** a resposta não contém o campo `password`

### Requirement: Login e controle de acesso no Streamlit
O `app.py` SHALL exibir uma tela de login, guardar o token em `st.session_state`, enviar `Authorization: Bearer <token>` nas chamadas protegidas e mostrar as telas administrativas somente a `type = "admin"`.

#### Scenario: Usuário não autenticado
- **WHEN** não há token na sessão
- **THEN** o app exibe apenas a tela de login

#### Scenario: Operador logado
- **WHEN** um operador está logado
- **THEN** as telas administrativas não são exibidas

### Requirement: Pendência do grupo auth/ do template
O grupo `auth/` e a tabela `user` do template SHALL ser tratados mediante `xano workspace push -d ./xano --dry-run` e aprovação explícita da pessoa. Nenhuma remoção nem push real é feito pelo agente.

#### Scenario: Resolução do bloqueio de push
- **WHEN** o dry-run é executado
- **THEN** o resultado é registrado e o destino de `auth/` e `user` é decidido com a pessoa antes de qualquer push

### Requirement: Cadastro de vagas restrito a administradores com validações numéricas
O sistema SHALL permitir o cadastro de novas vagas exclusivamente para administradores autenticados (`admin`), exigindo um número inteiro único, positivo (maior ou igual a 1), e rejeitando números duplicados, zero, negativos ou não inteiros.

#### Scenario: Administrador cadastra nova vaga válida com sucesso
- **WHEN** um administrador autenticado envia um número inteiro único e positivo (ex: número 31)
- **THEN** o sistema cadastra a vaga com status inicial `livre` e `active = true`

#### Scenario: Operador tenta cadastrar vaga
- **WHEN** um operador autenticado tenta cadastrar uma nova vaga
- **THEN** o sistema rejeita a operação com erro de acesso negado (403)

#### Scenario: Cadastro rejeita número duplicado, zero, negativo ou não inteiro
- **WHEN** um administrador tenta cadastrar uma vaga com número já existente, zero, negativo ou decimal
- **THEN** o sistema rejeita a operação com erro de validação

### Requirement: Inicialização, capacidade planejada e regularização de vagas
O sistema SHALL iniciar novas vagas com o status `livre` e `active = true`, considerando capacidade inicial planejada de 30 vagas sem limite máximo fixo, e SHALL permitir a regularização da vaga legada `number = 0` para um número positivo disponível preservando seu ID e histórico.

#### Scenario: Vaga legada number = 0 é regularizada
- **WHEN** a vaga com `number = 0` é atualizada administrativamente para um número positivo válido
- **THEN** o ID da vaga e suas chaves estrangeiras históricas em movimentações permanecem intactos

### Requirement: Edição de vagas restrita a administradores e proteção contra duplicidade
O sistema SHALL permitir a edição de informações de vagas exclusivamente por administradores autenticados, rejeitando edições por operadores (403), números duplicados/inválidos e alterações manuais de status incompatíveis com movimentações abertas.

#### Scenario: Administrador edita dados da vaga com sucesso
- **WHEN** um administrador autenticado atualiza o número ou tipo de uma vaga com dados válidos e únicos
- **THEN** o sistema atualiza o registro com sucesso

#### Scenario: Operador tenta editar vaga
- **WHEN** um operador autenticado tenta editar uma vaga
- **THEN** o sistema rejeita a operação com erro de acesso negado (403)

#### Scenario: Edição rejeita número duplicado ou inválido
- **WHEN** um administrador tenta atualizar uma vaga com número duplicado, zero, negativo ou decimal
- **THEN** o sistema rejeita a operação

#### Scenario: Edição impede alteração manual de status incompatível com movimentação aberta
- **WHEN** um administrador tenta alterar manualmente o status de uma vaga para `livre` enquanto houver movimentação aberta vinculada
- **THEN** o sistema rejeita a alteração para evitar inconsistência operacional

### Requirement: Desativação lógica restrita, segura e preservação histórica de vagas
O sistema SHALL permitir a desativação lógica de vagas (`active = false`) exclusivamente por administradores autenticados, restrita a vagas livres e sem movimentações abertas, bloqueando operadores (403) e preservando referências históricas de movimentações vinculadas.

#### Scenario: Administrador desativa vaga livre sem movimentação aberta
- **WHEN** um administrador solicita a desativação lógica de uma vaga livre e sem movimentação aberta
- **THEN** o sistema define `active = false` na vaga, preservando o histórico de movimentações passadas

#### Scenario: Operador tenta desativar vaga
- **WHEN** um operador autenticado tenta desativar uma vaga
- **THEN** o sistema rejeita a operação com erro de acesso negado (403)

#### Scenario: Tentativa de desativar vaga ocupada ou com movimentação aberta
- **WHEN** um administrador tenta desativar uma vaga ocupada ou que possua movimentação aberta pendente
- **THEN** o sistema rejeita a desativação para garantir a integridade dos dados

### Requirement: Campo cancelled em movimentações e definição de movimentação aberta
O sistema SHALL suportar um campo booleano `cancelled` (default `false`) na tabela `movimentacao` para representar movimentações canceladas ou de teste, considerando uma movimentação como aberta somente quando `exit_time == null && cancelled == false`.

#### Scenario: Movimentação cancelada não bloqueia vaga nem é encerrada na saída
- **WHEN** uma movimentação de teste é marcada com `cancelled = true`
- **THEN** o sistema a desconsidera como movimentação aberta, permitindo liberar a vaga, e rejeita tentativas de encerrá-la via `saida_POST`

#### Scenario: Preservação de dados históricos no cancelamento
- **WHEN** uma movimentação é marcada como cancelada
- **THEN** o `exit_time` original e demais dados históricos permanecem inalterados

### Requirement: Consulta e listagem de vagas ativas com autenticação
O sistema SHALL fornecer endpoints de listagem de vagas e consulta de disponibilidade e ocupação (`vaga_list_GET`, `vaga_ocupacao_GET`) filtrando exclusivamente vagas ativas (`active == true`), respeitando as regras de autenticação do sistema.

#### Scenario: Consulta de vagas e ocupação por usuário autenticado
- **WHEN** um usuário autenticado consulta a listagem de vagas ativas ou o resumo de ocupação
- **THEN** o sistema retorna apenas os dados das vagas ativas (`active == true`)

### Requirement: Controle restrito de status livre e ocupada com prevenção de ocupação simultânea
O sistema SHALL suportar exclusivamente os status `livre` e `ocupada`, atualizando-os automaticamente na entrada (muda para `ocupada`, bloqueando entradas em vagas já ocupadas, inativas ou com inconsistência) e na saída (muda para `livre`), prevenindo ocupações simultâneas.

#### Scenario: Entrada de veículo ocupa a vaga disponível e ativa
- **WHEN** um veículo registra entrada em uma vaga com status `livre` e `active = true`
- **THEN** o status da vaga é alterado para `ocupada`

#### Scenario: Saída de veículo libera a vaga ocupada
- **WHEN** um veículo registra saída de uma vaga com status `ocupada`
- **THEN** o status da vaga é alterado para `livre`

#### Scenario: Tentativa de entrada em vaga ocupada, inativa ou com inconsistência de status
- **WHEN** uma entrada é solicitada para uma vaga cujo status é `ocupada`, inativa (`active = false`) ou com movimentação aberta conflitante
- **THEN** o sistema rejeita a operação prevenindo ocupação simultânea

### Requirement: Módulo Financeiro e Faturamento
O sistema SHALL disponibilizar dados financeiros somente a administradores autenticados, calculados a partir de movimentações finalizadas e não canceladas.

#### Scenario: Consulta de indicadores financeiros por administrador
- **WHEN** um administrador consulta o endpoint financeiro
- **THEN** a resposta inclui faturamento do dia e do mês, ticket médio, quantidade de movimentações concluídas e histórico, usando o valor cobrado e o fuso `America/Sao_Paulo`

#### Scenario: Bloqueio de acesso financeiro para operadores
- **WHEN** um operador ou usuário não autenticado tenta consultar o endpoint financeiro
- **THEN** o sistema rejeita a chamada sem retornar dados financeiros

#### Scenario: Histórico de faturamento
- **WHEN** o administrador consulta o histórico
- **THEN** a resposta inclui somente movimentações com saída registrada e `cancelled = false`, com placa, vaga, entrada, saída e valor cobrado

#### Scenario: Filtro opcional de período
- **WHEN** a consulta inclui datas inicial e/ou final
- **THEN** o histórico e os indicadores consideram somente as movimentações finalizadas dentro dos limites informados

#### Scenario: Gráfico diário de valores cobrados
- **WHEN** o histórico contém saídas válidas com valores numéricos
- **THEN** o gráfico apresenta a soma diária dos valores por data local, sem incluir datas inválidas ou valores ausentes
