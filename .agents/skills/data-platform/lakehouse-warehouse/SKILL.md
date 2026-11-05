---
name: lakehouse-warehouse
description: "Design Bronze/Silver/Gold, object storage, open table formats and analytical warehouse models with clear responsibilities."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Lakehouse and Warehouse

## Responsibilities
- Object storage: durable bytes and large objects.
- Bronze: source-aligned raw records/files and ingestion envelopes.
- Silver: validated, normalized, typed, deduplicated and enriched datasets.
- Gold: business/analytical data products, aggregates and marts.
- Table format (e.g. Iceberg): table metadata, snapshots, schema/partition evolution over files.
- Query engine (e.g. Trino/Spark): compute and access; not storage itself.
- Warehouse/OLAP engine (e.g. ClickHouse): analytical serving based on measured workload.

## Modeling process
1. Define business question, consumer, grain, freshness, owner and quality SLA.
2. Profile source data; define staging model with minimal source-faithful renaming/casting.
3. Add intermediate models for reusable business logic.
4. Build marts using documented grain, measures, dimensions and slowly changing dimension policy where relevant.
5. Add uniqueness, not-null, relationships, accepted values and freshness tests.
6. Document models, owners, lineage and metric definitions.
7. Publish only approved data products; keep raw/PII access restricted.

## Data layout
Choose partitioning from observed query/filter patterns and file sizes. Avoid high-cardinality partition explosion and too many small files. Track compaction, snapshot expiration, orphan-file cleanup and retention. Never hardcode cloud credentials in SQL/model files.

## Consistency and performance
Document snapshot semantics and freshness. Prefer columnar formats for analytics. Measure scan bytes, query latency, partitions pruned, file count and warehouse load cost. Separate operational metadata DB from analytical warehouse.

## Acceptance
Validate grain, schema, data tests, incremental idempotency, late-arriving data, snapshot recovery, schema evolution, access policy and cost/performance with a representative query.
