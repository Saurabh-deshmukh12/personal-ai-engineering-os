"""`ai-os skills ...` -- discovery and schema validation over skills/<name>/SKILL.md.

`validate` is a real, working validator (not a stub): it checks the required
frontmatter fields and the required section headings from the SKILL.md
standard described in the spec (description, when to use, required inputs,
workflow, expected outputs, validation criteria, safety constraints).
"""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ai_os.cli.status import command_status
from ai_os.core.manifest import ManifestParseError, parse_markdown_manifest
from ai_os.core.paths import SKILLS_DIR
from ai_os.core.registry import CapabilityStatus, discover_skills, validate_skill_manifest

console = Console()
app = typer.Typer(help="Inspect and validate portable Agent Skills (SKILL.md).")


@app.command(name="list")
@command_status(CapabilityStatus.AVAILABLE)
def list_() -> None:
    """List every discovered skill under skills/."""
    skills = discover_skills(SKILLS_DIR)
    table = Table()
    table.add_column("Name", style="bold")
    table.add_column("Status")
    table.add_column("Description", overflow="fold")
    if not skills:
        table.add_row("(none registered yet)", "-", "Skill content lands in Milestone 5.")
    for cap in skills:
        table.add_row(cap.name, cap.status.value, cap.description)
    console.print(table)


@app.command()
@command_status(CapabilityStatus.AVAILABLE)
def info(name: str = typer.Argument(..., help="Skill name")) -> None:
    """Show full details for one skill definition."""
    skills = {cap.name: cap for cap in discover_skills(SKILLS_DIR)}
    cap = skills.get(name)
    if cap is None:
        console.print(f"[red]Unknown skill:[/red] {name}")
        raise typer.Exit(code=1)
    console.print(f"[bold]{cap.name}[/bold]  v{cap.version}  [{cap.status.value}]")
    console.print(cap.description)
    console.print(f"Source: {cap.source_path}")
    if cap.errors:
        console.print("[red]Validation errors:[/red]")
        for err in cap.errors:
            console.print(f"  - {err}")


@app.command()
@command_status(CapabilityStatus.AVAILABLE)
def validate(
    path: str = typer.Argument(
        None, help="Path to a SKILL.md file. Omit to validate every skill under skills/."
    ),
) -> None:
    """Validate a SKILL.md against the required schema. Exits non-zero on any failure."""
    targets: list[Path] = []
    if path:
        targets = [Path(path)]
    else:
        if SKILLS_DIR.exists():
            targets = sorted(SKILLS_DIR.glob("*/SKILL.md"))
        if not targets:
            console.print("[yellow]No SKILL.md files found to validate.[/yellow]")
            return

    any_failed = False
    for target in targets:
        try:
            parsed = parse_markdown_manifest(target)
        except ManifestParseError as exc:
            console.print(f"[red]FAIL[/red]  {target}: {exc}")
            any_failed = True
            continue

        errors = validate_skill_manifest(parsed)
        if errors:
            console.print(f"[red]FAIL[/red]  {target}")
            for err in errors:
                console.print(f"       - {err}")
            any_failed = True
        else:
            console.print(f"[green]OK[/green]    {target}")

    if any_failed:
        raise typer.Exit(code=1)
