# Trust Trash Website Experience Map

## Navigation / workspaces
1. Universal Search: query, source/type filters, results, source coverage, freshness, provenance, preview and open-at-source.
2. Connections: provider catalog, auth/scope explanation, connection test, resource discovery/selection, sync mode, health, reauth, pause and disconnect.
3. Data Explorer: connection/catalog/schema/resource tree, schema details, metadata, sample/preview, ACL, quality and lineage.
4. Pipelines: definitions, runs, schedules, assets/tasks, timeline, logs, retry/backfill/cancel, input/output and runbook.
5. Intelligence Studio: processor catalog, input scope, configuration, resource needs, dry-run, results, quality and version.
6. Lakehouse & Analytics: layers/datasets, data products, SQL/BI entry points, freshness, owners and quality.
7. Observability: platform health, connectors, workers, queues, query latency/coverage, data freshness, alerts, traces and runbooks.
8. Governance & Settings: workspaces, users, roles, policies, classifications, retention, audit and provider credentials.

## Global UI states
Loading, refreshing, empty, partial, stale, offline, forbidden, not found, error, success and destructive confirmation. A partial search must preserve per-source status. A provider connection must show scopes and selected resources, not just a green connected badge.

## UX principles
- Search is the primary landing workspace.
- Keep provenance and freshness visible at the result level.
- Do not represent a failed source as zero results.
- Use progressive disclosure for technical metadata.
- Prefer server-side filtering/pagination for large datasets.
- Ensure keyboard use, visible focus, semantic headings, accessible status announcements and responsive reflow.
- Heavy charts and graphs need text/table alternatives.
