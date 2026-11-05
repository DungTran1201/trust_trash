---
name: code-review
description: "Review Trust Trash changes for correctness, architecture boundaries, security, reliability, tests, UX and maintainability."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Code Review

Review in this order:
1. Behavior: does the change solve the use case and cover acceptance/edge cases?
2. Data correctness: are identity, provenance, timestamps, schema and source semantics preserved?
3. Authorization: are tenant/workspace/source/resource ACLs checked at every read/fetch boundary?
4. Architecture: are layer/module boundaries respected, contracts versioned and abstractions justified?
5. Reliability: timeout, cancellation, retries, idempotency, cursor, backpressure and partial failures?
6. Security: secrets, SQL, URLs, files and external payloads handled safely?
7. Performance: N+1 calls, unbounded fan-out, huge payloads, unbounded rendering or waterfalls?
8. Observability: can operation be correlated without leaking sensitive data?
9. Tests: do they prove behavior and include negative/partial paths?
10. Docs: are API, UX, operational and architecture docs updated?

## Finding format
Severity (blocker/high/medium/low), file/line, evidence, impact and concrete recommendation. Do not nitpick formatter-enforced style. Do not approve a visible security or data-loss path just because tests pass.
