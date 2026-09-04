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
`cric-core` exist yet as of 2026-08-29; Phase 0 creates the rest. Not blocked on a
decision anymore — D1 (org) and D2 (licence) are both Resolved in
`docs/OPEN_QUESTIONS.md` — just not yet dispatched.

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
signs off (`docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` §2).
**Freeze Point 1 (ID format) is ratified and locked** — `decisions/0004-freeze-point-1-identifier-format.md`,
approver Ashley, 2026-08-29. WP-6 (build-order item 1, identifier types), against the
locked grammar, is **merged** — `main` at `fda79b1` (PR #17): `src/cric_core/identifiers/`,
31 tests. Freeze Point 1 is now executable code, not only a locked grammar.

**Freeze Points 6 and 7 (knowledge-state vocabulary; review decision schema) are
ratified and locked as one unit** — `decisions/0007-freeze-points-6-7-knowledge-state-review-decision.md`,
approver Ashley, 2026-09-03. Not yet implemented; Honey's WP-18 (build-order item 2,
knowledge-state models) is the first code against them. Freeze Point 4 (provenance
model) briefly looked coupled into this ratification and was found not to be — it
remains separate and unratified.

**5 of 8 Freeze Points remain unratified:** 2 (base OKF frontmatter), 3 (temporal
model), 4 (provenance model), 5 (relationship representation), 8 (agent manifest
schema).

## cric-core: package and CI (WP-4, waves 1–2)

`cric-core` is a real, installable, versioned Python package as of 2026-08-29 (PR #13,
merged to `main` at `a41306d`): version `0.1.0`, declared in both `pyproject.toml` and
`src/cric_core/__init__.py`, kept in sync by a version-drift test proven to fail in
both directions (edit either file alone → red; revert → green). Build via
`python -m build` (`hatchling` backend, build-time only — not a runtime dependency).
Tests via `pytest`; either bare `pytest` or `python -m pytest` work from a cold shell,
because `[tool.pytest.ini_options]` sets `pythonpath = ["src"]` explicitly — not
because of `-m`'s cwd-insertion behaviour, which was this file's sibling `CLAUDE.md`'s
original (now corrected) reasoning. Zero runtime dependencies beyond the package
itself, confirmed via `pip list` in a clean venv.

CI (PR #14, merged to `main` at `e2867de`) runs on every push and pull request via
GitHub Actions: lint (`ruff`), type check (`mypy`), `python -m pytest`, `python -m
build`. All four confirmed non-vacuous — each caught a planted violation (unused
import, bad return type) before the planting was reverted, not just a clean pass
against near-empty source. `.gitignore` covers `dist/`, `build/`, `*.egg-info`,
`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`. Required status
checks on `main` are **enabled** (`contexts: ["test"]`, `strict: true`) — confirmed
live via `gh api repos/.../branches/main/protection`, not narrated from the
Engineering Coordinator's own report of taking the action.

Host-only note, not a project requirement: this machine's harness leaks
`PYTHONHOME`/`PYTHONPATH` into child processes, which breaks bare
`python3`/`pip`/`pytest`/`build` invocations locally (`ModuleNotFoundError: No module
named 'encodings'`) — `env -u PYTHONHOME -u PYTHONPATH` is required locally and is
documented in `CLAUDE.md` §7, not duplicated here. CI runs clean without the unset,
confirmed by PR #14's own green run — the falsification test the Engineering
Coordinator proposed for that exact assumption.

**Test suite size — authoritative source, not a snapshot:** `env -u PYTHONHOME -u
PYTHONPATH python3 -m pytest` at a named commit, with `git rev-parse HEAD` confirmed
equal to that commit in the same shell. A count is ambiguous without its unit stated
alongside it — `grep -c "^def test_"` counts test *functions*; `pytest`'s own summary
line counts collected test *cases*, and the two diverge the moment any function
carries `@pytest.mark.parametrize`. Both "32" and "21" were reported for this suite at
`main` `e8b0b69`..`45141a4` (before PR #29/WP-18 merges) and both were correct, for
different units: 21 test functions (20 in `tests/identifiers/test_identifier.py`, 1 in
`tests/test_version.py`), one of the 20 parametrized, expanding to **32 collected
cases** — the number `pytest` itself reports and CI's required check gates on. Expect
**139** once PR #29 merges (Honey's WP-18, `src/cric_core/knowledge_state/` plus four
test modules) — re-derive at that commit rather than trusting this figure past that
merge.

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
- **Standing job (assigned by the Engineering Coordinator, 2026-08-29, event
  `4e262256…f326454`):** the Memory & Knowledge Manager posts a consolidated decision
  digest to Ashley in this thread, triggered by a performed event, never a clock —
  either Ashley posts in the thread (he's present, hand him the current list), or a new
  Ashley-owned item is registered in `docs/OPEN_QUESTIONS.md` (the list changed, so
  replace it — superseding, not accumulating; one current list at a time). Format:
  **Blocking** (work stopped, who's idle) / **Non-blocking** (proceeding under a stated
  assumption he can overturn) / **Coverage window** stated explicitly (event range
  swept), so a silent gap is detectable rather than invisible. Each item: the question
  in one line, what it blocks, who's waiting, the recommendation and whose it is, and
  the event id it was raised at. **One item, one decision** (Engineering Coordinator's
  process finding, 2026-09-04, event `d63fc31601cc3570156db1d30b29d589fe01542dcb8f3ea2ea2a307083771f92`):
  when a single `docs/OPEN_QUESTIONS.md` row bundles two independently-answerable
  questions, answering one lets the row — and any digest built from it — read as fully
  resolved while the other rides along unaddressed. Split at the source register row
  when this is found, not just in how a given digest phrases it; see `docs/LESSONS.md`
  ("A bundled open-question item let a partial answer read as a full resolution").
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

## Governance and community-health files

Ashley asked for "proper decisions" on licence, README, contributing, code of conduct,
security, governance, CI, branch protection and decision records in one pass (event
`5e4d410b5988dbf69139e7b162262ef6bd4e38a4ce3a01a9c8d43949fd104b6b`,
2026-09-03T10:29:19Z). Status of each, pointing at the authoritative record rather than
restating it:

| Area | File(s) | Status | Record |
|---|---|---|---|
| Licence | `LICENSE` | AGPL-3.0, decided, applied | D2, `docs/OPEN_QUESTIONS.md` |
| README | `README.md` | Dual-audience rebuild dispatched (Fizz, WP-23a) | this thread |
| Contributing / Governance | `CONTRIBUTING.md`, `GOVERNANCE.md` | Root pointer files to existing PRD specs (Honey, WP-19) | `docs/OPEN_QUESTIONS.md` |
| Code of Conduct | `CODE_OF_CONDUCT.md` | Contributor Covenant v2.1 verbatim; **blocked on enforcement contact** | D8, `docs/OPEN_QUESTIONS.md` |
| Security | `SECURITY.md` | Private Vulnerability Reporting, live, stated unconditionally (Honey, WP-19a) | `docs/OPEN_QUESTIONS.md` |
| CI | `.github/workflows/ci.yml` | ruff → mypy → pytest → build; `test` required check; **no job added without an existing subject to examine** | ADR-0008 |
| Branch protection | GitHub repo settings | Strict mode + `enforce_admins`, unchanged; stated exit condition if a batch stalls badly | D3, `docs/OPEN_QUESTIONS.md` |
| Decision records | `decisions/`, `docs/DECISION_REGISTER.md` | Established convention, unchanged | `decisions/0001` |
| Build status (README) | — | **CI-generated, not hand-typed** — mechanism dispatched to Honey (WP-24), after WP-18 | ADR-0008 |
