# Planned Agent Roster

**Status: design/roadmap document.** None of these agents have a runtime yet
(agent execution is Milestone 5). This file records the intended
responsibilities, inputs, outputs, and permissions for each agent so that
Milestone 5 implements against an agreed contract rather than an improvised
one. Once an agent gets a real definition file, it will live as
`agents/<name>.md` and show up in `ai-os agents list`.

Every agent below is independently reusable. The Orchestrator Agent delegates
to only the agents a given task actually needs -- agents must not be wired
into unconditional delegation chains.

## Main orchestrator

### Orchestrator Agent
- **Responsibilities**: Receives a task, determines which specialized agent(s)
  it requires, delegates, and merges their outputs. Does not perform
  engineering work itself.
- **Inputs**: task description, current project scope (org/client/project id),
  capability registry snapshot.
- **Outputs**: delegation plan, final merged response.
- **Permissions**: read capability registry; invoke other agents. No direct
  memory write access, no GitHub write access.

### Project Intelligence Agent
- **Responsibilities**: Drives `ai-os init`/`analyze`/`refresh` -- detects
  languages/frameworks, inspects docs, maps architecture, dependencies, APIs,
  database, and deployment.
- **Inputs**: repository root path, existing project manifest (if any).
- **Outputs**: project briefing, discovered architecture facts with
  provenance, confirmation requests for ambiguous findings.
- **Permissions**: read-only filesystem access to the current project; memory
  write scoped to that project only.

## Engineering agents

### Solution Architect Agent
- **Responsibilities**: Proposes and evaluates architecture changes; records
  historical vs. current architecture decisions.
- **Inputs**: current architecture facts, proposed change description.
- **Outputs**: architecture decision record, superseded-fact markers (never
  silent overwrites).
- **Permissions**: memory read/write scoped to current project; no global
  write access.

### Backend Engineering Agent
- **Responsibilities**: Backend implementation tasks within a project's
  existing architecture and conventions.
- **Inputs**: task description, relevant project memory, codebase context.
- **Outputs**: code changes, test results.
- **Permissions**: filesystem write scoped to current project working tree.

### Frontend Engineering Agent
- **Responsibilities**: Frontend implementation tasks.
- **Inputs/Outputs/Permissions**: as Backend Engineering Agent, frontend scope.

### Database Engineering Agent
- **Responsibilities**: Schema analysis and migrations.
- **Inputs**: current schema facts, migration request.
- **Outputs**: migration scripts, updated schema facts (with history
  preserved), triggers `after-database-migration` hook.
- **Permissions**: project-scoped memory and filesystem write; no direct
  production database access.

### DevOps and Infrastructure Agent
- **Responsibilities**: Deployment and infrastructure analysis/changes.
- **Inputs**: deployment config, target environment.
- **Outputs**: infra change proposals, triggers `before-deployment` hook.
- **Permissions**: project-scoped; infra credential access only via the OS
  secret store, never inline.

### Debugging and Root Cause Analysis Agent
- **Responsibilities**: Reproduces and diagnoses bugs; records validated root
  causes as candidate learning observations.
- **Inputs**: bug report, logs, relevant project memory.
- **Outputs**: root cause record, suggested fix, classified observation for
  the learning engine.
- **Permissions**: project-scoped read/write; may emit observations but may
  not classify them as globally reusable itself (Memory Validation Agent/human
  review required).

### Code Review and Quality Agent
- **Responsibilities**: Reviews diffs for correctness, simplification,
  consistency.
- **Permissions**: read-only on the diff; no merge permission.

### Security Review Agent
- **Responsibilities**: Reviews changes for security issues (OWASP-class
  vulnerabilities, secret leakage, client-isolation violations).
- **Permissions**: read-only; may block a proposal from advancing but may not
  silently alter security policy.

### Testing Agent
- **Responsibilities**: Writes/executes tests, reports pass/fail, never
  reports fake success.
- **Permissions**: project-scoped filesystem and test-runner execution.

### Documentation Agent
- **Responsibilities**: Generates/updates documentation from actual code and
  recorded facts -- never invents capabilities that don't exist.
- **Permissions**: project-scoped filesystem write (docs only).

## Memory and evolution agents

### Engineering Memory Agent
- **Responsibilities**: Writes observations into scoped memory with full
  provenance (source repo, file/doc ref, commit/PR ref, timestamp, scope,
  confidence, current/historical/proposed status).
- **Permissions**: memory write strictly scoped to the originating
  organization/client/project id. Fails closed on missing scope.

### Memory Validation Agent
- **Responsibilities**: Detects duplicate/conflicting/stale facts; flags for
  human or Memory Validation review before superseding history.
- **Permissions**: memory read across the single current scope only; never
  cross-scope.

### Agent Evolution Agent
- **Responsibilities**: Proposes agent/skill/hook changes based on classified,
  sanitized observations; opens GitHub PRs for global proposals.
- **Permissions**: may create PRs; **may not merge them** and may not release
  a new global version without a human approval step.

### Skill Creation Agent
- **Responsibilities**: Drafts new SKILL.md files following the required
  schema (description, when to use, required inputs, workflow, outputs,
  validation criteria, safety constraints).
- **Permissions**: writes to `proposals/`, never directly to `skills/` for a
  global skill without going through the proposal/review flow.

### Integration Research Agent
- **Responsibilities**: Inspects a candidate integration's actual repository/
  docs/license before any adapter is implemented; never assumes undocumented
  API behavior (see Archify in `config/integrations.yaml`).
- **Permissions**: read-only, external web access for research only.

## Non-negotiable rules for every agent above

1. Every memory operation enforces `organization_id` / `client_id` /
   `project_id`. Missing scope fails closed.
2. No agent may copy raw client-specific knowledge into a global
   skill/agent/hook. Only sanitized, approved, generalized patterns may enter
   shared knowledge.
3. No agent may merge its own global change or silently modify security
   policy.
