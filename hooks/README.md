# Hooks

Empty until Milestone 6. Hooks are plain YAML manifests (not markdown, unlike
agents/skills) because they must stay deterministic and machine-checkable --
reasoning-heavy work belongs in an agent the hook invokes, not in the hook
definition itself.

## Manifest format (`hooks/<name>.yaml`)

```yaml
name: after-file-edit
trigger: after-file-edit
description: Fires after a file edit completes.
input: { file_path: string, diff: string }
output: { accepted: bool }
permissions: []
failure_behavior: log-and-continue   # or: block
deterministic: true
status: unavailable
planned_milestone: 6
```

Required keys: `name`, `trigger`, `input`, `output`, `permissions`,
`failure_behavior`, `deterministic`. Not every AI coding host supports every
trigger event -- host compatibility is recorded per-hook once Milestone 6
implements the host-specific adapters.

Required hook set (Section 7 of the spec): session-start, session-end,
before-tool-use, before-file-edit, after-file-edit, after-commit,
after-pull-request, after-architecture-change, after-database-migration,
before-deployment, memory-capture, memory-validation, project-refresh,
agent-evolution-proposal.
