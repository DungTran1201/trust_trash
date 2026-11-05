---
name: streaming-and-cdc
description: "Implement event-driven ingestion and streaming with explicit delivery semantics, checkpoints, event time, replay and consumer lag monitoring."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Streaming and CDC

## Design before technology
Identify event producer, event owner, key, ordering requirement, schema/version, volume, retention, delivery semantics, replay need and downstream SLA. Decide whether a queue, log-based broker, CDC or scheduled polling is sufficient before introducing Kafka/Flink.

## Event contract
Include `event_id`, `event_type`, `event_version`, `occurred_at`, `published_at`, `source_id`, `resource_id`/key, `workspace_id`, `trace_id`, payload and schema reference. Do not put secrets or unnecessary personal data in events.

## Producer rules
Use stable keys where per-entity ordering matters. Publish only after source state is durably committed or use transactional outbox. Schema changes must be backward-compatible or use a new version/topic. Producers must handle broker unavailability without losing source cursor state.

## Consumer rules
Assume at-least-once delivery unless end-to-end evidence proves otherwise. Consumers must be idempotent. Commit offset only after durable side effect. Use bounded retries, retry topics or DLQ, poison-message inspection, pause/resume and replay tooling. Do not claim exactly-once across arbitrary external sinks.

## Stream processing
Specify event time vs processing time, watermark, window, late-event policy, state/checkpoint, ordering, dedup key and state recovery. Keep deterministic transformations and version outputs. CDC must distinguish insert/update/delete, transaction metadata and snapshot phase.

## Operations
Monitor producer errors, throughput, partition skew, consumer lag, processing latency, checkpoint age/failures, DLQ depth, rebalance and broker disk retention. Document replay blast radius and offset reset procedure.

## Acceptance
Test duplicate, out-of-order, late event, schema evolution, consumer crash before/after commit, broker outage, replay, poison event, delete event and lag alert.
