"""Central path resolution for the AI-OS package.

Distinguishes three locations, per the local-first architecture:
  - REPO_ROOT: the central personal-ai-engineering-os source checkout (this repo).
  - user config dir: per-user settings (platformdirs), never contains client data.
  - user data dir: per-user local memory / event journal, never committed to git.
"""

from __future__ import annotations

from pathlib import Path

import platformdirs

APP_NAME = "ai-os"
APP_AUTHOR = "ai-os"

REPO_ROOT = Path(__file__).resolve().parents[3]

AGENTS_DIR = REPO_ROOT / "agents"
SKILLS_DIR = REPO_ROOT / "skills"
HOOKS_DIR = REPO_ROOT / "hooks"
INTEGRATIONS_REGISTRY_FILE = REPO_ROOT / "config" / "integrations.yaml"


def user_config_dir() -> Path:
    return Path(platformdirs.user_config_dir(APP_NAME, APP_AUTHOR))


def user_data_dir() -> Path:
    return Path(platformdirs.user_data_dir(APP_NAME, APP_AUTHOR))


def user_config_file() -> Path:
    return user_config_dir() / "config.yaml"


def project_manifest_file(project_root: Path) -> Path:
    return project_root / ".ai-os" / "project.yaml"
