"""Project understanding commands. Planned for Milestone 2 (project discovery)."""

from __future__ import annotations

import typer

from ai_os.cli.status import command_status, not_implemented
from ai_os.core.registry import CapabilityStatus

app = typer.Typer(help="Project discovery, architecture and dependency analysis.")

MILESTONE = 2


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def init() -> None:
    """Initialize AI-OS for the current project (discovery, manifest, memory namespace)."""
    not_implemented("ai-os init", MILESTONE, "Will detect languages/frameworks and create .ai-os/project.yaml.")


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def analyze() -> None:
    """Analyze the current project's architecture, APIs, DB and deployment."""
    not_implemented("ai-os analyze", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def context() -> None:
    """Print the current project briefing / context summary."""
    not_implemented("ai-os context", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def refresh() -> None:
    """Re-scan the project for architecture/dependency changes since last discovery."""
    not_implemented("ai-os refresh", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def architecture() -> None:
    """Show the recorded architecture (current + historical)."""
    not_implemented("ai-os architecture", MILESTONE)


@app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def dependencies() -> None:
    """List detected dependencies for the current project."""
    not_implemented("ai-os dependencies", MILESTONE)


@app.command(name="project-info")
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE)
def project_info() -> None:
    """Show organization_id/client_id/project_id and manifest details for this project."""
    not_implemented("ai-os project-info", MILESTONE)
