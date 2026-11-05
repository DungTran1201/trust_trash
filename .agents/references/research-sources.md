# Research Sources and Design Influence

Verified on 2026-11-05. This pack is original Trust Trash guidance; it does not copy third-party skill packs. Sources informed structure and topic coverage; always check current vendor docs before coding.

## Agent instruction and skill formats
- OpenAI Codex AGENTS.md guidance: https://developers.openai.com/codex/guides/agents-md/ — nested instructions, scope and concise repository guidance.
- OpenAI Harness Engineering: https://openai.com/index/harness-engineering/ — repository documentation as system of record, concise AGENTS.md as map/guardrails, mechanically verifiable conventions.
- OpenAI Skills: https://developers.openai.com/codex/skills/ — reusable skill directories and SKILL.md conventions.
- Agent Skills open specification: https://agentskills.io/specification — portable skill metadata and progressive disclosure.
- Anthropic skills repository: https://github.com/anthropics/skills — self-contained skills with SKILL.md, references, scripts and assets.
- GitHub awesome-copilot: https://github.com/github/awesome-copilot — reusable agents, instructions, prompts and skill examples.
- Awesome Agent Skills: https://github.com/VoltAgent/awesome-agent-skills — curated catalog for discovery, not an authority on every listed skill.

## Data platform engineering
- Dagster project structure: https://docs.dagster.io/guides/build/projects/project-structure — organizing assets, resources, jobs and tests by domain.
- dbt project structure: https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview — staging/intermediate/marts and modular transformations.
- Airbyte connector development: https://docs.airbyte.com/platform/connector-development/ — connector Builder/CDK and lifecycle.
- OpenLineage specification: https://openlineage.io/docs/spec/ — Job, Run, Dataset and lifecycle events.
- Trino connector development: https://trino.io/docs/current/develop/connectors.html — connector SPI and query federation boundaries.
- OpenSearch hybrid search: https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/ — lexical/vector fusion and ranking.
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/ — web application security verification baseline.

## Website engineering
- Next.js project structure: https://nextjs.org/docs/app/getting-started/project-structure — App Router routing and project conventions.
- Next.js testing: https://nextjs.org/docs/app/guides/testing — unit, component, integration and E2E strategy.
- Vercel agent-skills: https://github.com/vercel-labs/agent-skills — React/Next.js performance and web design guideline skills.
- React Frontend Skills: https://github.com/PyModel/react-frontend-skills — frontend skills, accessibility, performance and testing examples.

## How sources were used
- AGENTS.md remains short and path-scoped; detailed procedures live in skills/references.
- Skills use progressive disclosure and portable Markdown instructions.
- Data skills cover connector capabilities, checkpoints, immutability, data contracts, lineage, ACL, query coverage and operational recovery.
- Website skills cover App Router boundaries, typed data flow, state completeness, accessibility, performance and browser-extension security.
- Trust Trash-specific rules (source provenance, coverage semantics, ACL re-check, raw immutability and modular architecture) are derived from its product design, not copied from external repos.
