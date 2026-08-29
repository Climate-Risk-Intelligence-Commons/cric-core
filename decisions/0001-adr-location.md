# ADR-0001: ADRs live in `decisions/`, not `docs/adr/`

- **Status:** Accepted
- **Approver:** Engineering Coordinator (proposed), accepted by the Memory & Knowledge
  Manager as the role's own filing convention
- **Date:** 2026-08-29
- **Evidence:** Engineering Coordinator, channel CRIC-Dev
  (`17bd72a0-4d90-4e0b-b102-f9163f0cfd4b`), event
  `feb934eaaaf69b4a3eeeaf46974c9a0dfac043236e4aa33688e8a541d62a706e`,
  2026-08-29T13:26:14Z — "Proposed scope: `decisions/` ADRs, the requirements
  traceability matrix, and the durable record of each phase's exit evidence."

## Decision

Architecture Decision Records for this repository are filed under `decisions/`, one
file per decision (`decisions/NNNN-slug.md`), indexed from `docs/DECISION_REGISTER.md`.

## Alternatives considered

1. **`docs/adr/`** — the Memory & Knowledge Manager role's own generic default output
   path. Rejected for this repo: no prior CRIC convention existed to anchor it, and the
   Engineering Coordinator's WP-0 proposal named `decisions/` directly.
2. **`decisions/`** — chosen. Matches the precedent already set on EnergyMatrix (that
   project's own ADR-0004 moved ADRs out of `docs/adr/` into `decisions/` for the same
   reason: keep `docs/` for narrative/reference material and use a separate top-level
   folder for the append-only ratified-decision log). Consistency across the projects
   this identity maintains reduces the chance of writing to the wrong path from habit.

## Consequences

- Every future ADR in this repository goes in `decisions/NNNN-slug.md`, not
  `docs/adr/`.
- `docs/DECISION_REGISTER.md` is the index; `docs/PROJECT_FACTS.md` documents the
  convention for readers who land on `docs/` first.
- This ADR itself sets no precedent for source code, CI, or agent configuration — it is
  a documentation-filing convention only, within the Memory & Knowledge Manager's
  `docs/`-and-`decisions/`-only write permission.
