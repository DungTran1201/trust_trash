# Implementation Status

## Implemented in this starter
- FastAPI bootstrap and health endpoint
- Basic settings model
- Domain module folder scaffolds
- Shared Universal Resource and Search contracts
- Connector and Processor base contracts
- Worker entry-point placeholders
- Next.js landing/search placeholder
- Minimal Chrome extension reading active-tab title/URL after user action
- PostgreSQL local Compose service; optional OpenSearch and Redis profiles
- One backend smoke test

## Not implemented
- Real authentication, OAuth flows, RBAC/ABAC or tenant isolation
- Credential vault and secret encryption
- Real connectors, source synchronization, retries or cursor persistence
- Search index creation, planner, hybrid search or ranking
- Trino federation
- Data Lake, Iceberg, Data Warehouse and dbt pipelines
- Message broker event processing
- OCR, NLP, CV, embeddings or ML inference
- Production observability, alerting and dashboards
- Browser history/bookmark collection or Firefox extension

All placeholders must be replaced by tested implementations before production use.
