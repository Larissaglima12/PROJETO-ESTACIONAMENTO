# Spec Delta

## Purpose

Define a estrutura de dados e tabelas relacionais no Xano necessárias para o funcionamento do sistema de estacionamento (usuários, mensalistas, veículos, vagas e movimentações).

## ADDED Requirements

### Requirement: Tabela USUARIO
O sistema SHALL possuir uma tabela USUARIO para armazenar os dados de autenticação e perfil dos usuários do sistema com os campos nome, email, senha e tipo.

#### Scenario: Cadastro de usuário
- **WHEN** um novo usuário é cadastrado com nome, email, senha e tipo
- **THEN** o sistema armazena o registro na tabela USUARIO

### Requirement: Tabela MENSALISTA
O sistema SHALL possuir uma tabela MENSALISTA para gerenciar os clientes mensalistas com os campos nome, telefone, valor_mensalidade, data_inicio, data_fim e status.

#### Scenario: Cadastro de mensalista
- **WHEN** um mensalista é cadastrado com dados válidos e período de vigência
- **THEN** o sistema registra o mensalista na tabela MENSALISTA com status ativo

### Requirement: Tabela VEICULO
O sistema SHALL possuir uma tabela VEICULO para cadastrar os veículos com placa, modelo, cor, tipo e vinculo opcional com um mensalista (mensalista_id).

#### Scenario: Cadastro de veículo vinculado
- **WHEN** um veículo é cadastrado associado a um mensalista existente
- **THEN** o sistema registra a placa, modelo, cor, tipo e mensalista_id

### Requirement: Tabela VAGA
O sistema SHALL possuir uma tabela VAGA para gerenciar as vagas de estacionamento com os campos numero, tipo e status.

#### Scenario: Cadastro de vaga
- **WHEN** uma nova vaga é criada com número, tipo e status inicial livre
- **THEN** o sistema registra a vaga na tabela VAGA

### Requirement: Tabela MOVIMENTACAO
O sistema SHALL possuir uma tabela MOVIMENTACAO para registrar as entradas e saídas de veículos associando veiculo_id, vaga_id, usuario_id, entrada, saida e valor.

#### Scenario: Registro de movimentação
- **WHEN** uma entrada ou saída de veículo é processada
- **THEN** o sistema registra a movimentação relacionando veículo, vaga, usuário operador, horários e valores
