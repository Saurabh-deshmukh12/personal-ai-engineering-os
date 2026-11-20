# Changelog

## [Unreleased] - Milestone 1

### Added
- Python package `ai_os` (src layout), installable via `pip install -e .`.
- `ai-os` CLI (Typer) with: `version`, `status`, `health`, `help` / `/help`,
  `config show`/`validate`, `skills list`/`info`/`validate`,
  `agents list`/`info`, `hooks list`/`status`, `integrations list`/`status`.
- Capability registry (`ai_os.core.registry`) that dynamically derives
  `/help` output from the live CLI tree and the `agents/`, `skills/`,
  `hooks/`, `config/integrations.yaml` filesystem state.
- SKILL.md / agent manifest / hook manifest parsers and schema validators.
- User-level config loader with env-var override precedence.
- Full repository directory skeleton for all later milestones.
- Stub commands for every not-yet-implemented capability from the product
  spec; each exits non-zero with a "planned for Milestone N" message instead
  of reporting fake success.
- `AGENTS.md` (planned agent roster/contracts), `SECURITY.md` (isolation and
  approval rules), this changelog, `docs/roadmap.md`.
- Unit tests: CLI command registration, dynamic help generation, skill
  discovery + validation, agent discovery, hook registration, config
  load/validate.

### Not included in this milestone
See README.md "What is explicitly NOT implemented yet".
