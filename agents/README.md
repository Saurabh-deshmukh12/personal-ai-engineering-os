# Agent definitions

Empty until Milestone 5. See [AGENTS.md](../AGENTS.md) for the full planned
roster and contracts.

## Manifest format (`agents/<name>.md`)

```markdown
---
name: solution-architect-agent
role: Proposes and evaluates architecture changes
category: engineering
version: 0.1.0
status: unavailable   # available | installed | disabled | unavailable | requires_configuration
permissions:
  - memory:read
  - memory:write
planned_milestone: 5
---

## Responsibilities
...

## Inputs
...

## Outputs
...

## Permissions
...
```

`name`, `role`, `category` are required frontmatter fields. The four
`## Responsibilities` / `## Inputs` / `## Outputs` / `## Permissions`
headings are required in the body. `ai-os agents list` / `ai-os agents info`
will reject (status `invalid`) a manifest missing any of these.
