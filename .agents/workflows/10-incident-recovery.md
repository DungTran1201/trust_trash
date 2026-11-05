# 10 Incident Recovery

## Purpose
Diagnose and recover an incident without losing data or bypassing permissions.

## Steps
1. Establish impact, scope, start time and affected workspaces/sources.
2. Preserve logs/traces/run IDs and identify recent changes.
3. Contain safely: pause worker/source/query route or revoke credential as appropriate.
4. Determine whether data was lost, duplicated, exposed or delayed.
5. Recover from committed checkpoint or replay with idempotency.
6. Reconcile source, raw, refined, index and warehouse states.
7. Verify ACL, freshness, quality and user impact are restored.
8. Write incident report and preventive actions.

## Completion report
Recovery evidence, customer impact statement, incident report and prevention backlog.
