# Design

## Context

O sistema possui uma tabela `movimentacao` cujos campos `veiculo_id` e `vaga_id` estavam sem referência de tabela (`table = ""`). Para habilitar o uso de *addons* e garantir integridade referencial nativa no Xano, precisamos ajustar estes campos. Além disso, documentamos o modelo de referência e as regras operacionais (seção 13 do `project-overview.md`).

## Goals / Non-Goals

**Goals:**
- Corrigir as definições de chave estrangeira na tabela `movimentacao` (`veiculo` e `vaga`).
- Alinhar as especificações OpenSpec com as regras de negócio de referência.

**Non-Goals:**
- Implementar nova lógica de cálculo de tarifa nos endpoints de saída nesta Change (será tratado em Change dedicada).
- Modificar o frontend Streamlit.

## Decisions

- **Decisão 1:** Ajustar `table/movimentacao.xs` para declarar explicitamente `table = "veiculo"` em `veiculo_id` e `table = "vaga"` em `vaga_id`, alinhando-se com `xano/table/movimentacao.xs`.
  - *Rationale:* Garante consistência entre os arquivos locais do repositório e habilita recursos relacionais do Xano.

## Risks / Trade-offs

- [Desalinhamento com Xano remoto] Se o workspace remoto do Xano não for atualizado via `xano workspace push`, poderá haver divergência entre o modelo local e o remoto.
  - *Mitigação:* Recomendar uso de `xano workspace push --dry-run` antes de enviar as alterações ao Xano.
