# Spec Delta

## MODIFIED Requirements

### Requirement: Tabela MOVIMENTACAO
O sistema SHALL possuir uma tabela MOVIMENTACAO para registrar as entradas e saídas de veículos associando veiculo_id, vaga_id, usuario_id, entrada, saida e valor, com chaves estrangeiras válidas para veiculo, vaga e usuario.

#### Scenario: Registro de movimentação com chaves estrangeiras corretas
- **WHEN** uma entrada ou saída de veículo é processada
- **THEN** o sistema registra a movimentação relacionando veículo (`veiculo`), vaga (`vaga`) e usuário operador (`usuario`), mantendo integridade referencial.

## ADDED Requirements

### Requirement: Comportamento Atual (As-Is) dos Endpoints de Estacionamento
O sistema SHALL manter o comportamento atual dos endpoints existentes em Xano (entrada_POST que grava movimentação sem validar vaga livre ou veículo duplicado, e saida_POST que finaliza movimentação com valor fixo de R$ 15,00), sem alterar sua lógica nesta Change.

#### Scenario: Execução dos endpoints no estado atual
- **WHEN** uma requisição de entrada ou saída é feita aos endpoints atuais
- **THEN** o sistema executa a lógica existente sem bloqueios adicionais de validação de duplicidade ou cálculo dinâmico de tarifa.

### Requirement: Regras Alvo de Tarifação e Cobrança (Pendências / Próximas Changes)
O sistema SHALL, em versões futuras, calcular o valor devido na saída de veículos avulsos com base no tempo de permanência (frações de 15 min, R$ 3,00 por fração, tolerância de 15 min gratuitos, teto de R$ 25,00) e isentar mensalistas ativos.

#### Scenario: Planejamento de regra de cálculo futuro
- **WHEN** o sistema for evoluído para implementar o cálculo dinâmico de tarifa
- **THEN** a saída de veículos aplicará as regras alvo definidas na seção 13.
