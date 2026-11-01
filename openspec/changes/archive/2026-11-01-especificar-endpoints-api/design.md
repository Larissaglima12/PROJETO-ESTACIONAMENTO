# Design

## Context

See proposal.md - Why. As tabelas já existem no Xano; agora definimos a arquitetura de API Groups e Function Stacks para expor os endpoints CRUD e as regras de negócio de estacionamento.

## Goals / Non-Goals

**Goals:**
- Organizar os endpoints em API Groups no Xano (ex: `/auth`, `/mensalista`, `/veiculo`, `/vaga`, `parking/`).
- Definir a lógica de Function Stack para entrada (verificação de vaga livre, criação de movimentação, atualização de vaga) e saída (cálculo de horas, atualização de movimentação e liberação de vaga).

**Non-Goals:**
- Desenvolvimento do frontend da aplicação.

## Decisions

- **API Group Structure**:
  - `auth`: Autenticação de usuários (`/login`, `/signup`, `/me`).
  - `mensalistas`: CRUD de mensalistas (`GET`, `POST`, `PATCH`, `DELETE`).
  - `veiculos`: CRUD de veículos (`GET`, `POST`, `PATCH`, `DELETE`).
  - `vagas`: CRUD de vagas e consulta de status (`GET`, `POST`, `PATCH`, `DELETE`, `GET /vagas/ocupacao`).
  - `parking`: Operações de pátio (`POST /parking/entrada`, `POST /parking/saida`).

## Risks / Trade-offs

- [Concorrência em Vagas] → Garantir transações atômicas no Xano ao alocar uma vaga durante a entrada para evitar race conditions em vagas simultâneas.
