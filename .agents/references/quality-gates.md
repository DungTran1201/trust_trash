# Trust Trash Quality Gates

## Architecture
- Bounded context and ownership identified.
- Dependency direction respected; no framework/provider imports in domain.
- API/event/resource schema changes are versioned.
- No new service without a deployment/scaling/isolation reason.

## Data platform
- Source identity, timestamps, provenance and ACL retained.
- Cursor commit follows durable write.
- Raw source immutable; derived outputs versioned.
- Idempotency/retry/timeout/cancellation defined.
- Partial failures and coverage are explicit.
- Data quality and lineage evidence is recorded.
- Large data paths are streaming/paginated/bounded.

## Search
- Query fan-out bounded by deadline/concurrency/result budget.
- Denied/timeout/unsupported are not presented as no-results.
- ACL rechecked before snippets/fetch.
- SQL read-only, allowlisted and parameterized.
- Freshness and provenance visible.

## Website
- Loading/empty/partial/stale/error/forbidden states implemented as relevant.
- Semantic HTML, keyboard path, focus and accessible names.
- Responsive layout and theme contrast verified.
- Sensitive data not leaked through browser bundles, URL or shared cache.
- Typecheck, tests and production build pass.

## Release
- Tests map to acceptance criteria.
- Migrations/backfills/rollback plan reviewed.
- Secrets and privacy reviewed.
- Metrics/logs/traces/alerts/runbook updated.
- Docs and implementation status agree with code.
- Skipped checks and residual risks stated explicitly.
