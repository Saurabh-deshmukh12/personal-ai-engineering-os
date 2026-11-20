"""`ai-os hooks ...` -- discovery over hooks/*.yaml. Running a hook against a
real host event is Milestone 6 (MCP + lifecycle hooks); `list`/`status` here
only report what is defined.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from ai_os.cli.status import command_status, not_implemented
from ai_os.core.paths import HOOKS_DIR
from ai_os.core.registry import CapabilityStatus, discover_hooks

console = Console()
app = typer.Typer(help="Inspect defined lifecycle hooks.")

MILESTONE = 6


@app.command(name="list")
@command_status(CapabilityStatus.AVAILABLE)
def list_() -> None:
    """List every discovered hook definition under hooks/."""
    hooks = discover_hooks(HOOKS_DIR)
    table = Table()
    table.add_column("Name", style="bold")
    table.add_column("Status")
    table.add_column("Description", overflow="fold")
    if not hooks:
        table.add_row("(none registered yet)", "-", f"Hook definitions land in Milestone {MILESTONE}.")
    for cap in hooks:
        table.add_row(cap.name, cap.status.value, cap.description)
    console.print(table)


@app.command()
@command_status(CapabilityStatus.AVAILABLE)
def status(name: str = typer.Argument(..., help="Hook name")) -> None:
    """Show full details for one hook definition."""
    hooks = {cap.name: cap for cap in discover_hooks(HOOKS_DIR)}
    cap = hooks.get(name)
    if cap is None:
        console.print(f"[red]Unknown hook:[/red] {name}")
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
    """Dry-run a hook against a simulated trigger event."""
    not_implemented("ai-os hooks test", MILESTONE)
