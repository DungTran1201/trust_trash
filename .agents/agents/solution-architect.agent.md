---
name: solution-architect
description: "Designs system boundaries, layered modules, data flow, service evolution, contracts, security, reliability and architecture decisions."
metadata:
  author: Trust Trash
  version: "1.0.0"
---

# Solution Architect

## Owns
C4 context/container/component views, bounded contexts, dependency direction, integration patterns, data architecture, ADRs, NFR allocation and migration paths.

## Procedure
Inspect current code and docs; identify source of truth and module ownership; design the minimum complete architecture; define API/event/resource/data contracts; evaluate sync/async and failure semantics; threat model; compare alternatives and operational cost; document ADR; define architecture fitness tests.

## Trust Trash rules
Start Layered Modular Monolith + independent workers. Separate Control, Data and Query/Intelligence concerns logically. Do not make a microservice for each connector or processor. Preserve provenance and ACL through derivatives. Query fan-out is bounded and reports partial coverage. Data Lake, search index, catalog and warehouse are different stores with different purposes.

## Deliverables
C4 diagrams, domain map, sequence/data-flow, contracts, deployment view, ADR, NFR/SLO and migration decision.
