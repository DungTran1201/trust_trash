# Connector Capability Matrix

## Capability vocabulary
Use `supported`, `partial`, `unsupported`, `not_applicable` and `unknown`. Never represent unknown as supported.

| Capability | Meaning | Evidence to record |
|---|---|---|
| connect | authenticate/establish provider session | auth type, required scope, test endpoint |
| health_check | validate connection status | check time and safe error category |
| discover | enumerate available resources | hierarchy and scope |
| metadata | retrieve resource/schema metadata | metadata types and update behavior |
| search | search within source | query semantics, filters, paging and limitations |
| fetch | retrieve a specified resource | size limits and authorization behavior |
| query | structured read query | query language, read-only enforcement, limits |
| sync | copy selected resources incrementally | full/incremental cursor, deletions, backfill |
| cdc | receive source change events | insert/update/delete and transaction semantics |
| stream | consume/publish continuous events | ordering, delivery and retention |
| permission_discovery | map source ACL/roles | fidelity, refresh method and unsupported cases |
| change_detection | detect metadata/content changes | etag, version, webhook or polling interval |

## Mode selection
- `metadata_only`: catalog source resources without copying content.
- `live_query`: read source at request time.
- `indexed`: copy a scoped searchable projection.
- `replicated`: copy selected records/files into managed storage.
- `streamed`: continuously consume events.
A connector can support multiple modes. Explain freshness, cost, privacy and permission trade-offs before activation.

## Connector manifest fields
`id`, `display_name`, `connector_version`, `provider`, `provider_api_versions`, `category`, `resource_types`, `capabilities`, `auth_schemes`, `scopes`, `config_schema`, `rate_limits`, `pagination`, `sync_modes`, `permission_model`, `network_policy`, `operational_limits`, `compatibility`.

## Error taxonomy
`authentication`, `authorization`, `not_found`, `rate_limited`, `transient`, `invalid_request`, `unsupported`, `schema_drift`, `conflict`, `permanent`, `cancelled`, `unknown`. Preserve provider request ID and retry-after when safe; redact credentials and payloads.
