"""Section 10/19: a command that isn't implemented yet must never report fake
success -- it must fail loudly with a clear message naming the milestone."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from ai_os.cli.app import build_app

runner = CliRunner()

STUB_INVOCATIONS = [
    ["init"],
    ["analyze"],
    ["context"],
    ["refresh"],
    ["architecture"],
    ["dependencies"],
    ["project-info"],
    ["install"],
    ["uninstall"],
    ["learn"],
    ["evolve"],
    ["proposals"],
    ["release"],
    ["update"],
    ["memory", "status"],
    ["memory", "capture"],
    ["memory", "validate"],
    ["memory", "export"],
    ["memory", "delete"],
    ["integrations", "enable", "graphiti"],
    ["integrations", "disable", "graphiti"],
    ["integrations", "test", "graphiti"],
    ["agents", "test", "x"],
    ["hooks", "test", "x"],
    ["proposal", "review", "x"],
]


@pytest.mark.parametrize("args", STUB_INVOCATIONS, ids=lambda a: " ".join(a))
def test_stub_command_fails_loudly(args):
    result = runner.invoke(build_app(), args)
    assert result.exit_code != 0, f"{' '.join(args)} must not report success"
    assert "not yet implemented" in result.output.lower()
    assert "milestone" in result.output.lower()


def test_memory_search_requires_an_argument_but_is_still_a_stub():
    result = runner.invoke(build_app(), ["memory", "search", "foo"])
    assert result.exit_code != 0
    assert "not yet implemented" in result.output.lower()
