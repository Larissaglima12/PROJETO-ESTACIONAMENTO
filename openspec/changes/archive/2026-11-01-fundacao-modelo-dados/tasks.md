# Tasks

## 1. Modelo de dados

- [x] 1.1 Confirmar que `xano/table/movimentacao.xs` referencia `veiculo`, `vaga` e `usuario` (já está correto no arquivo e no Xano; apenas verificar).
- [x] 1.2 Documentar que a cópia `table/movimentacao.xs` da raiz não é a oficial (está com `table = ""` e não é usada pelo Xano CLI). Não apagar nada nesta Change.

## 2. Especificações

- [x] 2.1 Na spec delta, descrever o comportamento ATUAL (as-is) das tabelas e endpoints existentes, sem alterar a lógica.
- [x] 2.2 Na spec delta, registrar as regras da seção 13 como REQUISITOS ALVO, separados do comportamento atual.
- [x] 2.3 Na spec delta, listar as pendências: vaga livre na entrada, entrada duplicada, saída duplicada, tarifa fixa de R$ 15,00 no lugar do cálculo, placa duplicada, `usuario_id` vindo do token, status do usuário no login, ausência de endpoint de criação de vaga, `usuario_create_POST` e `usuario_list_GET` possivelmente sem autenticação, login fora do grupo Estacionamento, duas tabelas de usuário (`user` do template e `usuario` do projeto), push bloqueado pelos endpoints `auth/` e registro de teste em `movimentacao` com campos vazios.

## 3. Verificação

- [x] 3.1 Registrar na spec o resultado do dry-run já feito: tabelas do projeto sem diferença (atualizações em account, agent_conversation, agent_message, event_log e criação de user); bloqueio vindo dos endpoints `auth/` (`auth/login POST`, `auth/signup POST`, `reset/magic-link-login POST`) do template devido a `Invalid dbo name: user`. NÃO executado `xano workspace push` (nem `pull`) nesta Change, conforme restrição.
