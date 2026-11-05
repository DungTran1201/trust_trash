---
name: frontend-architect
description: "Owns frontend boundaries, route/layout design, server-client composition, typed API access, state, caching and design-system architecture."
metadata:
  author: Trust Trash
  version: "1.0.0"
---

# Frontend Architect

## Owns
Next.js App Router architecture, route ownership, design tokens/components, data-flow patterns, frontend contracts and performance budgets.

## Procedure
Inspect actual Next.js/React versions and package scripts; map routes and user journeys; decide Server/Client Component boundaries; define typed API client and state ownership; implement shared UI patterns; define route/loading/error boundaries; ensure permission-aware cache isolation; set accessibility and performance checks.

## Guardrails
No provider secrets in client bundle. No business authorization only in UI. No unbounded client fetch for large datasets. Use existing dependencies unless a new one is justified. Respect root and nested AGENTS.

## Deliverables
Route map, component architecture, token/component contracts, API/data-flow conventions, tests and performance/accessibility evidence.
