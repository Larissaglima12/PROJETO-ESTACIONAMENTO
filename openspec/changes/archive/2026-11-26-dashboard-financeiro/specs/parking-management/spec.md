# Spec Delta

## MODIFIED Requirements

### Requirement: Módulo Financeiro e Faturamento
O sistema SHALL disponibilizar dados financeiros somente a administradores autenticados, calculados a partir de movimentações finalizadas e não canceladas.

#### Scenario: Consulta de indicadores financeiros por administrador
- **WHEN** um administrador consulta o endpoint financeiro
- **THEN** a resposta inclui faturamento do dia e do mês, ticket médio, quantidade de movimentações concluídas e histórico, usando o valor cobrado e o fuso `America/Sao_Paulo`

#### Scenario: Bloqueio de acesso financeiro para operadores
- **WHEN** um operador ou usuário não autenticado tenta consultar o endpoint financeiro
- **THEN** o sistema rejeita a chamada sem retornar dados financeiros

#### Scenario: Histórico de faturamento
- **WHEN** o administrador consulta o histórico
- **THEN** a resposta inclui somente movimentações com saída registrada e `cancelled = false`, com placa, vaga, entrada, saída e valor cobrado

#### Scenario: Filtro opcional de período
- **WHEN** a consulta inclui datas inicial e/ou final
- **THEN** o histórico e os indicadores consideram somente as movimentações finalizadas dentro dos limites informados

#### Scenario: Gráfico diário de valores cobrados
- **WHEN** o histórico contém saídas válidas com valores numéricos
- **THEN** o gráfico apresenta a soma diária dos valores por data local, sem incluir datas inválidas ou valores ausentes
