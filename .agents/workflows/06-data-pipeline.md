# 06 Data Pipeline

## Purpose
Build a durable ingestion-to-published-data workflow.

## Steps
1. Define dataset grain, owner, freshness and contract.
2. Choose full/incremental/CDC and establish cursor/checkpoint commit point.
3. Extract and validate source envelope.
4. Persist immutable raw payload and ingestion metadata.
5. Transform to refined outputs with version and idempotency.
6. Run quality checks and quarantine failures with reason.
7. Publish index/Gold outputs and lineage.
8. Test replay, retry, schema drift, deletion and recovery.

## Completion report
Pipeline spec, data contract, lineage, quality checks and runbook.
