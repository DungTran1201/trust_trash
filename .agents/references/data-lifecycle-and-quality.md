# Data Lifecycle and Quality Reference

## Lifecycle states
Discovered → Selected → Authorized → Ingesting → Raw persisted → Validated → Refined → Indexed and/or Curated → Published → Stale/Paused/Deleted.
A state is not inferred from file existence alone. Record the responsible run and timestamps.

## Timestamp semantics
Keep distinct: `source_created_at`, `source_updated_at`, `discovered_at`, `ingested_at`, `processed_at`, `indexed_at`, `published_at`. Store UTC instants; preserve source timezone/offset as metadata where needed.

## Quality dimensions
Completeness, uniqueness, validity, consistency, timeliness, accuracy (where measurable), referential integrity and schema conformance. Define rules and thresholds per data product; no universal threshold without business context.

## Quarantine
Keep safe references to invalid artifact/record, error category, rule/version, run ID and replay route. Restrict access to quarantined data. Do not silently drop it or log sensitive payloads.

## Reprocessing
Re-run from immutable raw or source checkpoint. Version derived outputs. Ensure idempotent writes or use new output version. Reindex and rebuild analytical products as needed. Document whether replay is selective, partition-level or full rebuild.

## Deletion and retention
Deletion/retention applies to raw copies, derived text, chunks, embeddings, search indexes, caches, warehouse tables and exports. Track completion and exceptions. Retain only the audit metadata required by policy/law; do not keep content merely because deletion across stores is inconvenient.
