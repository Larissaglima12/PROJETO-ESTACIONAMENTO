# Design: Dashboard Financeiro e Faturamento

## Arquitetura do Backend (Xano)
- **Novo Endpoint:** `GET /parking/financeiro`
- **Tabela Principal:** `movimentacao`
- **Filtros:** `exit_time != null` e `cancelled == false`.
- **Campos Utilizados:** `amount` (decimal), `exit_time` (timestamp).
- **Segurança:** `auth = "usuario"`, com `precondition` verificando se `auth.type == "admin"`.

## Arquitetura do Frontend (Streamlit)
- **Menu Lateral:** Opção "💰 Faturamento" visível apenas para `user.type == "admin"`.
- **Layout:**
  - Cartões de métricas (Metric Cards) para Faturamento Dia, Mês, Total e Ticket Médio.
  - Gráfico de colunas/linhas para os últimos 7 dias.
  - Tabela detalhada de movimentações finalizadas.
- **Estilo:** Moderno, seguindo o padrão CSS já definido no `app.py`.

## Fluxo de Dados
1. Usuário Admin acessa a página de Faturamento.
2. Frontend solicita `GET /parking/financeiro`.
3. Backend calcula os agregados e retorna o JSON estruturado.
4. Frontend renderiza as métricas e a tabela.
