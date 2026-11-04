# Tasks

## 1. Backend (arquivos .xs, sem push)

- [x] 1.1 Consultar a documentação do Xano (via MCP developer-mcp) para: emitir token de autenticação sobre a tabela `usuario`, verificar senha em hash e obter o usuário autenticado (`$auth.id`). Registrar o que foi confirmado.
- [x] 1.2 Conferir `xano/table/usuario.xs` (campo de senha e `auth`) e ajustar somente se necessário.
- [x] 1.3 Criar `usuario_login_POST` sobre a tabela `usuario`: busca por e-mail, verificação de senha em hash, retorno do token e do `type`; erro genérico para credenciais inválidas.
- [x] 1.4 Atualizar `usuario_create_POST`: exigir autenticação, permitir somente `type = "admin"` (403 para operador) e gravar a senha em hash.
- [x] 1.5 Atualizar `usuario_list_GET`: exigir autenticação, permitir somente `type = "admin"` e não retornar o campo `password`.
- [x] 1.6 Atualizar `entrada_POST` e `saida_POST`: exigir autenticação e obter o `usuario_id` de `$auth.id`, removendo a leitura do corpo da requisição.
- [x] 1.7 Validar a sintaxe de cada `.xs` alterado com o validador de XanoScript do MCP.

## 2. Frontend Streamlit (`app.py`)

- [x] 2.1 Tela de login (e-mail e senha) que chama `usuario_login_POST`.
- [x] 2.2 Guardar token e dados do usuário em `st.session_state`.
- [x] 2.3 Função de requisição que injeta `Authorization: Bearer <token>` em todas as chamadas protegidas.
- [x] 2.4 Mostrar as telas administrativas apenas para `type = "admin"`.

## 3. Publicação no Xano (manual, com aprovação da pessoa)

- [x] 3.1 Rodar `xano workspace push -d ./xano --dry-run` e registrar o resultado (encontrado erro `Invalid dbo name: user` nos arquivos legados do template).
- [x] 3.2 Decidir com a pessoa o destino do grupo `auth/` e da tabela `user` do template (decidido preservar os arquivos legados sem alterações).
- [x] 3.3 Após a aprovação, realizar a publicação individual dos endpoints de autenticação e controle de usuários, confirmando no painel do Xano.

## 4. Verificação

- [x] 4.1 Criar o primeiro admin manualmente no painel do Xano, com a senha em hash (conforme a documentação confirmada em 1.1) - Confirmado pela criação manual na tabela `usuario`.
- [x] 4.2 Testar: login válido, login inválido, entrada e saída com `usuario_id` vindo do token, operador bloqueado (403) em `usuario_create_POST` e `usuario_list_GET`, listagem sem `password` (Validado e confirmado no Xano: logins testados, operador bloqueado, listagem sem senha, entrada associando usuario_id do token e saída liberando vaga).
