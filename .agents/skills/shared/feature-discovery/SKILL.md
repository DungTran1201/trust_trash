---
name: feature-discovery
description: "Turn an idea or request into a validated Trust Trash feature brief, business workflow, scope, non-functional requirements and testable acceptance criteria."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Feature Discovery

## Use when
A request introduces a capability, changes a user workflow, spans domains, or is too ambiguous to implement safely.

## Procedure
1. Restate the outcome, not the requested implementation. Identify user/actor, job-to-be-done, trigger, expected outcome and current workaround.
2. Map actors and boundaries: workspace/tenant, admin/operator/analyst/developer, external source owner and downstream consumer.
3. Describe as-is and to-be workflows. Identify alternate paths, manual steps, external systems, failure paths and human approvals.
4. Define in-scope, out-of-scope, assumptions, constraints and later phases. Do not silently expand scope.
5. Identify domain ownership: identity, connections, connector registry, resources, discovery, ingestion, processing, storage, analytics, governance or observability.
6. Capture input/output data, classification, source of truth, persistence, freshness, provenance, retention, deletion and reprocessing.
7. Capture NFRs: security, authorization, latency, availability, scale, cost, accessibility, operability and auditability.
8. Write observable acceptance criteria. Include success, empty, partial, denied, timeout and retry states.
9. Validate provider/API capability, licensing, rate limits and compatibility before assuming feasibility.
10. Produce `.agents/templates/feature-brief.md` and link relevant ADRs/specs.

## Trust Trash questions
- Is this discovery, live retrieval, indexing, replication, processing, analytics or administration?
- Does it read at source, copy data, or both?
- What connector capability is required and is it actually available?
- What does the user see when a source fails or its permissions are stale?
- Does a result expose a snippet/field requiring a second authorization check?
- Can it be delivered as a vertical slice without a new microservice?

## Output and quality gate
Feature brief, actors/use cases, workflow, acceptance criteria, NFRs, domain ownership, dependencies, risks and open decisions. Do not begin broad implementation while actor, data boundary, permission behavior or observable acceptance criteria are unknown. For low-risk work, document a concise assumption and proceed.
