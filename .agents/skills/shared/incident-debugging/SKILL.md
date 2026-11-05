---
name: incident-debugging
description: "Diagnose and recover failures across queries, connectors, ingestion, processing workers, storage and web application operations."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Incident Debugging

## Procedure
1. Establish impact, start time, affected workspace/source/resources, severity and user-visible symptoms.
2. Capture correlation ID, query ID, connector ID, job/run ID, worker ID and deployment version.
3. Check health/saturation: error rate, latency, queue depth, worker availability, memory, storage, DB pool and provider rate limits.
4. Follow logs/traces across component boundaries; redact secrets and private content.
5. Classify failure: provider/auth, network, schema drift, code regression, resource exhaustion, poison input, permission revocation, backlog or storage/index inconsistency.
6. Stop blast radius safely: pause connector/job, reduce concurrency, disable processor or serve partial results. Avoid deleting source data.
7. Apply smallest reversible mitigation; preserve cursor/checkpoint and evidence.
8. Verify recovery with bounded test and reconcile skipped/failed records.
9. Create incident report with timeline, root cause, impact, recovery and prevention.
10. Add regression test, alert/runbook improvement and ADR/doc updates.

## Recovery safety
Do not reset cursors, purge indexes, replay a topic or run a full backfill without understanding duplication, retention and data-loss effects. Prefer idempotent replay from known checkpoints.
