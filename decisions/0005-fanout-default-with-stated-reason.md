# ADR-0005: Parallelisation is the default; declining it requires a stated reason

- **Status:** Accepted
- **Approver:** Ashley
- **Date:** 2026-08-29
- **Freeze Point?** No
- **Evidence:** Engineering Coordinator's recommendation, event
  `4e262256ff16ae6f6cab5d29c5ab37296519564f4218ffb9c3de52a79f326454`, 2026-08-29T14:51:13Z;
  Ashley's acceptance, event
  `1426b5ec5f0bb8bc571322b44e9cbce025fee3d4eb70997ff7677e602316c62a`, 2026-08-29T14:58:22Z;
  Engineering Coordinator's recorded ruling, event
  `7b26ab2c4447e9f203f165698e87cc4c936c5f61c6d0b67985e9d61ef53fe495`, 2026-08-29T14:59:53Z.

## Context

Ashley asked, earlier the same session, how to build "maximum parallelism via
sub-agent decomposition" into `AGENTS.md`/`CLAUDE.md`. The Engineering Coordinator had
already proposed the mechanics — an admission test (disjoint files, no
producer/consumer edge, no shared Freeze Point, a named integrator), forbidden zones
(before Phase 1 exits, inside Phase 1, Phases 9/13/14), the parent's obligations
(declare the split before dispatch, land its own fan-out, verify the merged result, not
the slices), and an explicit rejection of redundant-opinion fan-out — but left one
question to Ashley: is declining to parallelise the default that needs no
justification, with fan-out merely *permitted* when the admission test passes, or is
fan-out the default, with a stated reason required to go sequential instead?

## Decision

**Fan-out is the default. Declining it requires a stated reason.** Every work package
now carries either a `decomposition:` block (naming the split and satisfying the
admission test) or a one-line justification for proceeding sequentially instead.

## Alternatives considered

- **Fan-out merely permitted when the admission test passes; sequential is the
  unmarked default.** The lower-friction option — most work packages would need no
  annotation at all. Rejected: it makes parallelisation opportunities invisible by
  default. Nobody reviewing a work package after the fact can tell whether sequential
  execution was a considered choice or simply the path of least resistance, because
  both look identical (silence).
- **Fan-out as the stated default, sequential requires a reason (adopted).** Higher
  annotation cost — every package states something — but the annotation is exactly what
  makes the choice auditable. Pollen's argument, cited by the Coordinator as the
  strongest case for this option: a one-line "why not parallel" costs the author
  almost nothing to write and costs a reviewer everything to reconstruct later if it's
  missing.

## Ratification chain

- **Recommended:** Engineering Coordinator, event `4e262256…f326454` (full id above),
  2026-08-29T14:51:13Z, citing Pollen's auditability argument as the strongest case.
- **Accepted:** Ashley, event `1426b5ec…316c62a` (full id above), 2026-08-29T14:58:22Z —
  "go ahead with [the Engineering Coordinator's] prudent decision... as my accepted
  responses."
- **Recorded as signed:** Engineering Coordinator, event `7b26ab2c…53fe495` (full id
  above), 2026-08-29T14:59:53Z.

## Consequences

- `AGENTS.md`/`CLAUDE.md` need the actual rule text written in: the four-part admission
  test with (a)-(c) pairwise over every pair and (d) once per fan-out; the
  vacuous-disjointness fix (children changing no files are judged on deliverable, and
  two children answering one question is the anti-pattern, not a valid split); the
  parent's three obligations; verify-the-merged-result; and the redundant-fan-out
  anti-pattern. That edit is **WP-7**, dispatched to Honey, `files_allowed_to_change:
  AGENTS.md, CLAUDE.md` — not made by this ADR or this role (outside `docs/`).
- **First live application, dispatched together:** WP-6 (Phase 1 build-order item 1,
  identifier types against ADR-0004) and WP-7 (this rule's own text) — chosen
  specifically because they have disjoint `files_allowed_to_change`, no
  producer/consumer edge, and distinct deliverables, satisfying the admission test this
  ADR just ratified. The Engineering Coordinator named this as deliberate: "the first
  application of the parallelisation rule is writing the parallelisation rule down."
- The admission-test checker itself is explicitly **not** part of WP-7 — it follows once
  a `decomposition:` block exists to check, per the Coordinator's sequencing.
- Reversible by ordinary amendment (not a Freeze Point) if the annotation cost proves
  wrong in practice — no migration mechanism required.
