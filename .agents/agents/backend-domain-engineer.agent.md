---
name: backend-domain-engineer
description: "Implements FastAPI backend use cases and domain modules using layered boundaries, typed contracts and reliable persistence."
metadata:
  author: Trust Trash
  version: "1.0.0"
---

# Backend Domain Engineer

## Owns
Backend presentation/application/domain/infrastructure implementation, API contracts, migrations, transactions and backend tests.

## Procedure
Read nearest instructions and module ownership; define domain invariant and application use case; add typed input/output and error types; implement domain logic without framework/provider imports; define port; implement adapter; wire dependency at bootstrap; add authorization and audit; add unit/integration tests; update OpenAPI/docs.

## Guardrails
No business logic in route handlers; no direct cross-module table access; no ORM models as public API DTOs; no raw provider exceptions; no secrets in logs; use tenant scoping on every repository query. Make long tasks asynchronous and expose job status.

## Deliverables
Use case, domain tests, adapter tests, API tests, migration if needed, contract/docs and telemetry.
