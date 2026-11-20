# Personal AI Engineering Operating System (AI-OS)

A local-first, reusable system for understanding software projects, maintaining
strictly client-isolated engineering memory, and running specialized AI agents,
skills, and lifecycle hooks across every project you work on.

**Status: Milestone 1 of 10 complete.** See [docs/roadmap.md](docs/roadmap.md) for
the full milestone plan and exactly what is and is not implemented yet. This
README describes the real, current state of the repository -- not the target
end state.

## What's implemented right now (Milestone 1)

- A real, installable Python package (`ai_os`) with a `ai-os` CLI entry point
  built on Typer.
- A **capability registry** (`ai_os.core.registry`) that dynamically scans the
  live CLI command tree plus `agents/`, `skills/`, `hooks/`, and
  `config/integrations.yaml` at call time -- nothing in `/help` is a hardcoded
  list, so dropping a new skill/agent/hook file in changes the output with no
  code change.
- A dynamic, unified help system: `ai-os help` and `ai-os /help`, with topic
  filters (`ai-os help agents`, `ai-os help skills`, `ai-os help hooks`,
  `ai-os help integrations`, `ai-os help memory`, `ai-os help commands`,
  `ai-os help examples`).
- A real SKILL.md schema validator: `ai-os skills validate`.
- User-level configuration loading (file + environment variable overrides,
  precedence: env > file > defaults) via `ai-os config show` / `validate`.
- `ai-os status`, `ai-os health`, `ai-os version`.
- Every command described in the product spec but **not yet implemented**
  (project discovery, memory, most of integrations, agent/hook execution,
  learning/evolution, install/uninstall) is registered in the CLI so it shows
  up in `--help`, but calling it prints "Not yet implemented: planned for
  Milestone N" and exits with a non-zero code. It never reports fake success.

## What is explicitly NOT implemented yet

- `ai-os init` / project discovery (Milestone 2).
- The memory gateway, scope enforcement, and client isolation guarantees
  (Milestones 3-4). **Do not rely on any isolation guarantee yet** -- there is
  no memory engine to isolate.
- Graphiti / Claude-Mem / Headroom / OmniRoute / Ponytail / Archify adapters
  (Milestone 7). `config/integrations.yaml` lists them as `unavailable` /
  `disabled` on purpose.
- Agent and hook *execution* (agent/skill/hook *definitions* can be discovered
  and validated once added, but nothing runs them yet) (Milestones 5-6).
- The continuous learning/evolution engine and GitHub PR automation for global
  proposals (Milestones 8-9).
- Plugin distribution/installation into Claude Code, Codex, etc. (Milestone 9).
- This repository has **not** been pushed to GitHub yet. No remote exists.

## Installation (local development)

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
ai-os --help
ai-os help
```

## Key commands available today

| Command | Status |
|---|---|
| `ai-os version` | Available |
| `ai-os status` | Available |
| `ai-os health` | Available |
| `ai-os help [topic]` / `ai-os /help [topic]` | Available |
| `ai-os config show` / `ai-os config validate` | Available |
| `ai-os skills list` / `info` / `validate` | Available |
| `ai-os agents list` / `info` | Available (lists definitions only; no execution) |
| `ai-os hooks list` / `status` | Available (lists definitions only; no execution) |
| `ai-os integrations list` / `status` | Available (read-only registry) |
| Everything else | Stubbed; run it to see the exact planned milestone |

Run `ai-os help commands` for the live, authoritative list -- this table will
drift as milestones land; the CLI output will not.

## Architecture notes

- Config lives in a per-user config directory (via `platformdirs`), never in
  this repository.
- `agents/`, `skills/`, `hooks/` hold portable, host-independent definitions.
  Host-specific wiring (Claude Code, Codex, ...) is deliberately kept separate
  and lands in Milestone 9.
- See [AGENTS.md](AGENTS.md) for the full planned agent roster,
  [SECURITY.md](SECURITY.md) for the non-negotiable client isolation and
  human-approval rules, and [CHANGELOG.md](CHANGELOG.md) for what shipped when.

## License

Proprietary. All rights reserved. Not for redistribution.
