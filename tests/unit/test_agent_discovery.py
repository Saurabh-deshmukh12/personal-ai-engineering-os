from __future__ import annotations

from ai_os.core.registry import CapabilityStatus, discover_agents

VALID_AGENT = """---
name: good-agent
role: Does a thing
category: engineering
version: 0.1.0
status: unavailable
permissions:
  - memory:read
---

## Responsibilities
x

## Inputs
x

## Outputs
x

## Permissions
x
"""

MISSING_SECTIONS_AGENT = """---
name: bad-agent
role: incomplete
category: engineering
---

## Responsibilities
x
"""


def _write_agent(tmp_path, filename, content):
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir(parents=True)
    (agents_dir / filename).write_text(content, encoding="utf-8")
    return agents_dir


def test_valid_agent_discovered(tmp_path):
    agents_dir = _write_agent(tmp_path, "good-agent.md", VALID_AGENT)
    caps = discover_agents(agents_dir)
    assert len(caps) == 1
    assert caps[0].name == "good-agent"
    assert caps[0].status == CapabilityStatus.UNAVAILABLE
    assert caps[0].permissions == ["memory:read"]


def test_agent_missing_sections_is_invalid(tmp_path):
    agents_dir = _write_agent(tmp_path, "bad-agent.md", MISSING_SECTIONS_AGENT)
    caps = discover_agents(agents_dir)
    assert caps[0].status == CapabilityStatus.INVALID


def test_readme_in_agents_dir_is_ignored(tmp_path):
    agents_dir = _write_agent(tmp_path, "README.md", "# Agents\n\nSee the docs.")
    caps = discover_agents(agents_dir)
    assert caps == []


def test_missing_agents_dir_returns_empty(tmp_path):
    assert discover_agents(tmp_path / "does-not-exist") == []
