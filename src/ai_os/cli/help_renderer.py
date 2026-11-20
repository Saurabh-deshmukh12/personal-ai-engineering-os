"""Renders the unified, dynamically-generated /help output.

Nothing here is a hardcoded capability list -- everything comes from a
CapabilityRegistry built fresh from the live CLI tree + filesystem scan
(ai_os.core.registry.build_registry). Adding a new skill/agent/hook file
changes this output with zero code changes.
"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from ai_os import __version__
from ai_os.core.config import ConfigLoadResult
from ai_os.core.registry import Capability, CapabilityRegistry, CapabilityStatus

STATUS_STYLE = {
    CapabilityStatus.AVAILABLE: "green",
    CapabilityStatus.INSTALLED: "green",
    CapabilityStatus.DISABLED: "yellow",
    CapabilityStatus.REQUIRES_CONFIGURATION: "yellow",
    CapabilityStatus.UNAVAILABLE: "red",
    CapabilityStatus.INVALID: "bold red",
}

TOPIC_ALIASES = {
    "agents": "agents",
    "skills": "skills",
    "hooks": "hooks",
    "integrations": "integrations",
    "memory": "memory",
    "commands": "commands",
    "examples": "examples",
}


def _status_cell(cap: Capability) -> str:
    style = STATUS_STYLE.get(cap.status, "white")
    label = cap.status.value.replace("_", " ")
    if cap.planned_milestone and cap.status in (CapabilityStatus.UNAVAILABLE, CapabilityStatus.REQUIRES_CONFIGURATION):
        label += f" (M{cap.planned_milestone})"
    return f"[{style}]{label}[/{style}]"


def _table_for(title: str, caps: list[Capability]) -> Table:
    table = Table(title=title, show_lines=False, expand=True)
    table.add_column("Name", style="bold")
    table.add_column("Status")
    table.add_column("Description", overflow="fold")
    if not caps:
        table.add_row("(none registered)", "-", "-")
        return table
    for cap in sorted(caps, key=lambda c: c.name):
        table.add_row(cap.name, _status_cell(cap), cap.description or "-")
    return table


def render_overview(
    console: Console,
    registry: CapabilityRegistry,
    config_result: ConfigLoadResult,
    project_scope: str,
) -> None:
    console.print(f"[bold]PERSONAL AI ENGINEERING OS[/bold]  v{__version__}")
    console.print(f"Config source: {config_result.source_file or '(defaults, no config file found)'}")
    console.print(f"Current project / client scope: {project_scope}")
    console.print()
    console.print(
        "Milestone 1 build: CLI + dynamic help + capability registry only. "
        "Project discovery, memory, integrations, agents/skills/hooks content, "
        "and the learning engine are scaffolded but not yet implemented -- "
        "see `ai-os help commands` for exact status per command."
    )
    console.print()
    console.print(_table_for("CLI commands", registry.cli_commands))
    console.print(_table_for("Agents", registry.agents))
    console.print(_table_for("Skills", registry.skills))
    console.print(_table_for("Hooks", registry.hooks))
    console.print(_table_for("Integrations", registry.integrations))
    console.print()
    console.print("Run [bold]ai-os help <topic>[/bold] for a focused view.")
    console.print("Topics: " + ", ".join(sorted(TOPIC_ALIASES)))
    console.print()
    console.print(
        "In an AI coding host (Claude Code, Codex, etc.) a bare `/help` only works if this "
        "project has registered a host-specific slash command or skill entry point for it -- "
        "it is not automatically available in every host. Use `ai-os help` from a terminal "
        "as the one guaranteed entry point."
    )


def render_topic(
    console: Console,
    registry: CapabilityRegistry,
    topic: str,
) -> bool:
    topic = topic.lower()
    if topic == "commands":
        console.print(_table_for("CLI commands", registry.cli_commands))
    elif topic == "agents":
        console.print(_table_for("Agents", registry.agents))
    elif topic == "skills":
        console.print(_table_for("Skills", registry.skills))
    elif topic == "hooks":
        console.print(_table_for("Hooks", registry.hooks))
    elif topic == "integrations":
        console.print(_table_for("Integrations", registry.integrations))
    elif topic == "memory":
        mem_caps = [c for c in registry.cli_commands if c.name.startswith("ai-os memory")]
        console.print(_table_for("Memory operations", mem_caps))
        console.print(
            "[yellow]The memory gateway itself is planned for Milestone 3 "
            "(scope enforcement) and Milestone 4 (Graphiti backend).[/yellow]"
        )
    elif topic == "examples":
        console.print("[bold]Examples[/bold]")
        console.print("  ai-os status")
        console.print("  ai-os help agents")
        console.print("  ai-os config show")
        console.print("  ai-os skills validate <path-to-SKILL.md>")
    else:
        return False
    return True
