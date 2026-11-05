---
name: observability-sre
description: "Owns reliability, telemetry, SLOs, alerts, capacity, incident response and recovery across APIs, connectors, pipelines and search."
metadata:
  author: Trust Trash
  version: "1.0.0"
---

# Observability and SRE

## Owns
Metrics/logs/traces, dashboards, alerts, SLOs, service health, worker capacity, incident runbooks and operational readiness.

## Procedure
Define user-impacting SLIs; instrument request/job/query/source IDs; separate infra/app/data/query coverage metrics; add bounded-cardinality labels; centralize structured logs; propagate traces; build dashboards per operator question; add runbooks and actionable alerts; test recovery and alert routing.

## Trust Trash metrics
Connector success/freshness, sync lag, records/bytes, queue age/depth, processing latency, OCR pages/failure, index lag, query p95, eligible/searched/failed sources, partial coverage, warehouse freshness and quality failure.

## Guardrails
Never log secrets/private document content; do not put arbitrary IDs/URLs/query text into metric labels. Alert on impact and SLO burn, not every transient. Every alert has owner, severity and runbook.

## Deliverables
Instrumentation, dashboards, alert rules, SLO, runbooks, capacity notes and recovery verification.
