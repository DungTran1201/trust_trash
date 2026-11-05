# Trust Trash Agent System

This folder contains project-specific agent guidance for the Trust Trash Unified Data Intelligence Platform.

## Contents
- `AGENT-INDEX.md`: task-to-agent and task-to-skill routing.
- `agents/`: role profiles for specialist agents and delegation boundaries.
- `skills/`: reusable workflows following the open Agent Skills `SKILL.md` pattern.
- `workflows/`: end-to-end playbooks from business discovery through implementation and release.
- `references/`: project-specific architecture, process, data and UX knowledge.
- `templates/`: reusable product, architecture, connector, processor, pipeline and web-page templates.
- `scripts/`: deterministic validation helpers for this pack.

## How to use
1. Keep repository `AGENTS.md` short; it is the always-relevant index and guardrail set.
2. Let nested `AGENTS.md` files add path-specific rules.
3. Load only skill(s) relevant to the task. Do not paste the entire catalog into every prompt.
4. Use an agent role profile when delegating a bounded workstream; use a workflow when a task has a repeatable sequence.
5. Treat `docs/` and source code as the source of truth. If instructions disagree with actual implementation, inspect, report the discrepancy and update docs only after validating the decision.

## Compatibility notes
- `AGENTS.md` follows the repository-instruction discovery pattern used by Codex and other coding agents that support nested agent instructions.
- Skills use the open `SKILL.md` folder convention: YAML frontmatter with `name` and `description`, followed by task instructions. Codex documents project skills in `.agents/skills`.
- `.agents/agents/*.agent.md` are portable role briefs, not a universal runtime registration format. A particular IDE may require copying/adapting these profiles into its own agent configuration location.
- `.agents/workflows/*.md` are reusable playbooks. They are not automatically executable slash commands unless the chosen IDE maps them.

## Safety and provenance
These files are original Trust Trash guidance informed by public documentation and repositories listed in `references/research-sources.md`. They do not vendor or reproduce third-party skill packs. Verify external APIs and provider capabilities against current vendor documentation before coding.


## Pack inventory
- 29 reusable skills: 8 shared engineering skills, 12 Data Platform skills and 9 Website Builder skills.
- 16 specialist role profiles for product, architecture, backend, connector, data, search, AI processing, governance, SRE, frontend, QA, security and technical writing.
- 10 end-to-end workflows covering discovery, architecture, backend modules, connectors, search, pipelines, processors, web features, release and incident recovery.
- 10 architecture/product references, 9 reusable templates and path-scoped `AGENTS.md` instructions.

See `PACK-MANIFEST.md` for the file groups and integration steps.
