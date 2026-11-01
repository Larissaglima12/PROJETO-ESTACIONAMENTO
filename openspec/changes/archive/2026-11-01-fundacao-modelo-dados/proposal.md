# Proposal

## Why

O modelo de dados e as especificações atuais possuem lacunas: não há documentação formal do comportamento atual das tabelas e endpoints, e as regras de negócio decididas (tarifa, tolerância, mensalista) ainda não estão implementadas. É necessário registrar o comportamento atual e as pendências antes de prosseguir com novos desenvolvimentos.

## What Changes

- Confirmar que as referências de chave estrangeira em `xano/table/movimentacao.xs` estão corretas (`veiculo_id` → `veiculo`, `vaga_id` → `vaga`, `usuario_id` → `usuario`). Nenhuma alteração de código é esperada.
- Especificar o comportamento ATUAL (as-is) das tabelas e endpoints existentes, sem alterar a lógica deles.
- Formalizar nas especificações OpenSpec (`parking-management`) as regras de negócio de referência (tarifação em frações de 15 min, teto de R$ 25,00, isenção para mensalistas ativos e validações fundamentais) como requisitos alvo, separados do comportamento atual.
- Registrar explicitamente as lacunas e pendências a serem abordadas em Changes futuras (validação de vaga livre, prevenção de entradas/saídas duplicadas, cálculo dinâmico de tarifa e autenticação via token).

## Capabilities

### New Capabilities
- Nenhuma (utiliza e expande a capacidade existente `parking-management`).

### Modified Capabilities
- `parking-management`: documentar o comportamento atual (as-is), as regras de negócio alvo e as pendências da operação de estacionamento.

## Impact

- Nenhuma alteração em arquivos `.xs` do Xano.
- Atualização das especificações em `openspec/specs/parking-management/spec.md` (via spec delta desta Change).