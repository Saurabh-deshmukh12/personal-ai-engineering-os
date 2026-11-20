# Skills

Empty until Milestone 5 populates the 25 skills listed in the product spec.
Each skill is its own directory containing `SKILL.md`.

## Manifest format (`skills/<name>/SKILL.md`)

```markdown
---
name: project-discovery
description: Detects languages, frameworks, architecture, and dependencies for a new project.
version: 0.1.0
status: unavailable   # available | installed | disabled | unavailable | requires_configuration
permissions:
  - filesystem:read
planned_milestone: 5
---

## When to use it
...

## Required inputs
...

## Workflow
...

## Expected outputs
...

## Validation criteria
...

## Safety constraints
...
```

`name` and `description` are required frontmatter fields. All six section
headings above are required in the body. Run `ai-os skills validate` to check
any SKILL.md against this schema -- that validator is real and working today,
even though no skills exist yet.
