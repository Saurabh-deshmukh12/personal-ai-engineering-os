"""`ai-os integrations ...` -- the integration registry (Graphiti, Claude-Mem,
Headroom, OmniRoute, Ponytail, Archify). `list`/`status` genuinely read
config/integrations.yaml; actually enabling/testing an adapter is Milestone 7.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from ai_os.cli.status import command_status, not_implemented
from ai_os.core.paths import INTEGRATIONS_REGISTRY_FILE
from ai_os.core.registry import CapabilityStatus, discover_integrations

console = Console()
app = typer.Typer(help="Manage optional third-party integrations.")

MILESTONE = 7


@app.command(name="list")
@command_status(CapabilityStatus.AVAILABLE)
def list_() -> None:
    """List every known integration and its current status."""
    integrations = discover_integrations(INTEGRATIONS_REGISTRY_FILE)
    table = Table()
    table.add_column("Name", style="bold")
    table.add_column("Status")
    table.add_column("Description", overflow="fold")
    for cap in integrations:
        table.add_row(cap.name, cap.status.value, cap.description)
    console.print(table)


@app.command()
@command_status(CapabilityStatus.AVAILABLE)
def status(name: str = typer.Argument(..., help="Integration name, e.g. graphiti")) -> None:
    """Show detailed status for one integration."""
    integrations = {cap.name: cap for cap in discover_integrations(INTEGRATIONS_REGISTRY_FILE)}
    cap = integrations.get(name)
    if cap is None:
        console.print(f"[red]Unknown integration:[/red] {name}")
        raise typer.Exit(code=1)
    console.print(f"[bold]{cap.name}[/bold]  v{cap.version}  [{cap.status.value}]")
    console.print(cap.description)
    if cap.permissions:
        console.print(f"Permissions: {', '.join(cap.permissions)}")
    if cap.planned_milestone:
        console.print(f"Planned for Milestone {cap.planned_milestone}.")


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def enable(name: str) -> None:
    """Enable an integration adapter."""
    not_implemented("ai-os integrations enable", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def disable(name: str) -> None:
    """Disable an integration adapter."""
    not_implemented("ai-os integrations disable", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def test(name: str) -> None:
    """Run the integration's health check."""
    not_implemented("ai-os integrations test", MILESTONE)
