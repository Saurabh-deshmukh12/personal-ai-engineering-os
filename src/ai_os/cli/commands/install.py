"""Install / uninstall the plugin into a coding host. Planned for Milestone 9."""

from __future__ import annotations

import typer

from ai_os.cli.status import command_status, not_implemented
from ai_os.core.registry import CapabilityStatus

app = typer.Typer(help="Install/uninstall the AI-OS plugin for a coding host.")

MILESTONE = 9


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def install() -> None:
    """Register the published plugin/skills for a supported host without cloning this repo."""
    not_implemented("ai-os install", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def uninstall() -> None:
    """Remove the registered plugin/skills for a supported host."""
    not_implemented("ai-os uninstall", MILESTONE)
