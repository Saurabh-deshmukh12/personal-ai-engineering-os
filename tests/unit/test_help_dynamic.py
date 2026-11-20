"""Proves /help is generated dynamically from the filesystem, not hardcoded:
adding a fixture skill/agent/hook to an empty temp directory must change the
registry output with zero code changes."""

from __future__ import annotations

from ai_os.cli.app import build_app
from ai_os.core.registry import build_registry

VALID_SKILL = """---
name: fixture-skill
description: A fixture skill for testing discovery.
version: 0.1.0
status: available
---

## When to use it
For tests.

## Required inputs
None.

## Workflow
Do the thing.

## Expected outputs
A result.

## Validation criteria
It works.

## Safety constraints
None.
"""


def _empty_registry(tmp_path):
    app = build_app()
    return build_registry(
        app,
        agents_dir=tmp_path / "agents",
        skills_dir=tmp_path / "skills",
        hooks_dir=tmp_path / "hooks",
        integrations_registry_file=tmp_path / "integrations.yaml",
    )


def test_registry_is_empty_with_no_fixtures(tmp_path):
    registry = _empty_registry(tmp_path)
    assert registry.skills == []
    assert registry.agents == []
    assert registry.hooks == []
    assert registry.integrations == []
    # The CLI command tree is always populated -- it does not depend on the filesystem.
    assert len(registry.cli_commands) > 0


def test_adding_a_skill_file_changes_discovery_with_no_code_change(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "fixture-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(VALID_SKILL, encoding="utf-8")

    app = build_app()
    registry = build_registry(
        app,
        agents_dir=tmp_path / "agents",
        skills_dir=skills_dir,
        hooks_dir=tmp_path / "hooks",
        integrations_registry_file=tmp_path / "integrations.yaml",
    )
    names = {cap.name for cap in registry.skills}
    assert "fixture-skill" in names


def test_removing_the_skill_file_makes_it_disappear_again(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "fixture-skill"
    skill_dir.mkdir(parents=True)
    manifest = skill_dir / "SKILL.md"
    manifest.write_text(VALID_SKILL, encoding="utf-8")

    app = build_app()
    registry_with = build_registry(
        app, tmp_path / "agents", skills_dir, tmp_path / "hooks", tmp_path / "integrations.yaml"
    )
    assert len(registry_with.skills) == 1

    manifest.unlink()
    registry_without = build_registry(
        app, tmp_path / "agents", skills_dir, tmp_path / "hooks", tmp_path / "integrations.yaml"
    )
    assert registry_without.skills == []
