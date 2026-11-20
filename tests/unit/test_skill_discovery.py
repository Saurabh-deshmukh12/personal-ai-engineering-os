from __future__ import annotations

from ai_os.core.registry import CapabilityStatus, discover_skills

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

MISSING_SECTIONS_SKILL = """---
name: bad-skill
description: missing sections
---

## When to use it
x
"""

NO_FRONTMATTER_SKILL = "# Not a manifest\n\nJust prose."


def _write_skill(tmp_path, name, content):
    skill_dir = tmp_path / "skills" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
    return tmp_path / "skills"


def test_valid_skill_discovered_as_available(tmp_path):
    skills_dir = _write_skill(tmp_path, "good-skill", VALID_SKILL)
    caps = discover_skills(skills_dir)
    assert len(caps) == 1
    assert caps[0].name == "good-skill"
    assert caps[0].status == CapabilityStatus.AVAILABLE
    assert caps[0].errors == []


def test_skill_missing_required_sections_is_invalid(tmp_path):
    skills_dir = _write_skill(tmp_path, "bad-skill", MISSING_SECTIONS_SKILL)
    caps = discover_skills(skills_dir)
    assert len(caps) == 1
    assert caps[0].status == CapabilityStatus.INVALID
    assert any("Required inputs" in e for e in caps[0].errors)


def test_skill_with_no_frontmatter_is_invalid(tmp_path):
    skills_dir = _write_skill(tmp_path, "no-frontmatter", NO_FRONTMATTER_SKILL)
    caps = discover_skills(skills_dir)
    assert len(caps) == 1
    assert caps[0].status == CapabilityStatus.INVALID


def test_missing_skills_dir_returns_empty(tmp_path):
    assert discover_skills(tmp_path / "does-not-exist") == []


def test_never_hardcodes_a_fake_skill_as_available(tmp_path):
    """Not create empty placeholder skills and claim they are implemented (spec section 6)."""
    assert discover_skills(tmp_path / "skills") == []
