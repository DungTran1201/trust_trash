# Agent and Skill Index

## Choose a role

| Role profile | Use for | Main skills |
|---|---|---|
| `agents/platform-orchestrator.agent.md` | Cross-domain delivery, sequencing and handoffs | feature-discovery, implementation-planning, release-and-documentation |
| `agents/product-business-analyst.agent.md` | Product scope, actors, workflows and acceptance | feature-discovery, website-product-spec |
| `agents/solution-architect.agent.md` | Bounded contexts, layer boundaries, ADRs and system design | architecture-and-adr, implementation-planning |
| `agents/backend-domain-engineer.agent.md` | FastAPI module and domain use cases | architecture-and-adr, test-driven-change, secure-change |
| `agents/connector-engineer.agent.md` | Source connectors, capabilities, authentication and sync | connector-development, connector-lifecycle |
| `agents/data-engineer.agent.md` | Ingestion, transformation, lakehouse, streaming | ingestion-and-etl, lakehouse-warehouse, streaming-and-cdc |
| `agents/universal-search-engineer.agent.md` | Query planning, federation, indexing and result merge | universal-search, federated-query, resource-metadata |
| `agents/ai-processing-engineer.agent.md` | OCR, NLP, CV and document intelligence | document-intelligence, processor-engineering |
| `agents/data-governance-engineer.agent.md` | ACL, lineage, quality, privacy and audit | data-quality-lineage-governance, secure-change |
| `agents/observability-sre.agent.md` | Logs, metrics, traces, SLOs and incident response | data-observability, incident-debugging |
| `agents/frontend-architect.agent.md` | Frontend architecture, app state and API integration | nextjs-app-router, frontend-data-flow |
| `agents/website-builder.agent.md` | Build complete user-facing pages and features | website-feature-delivery, design-system-accessibility |
| `agents/ux-accessibility-reviewer.agent.md` | UX, accessibility, responsive and visual review | design-system-accessibility, frontend-testing-performance |
| `agents/qa-test-engineer.agent.md` | Test strategy, regression and release gates | test-driven-change, frontend-testing-performance |
| `agents/security-reviewer.agent.md` | Threat review and security verification | secure-change, frontend-security |
| `agents/technical-writer.agent.md` | Product/technical docs, runbooks and ADR quality | release-and-documentation, architecture-and-adr |

## Shared engineering lifecycle
- `skills/shared/feature-discovery/SKILL.md`
- `skills/shared/architecture-and-adr/SKILL.md`
- `skills/shared/implementation-planning/SKILL.md`
- `skills/shared/test-driven-change/SKILL.md`
- `skills/shared/secure-change/SKILL.md`
- `skills/shared/code-review/SKILL.md`
- `skills/shared/release-and-documentation/SKILL.md`
- `skills/shared/incident-debugging/SKILL.md`

## Data platform
- `skills/data-platform/connector-development/SKILL.md`
- `skills/data-platform/connector-lifecycle/SKILL.md`
- `skills/data-platform/resource-metadata/SKILL.md`
- `skills/data-platform/universal-search/SKILL.md`
- `skills/data-platform/federated-query/SKILL.md`
- `skills/data-platform/ingestion-and-etl/SKILL.md`
- `skills/data-platform/lakehouse-warehouse/SKILL.md`
- `skills/data-platform/data-quality-lineage-governance/SKILL.md`
- `skills/data-platform/streaming-and-cdc/SKILL.md`
- `skills/data-platform/processor-engineering/SKILL.md`
- `skills/data-platform/document-intelligence/SKILL.md`
- `skills/data-platform/data-observability/SKILL.md`

## Website builder
- `skills/website-builder/website-product-spec/SKILL.md`
- `skills/website-builder/website-feature-delivery/SKILL.md`
- `skills/website-builder/nextjs-app-router/SKILL.md`
- `skills/website-builder/design-system-accessibility/SKILL.md`
- `skills/website-builder/frontend-data-flow/SKILL.md`
- `skills/website-builder/data-heavy-workspaces/SKILL.md`
- `skills/website-builder/frontend-testing-performance/SKILL.md`
- `skills/website-builder/browser-extension/SKILL.md`
- `skills/website-builder/frontend-security/SKILL.md`

## Skill selection rule
Start with one lifecycle skill for new work, add one domain skill for the main capability and one cross-cutting skill for risk. Avoid loading the entire catalog for a small change.

## Product and architecture references
- `references/product-capability-catalog.md`
- `references/module-function-map.md`
- `references/website-page-function-matrix.md`
- `references/data-platform-domain-map.md`
- `references/connector-capability-matrix.md`
- `references/search-response-contract.md`
- `references/data-lifecycle-and-quality.md`
- `references/website-experience-map.md`
- `references/quality-gates.md`
