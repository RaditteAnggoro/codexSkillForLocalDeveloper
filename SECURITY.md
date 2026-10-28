# Security

Skill instructions influence an agent's decisions. Review changes before using them with a sensitive repository, and grant tools only the access needed for the task.

## Reporting a vulnerability

Do not put credentials, private source, or exploitable sensitive details in a public issue. If the hosting repository offers GitHub's private vulnerability reporting, use **Security → Advisories → Report a vulnerability**. Otherwise, contact a repository administrator through an existing private channel and arrange a safe way to share the report.

Include the affected skill/tool version, a minimal sanitized reproduction, expected boundary, actual behaviour, and impact. No maintainer contact address or response-time commitment is established by this template.

## Scope

Reports about unintended tool use, data exposure, filesystem access in repository scripts, or instructions that expand a user's request are useful. The validator checks structure and local links; it is not a security audit of agent behaviour. Browser access and external integrations keep their own permissions and data-handling rules.
