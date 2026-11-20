"""Capability registry: the single source of truth behind `ai-os help` / `ai-os /help`.

Everything shown by the dynamic help system is derived here, at call time, by
scanning the actual filesystem (agents/, skills/, hooks/, config/integrations.yaml)
and introspecting the live Typer/Click CLI tree. Nothing in this module is a
hardcoded list of "what exists" -- that list is always re-derived, so a newly
dropped-in skill or agent shows up without any code change.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ai_os.core.manifest import ManifestParseError, ParsedManifest, parse_markdown_manifest

SKILL_REQUIRED_HEADINGS = [
    "When to use it",
    "Required inputs",
    "Workflow",
    "Expected outputs",
    "Validation criteria",
    "Safety constraints",
]
AGENT_REQUIRED_HEADINGS = ["Responsibilities", "Inputs", "Outputs", "Permissions"]
HOOK_REQUIRED_KEYS = [
    "name",
    "trigger",
    "input",
    "output",
    "permissions",
    "failure_behavior",
    "deterministic",
]


class CapabilityStatus(str, enum.Enum):
    AVAILABLE = "available"
    INSTALLED = "installed"
    DISABLED = "disabled"
    UNAVAILABLE = "unavailable"
    REQUIRES_CONFIGURATION = "requires_configuration"
    INVALID = "invalid"


class CapabilityCategory(str, enum.Enum):
    CLI_COMMAND = "cli_command"
    AGENT = "agent"
    SKILL = "skill"
    HOOK = "hook"
    INTEGRATION = "integration"


@dataclass
class Capability:
    name: str
    category: CapabilityCategory
    description: str
    version: str = "0.1.0"
    status: CapabilityStatus = CapabilityStatus.UNAVAILABLE
    permissions: list[str] = field(default_factory=list)
    invocation: str | None = None
    source_path: str | None = None
    planned_milestone: int | None = None
    errors: list[str] = field(default_factory=list)


def validate_skill_manifest(parsed: ParsedManifest) -> list[str]:
    errors: list[str] = []
    for required_field in ("name", "description"):
        if not parsed.frontmatter.get(required_field):
            errors.append(f"missing required frontmatter field '{required_field}'")
    for heading in SKILL_REQUIRED_HEADINGS:
        if not parsed.has_heading(heading):
            errors.append(f"missing required section heading '## {heading}'")
    return errors


def validate_agent_manifest(parsed: ParsedManifest) -> list[str]:
    errors: list[str] = []
    for required_field in ("name", "role", "category"):
        if not parsed.frontmatter.get(required_field):
            errors.append(f"missing required frontmatter field '{required_field}'")
    for heading in AGENT_REQUIRED_HEADINGS:
        if not parsed.has_heading(heading):
            errors.append(f"missing required section heading '## {heading}'")
    return errors


def validate_hook_manifest(data: dict[str, Any]) -> list[str]:
    errors = []
    for required_key in HOOK_REQUIRED_KEYS:
        if required_key not in data:
            errors.append(f"missing required key '{required_key}'")
    return errors


def discover_skills(skills_dir: Path) -> list[Capability]:
    capabilities: list[Capability] = []
    if not skills_dir.exists():
        return capabilities
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        manifest_path = skill_dir / "SKILL.md"
        if not manifest_path.exists():
            continue
        try:
            parsed = parse_markdown_manifest(manifest_path)
        except ManifestParseError as exc:
            capabilities.append(
                Capability(
                    name=skill_dir.name,
                    category=CapabilityCategory.SKILL,
                    description="(unparsable manifest)",
                    status=CapabilityStatus.INVALID,
                    source_path=str(manifest_path),
                    errors=[str(exc)],
                )
            )
            continue

        errors = validate_skill_manifest(parsed)
        status = (
            CapabilityStatus.INVALID
            if errors
            else CapabilityStatus(parsed.frontmatter.get("status", "unavailable"))
        )
        capabilities.append(
            Capability(
                name=parsed.frontmatter.get("name", skill_dir.name),
                category=CapabilityCategory.SKILL,
                description=parsed.frontmatter.get("description", ""),
                version=str(parsed.frontmatter.get("version", "0.1.0")),
                status=status,
                permissions=list(parsed.frontmatter.get("permissions", []) or []),
                invocation=f"ai-os skills info {parsed.frontmatter.get('name', skill_dir.name)}",
                source_path=str(manifest_path),
                planned_milestone=parsed.frontmatter.get("planned_milestone"),
                errors=errors,
            )
        )
    return capabilities


def discover_agents(agents_dir: Path) -> list[Capability]:
    capabilities: list[Capability] = []
    if not agents_dir.exists():
        return capabilities
    for manifest_path in sorted(agents_dir.glob("*.md")):
        if manifest_path.name.upper() == "README.MD":
            continue
        try:
            parsed = parse_markdown_manifest(manifest_path)
        except ManifestParseError as exc:
            capabilities.append(
                Capability(
                    name=manifest_path.stem,
                    category=CapabilityCategory.AGENT,
                    description="(unparsable manifest)",
                    status=CapabilityStatus.INVALID,
                    source_path=str(manifest_path),
                    errors=[str(exc)],
                )
            )
            continue

        errors = validate_agent_manifest(parsed)
        status = (
            CapabilityStatus.INVALID
            if errors
            else CapabilityStatus(parsed.frontmatter.get("status", "unavailable"))
        )
        capabilities.append(
            Capability(
                name=parsed.frontmatter.get("name", manifest_path.stem),
                category=CapabilityCategory.AGENT,
                description=parsed.frontmatter.get("description", parsed.frontmatter.get("role", "")),
                version=str(parsed.frontmatter.get("version", "0.1.0")),
                status=status,
                permissions=list(parsed.frontmatter.get("permissions", []) or []),
                invocation=f"ai-os agents info {parsed.frontmatter.get('name', manifest_path.stem)}",
                source_path=str(manifest_path),
                planned_milestone=parsed.frontmatter.get("planned_milestone"),
                errors=errors,
            )
        )
    return capabilities


def discover_hooks(hooks_dir: Path) -> list[Capability]:
    capabilities: list[Capability] = []
    if not hooks_dir.exists():
        return capabilities
    for manifest_path in sorted(hooks_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            capabilities.append(
                Capability(
                    name=manifest_path.stem,
                    category=CapabilityCategory.HOOK,
                    description="(unparsable manifest)",
                    status=CapabilityStatus.INVALID,
                    source_path=str(manifest_path),
                    errors=[str(exc)],
                )
            )
            continue

        errors = validate_hook_manifest(data)
        status = (
            CapabilityStatus.INVALID
            if errors
            else CapabilityStatus(data.get("status", "unavailable"))
        )
        capabilities.append(
            Capability(
                name=data.get("name", manifest_path.stem),
                category=CapabilityCategory.HOOK,
                description=data.get("description", data.get("trigger", "")),
                version=str(data.get("version", "0.1.0")),
                status=status,
                permissions=list(data.get("permissions", []) or []),
                invocation=f"ai-os hooks status {data.get('name', manifest_path.stem)}",
                source_path=str(manifest_path),
                planned_milestone=data.get("planned_milestone"),
                errors=errors,
            )
        )
    return capabilities


def discover_integrations(registry_file: Path) -> list[Capability]:
    capabilities: list[Capability] = []
    if not registry_file.exists():
        return capabilities
    data = yaml.safe_load(registry_file.read_text(encoding="utf-8")) or {}
    for entry in data.get("integrations", []):
        capabilities.append(
            Capability(
                name=entry["name"],
                category=CapabilityCategory.INTEGRATION,
                description=entry.get("description", ""),
                version=str(entry.get("version", "0.1.0")),
                status=CapabilityStatus(entry.get("status", "unavailable")),
                permissions=list(entry.get("permissions", []) or []),
                invocation=f"ai-os integrations status {entry['name']}",
                source_path=str(registry_file),
                planned_milestone=entry.get("planned_milestone"),
            )
        )
    return capabilities


def discover_cli_commands(typer_app: Any) -> list[Capability]:
    """Walk the live Typer command tree and report every registered command.

    Each command callback may carry an `__ai_os_status__` / `__ai_os_milestone__`
    attribute (set by the `@command_status(...)` decorator in ai_os.cli.status) --
    if absent, the command is assumed AVAILABLE since it has no stub marker.

    Deliberately duck-types rather than importing `click`: Typer >=0.16 vendors
    its own click fork internally (`typer._click`) and does not depend on the
    standalone `click` PyPI package, so `import click` fails even though the
    command tree underneath is still click-shaped (has `.commands` on groups).
    """
    group = typer_app if hasattr(typer_app, "commands") else _to_command_tree(typer_app)
    capabilities: list[Capability] = []
    _walk_command_group(group, prefix="ai-os", capabilities=capabilities)
    return capabilities


def _to_command_tree(typer_app: Any) -> Any:
    import typer

    return typer.main.get_command(typer_app)


def _walk_command_group(group: Any, prefix: str, capabilities: list[Capability]) -> None:
    for name, command in sorted(group.commands.items()):
        full_name = f"{prefix} {name}"
        if hasattr(command, "commands"):
            _walk_command_group(command, prefix=full_name, capabilities=capabilities)
            continue

        callback = getattr(command, "callback", None)
        status = getattr(callback, "__ai_os_status__", CapabilityStatus.AVAILABLE)
        milestone = getattr(callback, "__ai_os_milestone__", None)
        capabilities.append(
            Capability(
                name=full_name,
                category=CapabilityCategory.CLI_COMMAND,
                description=(command.help or command.short_help or "").strip(),
                status=status,
                invocation=full_name,
                planned_milestone=milestone,
            )
        )


@dataclass
class CapabilityRegistry:
    cli_commands: list[Capability]
    agents: list[Capability]
    skills: list[Capability]
    hooks: list[Capability]
    integrations: list[Capability]

    def all(self) -> list[Capability]:
        return [
            *self.cli_commands,
            *self.agents,
            *self.skills,
            *self.hooks,
            *self.integrations,
        ]


def build_registry(
    typer_app: Any,
    agents_dir: Path,
    skills_dir: Path,
    hooks_dir: Path,
    integrations_registry_file: Path,
) -> CapabilityRegistry:
    return CapabilityRegistry(
        cli_commands=discover_cli_commands(typer_app),
        agents=discover_agents(agents_dir),
        skills=discover_skills(skills_dir),
        hooks=discover_hooks(hooks_dir),
        integrations=discover_integrations(integrations_registry_file),
    )
