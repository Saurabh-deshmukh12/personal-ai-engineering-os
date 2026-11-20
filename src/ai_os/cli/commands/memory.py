"""`ai-os memory ...` -- memory gateway commands.

Scope enforcement lands in Milestone 3; the Graphiti-backed temporal provider
in Milestone 4. Every subcommand here is a stub until then: a project memory
feature must never silently report fake success.
"""

from __future__ import annotations

import typer

from ai_os.cli.status import command_status, not_implemented
from ai_os.core.registry import CapabilityStatus

app = typer.Typer(help="Scoped memory gateway: store, search, validate, export, delete.")

MILESTONE = 3


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def status() -> None:
    """Show memory backend status (SQLite journal + optional Graphiti) for this project scope."""
    not_implemented("ai-os memory status", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def search(query: str = typer.Argument(..., help="Search query")) -> None:
    """Search project/org/client memory within the current scope."""
    not_implemented("ai-os memory search", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def capture() -> None:
    """Capture a new observation into scoped memory with provenance."""
    not_implemented("ai-os memory capture", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def validate() -> None:
    """Validate stale/conflicting/duplicate facts in the current scope."""
    not_implemented("ai-os memory validate", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def export() -> None:
    """Export project memory for backup or migration."""
    not_implemented("ai-os memory export", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def delete() -> None:
    """Delete project memory per the retention policy."""
    not_implemented("ai-os memory delete", MILESTONE)
