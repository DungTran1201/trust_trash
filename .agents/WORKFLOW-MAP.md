# Trust Trash Business and Engineering Workflow Map

## Product-to-production lifecycle

| Stage | Business question | Primary artifacts | Agent/skills |
|---|---|---|---|
| 1. Discover | Who has the problem and why? | Problem brief, actors, as-is/to-be, use cases | Product Analyst; feature-discovery |
| 2. Specify | What must the product do and not do? | PRD/SRS, workflows, acceptance criteria, NFRs | Product Analyst; website-product-spec |
| 3. Design | Which domain owns the behavior? | C4 diagrams, data flow, API/event contracts, ADRs, threat model | Solution Architect; architecture-and-adr |
| 4. Plan | Which vertical slice is smallest and complete? | Task breakdown, dependency map, test plan | Orchestrator; implementation-planning |
| 5. Implement | Which layer/module changes? | Domain/application/adapter/UI code | Specialist agents and domain skills |
| 6. Verify | Does behavior satisfy acceptance and invariants? | Unit, contract, integration, E2E, security checks | QA; test-driven-change |
| 7. Operate | Can the team detect and recover failures? | Metrics, logs, traces, alerts, runbooks | SRE; data-observability |
| 8. Release | Is it safe and documented? | Migration notes, release notes, docs, rollback plan | Technical Writer; release-and-documentation |
| 9. Learn | What should change based on incidents/usage? | ADR updates, quality gaps, tech-debt items | Orchestrator; incident-debugging |

## Data platform workflows

### Source onboarding
Register provider → define scope and data owner → obtain least-privilege credentials → validate connection → discover resources/schema → inspect capabilities → configure sync/index/live retrieval → run bounded test → validate permission behavior → schedule/activate → monitor freshness and health → disconnect/revoke/retention when requested.

### Resource discovery and search
Authenticate → resolve workspace → parse query → identify intents/entities → load eligible source/capability catalog → enforce source scopes → build plan with deadlines/cost limits → execute index/federated/live/local paths in parallel → normalize results → deduplicate by stable identity → rank → re-check ACL → return results plus coverage/provenance/freshness → record query telemetry.

### Ingestion and processing
Discover/change detection → extract page/record/object → checkpoint → validate envelope/schema → persist immutable raw payload → emit durable event → process/normalize/enrich → quality checks → write refined artifact → update metadata/lineage → index searchable projection → publish analytical datasets when appropriate → reconcile failures and reprocess safely.

### Document intelligence
Receive source artifact → safety/type/size check → classify document → parse text/layout/tables or OCR → preserve page/coordinate references → normalize outputs → optional NLP/entity extraction → quality/confidence evaluation → write derived artifacts with processor/model version → index → preserve original and provenance.

### Data product lifecycle
Define consumer/business metric and grain → identify sources → staging models → intermediate transformations → marts/metrics → data tests → lineage/docs/owner → publish to warehouse/API/BI → monitor freshness and quality → deprecate with notice.

## Website builder workflows

### Build a feature page
Product brief → user journey → route/IA → information hierarchy → wireframe/state inventory → design tokens/components → API contract → server/client data boundary → implementation → accessibility/responsive review → automated tests → performance check → docs/release.

### Build a data-heavy screen
Define data grain and actions → choose table/list/chart/detail interaction → decide pagination/filter/sort server-side → URL state for shareable filters → loading/empty/partial/error/forbidden/stale states → virtualization only if needed → keyboard/accessibility → E2E for critical flow.

### Build a connection wizard
Provider selection → capability preview → permission/scope explanation → OAuth/credential input → secret-safe handoff → connection validation → resource discovery → select resources/scopes → choose live/index/sync mode → run test sync → show health and next steps.

## Cross-cutting quality gates
Security and permission checks, tenant isolation, source provenance, data-loss safety, accessible interaction, typed contracts, tests, observability, documentation and rollback/recovery are part of the feature—not follow-up tasks.
