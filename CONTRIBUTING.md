# Contributing to CRIC

Contribution types, the general contribution flow, pull request requirements,
knowledge/data/ontology/agent/model contribution paths, CODEOWNERS conventions,
automated checks and merge rules are specified in
[`docs/CRIC-PRD-v0.1/community/Contribution-and-Review-Process.md`](docs/CRIC-PRD-v0.1/community/Contribution-and-Review-Process.md).
Read that document before opening a pull request.

This file exists at the repository root so GitHub surfaces contribution guidance
automatically — in the pull request composer and the repository's Community
Standards checklist — without requiring anyone to already know where the PRD lives.
It is a pointer, not a copy; the process itself is not duplicated here.

## Before you contribute

- **Code of conduct.** All contribution is governed by
  [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
- **Security issues.** Do not open a public issue for a security vulnerability.
  See [`SECURITY.md`](SECURITY.md).
- **Governance and roles.** See [`GOVERNANCE.md`](GOVERNANCE.md) for who can
  approve what.
- **cric-core is the contract root.** Every other CRIC repository depends on this
  one; this repository may not depend on any domain-specific repository (see
  [`README.md`](README.md)).

## Quick version of the flow

```text
Issue/Proposal → Branch → Contribution → Automated validation → Review → Revision → Merge → Release
```

Not every small change needs an issue first — see the full document for what does.
