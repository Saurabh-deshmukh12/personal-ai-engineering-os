"""User-level configuration for AI-OS.

Precedence (highest wins): environment variables -> user config file -> defaults.
This file intentionally holds no client-specific or secret data: secrets belong in
the OS secret store or environment variables (see SECURITY.md).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError

from ai_os.core.paths import user_config_file

ENV_PREFIX = "AI_OS_"


class AIOSConfig(BaseModel):
    """Resolved, validated global configuration."""

    default_organization_id: str | None = Field(
        default=None, description="Default organization_id to suggest on `ai-os init`."
    )
    telemetry_enabled: bool = Field(
        default=False, description="Whether anonymous local usage stats are recorded."
    )
    llm_routing_policy: str = Field(
        default="local-only",
        description="Routing policy name for the OmniRoute adapter (Milestone 7).",
    )
    allow_global_proposal_pr_creation: bool = Field(
        default=False,
        description=(
            "Whether the evolution engine is allowed to open GitHub PRs for global "
            "proposals. Must be explicitly enabled by the human operator."
        ),
    )

    model_config = {"extra": "forbid"}


class ConfigLoadResult(BaseModel):
    config: AIOSConfig
    source_file: str | None
    env_overrides: list[str]
    errors: list[str]

    model_config = {"arbitrary_types_allowed": True}


def _read_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file {path} must contain a YAML mapping at the top level.")  # noqa: TRY004
    return data


def _env_overrides() -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    for field_name in AIOSConfig.model_fields:
        env_name = ENV_PREFIX + field_name.upper()
        if env_name in os.environ:
            raw = os.environ[env_name]
            if raw.lower() in {"true", "false"}:
                overrides[field_name] = raw.lower() == "true"
            else:
                overrides[field_name] = raw
    return overrides


def load_config(config_file: Path | None = None) -> ConfigLoadResult:
    path = config_file or user_config_file()
    errors: list[str] = []
    file_data: dict[str, Any] = {}
    source_file: str | None = None

    try:
        file_data = _read_yaml_file(path)
        if path.exists():
            source_file = str(path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"Failed to read {path}: {exc}")

    overrides = _env_overrides()
    merged = {**file_data, **overrides}

    try:
        config = AIOSConfig.model_validate(merged)
    except ValidationError as exc:
        errors.append(str(exc))
        config = AIOSConfig()

    return ConfigLoadResult(
        config=config,
        source_file=source_file,
        env_overrides=sorted(overrides.keys()),
        errors=errors,
    )


def save_config(config: AIOSConfig, config_file: Path | None = None) -> Path:
    path = config_file or user_config_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(config.model_dump(), fh, sort_keys=True)
    return path
