# Proposal

## Why

O projeto ainda não possui uma especificação para as operações básicas de um estacionamento. Definir o registro de entradas, a ocupação de vagas e o cálculo da tarifa permite estabelecer um comportamento consistente para controlar veículos e cobrar pelo tempo de permanência.

## What Changes

- Registrar a entrada de um veículo com sua placa e horário de entrada.
- Associar veículos em permanência a vagas disponíveis e manter a ocupação atualizada.
- Calcular o valor devido a partir do tempo entre entrada e saída, com tarifa por hora iniciada.
- Disponibilizar o controle da quantidade de vagas livres e ocupadas.

## Capabilities

### New Capabilities
- `parking-management`: registro de entradas e saídas, identificação por placa, cálculo de tarifa e controle de ocupação das vagas.

### Modified Capabilities
- Nenhuma.

## Impact

- Nova especificação em `openspec/changes/modulo-estacionamento/specs/parking-management/spec.md`.
- O repositório não contém código de aplicação ou testes atualmente; implementação, persistência, interface e configuração de capacidade/tarifa precisarão ser definidas durante o design.
