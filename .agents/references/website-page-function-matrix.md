# Website Page and Function Matrix

| Workspace / route family | Main user jobs | Primary functions | Critical states | Backend/domain owner |
|---|---|---|---|---|
| Universal Search | Find related data across connected sources | Search, filter, sort, paginate, preview, open source, inspect coverage | loading, empty, partial, stale, forbidden, timeout, cancelled | discovery/resources/governance |
| Connections catalog | Find an integration | provider search, capability compare, auth scopes, documentation | unsupported, unavailable, permission explanation | connector_registry |
| Connection setup | Connect and configure source | OAuth/secret ref, validate, discover, select scope/mode, test sync | auth pending, invalid, insufficient scope, degraded | connections/connector_registry |
| Connection detail | Operate a source | health check, pause/resume, reauth, sync history, disconnect | connected, degraded, reauth, paused, disconnecting | connections/ingestion |
| Data Explorer | Understand resources | hierarchy, schema, preview, metadata, provenance, ACL, lineage | loading, large resource, unsupported preview, denied, stale | resources/governance/storage |
| Pipeline list/detail | Operate data workflows | definitions, runs, schedule, run now, cancel, retry, backfill, logs | queued, running, succeeded, failed, cancelled, partial | ingestion/processing/orchestration |
| Intelligence Studio | Process resource data | processor catalog, config, run, preview, compare versions, quality | unsupported input, resource limit, low confidence, failed | processing |
| Lakehouse/Analytics | Consume curated data | Bronze/Silver/Gold, datasets, SQL, marts, freshness, owner | stale, quality-failed, query timeout, no permission | storage/analytics |
| Observability | Diagnose platform | health, metrics, logs, traces, source coverage, alerts, runbooks | alert open/acknowledged/resolved, telemetry gap | observability |
| Governance | Manage data safety | policies, roles, classification, retention, deletion, audit | pending approval, partial deletion, policy conflict | identity/governance |
| Settings | Configure workspace | members, roles, API clients, preferences, provider defaults | unauthorized, validation, revoke confirmation | identity/connections |

## Every page specification must include
Purpose/persona, route, permissions, primary action, secondary actions, data contract, filter/URL state, loading/empty/partial/stale/error/forbidden states, responsive behavior, accessibility, analytics, tests and acceptance criteria.
