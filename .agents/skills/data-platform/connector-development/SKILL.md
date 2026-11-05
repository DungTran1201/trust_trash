---
name: connector-development
description: "Build a source connector using the Trust Trash connector SDK, explicit capabilities, least-privilege authentication and normalized resource contracts."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Connector Development

## Purpose and boundaries
A connector is an adapter to one external system. It does not own universal search ranking, UI presentation, cross-source aggregation or downstream business analytics. It must declare capabilities honestly and expose source-native behavior through stable Trust Trash contracts.

## Discovery before implementation
1. Identify provider product/API and exact resource types in scope (account, project, bucket, schema, table, page, repository, issue, browser profile, etc.).
2. Read current official provider docs and terms. Verify API version, authentication flow, scopes, pagination, rate limits, quotas, change tokens, webhooks, payload size, deprecation and regional behavior.
3. Separate discovery, metadata, search, fetch, sync, CDC/stream, permission discovery and health-check capabilities. Mark each `supported`, `partial`, `unsupported` or `not_applicable` with explanation.
4. Define data owner, connection scope, source identity, retention, freshness target and expected query/update costs.

## Implementation lifecycle
1. Create manifest with stable connector ID, display name, version, provider/API versions, category, capabilities, auth schemes, resource types, scopes, config schema and operational limits.
2. Implement configuration validation before network activity. Never accept secrets in ordinary config or log them.
3. Implement `connect`, `health_check`, `discover`, `get_metadata`, `search`, `fetch`, `sync` and optional `stream` only where capability is declared. Use typed request/result envelopes.
4. Support pagination/cursors, bounded concurrency, provider rate limits, retry-after, exponential backoff with jitter and cancellation.
5. Preserve `source_id`, provider-native `external_id`, canonical URI, source timestamps, etag/checksum, owner and ACL reference.
6. Normalize provider errors into auth, permission, not-found, rate-limit, transient, invalid-request, unsupported and permanent-failure categories. Keep safe diagnostic detail, not raw secrets/payloads.
7. Make sync idempotent; persist cursor only after durable sink commit. Handle deleted/renamed resources and permission changes.
8. Add adapter contract tests using recorded fixtures or provider sandbox. Mock network for unit tests; keep live tests opt-in and credential-gated.
9. Add metrics: request count/latency, rate-limit events, pages/records/bytes, retries, cursor lag, auth failures and last successful sync.

## Required failure behavior
- Expired credentials: mark connection `reauth_required`; do not retry indefinitely.
- Permission denied: preserve source-level failure/coverage; do not treat as empty results.
- Rate limit: respect provider instruction and expose delayed/backoff status.
- Partial pagination failure: resume from last committed cursor without duplicating committed data.
- Provider schema drift: quarantine incompatible records and emit a schema-change event.

## Trust Trash invariants
Connectors run as untrusted integration code. Scope credentials to minimum resources/actions. Do not log access tokens, cookies, signed URLs or private payloads. Do not bypass provider ACL. Search result snippets and fetched content must be checked against current effective permissions. Never assert a capability that the provider/API cannot guarantee.

## Deliverables and acceptance
Connector manifest, adapter, config schema, permission mapping, contract tests, fixtures, README/runbook, capability matrix entry and an end-to-end test proving discover → search/fetch or sync → normalized resource → provenance. Include explicit unsupported capabilities.
