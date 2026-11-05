# Trust Trash Data Platform Domain Map

## Bounded contexts and ownership

| Context | Owns | Must not own |
|---|---|---|
| Identity | users, sessions, workspace membership, role grants | provider resource ACL semantics |
| Connections | configured provider accounts, scopes, credential references, connection lifecycle | query ranking or raw data transformation |
| Connector Registry | connector manifests, versions, capabilities, compatibility | per-user connection secrets |
| Resources | stable resource identity, normalized metadata, hierarchy, provenance refs | full content storage or search ranking |
| Discovery | query planning, routing, executors, result aggregation and coverage | source credentials or provider-specific payload parsing |
| Ingestion | sync plans, cursors, checkpoints, ingestion runs and raw-write coordination | business analytics models |
| Processing | processor registry/runtime, derived artifacts, model/processor execution | mutation of raw source objects |
| Storage | object/data storage abstraction and retention mechanics | source connector business rules |
| Analytics | analytical products, metrics, marts and warehouse access | universal full-text search |
| Governance | classification, policy, ACL mapping, retention and audit policy | UI-only permission decisions |
| Observability | telemetry, SLOs, alert routing and runbooks | business source-of-truth state |

## Three planes
- Control Plane: identity, connections, connector registry, metadata/policy and orchestration configuration.
- Data Plane: connector runtime, ingestion, processing, storage, event delivery and warehouse loading.
- Query & Intelligence Plane: query understanding/planning, indexed/federated/live retrieval, ranking and result response.

These are logical boundaries. They do not mandate three separate deployments.

## Data flow invariants
1. Keep original bytes/payload immutable in Bronze/raw storage.
2. Store metadata and content separately; resource record references source and derived artifacts.
3. A search index is a derived, permission-sensitive projection, not the canonical source.
4. Silver data is validated/normalized; Gold is modeled for a known analytical purpose.
5. Every derived object carries source lineage and processor/code version.
6. A cursor advances only after durable sink commit.
7. ACL revocation and deletion propagate to snippets, chunks, embeddings, caches and downstream copies.
8. A partial query reports which eligible sources were searched, skipped, denied, timed out or failed.

## Architecture evolution
Start Layered Modular Monolith plus independent worker processes. Extract a bounded context into a service only where deployment isolation, scale, fault containment, team ownership or runtime needs justify the distributed-system cost. Do not split by technical layer or one service per plugin.
