# Design

## Context

See proposal.md - Why. O projeto utiliza o backend Xano para persistência de dados e APIs. Precisamos estabelecer a modelagem relacional de tabelas para o módulo de estacionamento.

## Goals / Non-Goals

**Goals:**
- Definir o esquema relacional no Xano com as 5 tabelas solicitadas: USUARIO, MENSALISTA, VEICULO, VAGA e MOVIMENTACAO.
- Estabelecer os tipos de dados e chaves estrangeiras adequadas (ex: `mensalista_id` em VEICULO, `veiculo_id`, `vaga_id`, `usuario_id` em MOVIMENTACAO).

**Non-Goals:**
- Implementação de endpoints de API de regras de negócio nesta fase de modelagem de tabelas.
- Interface de usuário frontend.

## Decisions

- **Modelagem Relacional no Xano**: Utilizar as tabelas nativas do Xano com relacionamentos (Foreign Keys) para garantir integridade referencial entre VEICULO e MENSALISTA, e entre MOVIMENTACAO, VEICULO, VAGA e USUARIO.
- **Tipos de Dados**:
  - `USUARIO`: nome (Text), email (Text, único), senha (Text, hash), tipo (Text / Enum).
  - `MENSALISTA`: nome (Text), telefone (Text), valor_mensalidade (Decimal/Float), data_inicio (Timestamp/Date), data_fim (Timestamp/Date), status (Text / Enum).
  - `VEICULO`: placa (Text, único), modelo (Text), cor (Text), tipo (Text), mensalista_id (Table Reference / Integer, opcional).
  - `VAGA`: numero (Integer/Text), tipo (Text), status (Text / Enum).
  - `MOVIMENTACAO`: veiculo_id (Table Reference), vaga_id (Table Reference), usuario_id (Table Reference), entrada (Timestamp), saida (Timestamp, opcional), valor (Decimal/Float, opcional).

## Risks / Trade-offs

- [Integridade Referencial] → Garantir que chaves estrangeiras no Xano sejam configuradas corretamente para evitar órfãos em MOVIMENTACAO ou VEICULO.
