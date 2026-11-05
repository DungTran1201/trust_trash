# Trust Trash Product Capability Catalog

This catalog maps product domains to concrete user capabilities, workflows, API responsibilities, events and acceptance outcomes. It is a design baseline; implementation status must be checked in `docs/architecture/implementation-status.md`.

## 1. Identity and Workspace

| Capability | User function | Key workflow | Core rules |
|---|---|---|---|
| Sign-in/session | Sign in, sign out, renew session | Authenticate → establish session → audit | Secure cookie/session, CSRF policy, session revocation |
| Workspace | Create/select workspace, invite members | Create → assign owner → add members → switch | Tenant scope derived/verified server-side |
| Roles | Assign admin/operator/analyst/developer/viewer | Grant → review → revoke | Least privilege, audit all changes |
| API access | Create/revoke service credentials | Request → scope → reveal once → rotate/revoke | Hash/secret vault, never show secret again |

## 2. Connections and Connector Registry

| Capability | User function | Workflow | Outputs |
|---|---|---|---|
| Provider catalog | Browse/search available integrations | Select provider → inspect features/scopes | Provider and connector manifest |
| Add connection | Connect cloud/database/SaaS/site/browser | Draft → auth → validate → discover | Connection record, secret reference |
| Capability inspection | See live/index/sync/CDC/stream/ACL support | Read manifest → explain limitations | Capability report |
| Resource selection | Choose projects/buckets/schemas/tables/folders | Discover → filter → select scope | Resource selection policy |
| Sync mode | Select metadata/live/index/replicate/stream | Preview trade-offs → confirm | Sync plan |
| Connection health | Test, pause, resume, reauth, disconnect | State transition + audit | Health and lifecycle events |
| Connector operations | Inspect version, quotas, errors, cursor | Run → observe → retry/recover | Metrics, logs, run history |

## 3. Resources and Data Catalog

| Capability | User function | Required data |
|---|---|---|
| Browse hierarchy | Navigate provider/account/schema/folder/repository | parent resource and child resources |
| Schema inspect | View columns/types/constraints | schema snapshot and version |
| Resource details | View URI, owner, type, source timestamps | normalized resource metadata |
| Provenance | Trace original source and derived outputs | lineage references and run IDs |
| Freshness | Know whether source/index/output is current | source_updated_at, synced_at, indexed_at |
| Relationship | View related records/documents/code/assets | typed edges with evidence/confidence |
| Classification | See sensitivity and ownership | classification and stewardship metadata |

## 4. Universal Search and Retrieval

- Search by keyword, identifier, phrase, structured filter and (when configured) semantic meaning.
- Filter by workspace-authorized source, resource type, freshness and metadata.
- Execute indexed, federated, provider API or local-agent search according to declared capability.
- Retrieve safe snippet/preview and open original resource after authorization re-check.
- Display result source, native ID, provenance, timestamps, freshness and explainable match signals.
- Display query status and source coverage: eligible, searched, skipped, unsupported, unauthorized, timed out and failed.
- Support cursor pagination, sort, cancel and bounded result budgets.
- Distinguish no matches from sources that were unavailable or not queried.

## 5. Ingestion and Data Pipelines

| Capability | User function | Operational behavior |
|---|---|---|
| Sync plan | Configure full/incremental/cursor/CDC | Persist mode, schedule and limits |
| Run now | Trigger manual sync | Create run, authorize, execute and track |
| Schedule | Configure cadence/window | Orchestrator owns trigger; no duplicate scheduler |
| Run history | Inspect duration, records, bytes and state | Immutable run record |
| Retry | Retry failed safe work | Bounded retry and idempotency |
| Backfill/replay | Reprocess selected range/resource | Preview impact, checkpoint and version outputs |
| Quarantine | Inspect invalid records | Safe reference, reason, replay action |
| Pause/resume | Control source or pipeline | Stop new work and drain/cancel safely |

## 6. Processing and Intelligence

- Processor catalog: supported input types, output artifacts, version, resources, privacy mode.
- Run processor: select resource/scope, config, model and resource budget.
- Document extraction: text, layout, page regions, tables and OCR.
- NLP: language, entities, classification, relation extraction and optional summaries.
- CV: image preprocessing, classification/detection and structured results.
- Audio/video: transcription, segments, frame/scene metadata when supported.
- Evaluation: golden set, quality metrics, latency, memory and failure rate.
- Reprocessing: run a newer processor version without overwriting source or prior provenance.

## 7. Lakehouse, Warehouse and Analytics

- Browse Bronze/Silver/Gold datasets and their schemas, owners, freshness, quality and lineage.
- Explore analytical products and their grain/measure definitions.
- Query approved datasets with read-only SQL and limits.
- Expose warehouse views/API/BI datasets only with documented ownership and permissions.
- Manage compaction, snapshot retention and small-file health as operational tasks, not ad hoc UI actions.

## 8. Governance and Security

- Role and policy management; workspace and source scope.
- Secret references and token lifecycle; never return stored secret values.
- Data classification, ownership, retention and deletion requests.
- ACL synchronization and permission checks before search snippet/fetch/export.
- Audit connect/disconnect, scope changes, access, exports, policy changes and deletion.
- Data subject/source deletion propagates to raw copies, extracted text, chunks, embeddings, caches, search index and warehouse according to policy.

## 9. Observability and Operations

- Platform health: API, workers, DB, object storage, search and broker.
- Connector health and provider quota/rate-limit status.
- Pipeline/processor run states, queue age/depth and retries.
- Query p50/p95, source-level latency, error and partial coverage.
- Data freshness, volume anomalies, schema drift and quality failures.
- Centralized logs/traces with correlation and trace IDs.
- Alert center with owner, severity, runbook and resolution status.

## Cross-domain product rule
A user action that changes access, scope, lifecycle, data visibility or derived content must be represented in an auditable workflow with explicit status and recovery behavior. Every page maps to a backend capability and acceptance criteria; a visual-only screen is not a delivered feature.
