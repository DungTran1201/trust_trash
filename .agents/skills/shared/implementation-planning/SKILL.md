---
name: implementation-planning
description: "Create a dependency-aware vertical-slice plan for backend, data platform and website changes with implementation and verification checkpoints."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Implementation Planning

## Procedure
1. Confirm business outcome and acceptance criteria.
2. Inspect source, tests, contracts, migrations and existing patterns.
3. List affected bounded contexts and file areas; note public contracts and generated files.
4. Split work into vertical slices that each produce testable behavior. Avoid layers-only plans.
5. Order tasks: contract/domain invariant → application use case → adapter/API/UI → integration → observability/docs.
6. Mark data migrations, backfills, permission changes and provider setup explicitly.
7. Define test matrix: unit, contract, adapter integration, API integration, browser E2E, load/security as risk requires.
8. Define rollback or safe-disable behavior for integrations, migrations and jobs.
9. Identify safe parallel tasks. Avoid concurrent edits to the same contract/files without ownership.
10. Track implementation status; do not claim a placeholder is complete.

## Task format
Outcome; scope/non-goals; affected modules/files; contracts/schema; steps; test plan; security/data implications; observability/docs; rollback; definition of done.

## Quality gate
A plan must be understandable without chat history. For a simple isolated change, use a short checklist instead of ceremony.
