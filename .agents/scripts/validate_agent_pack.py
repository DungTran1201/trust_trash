#!/usr/bin/env python3
"""Validate Trust Trash AGENTS.md, portable Agent Skills, roles and workflows."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / ".agents"
ERRORS: list[str] = []
WARNINGS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def yaml_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        if line.startswith("  ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def check_exists(rel: str) -> None:
    if not (ROOT / rel).is_file():
        fail(f"Missing required file: {rel}")


def main() -> int:
    for rel in ["AGENTS.md", ".agents/README.md", ".agents/AGENT-INDEX.md",
                ".agents/WORKFLOW-MAP.md", ".agents/VERSION",
                ".agents/references/research-sources.md"]:
        check_exists(rel)

    skill_files = sorted((AGENTS / "skills").rglob("SKILL.md"))
    if len(skill_files) < 25:
        fail(f"Expected at least 25 skills; found {len(skill_files)}")
    skill_names: set[str] = set()
    for path in skill_files:
        rel = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8")
        fm = yaml_frontmatter(content)
        name = fm.get("name", "")
        description = fm.get("description", "")
        expected = path.parent.name
        if name != expected:
            fail(f"{rel}: frontmatter name '{name}' must match directory '{expected}'")
        if not description:
            fail(f"{rel}: missing frontmatter description")
        if name in skill_names:
            fail(f"Duplicate skill name: {name}")
        skill_names.add(name)
        if len(content.strip()) < 500:
            WARNINGS.append(f"{rel}: unusually short skill; verify it is actionable")
        if "## " not in content:
            fail(f"{rel}: no section headings found")

    role_files = sorted((AGENTS / "agents").glob("*.agent.md"))
    if len(role_files) < 12:
        fail(f"Expected at least 12 role profiles; found {len(role_files)}")
    for path in role_files:
        fm = yaml_frontmatter(path.read_text(encoding="utf-8"))
        if not fm.get("name") or not fm.get("description"):
            fail(f"{path.relative_to(ROOT)}: missing name/description frontmatter")

    workflow_files = sorted((AGENTS / "workflows").glob("*.md"))
    if len(workflow_files) < 8:
        fail(f"Expected at least 8 workflows; found {len(workflow_files)}")
    for path in workflow_files:
        body = path.read_text(encoding="utf-8")
        if "## Steps" not in body or "## Completion report" not in body:
            fail(f"{path.relative_to(ROOT)}: missing steps/completion section")

    required_nested = [
        "apps/web/AGENTS.md", "apps/browser-extension/AGENTS.md", "apps/local-agent/AGENTS.md",
        "backend/AGENTS.md", "backend/src/trust_trash/AGENTS.md",
        "backend/src/trust_trash/modules/discovery/AGENTS.md",
        "backend/src/trust_trash/modules/ingestion/AGENTS.md",
        "backend/src/trust_trash/modules/processing/AGENTS.md",
        "backend/src/trust_trash/modules/governance/AGENTS.md",
        "backend/src/trust_trash/connector_sdk/AGENTS.md",
        "backend/src/trust_trash/processor_sdk/AGENTS.md",
        "backend/src/trust_trash/bootstrap/AGENTS.md", "backend/src/trust_trash/shared/AGENTS.md",
        "apps/web/src/shared/AGENTS.md", "apps/web/src/shared/contracts/AGENTS.md",
        "apps/web/src/shared/domain/AGENTS.md", "apps/web/src/shared/infrastructure/AGENTS.md",
        "backend/tests/AGENTS.md", "contracts/AGENTS.md", "infra/AGENTS.md",
        "orchestration/AGENTS.md", "docs/AGENTS.md", "scripts/AGENTS.md",
    ]
    for rel in required_nested:
        check_exists(rel)

    reference_files = list((AGENTS / "references").glob("*.md"))
    template_files = list((AGENTS / "templates").glob("*"))
    if len(reference_files) < 10:
        fail(f"Expected at least 10 references; found {len(reference_files)}")
    if len(template_files) < 9:
        fail(f"Expected at least 9 templates; found {len(template_files)}")

    # Ensure every Markdown path in the index resolves within .agents.
    index_text = (AGENTS / "AGENT-INDEX.md").read_text(encoding="utf-8")
    for token in re.findall(r"`([^`]+\.md)`", index_text):
        if not (AGENTS / token).is_file():
            fail(f"AGENT-INDEX.md references missing path: {token}")

    # Check for malformed or empty AGENTS instructions.
    for path in ROOT.rglob("AGENTS.md"):
        if any(part in {".git", ".venv", "node_modules", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8").strip()
        if len(text) < 120:
            WARNINGS.append(f"{path.relative_to(ROOT)}: very short; check whether intentional")

    print(f"Skills: {len(skill_files)} | Roles: {len(role_files)} | Workflows: {len(workflow_files)}")
    print(f"Nested AGENTS.md: {sum(1 for _ in ROOT.rglob('AGENTS.md'))}")
    if WARNINGS:
        print("\nWarnings:")
        for item in WARNINGS:
            print(f"- {item}")
    if ERRORS:
        print("\nErrors:")
        for item in ERRORS:
            print(f"- {item}")
        return 1
    print("Agent pack validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
