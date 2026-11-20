"""Marks CLI command implementation status so the registry never has to guess.

Every command in ai_os.cli.commands.* is decorated with either
`@command_status(CapabilityStatus.AVAILABLE)` (the default, implicit if omitted)
or `@command_status(CapabilityStatus.UNAVAILABLE, planned_milestone=N)`.
Unimplemented commands must call `not_implemented(...)` from their body too, so
that running them never silently "succeeds" -- see section 10/19 of the spec.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

import typer
from rich.console import Console

from ai_os.core.registry import CapabilityStatus

F = TypeVar("F", bound=Callable)

console = Console(stderr=True)


def command_status(
    status: CapabilityStatus, planned_milestone: int | None = None
) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        func.__ai_os_status__ = status  # type: ignore[attr-defined]
        func.__ai_os_milestone__ = planned_milestone  # type: ignore[attr-defined]
        return func

    return decorator


def not_implemented(command_name: str, milestone: int, detail: str = "") -> None:
    """Call from the body of a stub command. Exits non-zero; never prints fake success."""
    console.print(
        f"[bold yellow]Not yet implemented:[/bold yellow] `{command_name}` is planned for "
        f"Milestone {milestone} and is not available in this build."
        + (f"\n{detail}" if detail else "")
    )
    raise typer.Exit(code=2)
