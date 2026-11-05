# 05 Universal Search

## Purpose
Implement end-to-end federated/indexed/live search with honest coverage.

## Steps
1. Authenticate and resolve workspace and user policy.
2. Normalize query and detect intent/entities; keep LLM optional.
3. Select eligible connectors by capability and permission.
4. Build bounded plan with per-source deadline, budget and cancellation.
5. Execute index, federated, API and local paths in parallel.
6. Normalize, dedupe by stable identity, rank and preserve evidence.
7. Re-check ACL before snippets/fetch.
8. Return results, coverage, freshness, provenance and partial status.

## Completion report
Search response contract, tests for partial failure/security, latency and coverage telemetry.
