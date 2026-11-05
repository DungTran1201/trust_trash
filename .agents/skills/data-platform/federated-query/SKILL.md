---
name: federated-query
description: "Design safe structured queries across heterogeneous databases and lakehouse catalogs without confusing SQL federation with full-text search."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Federated Query

## Scope
Federated query is for structured data (schemas, tables, views and approved records). Use a search engine for full-text documents and semantic retrieval. A SQL engine such as Trino can be adopted when connector breadth, query scale and operational cost justify it.

## Workflow
1. Discover catalog/schema/table metadata and persist owner, classification, schema version and source capability.
2. Determine whether the request is schema discovery, bounded record lookup, aggregation or analytical query.
3. Authorize workspace, source, catalog, schema, table, column and row scope before query planning.
4. Resolve logical resource names to approved physical names using catalog metadata; never accept arbitrary client-provided catalog identifiers.
5. Build a typed query plan. Prefer parameterized SQL or a constrained query AST; do not concatenate user text into SQL.
6. Enforce read-only identity, allowlisted objects, timeout, max rows/bytes, concurrency and estimated-cost budget.
7. Push filters/projections down only where semantics are equivalent. Document unsupported operations and type coercions.
8. Execute and normalize schema/result metadata while preserving source and query provenance.
9. Return partial/failure details per source. Do not silently reinterpret denied as empty.
10. Record query plan, source, duration, rows/bytes and safe error category; redact literals and sensitive values.

## Semantics to document
Null behavior, timestamps/time zones, decimal precision, collation/case sensitivity, nested types, pagination/order guarantees, transaction consistency, snapshot isolation and source freshness differ by provider. Do not promise cross-source ACID transactions.

## Security
Read-only credentials by default. Restrict system catalogs and PII columns. Apply row/column policy at the source where possible and again in the query layer. Prevent SQL injection, arbitrary function execution, file/table functions, external network access and denial-of-service queries.

## Acceptance
Test allowlisted query, denied catalog/table/column, parameter binding, timeout, row cap, partial federation, type conversion, null/time-zone behavior, query cancellation and audit record.
