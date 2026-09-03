# Security Policy

This is the vulnerability-disclosure policy for `cric-core`. It is distinct from
[`docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md`](docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md),
which specifies security *design* (threat categories, tool permissions, prompt
injection handling, agent workspace isolation) rather than how to report a
vulnerability against this repository.

## Reporting a vulnerability

Report privately — do not open a public GitHub issue. Per
`docs/CRIC-PRD-v0.1/community/Open-Source-Governance.md`'s Security Governance
section: *"Security vulnerabilities should have a private reporting route. Sensitive
vulnerabilities should not require immediate public issue disclosure."*

**Preferred channel: GitHub Private Vulnerability Reporting**, via this
repository's Security tab → "Report a vulnerability."

**Status as of this writing: not yet enabled on this repository** — verified via
the GitHub API (`private-vulnerability-reporting` → `false`) at the time this
policy was written. Enabling it is a one-time, reversible repository-admin
setting (Settings → Security → Private vulnerability reporting); it is not a
content change and isn't something this pull request can do on its own
authority. Flagged as an action item for whoever holds repository admin.

**Until it is enabled**, there is no confirmed private channel for this
repository specifically. Do not route a report through a public issue, pull
request, or discussion in the meantime — hold it and escalate the "channel not
yet live" gap itself so it gets fixed, rather than defaulting to a public
report.

## Scope

In scope: `cric-core` itself — the identifier/version/knowledge-graph code
under `src/`, its CI/CD configuration, and its dependency chain. Out of scope:
the specification documents under `docs/` (a documentation error is a normal
issue or pull request, not a security report) and any deployed instance not
operated by this project directly, since `cric-core` v0.1 ships no running
service.

## What to expect

Handling follows `Security-and-Responsible-AI.md`'s Incident Response section:
affected-artefact identification, token revocation where relevant, provenance
impact analysis, and downstream-dependency identification for anything that
propagates into the repositories that depend on `cric-core`. There is no
published response-time SLA yet — this project has not shipped a release, and a
commitment here should not be made ahead of that.

## Supported versions

`cric-core` has not reached a v0.1 release. There is no version table yet;
security fixes land on `main`.
