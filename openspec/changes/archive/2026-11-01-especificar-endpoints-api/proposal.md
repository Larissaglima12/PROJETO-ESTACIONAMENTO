# Proposal

## Why

Agora que as tabelas de banco de dados (`USUARIO`, `MENSALISTA`, `VEICULO`, `VAGA`, `MOVIMENTACAO`) foram criadas e validadas no Xano, é necessário especificar os endpoints de API e as regras de negócio essenciais (CRUD para todas as entidades e fluxo operacional de estacionamento para registro de entrada e saída de veículos com cálculo de tarifa).

## What Changes

- Especificação de rotas CRUD (Create, Read, Update, Delete) para as tabelas: `usuario`, `mensalista`, `veiculo`, `vaga`.
- Especificação de endpoints de movimentação:
  - Registro de entrada de veículo (validando placa única, vínculo/mensalista e disponibilidade de vaga).
  - Consulta de ocupação de vagas.
  - Registro de saída de veículo com cálculo automático de permanência e tarifa.

## Capabilities

### New Capabilities
- (Nenhuma)

### Modified Capabilities
- `parking-management`: Adiciona requisitos de especificação de endpoints de API para CRUD e regras de negócio de entrada/saída de veículos.

## Impact

- APIs no Xano: Definição dos endpoints REST para gerenciamento de dados e operações do estacionamento.
- Regras de Negócio: Automação da ocupação de vagas, validações de placas e cálculo de tarifas de permanência.
