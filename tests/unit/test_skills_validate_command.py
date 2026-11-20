from __future__ import annotations

from typer.testing import CliRunner

from ai_os.cli.app import build_app

runner = CliRunner()

VALID_SKILL = """---
name: good-skill
description: valid
version: 0.1.0
status: available
---

## When to use it
x

## Required inputs
x

## Workflow
x

## Expected outputs
x

## Validation criteria
x

## Safety constraints
x
"""

INVALID_SKILL = """---
name: bad-skill
---

## When to use it
x
"""


def test_validate_passes_for_a_well_formed_skill(tmp_path):
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text(VALID_SKILL, encoding="utf-8")
    result = runner.invoke(build_app(), ["skills", "validate", str(skill_file)])
    assert result.exit_code == 0
    assert "OK" in result.output


def test_validate_fails_for_a_broken_skill(tmp_path):
    skill_file = tmp_path / "SKILL.md"
    skill_file.write_text(INVALID_SKILL, encoding="utf-8")
    result = runner.invoke(build_app(), ["skills", "validate", str(skill_file)])
    assert result.exit_code != 0
    assert "FAIL" in result.output


def test_help_commands_run_successfully():
    for topic in ["agents", "skills", "hooks", "integrations", "memory", "commands", "examples"]:
        result = runner.invoke(build_app(), ["help", topic])
        assert result.exit_code == 0, f"ai-os help {topic} failed: {result.output}"


def test_help_rejects_unknown_topic():
    result = runner.invoke(build_app(), ["help", "not-a-real-topic"])
    assert result.exit_code != 0
