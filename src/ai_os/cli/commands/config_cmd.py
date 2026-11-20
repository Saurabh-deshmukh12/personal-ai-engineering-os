"""`ai-os config ...` -- show/validate the resolved global configuration."""

from __future__ import annotations

import typer
from rich.console import Console

from ai_os.cli.status import command_status
from ai_os.core.config import load_config
from ai_os.core.registry import CapabilityStatus

console = Console()
app = typer.Typer(help="Show and validate the resolved AI-OS configuration.")


@app.command(name="show")
@command_status(CapabilityStatus.AVAILABLE)
def show() -> None:
    """Print the resolved configuration (file + env overrides merged)."""
    result = load_config()
    console.print(f"Source file: {result.source_file or '(none, using defaults)'}")
    console.print(f"Env overrides applied: {', '.join(result.env_overrides) or '(none)'}")
    console.print(result.config.model_dump_json(indent=2))
    if result.errors:
        console.print("[red]Errors:[/red]")
        for err in result.errors:
            console.print(f"  - {err}")


@app.command(name="validate")
@command_status(CapabilityStatus.AVAILABLE)
def validate() -> None:
    """Validate the configuration file against the schema. Exits non-zero on failure."""
    result = load_config()
    if result.errors:
        console.print("[red]Invalid configuration:[/red]")
        for err in result.errors:
            console.print(f"  - {err}")
        raise typer.Exit(code=1)
    console.print("[green]Configuration is valid.[/green]")
