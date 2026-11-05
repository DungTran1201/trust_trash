---
name: processor-engineering
description: "Develop plug-in processors for structured, document and multimodal data with versioned contracts, isolation, resource limits and reproducible outputs."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Processor Engineering

## Processor contract
A processor declares stable ID, version, input resource types/formats, output artifact types/schema, dependencies/models, CPU/RAM/GPU needs, max input size, timeout, determinism, language support, security profile and configuration schema.

## Execution lifecycle
Validate manifest → authorize resource → fetch or stream input → verify type/size/checksum → stage read-only input → execute in isolated worker → validate output schema → persist derived artifact/version → record provenance/metrics → publish resource/index events.

## Design rules
- Never mutate source bytes. Derived artifacts use separate IDs/paths and include source references.
- Avoid loading very large files fully into RAM; stream/chunk/page where possible.
- Bound CPU, memory, file descriptors, subprocesses, network egress and execution time.
- Treat parser/model output as untrusted. Validate JSON/schema and sanitize before UI rendering.
- Make retry behavior explicit; deterministic processors should produce same logical output for same input/version/config.
- Store processor, model, prompt/config and library versions needed for reproducibility.
- Keep model loading outside per-record loop; use bounded batching and worker pools.

## Results
Return artifact references, structured metadata, warnings, confidence where meaningful, source offsets/page/region references, quality metrics and structured failure details. Confidence values are not interchangeable across models or calibrated probabilities unless validated.

## Evaluation
Create representative golden datasets and benchmark quality, throughput, latency, peak memory, cost and failure rate. Include Vietnamese/English and edge cases when relevant to the supported language scope.

## Acceptance
Manifest validation, input limit, timeout, malformed output, retry/idempotency, source immutability, provenance, resource isolation and golden-set quality tests.
