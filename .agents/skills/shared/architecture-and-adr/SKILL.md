---
name: architecture-and-adr
description: "Design changes within the Layered Modular Monolith, define domain boundaries and contracts, and record important technical decisions as ADRs."
metadata:
  author: Trust Trash
  version: "1.0.0"
  domain: trust-trash
---

# Architecture and ADR Workflow

## Use when
A change affects module boundaries, storage, query execution, external integrations, deployment, security, data contracts or technology choices.

## Procedure
1. Read root/nearest `AGENTS.md`, architecture docs and implementation status.
2. Trace the current request/data path before proposing a new component.
3. Identify the owning bounded context and public interface.
4. Apply dependency rule: Presentation → Application → Domain; Infrastructure implements ports and depends inward. Domain imports no framework/provider implementation.
5. Decide whether behavior belongs in an existing module, plugin, worker or separate deployable. Do not create a service because a folder exists.
6. Define contracts: command/query, DTO, error taxonomy, event schema, idempotency, versioning and ownership.
7. Draw sequence/data-flow and deployment implications, including auth, failure, retry, consistency and observability paths.
8. Compare at least one alternative. Record cost, operational burden, lock-in and migration path.
9. Write ADR with `.agents/templates/adr.md`; mark proposed/accepted/deprecated/superseded.
10. Add architecture fitness checks where a boundary can be enforced mechanically.

## Required questions
Who owns the invariant/data? Sync or async? What if downstream is unavailable? Consistency model? Contract versioning? How does caller know coverage/freshness/provenance? Can this work without another service/database?

## Quality gate
Never introduce direct cross-module table dependency, secret leak, unbounded fan-out or unobservable background workflow. Update module map and ADR when a public boundary changes.
