# Design

## Context

O projeto possui uma dualidade entre a tabela `user` do template Xano (utilizada pelos endpoints de `auth/`) e a tabela de domínio `usuario` (utilizada nas regras de estacionamento). Esta change resolve o conflito unificando a autenticação sobre a tabela `usuario`, garantindo que os endpoints de movimentação obtenham o operador autenticado diretamente do token JWT e que endpoints administrativos exijam perfil de Administrador.

## Goals / Non-Goals

**Goals:**
- Consolidar a autenticação no Xano baseada na tabela `usuario`.
- Atualizar `entrada_POST` e `saida_POST` para extrair `usuario_id` de `$auth.id`.
- Adicionar validação de perfil `admin` em `usuario_create_POST` e `usuario_list_GET`.
- Implementar fluxo de login e sessões no Streamlit (`app.py`).

**Non-Goals:**
- Modificar o algoritmo de cálculo de tarifas de estacionamento.
- Criar novas tabelas ou migrações complexas de banco de dados.

## Decisions

- **Decisão 1: Autenticação via tabela `usuario`**
  - *Rationale:* Evita duplicação de entidades de usuário e elimina o erro `Invalid dbo name: user` no push do workspace.
  - *Alternativas consideradas:* Manter `user` do template e relacionar com `usuario` (descartado por manter complexidade desnecessária).
- **Decisão 2: Extração de `usuario_id` via `$auth.id`**
  - *Rationale:* Garante segurança e integridade das movimentações de estacionamento.
  - *Alternativas consideradas:* Continuar recebendo `usuario_id` no corpo da requisição (descartado por falhas de segurança e falsificação de operador).
- **Decisão 3: Validação de RBAC por `precondition` no XanoScript**
  - *Rationale:* Abordagem idiomática no Xano para rejeitar acessos não autorizados a endpoints protegidos.

## Risks / Trade-offs

- [Incompatibilidade de payload em requisições legadas] Clientes que enviavam `usuario_id` no JSON do corpo deixarão de fazê-lo.
  - *Mitigação:* Atualizar o frontend Streamlit e documentar a mudança de contrato na API.
