from __future__ import annotations

import os

from ai_os.core.config import AIOSConfig, load_config, save_config


def test_defaults_when_no_file(tmp_path, monkeypatch):
    for key in list(os.environ):
        if key.startswith("AI_OS_"):
            monkeypatch.delenv(key, raising=False)
    result = load_config(config_file=tmp_path / "does-not-exist.yaml")
    assert result.config == AIOSConfig()
    assert result.source_file is None
    assert result.errors == []


def test_file_values_are_applied(tmp_path):
    path = tmp_path / "config.yaml"
    save_config(AIOSConfig(default_organization_id="acme"), config_file=path)
    result = load_config(config_file=path)
    assert result.config.default_organization_id == "acme"
    assert result.source_file == str(path)


def test_env_var_overrides_file(tmp_path, monkeypatch):
    path = tmp_path / "config.yaml"
    save_config(AIOSConfig(default_organization_id="from-file"), config_file=path)
    monkeypatch.setenv("AI_OS_DEFAULT_ORGANIZATION_ID", "from-env")
    result = load_config(config_file=path)
    assert result.config.default_organization_id == "from-env"
    assert "default_organization_id" in result.env_overrides


def test_unknown_field_is_an_error_not_a_silent_ignore(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("not_a_real_field: 123\n", encoding="utf-8")
    result = load_config(config_file=path)
    assert result.errors, "An unknown config field must surface as an error, not be silently dropped."
