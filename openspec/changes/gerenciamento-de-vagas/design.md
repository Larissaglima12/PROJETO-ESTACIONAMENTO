# Design

## Context

See `proposal.md` for the motivation and objectives of this change. The system currently possesses a `vaga` table in Xano with schema fields (`id`, `created_at`, `number`, `type`, `status`) and a global unique index on `number`. Existing endpoints include `vaga_list_GET` and `vaga_ocupacao_GET`, but administrative creation, update, and logical deactivation endpoints for vagas need to be implemented or refined, along with robust validation in entry and exit flows, removal of the `manutencao` status, enforcement of logical deletion via `active`, and introduction of the `cancelled` flag on `movimentacao` to handle legacy test records without faking exit times.

## Goals / Non-Goals

**Goals:**
- Implement admin-only creation (`vaga_create_POST`), update, and logical deactivation of vagas with validation for unique, positive integer numbers.
- Maintain the global unique index on `vaga.number`, permanently reserving numbers of deactivated vagas so they cannot be reused.
- Restrict vaga status exclusively to `livre` and `ocupada`, removing `manutencao`.
- Enforce strict safety rules on logical deactivation (blocking deactivation of occupied vagas or vagas with open movement dependencies).
- Implement logical deletion via an `active` boolean field, preserving historical movement references (`movimentacao.vaga_id`).
- Implement the `cancelled` boolean field on `movimentacao` (default `false`) for explicit logical cancellation of test or erroneous movements.
- Validate status consistency, active status, and concurrency during vehicle entry (`entrada_POST`) and exit (`saida_POST`).
- Integrate vaga management UI in Streamlit restricted to administrators.

**Non-Goals:**
- Automatic mass creation of the 30 initial records in the database.
- Implementation of parking fee calculation rules (deferred to a future change).
- Introduction of frontend frameworks other than Streamlit.

## Decisions

### 1. Architecture and Authorization
- **Rationale:** Reuse the established security pattern where Xano endpoints enforce authentication (`auth = "usuario"`) and explicit precondition checks (`$current_user.type == "admin"`), as successfully applied in `usuario_list_GET` and `usuario_create_POST`. Administrative mechanisms for canceling movements or managing vagas require proper admin authorization.

### 2. Vaga Status Schema and Logical Deletion
- **Rationale:**
  - Update the `status` enum in `xano/table/vaga.xs` to contain exclusively `["livre", "ocupada"]`, removing `manutencao`.
  - Introduce an `active` boolean field on the `vaga` table for logical deactivation (soft delete).
- **Number Reservation:** The global unique index on `vaga.number` is maintained. When a vaga is deactivated (`active = false`), its number remains reserved and cannot be reassigned to a new vaga, preserving historical auditability and preventing index collisions.

### 3. Deactivation Safety Rules and Historical Integrity
- **Rationale:** A vaga can only be deactivated by an administrator if:
  1. Its current status is `livre`.
  2. It has **no open movement** (`exit_time == null && cancelled == false`) associated with it in the `movimentacao` table.
- **Impact on History:** Vagas with historical closed movements can be successfully deactivated. The vaga record remains in the database with `active = false`, preserving all foreign key references (`movimentacao.vaga_id`).

### 4. Handling Legacy Test Movements (`cancelled` flag)
- **Rationale:** To cleanly handle test records like movement ID 3 without inventing exit times or deleting history, a boolean field `cancelled` (default `false`) is added to `movimentacao`.
- **Open Movement Definition:** A movement is considered open strictly when `exit_time == null && cancelled == false`.
- **Safety Checks:** `saida_POST` rejects attempts to close cancelled movements. Regularization of test movement ID 3 is planned via manual setting of `cancelled = true` upon specific human authorization. Historical movements (IDs 1, 2, and 4) remain preserved without automatic changes.

### 5. Regularization of Legacy Vaga (`number = 0`)
- **Rationale:** The template-generated vaga with `number = 0` must be regularized by assigning a positive available number (e.g., `number = 1`), preserving its `id` and all historical foreign key references in `movimentacao.vaga_id`.

### 6. Concurrency Control in Vehicle Entry
- **Rationale:** To prevent race conditions where two concurrent requests attempt to occupy the same free vaga simultaneously, `entrada_POST` is planned to utilize `db.transaction` with `isolation = "serializable"`.

## Risks / Trade-offs

- [Conflito de concorrência e serialização] → **Mitigation:** Use `db.transaction` with serializable isolation and robust `try_catch` error handling.
- [Inconsistência de movimentações abertas] → **Mitigation:** Enforce `exit_time == null && cancelled == false` globally across queries and validations.

## Migration & Rollback Plan

1. **Pre-Migration Audit:** Inspect existing `status` values, legacy vaga `number = 0`, and movement records.
2. **Schema Update:** Add `active` to `vaga`, add `cancelled` to `movimentacao`, and restrict `status` enum to `["livre", "ocupada"]`.
3. **Data Migration:** Explicitly set `active = true` and `cancelled = false` on existing records. Regularize legacy vaga number.
4. **Endpoint & App Deployment:** Publish updated Xano endpoints and Streamlit frontend.
5. **Testing & Validation:** Run functional tests, auth checks, cancellation handling, and concurrency race-condition tests.
6. **Rollback Strategy:** Revert schema/endpoint changes via Xano workspace tools while accounting for production movement data to prevent data loss.
