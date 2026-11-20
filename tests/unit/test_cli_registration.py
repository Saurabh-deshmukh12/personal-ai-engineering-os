"""CLI command registration: every command the spec requires must actually
be registered on the root app (available or stubbed -- either is fine, but
it must exist)."""

from __future__ import annotations

from ai_os.cli.app import build_app
from ai_os.core.registry import discover_cli_commands

EXPECTED_TOP_LEVEL = {
    "ai-os version",
    "ai-os status",
    "ai-os health",
    "ai-os help",
    "ai-os /help",
    "ai-os init",
    "ai-os install",
    "ai-os uninstall",
    "ai-os analyze",
    "ai-os context",
    "ai-os refresh",
    "ai-os architecture",
    "ai-os dependencies",
    "ai-os project-info",
    "ai-os learn",
    "ai-os evolve",
    "ai-os proposals",
    "ai-os release",
    "ai-os update",
}

EXPECTED_GROUPED = {
    "ai-os memory status",
    "ai-os memory search",
    "ai-os memory capture",
    "ai-os memory validate",
    "ai-os memory export",
    "ai-os memory delete",
    "ai-os integrations list",
    "ai-os integrations status",
    "ai-os integrations enable",
    "ai-os integrations disable",
    "ai-os integrations test",
    "ai-os agents list",
    "ai-os agents info",
    "ai-os agents test",
    "ai-os skills list",
    "ai-os skills info",
    "ai-os skills validate",
    "ai-os hooks list",
    "ai-os hooks status",
    "ai-os hooks test",
    "ai-os proposal review",
    "ai-os config show",
    "ai-os config validate",
}


def test_all_spec_commands_are_registered():
    app = build_app()
    names = {cap.name for cap in discover_cli_commands(app)}
    missing = (EXPECTED_TOP_LEVEL | EXPECTED_GROUPED) - names
    assert not missing, f"Commands missing from CLI registration: {sorted(missing)}"


def test_no_duplicate_command_names():
    app = build_app()
    names = [cap.name for cap in discover_cli_commands(app)]
    assert len(names) == len(set(names)), "Duplicate command names registered"
