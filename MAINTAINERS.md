# Maintainers

The operating rules in [`AGENTS.md`](AGENTS.md) cite **roles**, never people. This file
is the only place a person or organisation is named as an authority. A roster change is
made here and nowhere else — it never requires touching `AGENTS.md` or any rule
document.

Role definitions live in
[`docs/CRIC-PRD-v0.1/community/Open-Source-Governance.md`](docs/CRIC-PRD-v0.1/community/Open-Source-Governance.md);
this file records who currently holds them.

## Human approval authority

Two roles hold human approval authority, defined in
[`Open-Source-Governance.md`](docs/CRIC-PRD-v0.1/community/Open-Source-Governance.md)
§Roles and §Project Stewardship, and split by scope in [`AGENTS.md`](AGENTS.md) §4.

| Role | Scope | Current holder |
|---|---|---|
| **Core Maintainer** | Stable changes to CRIC Core contracts: architecture changes, Architecture Freeze Point ratification and any post-lock migration, breaking schema changes, semantic redefinition of a stable type, safety-relevant concepts, deprecation of a widely used type. | Ashley Derrick <ashley@eyekyam.com> |
| **Project Steward** | Production deployment, credentials, destructive or irreversible actions, security-sensitive changes, licensing, significant cost, and any change of scope or business intent. | Eyekyam Risk Resolutions — the founding organisation. Contacts: ashley@eyekyam.com (CTO), vidya@eyekyam.com (CEO). |

## Build-time engineering roles

The five build-time engineering roles in [`AGENTS.md`](AGENTS.md) §9 are
**agent-held and harness-agnostic**:

- Requirements Analyst
- Implementation Engineer
- Independent Verifier
- Memory & Knowledge Manager
- Engineering Coordinator

Each is defined by its **mandate** and nothing else — not by a harness, model, vendor or
persistent identity. They have **no named holder by design**: whichever agent or person
picks one up inherits the mandate and its stated limits for the duration of a work
package. Listing holders here would be a category error, so none are listed.

**No agent holds either human approval role.** Agents prepare branches and pull requests;
the approvals in the table above stay with the humans named there.

## The rest of the governance role set

[`Open-Source-Governance.md`](docs/CRIC-PRD-v0.1/community/Open-Source-Governance.md)
§Roles defines the full set — User, Contributor, Reviewer, Domain Reviewer, Ontology
Reviewer, Maintainer, Core Maintainer. This roster covers only the roles that currently
have holders; a role's absence here means nobody holds it yet, not that it does not
exist.

## Changing this file

A roster change is a normal pull request against `main`, reviewed like any other change.

Adding or removing a **Core Maintainer** is a Project Steward decision —
[`Open-Source-Governance.md`](docs/CRIC-PRD-v0.1/community/Open-Source-Governance.md)
§Maintainer Authority places "approve role assignments" with maintainer authority, and
§Project Stewardship places the appointment of maintainers with the founding
organisation acting as steward.
