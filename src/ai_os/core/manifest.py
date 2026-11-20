"""Shared parsing for markdown-with-YAML-frontmatter manifest files.

Used by agent definitions (agents/*.md) and skill definitions
(skills/<name>/SKILL.md). Hook manifests are plain YAML (hooks/*.yaml)
and are parsed directly with yaml.safe_load instead.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

FRONTMATTER_DELIMITER = "---"


class ManifestParseError(ValueError):
    pass


@dataclass
class ParsedManifest:
    frontmatter: dict[str, Any]
    body: str
    source_path: Path

    def has_heading(self, heading_text: str) -> bool:
        needle = heading_text.strip().lower()
        for line in self.body.splitlines():
            stripped = line.strip().lstrip("#").strip().lower()
            if stripped == needle:
                return True
        return False


def parse_markdown_manifest(path: Path) -> ParsedManifest:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0].strip() != FRONTMATTER_DELIMITER:
        raise ManifestParseError(
            f"{path}: expected the file to start with a '---' YAML frontmatter block."
        )

    try:
        closing_index = lines[1:].index(FRONTMATTER_DELIMITER) + 1
    except ValueError as exc:
        raise ManifestParseError(f"{path}: frontmatter block is not closed with '---'.") from exc

    frontmatter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :])

    try:
        frontmatter = yaml.safe_load(frontmatter_text) or {}
    except yaml.YAMLError as exc:
        raise ManifestParseError(f"{path}: invalid YAML frontmatter: {exc}") from exc

    if not isinstance(frontmatter, dict):
        raise ManifestParseError(f"{path}: frontmatter must be a YAML mapping.")

    return ParsedManifest(frontmatter=frontmatter, body=body, source_path=path)
