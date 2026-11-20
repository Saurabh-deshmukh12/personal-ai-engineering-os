"""Root Typer application assembly.

Flat top-level commands (version, status, init, analyze, ...) are merged
directly onto the root app from their own module so each module stays small;
grouped commands (memory, integrations, agents, skills, hooks, proposal) are
mounted as real subgroups via add_typer, matching the `ai-os <group> <verb>`
shape from the spec.
"""

from __future__ import annotations

import typer

from ai_os.cli.commands import agents as agents_cmd
from ai_os.cli.commands import config_cmd, core, install, learning, project
from ai_os.cli.commands import hooks as hooks_cmd
from ai_os.cli.commands import integrations as integrations_cmd
from ai_os.cli.commands import memory as memory_cmd
from ai_os.cli.commands import skills as skills_cmd

FLAT_MODULES = [core, project, install, learning.flat_app]


def _merge_flat(root: typer.Typer, module_or_app: object) -> None:
    sub_app = module_or_app if isinstance(module_or_app, typer.Typer) else module_or_app.app  # type: ignore[attr-defined]
    root.registered_commands.extend(sub_app.registered_commands)


def build_app() -> typer.Typer:
    root = typer.Typer(
        name="ai-os",
        help="Personal AI Engineering Operating System.",
        no_args_is_help=True,
        add_completion=False,
    )

    for module in FLAT_MODULES:
        _merge_flat(root, module)

    root.add_typer(memory_cmd.app, name="memory")
    root.add_typer(integrations_cmd.app, name="integrations")
    root.add_typer(agents_cmd.app, name="agents")
    root.add_typer(skills_cmd.app, name="skills")
    root.add_typer(hooks_cmd.app, name="hooks")
    root.add_typer(learning.proposal_app, name="proposal")
    root.add_typer(config_cmd.app, name="config")

    return root


def main() -> None:
    build_app()()


app = build_app()

if __name__ == "__main__":
    main()
