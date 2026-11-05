---
name: connector-lifecycle
description: "Operate the full connection lifecycle from provider authorization and discovery through sync, reauthorization, disconnect, deletion and recovery."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Connector Lifecycle

## Lifecycle states
Model connection state explicitly: `draft`, `auth_pending`, `validating`, `connected`, `degraded`, `reauth_required`, `paused`, `disconnecting`, `disconnected`, `error`. Do not infer connection health from the existence of a credential record.

## Onboarding workflow
1. User selects provider and sees supported capabilities, requested scopes and data categories before authorizing.
2. Create a connection draft bound to workspace and creator.
3. Complete OAuth/service-account/local-agent handshake using a secret-safe flow (PKCE/state for OAuth where applicable); store secret in a vault and persist only a reference.
4. Validate credentials with a minimal health check; report missing scopes separately from invalid credentials.
5. Discover resource hierarchy and schemas without downloading full content by default.
6. Let user select resources and modes: metadata-only, live query, index, incremental sync, full replication or stream. Explain costs/freshness and implications.
7. Run a bounded sample; validate ACL mapping and source provenance before activating.
8. Schedule sync or register webhook/CDC only after explicit activation.

## Ongoing operations
Track `last_checked_at`, `last_success_at`, source cursor, sync watermark, error class, retry time, capability version and provider API version. Support pause/resume, reauth, scope change, incremental rescan and backfill. A failed sync must not overwrite the last good snapshot.

## Disconnect and deletion
1. Stop new query fan-out and scheduled work.
2. Cancel or drain active jobs safely.
3. Revoke provider token when supported and delete local secret reference/material.
4. Apply user-selected retention policy to raw copies, derived data, embeddings and indexes.
5. Tombstone or delete resources and invalidate cache/index entries; retain only legally/operationally required audit metadata.
6. Emit an audit event and show completion/partial failure clearly.

## Failure & recovery
Re-authenticate rather than retrying permanent authorization errors. Retry transient provider outages with jitter and budget. Resume from committed cursor. Detect revoked/removed resources and changed ACLs. A reconnected provider must not automatically widen scopes beyond the prior approved scope.

## UI requirements
Connection list must show provider, owner, scope count, enabled capabilities, status, last check, last sync, freshness, resource count and action. Details view must show permissions/scopes, selected resources, sync history, errors, pause/reauth/disconnect and deletion policy.

## Acceptance
Test create, invalid credential, insufficient scope, empty discovery, activation, paused, expired token, rate limit, provider outage, reauth, disconnect, deletion propagation and audit history. Never show `connected` until validation succeeds.
