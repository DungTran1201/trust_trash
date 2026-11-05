---
name: ingestion-and-etl
description: "Build durable batch ingestion and ETL/ELT workflows with checkpoints, immutable raw data, quality gates and safe reprocessing."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Ingestion and ETL

## Lifecycle
Source discovery/change detection → extract → checkpoint → validate envelope → durable raw write → emit event → transform → quality checks → refined write → metadata/lineage update → optional indexing/warehouse publish.

## Extraction
- Support full snapshot and incremental/cursor modes explicitly.
- Persist cursor/watermark only after the corresponding sink write commits.
- Handle pagination, deletions/tombstones, source schema drift and late updates.
- Bound concurrency and bytes; respect provider rate limits and retry-after.
- Make each batch/task idempotent using source identity, cursor/window and content checksum.

## Storage rules
Raw/Bronze is immutable from the application perspective. Store original payload/file plus an envelope containing source, external ID, URI, timestamps, checksum, connector version, run ID and classification. Never replace the raw artifact with cleaned text or a converted file. Derived outputs go to separate versioned paths/tables.

## Transformation
Keep extraction, normalization, enrichment and analytics models separate. Define input/output schema and null/type rules. Make transformations deterministic where possible. Record code/processor version and parameters. Avoid mixing source connector concerns with business transformations.

## Failure behavior
Transient: bounded exponential backoff with jitter. Permanent: stop and expose actionable error. Invalid data: quarantine with reason and safe reference. Poison message: dead-letter after configured attempts. Sink unavailable: do not advance cursor. Partial batch: commit only confirmed records or use a recoverable staging/manifest protocol.

## Reprocessing
Support replay by source/resource, ingestion run, time window, dataset or processor version. Reprocessing creates new derived versions; do not mutate historical provenance or duplicate warehouse facts. Provide dry-run/impact preview for destructive rebuilds.

## Acceptance
Test initial load, incremental update, deletion, page boundary, retry, process crash before/after sink commit, duplicate event, schema change, quarantine, backfill, raw immutability and end-to-end lineage.
