# CRIC — Project Facts

Maintained by the Memory & Knowledge Manager. This is a living index of facts, not a
duplicate of the PRD — where a fact is fully specified in `docs/CRIC-PRD-v0.1/`, this
file points there rather than restating it, per that folder's own authority precedence
(`CRIC-PRD-MASTER.md` §Implementation Authority: released `cric-core` contracts >
`CRIC-Schema-and-Vocabulary-Registry.md` > `CRIC-PRD-MASTER.md` > specialised docs >
examples).

## Purpose

Open-source, provenance-preserving, temporally aware knowledge/data/modelling/agentic
infrastructure for climate-risk evidence — built so humans, deterministic software, and
agents operate on the same inspectable evidence base. First domain: Cryosphere/GLOF.
Source: `docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md`.

## Repository and channel

- **Channel:** CRIC-Dev (`17bd72a0-4d90-4e0b-b102-f9163f0cfd4b`)
- **Repo root:** `/home/ash/Eyekyam/CRIC-Core`
- **Remote:** authoritative value is `git remote get-url origin`, or the repo's
  `full_name` from `GET /repos/{owner}/{repo}` — check one of those directly for
  current truth rather than trusting this line, which is a dated observation, not a
  live pointer, and *will* go stale the next time this changes. Last verified:
  `Climate-Risk-Intelligence-Commons/cric-core`, transfer confirmed complete
  2026-08-29T14:08:50Z. The old `ashley-eyekyam/cric-core` URL redirects (GitHub's
  standard post-transfer behaviour, confirmed by the Engineering Coordinator, not
  merely expected). Org-owned, public, default branch `main`, branch protection
  survived the move unchanged and enforcement was re-verified against the new URL.
  Full decision history: `decisions/0002-defer-github-organisation.md` (superseded)
  and `decisions/0003-create-github-organisation.md` (current — including the still-open
  item, whether repo creation works *inside* the org, proven by the first real Phase 0
  repository rather than a throwaway test).
- **Default branch:** `main`, AGPL-3.0 (repo-creation-time choice for `cric-core`
  specifically — see D2 in `OPEN_QUESTIONS.md` for whether this generalises to every
  repository in the family)

## Planned repository family (per `CRIC-Repository-Dependency-and-Implementation-Sequence.md`)

`cric-core, cric-knowledge, cric-data, cric-ingest, cric-cryosphere, cric-glof,
cric-models, cric-agents, cric-review, cric-api, cric-ui, cric-docs` — 12 repositories,
`cric-core` first (every other repository consumes its contracts). None except
`cric-core` exist yet as of 2026-08-29; Phase 0 creates the rest, blocked on D1/D2.

## Process stack (ruled by the Engineering Coordinator, 2026-08-29)

| Layer | Owner | Scope |
|---|---|---|
| State & sequence | GSD (`.planning/`) | PROJECT/REQUIREMENTS/ROADMAP/STATE, phase status |
| Task shape | CRIC's own Coding-Agent Work Package Rule (YAML) | Binding — no implementation starts without one |
| Per-package craft | superpowers skills | TDD by default, worktrees, debugging, review, verification |
| Accountability | Fizz / Honey / Pollen / Memory & Knowledge Manager / Engineering Coordinator | Decide / implement / verify / record / coordinate |

Codex (`codex-cli 0.146.1`) is an adversarial second opinion (review / challenge /
consult modes) on freeze-point and security-sensitive work packages for v0.1 — not a
primary implementer. Bootstrap entry point is `/gsd-ingest-docs docs/CRIC-PRD-v0.1
--mode new` with an explicit `--manifest` pinning Registry > MASTER > specialised docs
(GSD's own default precedence, `ADR > SPEC > PRD > DOC`, disagrees with CRIC's
Implementation Authority rule and would silently resolve conflicts the wrong way if
left unpinned). Full reasoning: Engineering Coordinator's message, channel event
`feb934eaaaf69b4a3eeeaf46974c9a0dfac043236e4aa33688e8a541d62a706e`, 2026-08-29T13:26:14Z.

## Architecture Freeze Points

8 total, all produced in Phase 1 (`cric-core`): ID format, base OKF frontmatter,
temporal model, provenance model, relationship representation, knowledge-state
vocabulary, review decision schema, agent manifest schema. Per
`CRIC-Repository-Dependency-and-Implementation-Sequence.md`, each "remains possible to
change but requires explicit migration after freeze." Ratification checkpoint: Fizz
assembles and cites the candidate → Pollen does blast-radius verification → Ashley
signs off (`docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` §2). None are
ratified yet — Phase 1 has not started.

## Requirements traceability

`docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md` is the canonical,
already-existing R-001…R-041 matrix (requirement → primary/supporting spec → v0.1
verification test). The Memory & Knowledge Manager keeps its "v0.1 Verification"
column current as each phase produces evidence, rather than maintaining a duplicate
matrix elsewhere. R-041 is currently marked "PROPOSED — pending Ashley's decision, not
yet ratified" in that file; tracked as an open item until Ashley rules on it.

## Documentation conventions for this repo

- ADRs live in `decisions/` (not `docs/adr/`) — see `decisions/0001-adr-location.md`.
- `docs/DECISION_REGISTER.md` indexes all ADRs.
- `docs/OPEN_QUESTIONS.md` tracks D/U items with owner, blocks, raised/resolved dates.
- `docs/LESSONS.md` captures recurring defects and reusable patterns.
- `docs/PHASE_EXIT_LOG.md` (created once Phase 0/1 produce exit evidence) will hold the
  durable record of each phase's exit criterion and the evidence that satisfied it.
- **Recording a fact about live external state (a remote URL, a branch's protection
  config, an org's settings — anything that can change out from under this file)**:
  classify it when it's written, not later — the moment you know whether re-derivation
  is cheap is the moment you've just done it.
  - **Cheap and deterministic to re-derive** (one command or API call): record the
    authoritative source plus a dated observation, never an embargo instruction. E.g.
    `authoritative: git remote get-url origin; currently
    Climate-Risk-Intelligence-Commons/cric-core (verified 2026-08-29T14:08Z)`. A
    pointer to where truth lives cannot go stale the way "don't treat X as live until
    confirmed" can — that construction is stale the instant confirmation happens, and
    goes stale *silently*, because nothing re-reads it. (This is exactly what happened
    to this file's own Remote field between authoring and merge on 2026-08-29 — see
    `docs/LESSONS.md`.)
  - **Expensive or judgment-based** (a human decision, an external party, real work to
    establish): record value, date, owner, **and a trigger that names an event a
    person performs** — not a review cadence, and not an absence or a deadline either.
    "Re-check when Phase 0 creates the first additional repository" fires by itself,
    because someone is necessarily present when it happens. "Re-check if the transfer
    hasn't completed by Friday" or "revisit if no one has claimed this in a month" have
    nobody present when they fire — nothing happens, so nothing notices — and are the
    same failure as "owner: Coordinator, review periodically" wearing a date. **If the
    honest trigger for a fact is an absence or a deadline rather than a performed
    event, the fact does not belong in this file.** It belongs in
    `docs/OPEN_QUESTIONS.md` with an owner, where chasing it on no particular schedule
    is that owner's actual job — that is the boundary between the two files: this one
    holds facts with performed-event triggers, `OPEN_QUESTIONS.md` holds the ones whose
    trigger is an absence.
- **Citing an ADR alongside a PRD section that reality has overtaken** (e.g.
  `decisions/0003-create-github-organisation.md` recording that
  `product/Repository-and-System-Architecture.md:137`'s org-layout illustration is now
  descriptive, not aspirational): the citation is the right fix below a threshold, and
  a tax on readability above it. **A PRD section earns a consolidated amendment pass —
  folding the accumulated annotations back into the source — when understanding
  current state requires opening a second document.** Test it by deletion, not by
  status label: remove the superseded ADR from your reading; if you still understand
  the current position, the chain counts as **one**; if you don't, it counts as
  **two**, regardless of what the status lines say. Counting *live* citations (this
  rule's own first draft, corrected before it ever merged) is the wrong proxy: status
  is metadata anyone can attach, and it lets a superseding ADR
  that says only "supersedes ADR-000N" without restating the substance sit at "one
  live citation" forever while a reader still has to open both documents to understand
  anything — exactly the decay this rule exists to prevent. The deletion test measures
  what actually matters, reader burden, directly.
  - Verified against the present case, not asserted: `decisions/0003`'s Consequences
    section states the aspirational→descriptive move and the casing guidance directly;
    delete `decisions/0002` from the reading and you still know where the repositories
    live and which casing to use. `Repository-and-System-Architecture.md:137` passes
    the test at one, so today's ruling (no PRD edit, ADR-0003 sufficient) doesn't
    contradict itself.
  - Below the threshold: annotate — cite the ADR alongside the PRD section, don't edit
    the PRD.
  - At or above it: writing the citation that fails the deletion test is itself the
    performed event that trips the trigger — whoever writes it is present and can see
    it happen. That ADR's author flags the section for a consolidation pass rather
    than annotating past it.
  - **A backstop trigger, also a performed event, not a deadline:** Phase 14 is the
    v0.1 release gate, where the Definition of Done requires an external researcher to
    walk the whole chain from a clean clone — a PRD that needs an ADR chain read
    alongside it to be understood fails that bar on its own terms. So Phase 14 is when
    all accumulated annotations get folded back into the source, regardless of whether
    any single section crossed the threshold on its own.
  - **Quality bar this gives supersession, now load-bearing rather than just good
    style:** a superseding ADR should be self-contained on the point it supersedes —
    state the current substance directly rather than only "supersedes ADR-000N" — so
    the chain a reader must open stays at one. `decisions/0003` already does this; hold
    future superseding ADRs to the same bar.
