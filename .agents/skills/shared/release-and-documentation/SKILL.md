---
name: release-and-documentation
description: "Prepare implementation status, migration notes, runbooks, release notes and operational documentation for Trust Trash changes."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Release and Documentation

## Documentation by change type
- Product behavior: feature brief/use cases and UI state/copy changes.
- Public API: endpoint, auth, request/response, errors, pagination, rate limits and examples.
- Event/worker: schema version, producer/consumer, retry/DLQ, idempotency and replay.
- Data model: owner, grain, schema, freshness, quality, retention and lineage.
- Connector: provider scopes, supported capabilities, limits, sync mode, known gaps and revocation.
- Processor: input/output formats, model/version, resource needs, confidence and failure semantics.
- Infrastructure: ports, secrets, volumes, backup/restore, resource limits and upgrade/rollback.

## Procedure
1. Compare code against acceptance criteria and implementation status.
2. Update relevant docs and examples.
3. Add migration/backfill guidance for schema/data changes.
4. Write an operational runbook for new recurring/background behavior.
5. Record known limitations and unsupported capability states.
6. Prepare release notes: added, changed, fixed, security, migrations and known issues.
7. Verify links point to current sources of truth.

Never state a feature is complete when only a contract, stub, mock or UI shell exists.
