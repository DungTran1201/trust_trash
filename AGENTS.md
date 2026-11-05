# Trust Trash — Repository Instructions

## Mission
Trust Trash is a **Unified Data Intelligence Platform**. It connects authorized data sources; discovers, searches, retrieves, synchronizes and processes heterogeneous resources; and serves governed analytics. It is not merely an ETL application and must not silently claim complete coverage when a source is unavailable or unsupported.

## Architecture baseline
- Start with a **Layered Modular Monolith** and independent worker processes. Extract selective microservices only when measured scaling, deployment, isolation or ownership needs justify it.
- Frontend and backend have separate presentation, application, domain and infrastructure boundaries.
- Backend domain modules own their business rules and data. Cross-module calls use public application contracts or events, never another module's private implementation or tables.
- Domain code must not import frameworks, database drivers, provider SDKs, OpenSearch clients or cloud SDKs.
- Connector capabilities are explicit. Never infer that every connector supports search, sync, CDC, streaming, schema discovery or permission discovery.
- Preserve source identity, URI, provenance, ACL reference, freshness and processing version across every transformation.
- Separate source data, metadata, search index, derived content and analytical models.

## Repository map
- `apps/web/`: Next.js website builder and product UI. Read `apps/web/AGENTS.md` and relevant nested instructions.
- `apps/browser-extension/`: browser integration; treat browser permissions and local data as sensitive.
- `apps/local-agent/`: optional user-controlled local execution agent; never treat it as unrestricted machine access.
- `backend/src/trust_trash/modules/`: backend bounded contexts, each internally layered.
- `backend/src/trust_trash/connector_sdk/`: connector contracts and runtime abstractions.
- `backend/src/trust_trash/processor_sdk/`: processor contracts and runtime abstractions.
- `backend/src/trust_trash/workers/`: independent execution entry points.
- `contracts/`: versioned cross-module and cross-process contracts.
- `orchestration/`: Dagster definitions and pipeline orchestration.
- `infra/`: local and deployment infrastructure configuration.
- `.agents/`: role profiles, reusable skills, workflows, references and templates.

## Before changing code
1. Read this file and the closest nested `AGENTS.md` files on the path being changed.
2. Inspect the current implementation, tests, conventions and `docs/architecture/implementation-status.md`. Do not assume a placeholder is implemented.
3. Load only relevant skills from `.agents/skills/`.
4. For multi-file or cross-domain work, write a short plan: business outcome, affected modules, contracts, data/security impacts, tests and docs.
5. Prefer the smallest complete vertical slice. Do not create speculative abstractions or services.

## Non-negotiable engineering rules
- Validate external input at boundaries; validate domain invariants in the domain layer.
- Use typed DTOs/contracts and explicit error models. Do not expose provider exceptions or internal stack traces.
- Apply tenant/workspace scope and source ACL checks before returning indexed or live-retrieved content. Re-check before content fetch when permissions can change.
- Never log credentials, access tokens, cookies, raw secrets, private document contents or unrestricted PII.
- Make retries safe: use idempotency keys, checkpoints/cursors, bounded retries with backoff and dead-letter/quarantine handling where applicable.
- Never overwrite raw source objects with derived data. Store derived artifacts with lineage and processor version.
- Use UTC timestamps internally; distinguish source-updated, ingested, processed and indexed timestamps.
- Query fan-out must have deadlines, concurrency limits, cancellation and partial-result semantics.
- Do not claim exhaustive search. Report searched, skipped, unauthorized, unsupported, timed-out and failed sources distinctly.
- Explain why a production dependency is needed, its operational cost and fallback/alternative.
- Do not turn every module or processor into a microservice.

## Definition of done
- Business behavior and acceptance criteria are satisfied.
- Relevant unit, contract, integration and/or E2E tests are added or updated.
- Lint, type checks and targeted tests pass; report checks that could not run.
- API, event, resource, connector or database contract changes are versioned and documented.
- Permissions, tenant isolation, secrets, error handling, retries and observability are reviewed.
- User-facing loading, empty, partial, error and success states are handled where applicable.
- Architecture/product docs and implementation status are updated when behavior or boundaries change.

## Commands (confirm against current manifests)
- Backend install: `cd backend && pip install -e ".[dev]"`
- Backend tests: `cd backend && pytest`
- Backend lint: `cd backend && ruff check src tests`
- Frontend dev: `cd apps/web && npm run dev`
- Frontend checks: inspect `apps/web/package.json`; run available scripts.
- PostgreSQL: `docker compose -f infra/compose/docker-compose.yml up -d postgres`
- Agent pack validation: `python .agents/scripts/validate_agent_pack.py`

## Task routing
- Product/business: `.agents/skills/shared/feature-discovery/SKILL.md`
- Architecture: `.agents/skills/shared/architecture-and-adr/SKILL.md`
- Connector: `.agents/skills/data-platform/connector-development/SKILL.md`
- Search: `.agents/skills/data-platform/universal-search/SKILL.md`
- Ingestion/ETL: `.agents/skills/data-platform/ingestion-and-etl/SKILL.md`
- Quality/lineage/governance: `.agents/skills/data-platform/data-quality-lineage-governance/SKILL.md`
- Website: `.agents/skills/website-builder/website-feature-delivery/SKILL.md`
- UI/accessibility: `.agents/skills/website-builder/design-system-accessibility/SKILL.md`
- Full catalog: `.agents/AGENT-INDEX.md`

## Documentation authority
`docs/` is the project knowledge base and source of truth. Keep this file concise; add durable detail to design docs, runbooks, ADRs or skill references.
