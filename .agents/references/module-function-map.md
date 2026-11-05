# Backend Module Function Map

| Module | Functions/use cases | Primary records | Public events/outputs |
|---|---|---|---|
| identity | sign-in/session/workspace/member/role/service credential | User, Workspace, Membership, RoleGrant, Session | membership/role/session audit |
| connections | create, validate, inspect, pause, resume, reauth, disconnect | Connection, CredentialReference, ResourceSelection | connection state changed |
| connector_registry | list/install/validate/version/resolve manifest/capability | ConnectorDefinition, ConnectorVersion, Capability | connector registered/updated |
| resources | upsert/discover/get/list/relationship/provenance/freshness | Resource, ResourceVersion, ResourceRelation | resource discovered/changed/deleted |
| discovery | parse/plan/route/execute/aggregate/rank/coverage | SearchQuery, QueryExecution, SearchHit, SourceCoverage | query completed/partial/failed |
| ingestion | plan/run/sync/checkpoint/backfill/replay/quarantine | SyncPlan, IngestionRun, Cursor, Checkpoint, QuarantineItem | ingestion started/completed/failed |
| processing | register processor/run/cancel/validate/store derived output | ProcessorDefinition, ProcessingRun, Artifact | processor run lifecycle, artifact created |
| storage | store/get/delete/version/list object and dataset | ObjectReference, DatasetReference, StoragePolicy | storage lifecycle event |
| analytics | register data product/query metrics/publish mart | DataProduct, MetricDefinition, QueryRecord | data product published/refreshed |
| governance | classify/evaluate ACL/retention/delete/audit | Policy, Classification, AccessDecision, RetentionRule, AuditEvent | policy and access audit |
| observability | ingest telemetry, query health, alert, runbook status | Metric/Log/Trace refs, Alert, SLO | alert lifecycle |

## Layer responsibilities per module
- Presentation: transport adapters and request/response DTO only.
- Application: orchestrate use cases and transactions; coordinate ports.
- Domain: invariants, entities, value objects and policy decisions.
- Infrastructure: ORM, provider SDK, search client, storage, broker and external integration implementations.

Do not let a module invoke private repositories of another module. Expose public application contracts or versioned events.
