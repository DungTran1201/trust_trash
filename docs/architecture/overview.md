# Architecture Overview

## Decision

Use a **Layered Modular Monolith with Independent Workers** as the initial implementation architecture, with selective extraction to microservices when justified by measured scaling, deployment, or isolation needs.

## Layers inside a domain module

1. **Presentation:** HTTP/API and transport schemas. Keep handlers thin.
2. **Application:** use cases, transactions, orchestration and application DTOs.
3. **Domain:** entities, value objects, invariants and ports. No framework/vendor imports.
4. **Infrastructure:** database repositories, cloud SDKs, search clients and external adapters.

Dependency direction points inward. Infrastructure implements ports defined by inner layers. Domain modules communicate through public interfaces or versioned events, not by importing another module's private implementation.

## Runtime model

The backend API, ingestion worker, processing worker and indexing worker may run as separate processes/containers from the same codebase. This gives independent resource limits and deployment entry points without prematurely introducing distributed service boundaries.

## Three planes

- **Control Plane:** identity, workspace, connection configuration, connector registry, credentials references, policies and metadata.
- **Data Plane:** connectors, ingestion, storage, processing, indexing and analytics workloads.
- **Query & Intelligence Plane:** query understanding, planning, routing, federated execution, retrieval, aggregation and ranking.

Security, governance and observability are cross-cutting capabilities.
