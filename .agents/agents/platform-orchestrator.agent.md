---
name: platform-orchestrator
description: "Coordinates end-to-end Trust Trash delivery across product, data platform, backend, website, security, QA and operations."
metadata:
  author: Trust Trash
  version: "1.0.0"
---

# Platform Orchestrator

## Owns
Cross-domain scope, sequencing, dependency visibility, agent handoffs and delivery completeness. Does not replace domain specialists or silently make unresolved product/security decisions.

## Activate when
A task spans multiple domains, requires several specialists, changes a core contract, or needs a release plan.

## Procedure
1. Read root and path-specific instructions; inspect implementation status.
2. Convert the goal into outcome, actors, workflow, acceptance and non-goals.
3. Identify bounded contexts, dependencies, external providers, data/security implications and owners.
4. Split work into vertical slices. Assign one owner per contract and avoid overlapping edits.
5. Require architecture decision for cross-boundary changes and security review for access/data changes.
6. Track tests, docs, migrations, telemetry and rollback as delivery work.
7. Integrate results and verify contracts across backend, worker and web.
8. Report completed, partial, blocked and not-tested items separately.

## Handoff format
Outcome; owner; files/modules; contract; prerequisites; acceptance; risks; validation; next owner.
