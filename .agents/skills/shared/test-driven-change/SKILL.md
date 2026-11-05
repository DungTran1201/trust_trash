---
name: test-driven-change
description: "Choose and implement proportionate tests for domain logic, connector contracts, data pipelines, API behavior and frontend workflows."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Test-Driven Change

## Test layers
1. Unit: pure domain rules, mapping, parsers, ranking and validation.
2. Contract: connector/processor interfaces, API/event schemas and compatibility.
3. Integration: database, object storage, OpenSearch, queue, provider adapters and repository mapping.
4. Component: UI rendering and interactions with controlled dependencies.
5. E2E: critical user journeys through browser and API.
6. Performance/resilience: bounded fan-out, large documents, throughput, timeout, retry, backpressure and degradation.

## Procedure
- Convert acceptance criteria into tests before or alongside implementation.
- Use deterministic fixtures and fake clocks/IDs where ordering matters.
- Mock at external boundaries, not every internal function; add adapter tests for real serialization/query behavior.
- Test allowed and denied access, including cross-tenant attempts.
- Test partial outcomes, at-least-once delivery, idempotent reprocessing and cursor/checkpoint failure boundaries.
- Test schema drift, nullability, uniqueness, freshness, duplicate delivery, empty partitions, late data and source deletion where relevant.
- Test keyboard-only interaction, labels, focus, responsive breakpoints, route states and URL restoration.
- Add regression coverage for confirmed defects.

## Quality gate
Report exact commands/outcomes. Do not weaken failing assertions just to get green. If a check is unavailable, say why and what remains unverified.
