"""Core commands: version, status, health, help / "/help"."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ai_os import __version__
from ai_os.cli.help_renderer import render_overview, render_topic
from ai_os.cli.status import command_status
from ai_os.core.config import load_config
from ai_os.core.paths import (
    AGENTS_DIR,
    HOOKS_DIR,
    INTEGRATIONS_REGISTRY_FILE,
    SKILLS_DIR,
    project_manifest_file,
    user_config_dir,
    user_data_dir,
)
from ai_os.core.registry import CapabilityStatus, build_registry

console = Console()
app = typer.Typer(help="Core system commands.")


def _project_scope(cwd: Path) -> str:
    manifest = project_manifest_file(cwd)
    if manifest.exists():
        return f"initialized project at {manifest} (see `ai-os project-info`)"
    return "no project scope (run `ai-os init` -- planned Milestone 2)"


@app.command()
@command_status(CapabilityStatus.AVAILABLE)
def version() -> None:
    """Print the installed ai-os version."""
    console.print(f"ai-os {__version__}")


@app.command()
@command_status(CapabilityStatus.AVAILABLE)
def status() -> None:
    """Show config resolution, directories, and registered-capability counts."""
    config_result = load_config()
    from ai_os.cli.app import build_app

    registry = build_registry(
        build_app(), AGENTS_DIR, SKILLS_DIR, HOOKS_DIR, INTEGRATIONS_REGISTRY_FILE
    )
    console.print(f"[bold]ai-os[/bold] {__version__}")
    console.print(f"User config dir: {user_config_dir()}")
    console.print(f"User data dir:   {user_data_dir()}")
    console.print(f"Config file:     {config_result.source_file or '(not found, using defaults)'}")
    if config_result.errors:
        console.print("[red]Config errors:[/red]")
        for err in config_result.errors:
            console.print(f"  - {err}")
    console.print(f"Project scope:   {_project_scope(Path.cwd())}")
    console.print()
    console.print(f"CLI commands registered: {len(registry.cli_commands)}")
    console.print(f"Agents registered:       {len(registry.agents)}")
    console.print(f"Skills registered:       {len(registry.skills)}")
    console.print(f"Hooks registered:        {len(registry.hooks)}")
    console.print(f"Integrations known:      {len(registry.integrations)}")


@app.command()
@command_status(CapabilityStatus.AVAILABLE)
def health() -> None:
    """Run basic self-checks and report OK/FAIL per check."""
    checks: list[tuple[str, bool, str]] = []

    config_result = load_config()
    checks.append(("config loads without error", not config_result.errors, str(config_result.errors)))

    for name, path in (("agents dir", AGENTS_DIR), ("skills dir", SKILLS_DIR), ("hooks dir", HOOKS_DIR)):
        checks.append((f"{name} exists", path.exists(), str(path)))

    checks.append(
        (
            "integrations registry file exists",
            INTEGRATIONS_REGISTRY_FILE.exists(),
            str(INTEGRATIONS_REGISTRY_FILE),
        )
    )

    all_ok = True
    for name, ok, detail in checks:
        mark = "[green]OK[/green]" if ok else "[red]FAIL[/red]"
        console.print(f"{mark}  {name}" + (f"  ({detail})" if not ok else ""))
        all_ok = all_ok and ok

    if not all_ok:
        raise typer.Exit(code=1)


def _help_impl(topic: str | None) -> None:
    config_result = load_config()
    from ai_os.cli.app import build_app

    registry = build_registry(
        build_app(), AGENTS_DIR, SKILLS_DIR, HOOKS_DIR, INTEGRATIONS_REGISTRY_FILE
    )
    scope = _project_scope(Path.cwd())

    if topic is None:
        render_overview(console, registry, config_result, scope)
        return

    if not render_topic(console, registry, topic):
        console.print(f"[red]Unknown help topic:[/red] {topic}")
        console.print("Try one of: agents, skills, hooks, integrations, memory, commands, examples")
        raise typer.Exit(code=1)


@app.command(name="help")
@command_status(CapabilityStatus.AVAILABLE)
def help_command(
    topic: str = typer.Argument(
        None, help="agents | skills | hooks | integrations | memory | commands | examples"
    ),
) -> None:
    """Dynamically generated capability help. Try: ai-os help agents"""
    _help_impl(topic)


@app.command(name="/help")
@command_status(CapabilityStatus.AVAILABLE)
def slash_help_command(
    topic: str = typer.Argument(
        None, help="agents | skills | hooks | integrations | memory | commands | examples"
    ),
) -> None:
    """Alias for `ai-os help`, matching the spec's `ai-os /help` invocation."""
    _help_impl(topic)
