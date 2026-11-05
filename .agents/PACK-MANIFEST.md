# Agent Pack Manifest

Version: 1.0.0  
Research checked: 2026-11-05

## Inventory

| Group | Count | Purpose |
|---|---:|---|
| `AGENTS.md` | 38 | Root and path-specific repository instructions |
| Skills | 29 | Reusable Data Platform, Website Builder and shared engineering procedures |
| Specialist roles | 16 | Role briefs for delegating bounded work |
| Workflows | 10 | Business and engineering playbooks |
| References | 10 | Product capability, domain, connector, search, quality, UX and source references |
| Templates | 9 | Feature, ADR, connector, processor, query, pipeline, page, test and incident templates |

## Integration into an existing repository

1. Unzip `trust-trash-agent-pack-overlay.zip` at the repository root; preserve the folder paths.
2. Review the root `AGENTS.md` and merge it with any repository-specific instructions rather than blindly replacing custom project rules.
3. Keep nested `AGENTS.md` files only where the corresponding path exists; adjust if your repository layout differs.
4. Start at `.agents/README.md`, then use `.agents/AGENT-INDEX.md` to choose one role, one domain skill and one cross-cutting skill as needed.
5. Run `python .agents/scripts/validate_agent_pack.py`.
6. Adapt `.agents/agents/*.agent.md` and `.agents/workflows/*.md` to IDE-native registration only if your agent runtime requires it. Their portable source remains in `.agents/`.

## Source-of-truth rules

- `AGENTS.md`: concise scope and non-negotiable guardrails.
- `SKILL.md`: procedural knowledge loaded only for relevant tasks.
- `agents/*.agent.md`: role boundaries, responsibilities and handoff expectations.
- `workflows/*.md`: sequence and completion reports.
- `references/`: stable project/product knowledge.
- `templates/`: artifacts that agents should produce.
- `docs/` and code remain authoritative for actual implementation status.

## Validation

The included validator checks skill metadata and layout, specialist role profiles, workflow structure and required nested instructions. It does not prove that every recommendation is implemented or that every provider API is currently available.
