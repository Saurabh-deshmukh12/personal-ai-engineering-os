from __future__ import annotations

import yaml

from ai_os.core.registry import CapabilityStatus, discover_hooks

VALID_HOOK = {
    "name": "good-hook",
    "trigger": "after-file-edit",
    "description": "test hook",
    "input": {"file_path": "string"},
    "output": {"accepted": "bool"},
    "permissions": [],
    "failure_behavior": "log-and-continue",
    "deterministic": True,
    "status": "unavailable",
}

INCOMPLETE_HOOK = {"name": "bad-hook", "trigger": "after-commit"}


def _write_hook(tmp_path, filename, data):
    hooks_dir = tmp_path / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    (hooks_dir / filename).write_text(yaml.safe_dump(data), encoding="utf-8")
    return hooks_dir


def test_valid_hook_discovered(tmp_path):
    hooks_dir = _write_hook(tmp_path, "good-hook.yaml", VALID_HOOK)
    caps = discover_hooks(hooks_dir)
    assert len(caps) == 1
    assert caps[0].name == "good-hook"
    assert caps[0].status == CapabilityStatus.UNAVAILABLE
    assert caps[0].errors == []


def test_incomplete_hook_is_invalid(tmp_path):
    hooks_dir = _write_hook(tmp_path, "bad-hook.yaml", INCOMPLETE_HOOK)
    caps = discover_hooks(hooks_dir)
    assert caps[0].status == CapabilityStatus.INVALID
    assert len(caps[0].errors) >= 1


def test_missing_hooks_dir_returns_empty(tmp_path):
    assert discover_hooks(tmp_path / "does-not-exist") == []
