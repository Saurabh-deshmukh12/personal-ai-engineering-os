"""`ai-os agents ...` -- discovery over agents/*.md. The agent execution
engine (actually running an agent) is Milestone 5; `list`/`info` here only
report what is *defined*, honestly, via CapabilityStatus.UNAVAILABLE when no
runtime exists yet.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from ai_os.cli.status import command_status, not_implemented
from ai_os.core.paths import AGENTS_DIR
from ai_os.core.registry import CapabilityStatus, discover_agents

console = Console()
app = typer.Typer(help="Inspect defined agents (orchestrator, engineering, memory/evolution).")

MILESTONE = 5


@app.command(name="list")
@command_status(CapabilityStatus.AVAILABLE)
def list_() -> None:
    """List every discovered agent definition under agents/."""
    agents = discover_agents(AGENTS_DIR)
    table = Table()
    table.add_column("Name", style="bold")
    table.add_column("Status")
    table.add_column("Description", overflow="fold")
    if not agents:
        table.add_row("(none registered yet)", "-", f"Agent definitions land in Milestone {MILESTONE}.")
    for cap in agents:
        table.add_row(cap.name, cap.status.value, cap.description)
    console.print(table)


@app.command()
@command_status(CapabilityStatus.AVAILABLE)
def info(name: str = typer.Argument(..., help="Agent name")) -> None:
    """Show full details for one agent definition."""
    agents = {cap.name: cap for cap in discover_agents(AGENTS_DIR)}
    cap = agents.get(name)
    if cap is None:
        console.print(f"[red]Unknown agent:[/red] {name}")
        raise typer.Exit(code=1)
    console.print(f"[bold]{cap.name}[/bold]  v{cap.version}  [{cap.status.value}]")
    console.print(cap.description)
    console.print(f"Source: {cap.source_path}")
    if cap.permissions:
        console.print(f"Permissions: {', '.join(cap.permissions)}")
    if cap.errors:
        console.print("[red]Validation errors:[/red]")
        for err in cap.errors:
            console.print(f"  - {err}")


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def test(name: str) -> None:
    """Dry-run an agent's defined workflow against fixtures."""
    not_implemented("ai-os agents test", MILESTONE)
