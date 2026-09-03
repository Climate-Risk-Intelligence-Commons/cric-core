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

**Report via this repository's Security tab → "Report a vulnerability."** That
opens a private draft security advisory visible only to you and the
repository's admins.

If you can't reach that form — no GitHub account, or an access problem on your
end — contact a repository admin directly through the
[Climate-Risk-Intelligence-Commons](https://github.com/Climate-Risk-Intelligence-Commons)
GitHub organisation. Either way, don't fall back to a public issue, pull
request, or discussion.

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
