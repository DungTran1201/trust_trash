# Agent Runtime Compatibility

## Portable core
- Root and nested `AGENTS.md`: repository/path instructions for coding agents that support this convention.
- `.agents/skills/<skill-name>/SKILL.md`: reusable skills with YAML `name`/`description` frontmatter and task instructions.
- `.agents/agents/*.agent.md`: portable specialist role briefs. They are not automatically registered by every IDE/runtime.
- `.agents/workflows/*.md`: human/agent playbooks, not automatically executable slash commands unless a runtime maps them.

## Runtime setup
Before claiming a role or workflow is auto-discovered, verify the selected tool's documented discovery path. If necessary, adapt role profiles to the runtime's agent configuration (for example, an IDE-specific agent directory) without forking the source-of-truth profile.

## Instruction loading
Read root `AGENTS.md` and every nested file along the edited path. Keep each instruction file concise and scoped. Use skills only when relevant; do not load the whole catalog for every task. Avoid duplicated contradictory rules.

## Portability
Keep skill content tool-agnostic. Tool invocation syntax, MCP tool names and IDE-specific commands belong in a runtime adapter document, not the portable skill, unless the task is explicitly runtime-specific.
