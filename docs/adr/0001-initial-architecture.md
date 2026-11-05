# ADR-0001: Initial Application Architecture

- Status: Accepted as project direction
- Date: 2026-11-05

## Context

Trust Trash combines universal data discovery, connectors, ingestion, data processing, storage, analytics, governance and observability. Workloads differ substantially, but domain boundaries and contracts are still being discovered.

## Decision

Start with a layered modular monolith. Run API and resource-heavy/asynchronous workers as separate processes from the same codebase. Keep module boundaries and public contracts explicit. Extract selected bounded contexts into microservices only when measured operational needs justify it.

## Consequences

Positive:
- Lower operational complexity during foundation work.
- Easier local debugging and end-to-end testing.
- Clear domain boundaries support future extraction.
- Workers can scale independently without full microservices overhead.

Trade-offs:
- Requires discipline to prevent cross-module coupling.
- A shared deployment/release may remain necessary for the API application.
- Future extraction requires stable contracts, ownership and event semantics.
