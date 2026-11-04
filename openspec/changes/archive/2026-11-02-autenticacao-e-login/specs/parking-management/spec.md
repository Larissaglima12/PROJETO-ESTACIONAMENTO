## ADDED Requirements

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