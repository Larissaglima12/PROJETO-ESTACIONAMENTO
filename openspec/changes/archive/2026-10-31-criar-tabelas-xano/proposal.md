# Proposal

## Why

Para implementar o módulo de estacionamento no backend Xano, é necessário estruturar e criar as tabelas de banco de dados relacionais que darão suporte ao sistema: USUARIO, MENSALISTA, VEICULO, VAGA e MOVIMENTACAO. Isso permitirá o cadastro de usuários, gestão de mensalistas, controle de veículos, gerenciamento de vagas e registro de entradas/saídas.

## What Changes

- Criação da tabela **USUARIO** no Xano (campos: nome, email, senha, tipo).
- Criação da tabela **MENSALISTA** no Xano (campos: nome, telefone, valor_mensalidade, data_inicio, data_fim, status).
- Criação da tabela **VEICULO** no Xano (campos: placa, modelo, cor, tipo, mensalista_id).
- Criação da tabela **VAGA** no Xano (campos: numero, tipo, status).
- Criação da tabela **MOVIMENTACAO** no Xano (campos: veiculo_id, vaga_id, usuario_id, entrada, saida, valor).

## Capabilities

### New Capabilities
- `parking-management`: Estrutura de dados e tabelas relacionais no Xano para o módulo de estacionamento.

### Modified Capabilities
- (Nenhuma)

## Impact

- Banco de dados Xano: Criação de 5 novas tabelas relacionais com seus respectivos campos e índices.
- Endpoints e lógica de negócio subsequentes que consumirão essas tabelas.
