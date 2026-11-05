---
name: data-observability
description: "Instrument connector, query, ingestion, processing and storage operations with actionable metrics, logs, traces, coverage, freshness and recovery runbooks."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Data Observability

## Four observability dimensions
1. Infrastructure: CPU, RAM, disk, network, containers, DB and broker health.
2. Application: request rate, errors, latency, saturation, worker state and queue depth.
3. Data/pipeline: records/bytes, freshness, volume, schema changes, quality failures, lineage and backlog.
4. Query coverage: eligible/searched/skipped/unsupported/unauthorized/timed-out/failed sources and per-source latency/freshness.

## Instrumentation
Use structured JSON logs, consistent service/module/worker/source/run/query IDs, metrics with bounded-cardinality labels and traces with propagated trace/context IDs. Prefer OpenTelemetry semantic conventions. Never put user IDs, raw queries, document IDs or arbitrary URLs into metric labels.

## Required events and metrics
Connection validation, sync start/complete/fail, cursor age, provider rate limits, extraction bytes/records, retry count, queue wait, processing duration, OCR pages/errors, index lag, search fan-out, result count, partial coverage, warehouse load and data freshness.

## Alert design
Alert on user-impacting symptoms and SLO burn, not every transient exception. Include owner, severity, threshold/window, runbook, dedup/grouping and recovery condition. Separate warning from paging. Avoid alert storms from per-record failures.

## Operations
Every dashboard must answer: what is unhealthy, who owns it, what changed, user/data impact, where to inspect, how to recover and how to verify recovery. Maintain runbooks for expired credentials, provider outage, stuck cursor, DLQ growth, indexing lag, storage full, quality regression and ACL revocation.

## Privacy
Redact credentials, authorization headers, cookies, signed URLs, PII and private document contents. Avoid high-cardinality labels and unbounded log retention.

## Acceptance
Test metrics emission, trace propagation, log correlation, queue lag alert, connector failure alert, data freshness alert, partial search coverage and privacy redaction.
