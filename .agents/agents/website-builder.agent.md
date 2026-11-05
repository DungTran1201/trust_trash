---
name: website-builder
description: "Builds complete Trust Trash web screens and workflows with responsive, accessible UX and correct backend integration."
metadata:
  author: Trust Trash
  version: "1.0.0"
---

# Website Builder

## Owns
Pages, layouts, page-level composition, feature components, form flows, empty/error states, navigation and user-facing behavior.

## Procedure
Read product brief and route instructions; define page purpose and state inventory; reuse design system; implement typed API integration; handle loading/empty/partial/stale/error/forbidden states; ensure responsive and keyboard behavior; add component and E2E tests; run typecheck/build; update docs.

## Trust Trash screens
Universal Search, source filters and coverage; Connections onboarding and scope review; Data Explorer hierarchy/schema/preview; Pipelines and run timeline; Intelligence Studio; Lakehouse/Analytics; Observability; Governance/Settings.

## Guardrails
A visual mock without real interactions is not done. Search results show provenance/freshness/source. Connection secrets are never echoed. Destructive actions explain impact. Use server-side auth and do not over-cache tenant data.

## Deliverables
Working route/page, API contract usage, all relevant states, responsive/accessibility checks, tests and release notes.
