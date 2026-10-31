# Spec Delta

## Purpose

Define as operações essenciais de um estacionamento: registrar veículos em permanência, controlar a ocupação das vagas e calcular o valor devido na saída.

## ADDED Requirements

### Requirement: Registrar entrada de veículo
O sistema SHALL registrar a placa e o horário de entrada de cada veículo e associá-lo a uma vaga livre. A mesma placa não pode ter mais de uma permanência ativa.

#### Scenario: Entrada com vaga disponível
- **WHEN** uma entrada é solicitada para uma placa sem permanência ativa e há vaga livre
- **THEN** o sistema registra a entrada e associa o veículo a uma vaga ocupada

#### Scenario: Entrada sem vagas livres
- **WHEN** uma entrada é solicitada e todas as vagas estão ocupadas
- **THEN** o sistema não registra a permanência e informa que não há vaga disponível

#### Scenario: Placa já está no estacionamento
- **WHEN** uma entrada é solicitada para uma placa com permanência ativa
- **THEN** o sistema rejeita a entrada duplicada e preserva o registro existente

### Requirement: Controlar a ocupação das vagas
O sistema SHALL manter a quantidade de vagas livres e ocupadas consistente com as permanências ativas e permitir consultar essa ocupação.

#### Scenario: Consultar ocupação
- **WHEN** a ocupação do estacionamento é consultada
- **THEN** o sistema informa as quantidades de vagas livres e ocupadas

#### Scenario: Liberar vaga após saída
- **WHEN** a saída de um veículo é concluída
- **THEN** o sistema encerra a permanência e torna a vaga associada disponível

### Requirement: Calcular tarifa na saída
O sistema SHALL calcular o valor devido na saída usando a tarifa horária configurada e cobrar cada hora iniciada da permanência.

#### Scenario: Saída após uma hora iniciada
- **WHEN** a saída é solicitada para um veículo com permanência ativa
- **THEN** o sistema calcula o tempo entre a entrada e a saída, arredonda qualquer fração para a próxima hora e informa o valor devido

#### Scenario: Saída sem permanência ativa
- **WHEN** uma saída é solicitada para uma placa sem permanência ativa
- **THEN** o sistema rejeita a solicitação e não altera a ocupação
