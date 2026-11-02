# Proposal

## Why

O template inicial do Xano usa uma tabela `user` genérica e endpoints em `auth/` que entram em conflito com a tabela de domínio `usuario` do projeto, e esse conflito bloqueia o push do workspace (`Invalid dbo name: user`). Além disso, `entrada_POST` e `saida_POST` recebem o `usuario_id` no corpo da requisição em vez de obtê-lo do token, e `usuario_create_POST` e `usuario_list_GET` não têm controle de acesso por perfil. Não existe endpoint de login sobre a tabela `usuario`.

## What Changes

- Criar `usuario_login_POST` sobre a tabela `usuario`, com verificação de senha em hash e emissão de token de autenticação.
- Exigir autenticação em `entrada_POST` e `saida_POST`; o `usuario_id` da movimentação passa a vir do token (`$auth.id`) e deixa de ser lido do corpo da requisição.
- Proteger `usuario_create_POST` e `usuario_list_GET`: somente `type = "admin"` (resposta 403 para operador). A listagem não retorna o campo `password`.
- Garantir que `usuario_create_POST` grave a senha em hash.
- Sem cadastro público (signup). O primeiro administrador é criado manualmente no painel do Xano; depois, apenas administradores criam operadores.
- Registrar como tarefa a resolução do grupo `auth/` do template: um `xano workspace push -d ./xano --dry-run` é obrigatório antes de qualquer remoção, e nenhum push real é feito nesta Change.
- Streamlit (`app.py`): tela de login, token em `st.session_state` e cabeçalho `Authorization: Bearer` em todas as chamadas à API.

## Out of Scope

Cálculo de cobrança, validação de vaga livre, entrada e saída duplicadas, cadastro de vagas e painel de ocupação.

## Capabilities

### New Capabilities
- Nenhuma.

### Modified Capabilities
- `parking-management`: autenticação por token, `usuario_id` das movimentações obtido do token e controle de acesso por perfil (admin e operador).

## Impact

- `xano/api/parking/` (`entrada_POST`, `saida_POST`, `usuario_create_POST`, `usuario_list_GET`) e novo `usuario_login_POST`.
- `xano/table/usuario.xs` (conferir o campo de senha e o `auth`).
- `xano/api/authentication/` (grupo `auth/` do template): apenas registrado como pendência, sem remoção nesta Change.
- `app.py`.