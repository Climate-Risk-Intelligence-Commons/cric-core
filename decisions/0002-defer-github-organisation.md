# ADR-0002: Defer creating the `climate-risk-intelligence-commons` GitHub organisation

- **Status:** Accepted
- **Approver:** Ashley
- **Date:** 2026-08-29
- **Evidence:** Ashley, channel CRIC-Dev (`17bd72a0-4d90-4e0b-b102-f9163f0cfd4b`), event
  `1c8b1d69909171e7cc76dec3dc6d9977f05ccd5c850cf937e59626cca46c689f`, 2026-08-29T13:43:22Z
  — "as far as D1 is concerned, I don't want to do this organization thing anymore. it's
  too complicated. let's do all that later on. I don't want to create an organization."
  Superseded Ashley's own earlier agreement with the Engineering Coordinator's
  create-the-org recommendation, event `a9c02cd0a892ce2e…`, 2026-08-29T13:31:46Z, 12
  minutes prior — see Alternatives below for what changed between the two.

## Context

`product/Repository-and-System-Architecture.md` names `github.com/climate-risk-intelligence-commons/`
as CRIC's repository layout. Today, and for the foreseeable future per this ADR, the
repository family lives under `github.com/ashley-eyekyam/` instead. This is a deliberate
deviation from a named PRD layout, not an oversight, and is recorded so nobody later
reads that document's repository-layout section as a current statement of fact.

## Decision

Stay at `github.com/ashley-eyekyam/cric-core` (and the eleven sibling repositories
Phase 0 creates) for now. No `climate-risk-intelligence-commons` organisation is
created at this time. Phase 0 repository creation is **not** blocked by this —
the Engineering Coordinator's existing GitHub token creates repositories directly
under `ashley-eyekyam/`.

## Alternatives considered

1. **Create the organisation now, transfer `cric-core` into it.** Ashley's initial
   position (13:31:46Z): agreed with the Coordinator's recommendation, on the
   Coordinator's own stated logic — deciding this after Phase 0 means renaming twelve
   repositories and breaking clone URLs/package names/citation paths later; deciding
   now costs about ten minutes; it is also a governance signal consistent with
   `community/Open-Source-Governance.md`'s premise of a commons rather than a
   repository whose meaning depends on one organisation. Superseded 12 minutes later:
   Ashley found the org-creation mechanics themselves ("this organization thing")
   too complicated to do right now, independent of whether the governance argument for
   eventually having one still holds.
2. **Defer the organisation, stay at `ashley-eyekyam/`.** Chosen. Ashley's explicit,
   final instruction, given after weighing the ten-minutes-now-vs-later argument
   directly and choosing to defer anyway.

## Consequences

- `product/Repository-and-System-Architecture.md`'s `github.com/climate-risk-intelligence-commons/`
  layout is **aspirational, not descriptive**, until this ADR is revisited. Any build-time
  agent citing that document's repository-layout section should cite this ADR alongside
  it for current state.
- Reversible, not a Freeze Point — organisation transfer remains straightforward later
  (GitHub preserves history, issues, and PRs, and leaves a redirect from the old URL,
  per the Coordinator's own verification in event `c7908076e35061af…`).
- Phase 0 proceeds unblocked: the Coordinator's token creates repositories directly
  under `ashley-eyekyam/` without needing `admin:org` scope.
- D2 (per-repository outbound licence: code AGPL-3.0, knowledge/data/docs CC-BY-4.0) is
  unaffected — Ashley's message addressed D1 only.
