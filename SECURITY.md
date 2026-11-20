# Security Policy

## Non-negotiable architectural rules

### Client isolation
Every project carries `organization_id`, `client_id`, `project_id`. Every
memory read/write/search/retrieve/update must enforce all three. A request
missing any of them must fail closed (reject), never fall back to an
unscoped or wildcard read. A global agent must never access raw
client-specific knowledge; only sanitized, approved, generalized patterns may
enter shared/global knowledge.

**Current status**: the memory engine does not exist yet (Milestones 3-4), so
there is no isolation guarantee to rely on today. `tests/isolation/` and
`tests/security/` are reserved for the cross-client isolation test described
below and will be populated once the memory gateway exists -- do not assume
isolation is enforced until those tests exist and pass.

### Agent evolution
Agents may discover improvements, propose skills/agents/hooks, open GitHub
pull requests, and run automated tests. Agents must **not**: merge their own
global changes, release a new global version without human approval, modify
security policy silently, or copy confidential client information into a
global skill/agent/hook.

### Memory provenance
Every important technical fact retains: source repository, file/doc
reference, commit/PR reference (where available), observation timestamp,
scope, confidence, and current/historical/proposed status. Historical
architecture is superseded, never silently overwritten.

## Secrets

Credentials live in the OS secret store or environment variables -- never in
this repository, never in a project manifest, never in a memory record. CI
and local tooling must redact secrets before they reach any log, proposal
evidence file, or GitHub PR body.

## Required test coverage (tracked against `tests/`)

- Client isolation / missing-scope rejection (critical: two client scopes,
  verify neither can read/search/update/delete the other's memory).
- Secret redaction.
- Human-approval enforcement before any global release.
- Sanitization of learning observations before they reach a global proposal.

## Reporting

This is a personal-use private repository with no public distribution at this
time. If you are a collaborator and find a security issue, open an issue in
this repository directly.
