# Proposal

## Why

O modelo de dados e as especificações atuais possuem lacunas estruturais (como a falta de referências de chave estrangeira em `movimentacao` para `veiculo` e `vaga`, além da ausência de documentação formal sobre regras decididas, ainda não implementadas). É necessário consolidar a fundação do modelo de dados e registrar o comportamento atual e as pendências futuras antes de prosseguir com novos desenvolvimentos.

## What Changes

- Corrigir as referências de chave estrangeira em `xano/table/movimentacao.xs` para que `veiculo_id` aponte para `veiculo`, `vaga_id` aponte para `vaga`, e conferir que `usuario_id` aponta para `usuario`.
- Especificar o comportamento ATUAL (as-is) das tabelas e endpoints existentes, sem alterar a lógica deles.
- Formalizar nas especificações OpenSpec (`parking-management`) as regras de negócio de referência (tarifação em frações de 15 min, teto de R$ 25,00, isenção para mensalistas ativos e validações fundamentais) como requisitos alvo.
- Registrar explicitamente as lacunas e pendências a serem abordadas em Changes futuras (validação de vaga livre, prevenção de entradas/saídas duplicadas, cálculo dinâmico de tarifa e autenticação via token).

## Capabilities

### New Capabilities
- Nenhuma (utiliza e expande a capacidade existente `parking-management`).

### Modified Capabilities
- `parking-management`: atualização das especificações para refletir as referências relacionais corretas, documentar o comportamento atual (as-is) e consolidar as regras de negócio alvo e pendências da operação de estacionamento.

## Impact

- Ajuste na definição de tabela Xano em `xano/table/movimentacao.xs` para suportar integridade referencial e *addons*.
- Atualização das especificações em `openspec/specs/parking-management/spec.md`.
