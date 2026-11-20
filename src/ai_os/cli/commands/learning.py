"""Continuous learning / evolution commands. Planned for Milestone 8 (engine)
and Milestone 9 (GitHub PR automation for global proposals). Human approval
is architecturally required before any global release -- see section 3/9 of
the spec and SECURITY.md. No command here may ever auto-merge.
"""

from __future__ import annotations

import typer

from ai_os.cli.status import command_status, not_implemented
from ai_os.core.registry import CapabilityStatus

flat_app = typer.Typer()
proposal_app = typer.Typer(help="Review a single global-improvement proposal.")

MILESTONE_ENGINE = 8
MILESTONE_RELEASE = 9


@flat_app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE_ENGINE)
def learn() -> None:
    """Run OBSERVE -> CLASSIFY -> SANITIZE on recent engineering activity in this project."""
    not_implemented("ai-os learn", MILESTONE_ENGINE)


@flat_app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE_ENGINE)
def evolve() -> None:
    """Generate a global-improvement proposal from accumulated classified observations."""
    not_implemented("ai-os evolve", MILESTONE_ENGINE)


@flat_app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE_ENGINE)
def proposals() -> None:
    """List open proposals under proposals/."""
    not_implemented("ai-os proposals", MILESTONE_ENGINE)


@flat_app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE_RELEASE)
def release() -> None:
    """Publish a versioned release after a human-approved proposal merges."""
    not_implemented("ai-os release", MILESTONE_RELEASE, "Never auto-merges; requires human approval first.")


@flat_app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE_RELEASE)
def update() -> None:
    """Update this project's installed plugin/skills to an approved release version."""
    not_implemented("ai-os update", MILESTONE_RELEASE)


@proposal_app.command()
@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=MILESTONE_ENGINE)
def review(proposal_id: str = typer.Argument(..., help="Proposal folder name under proposals/")) -> None:
    """Open one proposal's evidence/diff/test-results for human review."""
    not_implemented("ai-os proposal review", MILESTONE_ENGINE)
