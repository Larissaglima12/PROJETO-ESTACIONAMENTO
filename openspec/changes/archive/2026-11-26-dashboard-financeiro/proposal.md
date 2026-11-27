# Proposal: Dashboard Financeiro e Faturamento

## Why
O sistema acadêmico de gestão de estacionamento precisa de um módulo financeiro para que administradores possam acompanhar o faturamento diário, mensal, movimentações finalizadas, ticket médio e histórico de valores cobrados, atendendo plenamente aos requisitos de gestão financeira do projeto.

## What Changes
- **Página de Faturamento (Streamlit):** Adicionar uma aba/página exclusiva para administradores ("Faturamento") no menu lateral logo após "Movimentação".
- **Indicadores Financeiros:** Exibir faturamento do dia, faturamento do mês, total de movimentações finalizadas e ticket médio com formatação monetária brasileira (R$).
- **Histórico e Gráficos:** Apresentar histórico tabular de movimentações finalizadas (placa, entrada, saída, valor) e evolução recente.
- **Proteção de Acesso:** Garantir restrição de acesso a administradores tanto no frontend quanto no backend.

## Impact
- **Frontend (Streamlit):** Nova aba/visão para administradores com indicadores e filtros.
- **Backend (Xano):** Utilização de dados de movimentações finalizadas (`exit_time != null`, `cancelled == false`, campo `amount`).
