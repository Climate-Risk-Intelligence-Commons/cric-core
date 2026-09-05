# CRIC — Phase 1 Completion Plan

Maintained by the Memory & Knowledge Manager (drafted by WP-34). Citations below were
verified directly against files at this worktree's HEAD, `fa22597c24ccf96a2b5c644669239e1c651050d5`
(identical to `52ea553` for every file cited here except `README.md`, which this
document does not cite). Re-verify line numbers if citing against a later commit.

This file has two parts, deliberately separated:

- **Part 1** is the standing build order and wave structure. It does not date-rot —
  it describes the sequence and dependency shape of Phase 1's work, not a live count.
- **Part 2** is a dated status snapshot, kept to a single pointer sentence on purpose
  (see that section for why).

---

## Part 1 — Standing build order and wave structure

### 1. Phase 1's 11-item build order

Source: `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md`
("the Sequence document" below). Phase 1's exit criterion, quoted verbatim and
confirmed present at the cited line:

> "Exit criterion: canonical example OKF nodes validate."
> — `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:49`

The build order itself is `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:35-47`.
The document's own Architecture Freeze Points list (the 8 FPs referred to below) is at
`docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:262-275`.

Per **ADR-0009** (`decisions/0009-fp-requirement-verification.md`), any requirement
naming a Freeze Point must resolve to exactly one of three states: (1) shipped code
exists, (2) a signed ADR exists with no code yet, or (3) neither exists, in which case
it is an **unratified proposal**, stated as such, never as a settled requirement. The
table below applies that test to every Freeze-Point-bearing item, verified directly
against `decisions/` (currently `0001`–`0009`, no entry for FP2/3/4/5/8) and
`src/cric_core/` (currently only `identifiers/` and `knowledge_state/`).

| # | Build-order item | Freeze Point (of the 8) | ADR-0009 state | What it needs |
|---|---|---|---|---|
| 1 | identifier types | FP1 — ID format | **Shipped code + signed ADR** | None (first item) |
| 2 | knowledge-state models | FP6 — knowledge-state vocabulary | **Shipped code + signed ADR** | Item 1 (every node needs an ID) |
| 3 | temporal models | FP3 — temporal model | **Unratified proposal** (no ADR, no code) | Items 1–2, sequentially |
| 4 | spatial models | *(none of the 8)* | n/a | Items 1–3, sequentially; externally blocked — see Wave 2 |
| 5 | provenance | FP4 — provenance model | **Unratified proposal** (no ADR, no code) | Items 1–4, sequentially |
| 6 | base object hierarchy | FP2 — base OKF frontmatter | **Unratified proposal** (no ADR, no code) | Items 1–5, sequentially, plus FP2's own internal disagreement resolved (see below) |
| 7 | relationship model | FP5 — relationship representation | **Unratified proposal** (no ADR, no code) | Items 1–6, sequentially |
| 8 | ontology registry | *(none of the 8)* | n/a | Items 1–7, sequentially |
| 9 | review contracts | FP7 — review decision schema | **Signed ADR; partially shipped** (see below) | Items 1–8, sequentially |
| 10 | validation framework | *(none of the 8)* | n/a | Items 1–9, sequentially (needs schemas to validate against) |
| 11 | JSON Schema export | *(none of the 8)* | n/a | Items 1–10, sequentially (exports the finished schemas) |

Detail per Freeze-Point-bearing item, each independently verified:

- **Item 1 / FP1.** Signed ADR: `decisions/0004-freeze-point-1-identifier-format.md`
  (Status "Accepted — Architecture Freeze Point," Approver Ashley, Date 2026-08-29 —
  `decisions/0004-freeze-point-1-identifier-format.md:1-6`). Shipped code:
  `src/cric_core/identifiers/__init__.py` exists, confirmed by directory listing.
  Both states present — resolves cleanly under ADR-0009 branch 1.
- **Item 2 / FP6.** Signed ADR: `decisions/0007-freeze-points-6-7-knowledge-state-review-decision.md`
  (Status "Accepted — Architecture Freeze Points," Approver Ashley, Date 2026-09-03 —
  `decisions/0007-freeze-points-6-7-knowledge-state-review-decision.md:1-7`). Shipped
  code: `src/cric_core/knowledge_state/__init__.py`, whose module docstring states it
  implements "Architecture Freeze Points 6 + 7" (`src/cric_core/knowledge_state/__init__.py:1`).
  Both states present.
- **Item 3 / FP3.** `decisions/` has no `NNNN`-numbered ADR for the temporal model
  (directory listing: `0001`–`0009`, none titled or scoped to FP3), and
  `src/cric_core/` has no temporal module. Per ADR-0009 branch 3, this is an
  **unratified proposal** — any document describing a temporal-model requirement must
  say so, not present it as settled. Currently the subject of in-progress Wave 1 work
  (WP-29; see below) — still unratified until an ADR is signed.
- **Item 5 / FP4.** Same check: no ADR, no code. **Unratified proposal.** In progress
  under WP-29's sibling package WP-30 (see Wave 1). `docs/PROJECT_FACTS.md:91-92`
  records that FP4 was briefly thought coupled into the FP6+7 ratification and was
  found not to be — it remains separately unratified.
- **Item 6 / FP2.** Same check: no ADR, no code. **Unratified proposal.** FP2 also
  carries its own internal defect, independent of ratification timing:
  `docs/PROJECT_FACTS.md:98-114` documents three disagreeing canonical declarations of
  "base OKF frontmatter" field lists (`CRICObject`, 13 fields; `Universal Frontmatter`,
  16 keys; `.planning/REQUIREMENTS.md`'s `OKF-01`, 6 fields with invented/mislocated
  content) — tracked as `docs/OPEN_QUESTIONS.md` D10, not yet dispatched as a work
  package as of this reading (`docs/OPEN_QUESTIONS.md:26`, "Found, not yet dispatched
  as a work package — deliberate, not a stall").
- **Item 7 / FP5.** Same check: no ADR, no code. **Unratified proposal.** In progress
  under WP-31 (see Wave 1).
- **Item 9 / FP7.** Signed ADR: the same `decisions/0007-...` document ratifies FP7
  alongside FP6. Code state is **more nuanced than a clean "no code yet"**: some of
  FP7's ratified content is already shipped inside the FP6 module —
  `REVIEW_DECISION_ENTRY_STATUS`, `REVIEW_DECISION_ALLOWED_ORIGINS`, and
  `validate_review_decision_origin` all exist in
  `src/cric_core/knowledge_state/__init__.py:294-308`, and its docstring's Decision 8
  (`src/cric_core/knowledge_state/__init__.py:36-39`) names this explicitly as
  ratified FP7 content. But build-order item 9 itself — "review contracts" as its own
  deliverable (the fuller `ReviewDecision` schema/dataclass) — has not shipped as a
  distinct module; that is WP-32's current work (see Wave 1). Framed precisely: FP7 is
  ratified (ADR-0009 branch 2 satisfied) with a partial down payment already in branch-1
  territory, and WP-32 completes branch 1 for the item as a whole.
- **Items 4, 8, 10, 11.** None of these four build-order items corresponds to any of
  the 8 Freeze Points listed in the Sequence document
  (`docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:262-275`)
  or in `docs/CRIC-Implementation-Team/Domain-Phase-Mapping.md:76-83`'s per-Freeze-Point
  table — confirmed by checking both lists directly. They carry no Freeze-Point
  verification obligation under ADR-0009.

**Flag for the integrator, not resolved here:** FP8 (agent manifest schema) is listed
as one of the 8 Freeze Points "produced in Phase 1" (`docs/PROJECT_FACTS.md:71-73`;
Sequence document `:262-273`), but none of the 11 build-order items is named "agent
manifest," and `docs/CRIC-Implementation-Team/Domain-Phase-Mapping.md:83` ties FP8 only
to Phase 8 (`cric-agents`) as the phase it gates, not to a Phase 1 build-order item that
produces it. Item 8, "ontology registry," is the closest numeric candidate but nothing
in the corpus states that association. This may be an intentional omission (FP8's
schema might be a byproduct of another item) or a genuine documentation gap — I did not
rule on it, per this package's scope.

### 2. The three-wave structure

#### Wave 1 (in progress as of this writing)

One line each, per current work-package assignment — full dispatch detail lives in
the channel and will land in `docs/DECISION_REGISTER.md`/ADRs once any of these
ratify:

- **WP-29** — FP3 (temporal model) candidate work.
- **WP-30** — FP4 (provenance model) candidate work. Critical path: per
  `docs/CRIC-Implementation-Team/Domain-Phase-Mapping.md:79`, FP4 gates Phases 3
  (`cric-data`), 5, 6, 9, and 10 — including the data layer (Phase 3), confirmed by
  cross-referencing that row against the Sequence document's own Phase 3 header
  (`docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:63`).
- **WP-31** — FP5 (relationship representation) candidate work.
- **WP-32** — build-order item 9 (review contracts). Code, no new Freeze Point to
  ratify — FP7 is already signed (`decisions/0007-...`); this ships the remaining
  `ReviewDecision` deliverable against it (see item 9 detail above).
- **WP-33** — implementation of ADR-0008 (`decisions/0008-ci-generated-build-status.md`):
  CI-generated build status, replacing hand-typed README status content.
- **WP-34** — this package: records (the file you are reading).

#### Wave 2

- **Build-order item 4 (spatial models).** Blocked on a coordinate-reference-system
  (CRS) decision. I searched for a corresponding entry and found **none**: neither
  `docs/OPEN_QUESTIONS.md` nor `decisions/` names a CRS decision, an owner, or a
  tracking ID. The corpus mentions CRS only as a downstream validation/processing
  target — `docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md:93` ("valid CRS"),
  `docs/CRIC-PRD-v0.1/data/Data-Commons-Architecture.md:159` ("CRS transformation"),
  `docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md:116` ("CRS
  conversion") — never as a named, owned open decision. **Flag for the integrator:**
  this block is real (item 4 cannot proceed without a CRS choice) but currently has no
  citable open-question record; it may be worth opening a `docs/OPEN_QUESTIONS.md` D-item
  for it rather than leaving the block undocumented.
- **Build-order item 6 (base object hierarchy).** Unblocks once items 3, 4, and 5 are
  signed (items 3–5 are listed at
  `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:39-41`,
  item 6 immediately after at `:42` — sequential build order, not an independently
  stated cross-dependency beyond the numbering), and separately once FP2's own
  three-way disagreement (D10, above) is reconciled — two independent blockers, not
  one.
- **Pydantic enters here.** `cric-core` currently has **zero runtime
  dependencies** — confirmed via `pip list` in a clean venv per
  `docs/PROJECT_FACTS.md:142-143`. The Schema and Vocabulary Registry names Pydantic as
  the project's runtime schema authority: "Runtime schema authority: **Pydantic**."
  (`docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md:14`, verified directly).
  Items 4 and 6 are the first Phase 1 build-order items that plausibly require actual
  schema modelling (spatial geometry types; the base object hierarchy shared by every
  canonical type) — Wave 2 is where Pydantic is expected to become a real runtime
  dependency of `cric-core` for the first time, not merely a stated intention.

#### Wave 3

- **Build-order items 8, 10, 11** (ontology registry; validation framework; JSON
  Schema export) follow once items 1–7 are in place, per the sequential build order.
- **Canonical example OKF nodes validating** is Phase 1's actual exit criterion,
  quoted and cited at the top of Part 1
  (`docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:49`) —
  it is not itself a numbered build-order item, it is the condition that closes the
  phase once items 1–11 exist.
- **A Data & Geospatial Engineer role, trigger: Wave 3 opening.** I could not verify
  this against the corpus and want to flag it plainly rather than launder it into
  settled content. `docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` is this
  project's own authoritative role-gap analysis, and its explicit restraint principle
  is that "a role only earns creation when a specific named phase or task needs it and
  the four existing generalists... provably don't cover it"
  (`docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md:7-8`). That document
  evaluates three candidate roles and reaches verdicts of Reject / Accept-narrowly /
  Reject for a Freeze-Point-ratification role, a Build & Release Engineer, and a
  Domain/Ontology Specialist respectively
  (`docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md:206-215`) — it does not
  mention a "Data & Geospatial Engineer" anywhere, and a repo-wide search for
  "geospatial" turns up only technical/domain references (geospatial toolsets, tests,
  stack sections), never a role name. **This may be current, not-yet-documented
  planning intent, or it may be stale — I did not resolve which. Carrying it forward
  as an open item for the integrator rather than stating it as fact.**
- **Parallel Workstreams claim, verified.** The Sequence document's own Parallel
  Workstreams section states: "After Phase 1: Knowledge Commons; Data Commons;
  Cryosphere ontology; Agent runtime; review protocol; documentation can progress
  substantially in parallel."
  (`docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:249-260`).
  Cross-referencing those workstream names against the same document's own phase
  headers confirms five of the six map onto numbered phases: Knowledge Commons → Phase
  2 (`:51`, `cric-knowledge`); Data Commons → Phase 3 (`:63`, `cric-data`); Cryosphere
  ontology → Phase 4 (`:77`, `cric-cryosphere`/`cric-glof`); review protocol → Phase 7
  (`:124`, `cric-review`); Agent runtime → Phase 8 (`:136`, `cric-agents`) — i.e.
  **Phases 2, 3, 4, 7, and 8 open in parallel once Phase 1 exits**, confirming the
  claim. "Documentation," the sixth listed workstream, is cross-cutting and does not
  correspond to a numbered phase.

---

## Part 2 — Dated status snapshot

Current build-order position, test count, and commit are tracked in
`docs/PROJECT_FACTS.md` — this file states the durable sequence, not a live count.

(Authored 2026-09-05, against HEAD `fa22597c24ccf96a2b5c644669239e1c651050d5`, purely
to date this document — not as a substitute for `docs/PROJECT_FACTS.md`'s own
authoritative, re-derivable figures.)
