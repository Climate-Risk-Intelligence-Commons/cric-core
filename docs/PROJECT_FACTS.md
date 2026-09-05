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
**A bootstrap run's output is not build-ready on its own** — `decisions/0009-fp-requirement-verification.md`
requires every requirement naming a Freeze Point to resolve against shipped
code, a signed ADR, or be marked an unratified proposal, before anyone builds from it.
Current status of the one run that's happened: `docs/OPEN_QUESTIONS.md` D6.

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
approver Ashley, 2026-09-03. **Implemented** — Honey's WP-18 (build-order item 2,
knowledge-state models), PR #29, merged to `main` `f5d8a06` (2026-09-04):
`src/cric_core/knowledge_state/`, verified against the ADR decision-by-decision and
attacked by planted violation on all four highest-risk criteria (Pollen), full suite
re-verified 139 passed. Freeze Point 1 and Freeze Points 6+7 are now both executable,
tested code — two of the now-six ratified Freeze Points implemented (see below;
Freeze Points 3, 4 and 5 ratified 2026-09-05, no shipped code yet). Freeze Point 4
(provenance model) briefly looked coupled into the FP6+7 ratification and was found
not to be — it ratified separately as ADR-0011, below.

**Freeze Point 7 gained a second piece of shipped code, 2026-09-05: Honey's WP-32
(build-order item 9, registry §10), PR #38, merged to `main` `72f3fb7`** —
`src/cric_core/review/__init__.py`: `ReviewQueueState` (9 values) and
`ReviewDecisionValue` (6 values), same `StrEnum`+`.parse()`-raises idiom as
`knowledge_state/`, byte-exact on §10's deliberately-mixed hyphen/underscore forms
(tested explicitly against normalisation), no ratified decision→knowledge_state
mapping built (none exists in ADR-0007 or registry §10 — building one would have
invented Freeze Point content). **Shipped as propagation of ADR-0007, not a new
signature** — the Coordinator's own ruling, stated so it is overturnable rather than
assumed: ADR-0007 ratified FP7 without enumerating either vocabulary, so transcribing
§10's own unhedged "Canonical Review States"/"Canonical `ReviewDecision.decision`
values" is the ADR-0006 precedent (propagation), not an amendment (contrast §8's
hedged "include"/"may include" for predicates, which is why FP5 needed a closure
decision — ADR-0010, below — and this didn't). Non-author-reviewed per this package's
own requirement (Pollen, clean pass). Full local gate at merge: `ruff`/`mypy` clean,
bare `pytest` **166 passed** (139 existing + 27 new), `rev-parse` unchanged
before/after.

**Freeze Point 5 (relationship representation) is ratified and locked** —
`decisions/0010-freeze-point-5-relationship-representation.md`, ruled by the
Engineering Coordinator 2026-09-05, signed by Ashley 2026-09-05 (blanket approval,
event `524472fa44b27d8f732d4033e444891120a5b7f155bef69e4ab21a19738482a3`, 13:38:43Z,
covering D18/D21/D22 together — see `docs/OPEN_QUESTIONS.md` D18). Predicate
vocabulary closed at exactly 35 (registry §8's 11 core + 23 spatial/domain + 1
structural, excluding the two deprecated predicates and one rejected predicate);
direction representation ratified as `out_edges`/`in_edges` traversal indices, named
inverse pairs treated as an authoring convenience rather than a requirement. Two
consequences ship with the ruling: `affected` becomes invalid, `impacted` canonical
(propagation of registry §8:223, same shape as ADR-0006); and
`Cryosphere-Ontology.md`'s existing `associated_with`/`connected_to` usage becomes
non-conformant on day one, needing an owner (`docs/OPEN_QUESTIONS.md` D20). **Carved
out, not ratified:** the relationship entry schema's `evidence` field —
`Core-Ontology-Specification.md:440` requires it, no field of that name exists on the
schema, and `evidence_nodes` is Claim-schema-only corpus-wide — tracked as D19.

**Freeze Point 4 (provenance model) is ratified and locked** —
`decisions/0011-freeze-point-4-provenance-model.md`, ruled by the Engineering
Coordinator 2026-09-05, signed by Ashley 2026-09-05 (blanket approval, event
`524472fa44b27d8f732d4033e444891120a5b7f155bef69e4ab21a19738482a3`, 13:38:43Z,
covering D18/D21/D22 together — see `docs/OPEN_QUESTIONS.md` D21). Ratified: the
promotion rule (standalone `ProvenanceRecord` on meeting
`Core-Ontology-Specification.md:54-58`'s field-vs-node trigger); the record's full
shape when promoted; "significant" (§9's backward-traversal MUST) means a non-empty
`parents` list, chosen over the alternative because `Source` — both a promoted §3
type and the corpus's own lineage root with nothing upstream by design — makes the
alternative vacuous or unsatisfiable with no stated exception; and a conditional
source-hash rule (dereference the `Asset` when `source.node_ids` is populated, hash
required on the record itself when only `source.uris` is populated, matching `:129`'s
externally-changing-URL scenario). **Excluded from the signature:** the
embedded-baseline field count. The nine-flat-field `provenance:` block comes entirely
from the OKF Universal Frontmatter, one side of D10's still-unresolved three-way
disagreement about FP2's own subject — folding it into FP4 would have resolved an FP2
question as a side effect of ratifying FP4. Tracked at D10, not settled here.
**Consequence stated explicitly, correcting the Coordinator's own earlier framing to
Ashley:** Phase 3's gate is FP4 *and* FP2 (D10), not FP4 alone — FP4 unblocks the
standalone node and promotion logic but does not settle what a `DataAsset`'s own
embedded `provenance` field contains.

**Freeze Point 3 (temporal model) is ratified and locked** —
`decisions/0012-freeze-point-3-temporal-model.md`, ruled by the Engineering
Coordinator 2026-09-05, signed by Ashley 2026-09-05 (blanket approval, event
`524472fa44b27d8f732d4033e444891120a5b7f155bef69e4ab21a19738482a3`, 13:38:43Z,
covering D18/D21/D22 together — see `docs/OPEN_QUESTIONS.md` D22). Ratified:
`false`/`absent`/`not detected` are excluded from both registry
§5 and §6 — a well-supported negative (two independent whole-corpus sweeps, zero
hits, plus `:365`'s positive prohibition on collapsing `unknown` into `false`); and
registry §6's unqualified "negative training labels" scope governs over
Training-Data's narrower "confirmed negatives" restatement (specialised document
loses to rank-1 registry on precedence). **Declined, not ratified:** whether those
three tokens belong on `Observation.value` — unconstrained by omission, not
affirmatively supported (the corpus states no type for `Observation.value` at all), so
a Freeze Point may not rest on "nothing forbids it." Stays open — D23. **Excluded from
the signature:** "no known evidence" as a new value on `Evidence`/`Claim` — invention,
not transcription, `Evidence` has no such extension point today. Also tracked at D23.
**D13 (intra-registry `unknown`/`disputed` collision) carried as established
precedent** — the field path determines the vocabulary, the same ruling that already
settled `epistemic.status` versus `knowledge_state.status` — not re-attacked, stays a
recorded question. **Named explicitly as a third level of citation discipline, worth
keeping as a standing check** (found attacking this candidate): does the citation
resolve → does its label match the cited body → does the cited document's own
supporting claim hold up against the text it describes.

**Pattern named across this round, worth its own entry in `docs/LESSONS.md`:**
"absence of prohibition read as presence of support" appeared three times in one day
— FP4's original field-count claim (borrowed from a disputed source with nothing
saying it didn't apply), FP3's original `Observation.value` placement (an untyped
field with nothing saying it was closed), and this morning's `derived_from` inference
that wrongly closed carve-out #4. All three caught, none by the author alone.

**FP2 has an unresolved internal disagreement, found 2026-09-04 (WP-28, Fizz/Pollen/Engineering
Coordinator) and not yet a dispatched work package.** FP2's entire subject is "which
fields every canonical object carries." **Three** documents purport to declare that,
and they disagree. `Core-Ontology-Specification.md`'s `# CRICObject` lists 13 fields;
`OKF-Knowledge-Graph-Specification.md`'s `# Universal Frontmatter` YAML lists 16 keys.
Arithmetic closes exactly (independently re-derived by both Pollen and the Coordinator,
`main` `f5d8a06`): `CRICObject`'s `schema_version` splits into `cric_schema_version` +
`okf_version` (net +1), and `spatial` + `epistemic` are wholly absent from `CRICObject`
(net +2) — 13 − 1 + 2 = 16. Neither list is a miscount of the other; they are two
genuinely different canonical declarations. **A third surfaced testing ADR-0009**
(2026-09-04, found by the Coordinator, attacked and confirmed by Pollen same day):
`.planning/REQUIREMENTS.md`'s `OKF-01` (rescue ref `74ac966`) lists 6 mandatory header
fields, of which only 2 (`id`, `knowledge_state`) match the 12 the other two
declarations agree on — `source_type` is invented outright (zero occurrences
corpus-wide), `content_hash` is a real field (`content_sha256`, doubly attested,
nested under `provenance:`) renamed and relocated, and the ten remaining shared
fields are simply absent. Full mechanism and citations: `docs/OPEN_QUESTIONS.md` D10.
Separately, the same WP-28 round settled
where `Claim`'s epistemic field lives: `epistemic.status`, nested, populated from the
unanimous eight-value vocabulary (citation-accuracy grounds — two of three flat
`epistemic_status` instances misquote their own cited source; ADR-0007's `modified_values`
exclusion does not reach it, checked directly against `decisions/0007:63`'s stated
scope, so **FP6 stays locked, untouched**). `epistemic`'s *content* (its vocabulary,
its relationship to `knowledge_state`) is named by no freeze point in the current
8-item list — not FP2 (structure ≠ content, same reasoning that made `knowledge_state`
need its own FP6 despite living in FP2's frontmatter block), not FP3 (`Sequence.md`'s
own FP3 line is three words, "temporal model," no "epistemic"). Blocks build-order item
6 (`CRICObject` base hierarchy) once picked up — not yet dispatched as a work package;
the Coordinator is deliberately taking time on the routing rather than ruling quickly,
having withdrawn one same-day routing ruling already (FP2, in favour of Pollen's "gap,
not a choice" finding). New open item, not ratified, not attacked: whether
`modified_values` should also exclude `epistemic.status` on policy grounds separate
from ADR-0007's own stated scope.

## Phase 1 build-order position

Per `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md:49`,
Phase 1 (`cric-core`)'s exit criterion is, verbatim: "Exit criterion: canonical example
OKF nodes validate." The same file's build order (`:37`–`:47`) lists exactly **11**
items: 1 identifier types; 2 knowledge-state models; 3 temporal models; 4 spatial
models; 5 provenance; 6 base object hierarchy; 7 relationship model; 8 ontology
registry; 9 review contracts; 10 validation framework; 11 JSON Schema export.

Items 1–2 are shipped: `src/cric_core/identifiers/` (WP-6, PR #17, `main` `fda79b1`)
and `src/cric_core/knowledge_state/` (WP-18, PR #29, `main` `f5d8a06`) — both already
covered in Architecture Freeze Points above. Confirmed live in this worktree at its
citation pin, `fa22597`: `ls src/cric_core/` shows both directories present with real
content, not stubs — `identifiers/__init__.py` (3737 bytes) and
`knowledge_state/__init__.py` (12794 bytes). **Item 9 has since shipped too — caught
stale by Honey's PR #39 review, not by this pass:** this branch was rebased onto
`origin/main` `72f3fb7` after this prose was drafted (to avoid conflicts) without the
prose being updated to match, and `72f3fb7` includes PR #38 (WP-32,
`src/cric_core/review/`, review contracts) merged before that rebase point. **Items
3–8 and 10–11 are open** — no package code exists yet for temporal models, spatial
models, provenance, base object hierarchy, relationship model, ontology registry,
validation framework, or JSON Schema export.

**Test suite, re-verified live for this fact, 2026-09-05:** `git rev-parse HEAD`
before and after the run both returned `fa22597c24ccf96a2b5c644669239e1c651050d5`
(nothing moved under it mid-run). `env -u PYTHONHOME -u PYTHONPATH python3 -m pytest`
at that commit reports, in pytest's own summary line, "139 passed in 0.31s" — the
collected-*case* unit this file's own "Test suite size" note above documents (not the
`grep -c "^def test_"` test-*function* count, a different unit). This matches the
"139" already on record at `main` `a3e88a1` (2026-09-04): no test-affecting merge
landed between `a3e88a1` and `fa22597`.

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

**Pydantic mandate vs. current implementation (verified 2026-09-05):**
`docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md:14` states, verbatim under
§1 Canonical Naming Rules: "Runtime schema authority: **Pydantic**." Corpus-wide, **18**
documents under `docs/CRIC-PRD-v0.1/` mention Pydantic (`grep -ril pydantic
docs/CRIC-PRD-v0.1/ | wc -l` → 18, this pass). `pyproject.toml` currently has no
`[project.dependencies]` table at all — not merely an empty one, the runtime-dependency
section doesn't exist yet — only `[project.optional-dependencies] dev`. Both shipped
build-order items are stdlib-only, confirmed by reading their imports:
`identifiers/__init__.py` imports only `re` and `dataclasses` (plus
`__future__.annotations`); `knowledge_state/__init__.py` imports only
`collections.abc`, `dataclasses`, `enum`, and `typing`. **Build-order item 6 (base
object hierarchy, `CRICObject`) is where this changes** — that is the first build-order
item that needs a schema runtime under the Registry's own naming rule. This is
propagation of a rank-1 registry instruction already made (Registry > MASTER >
specialised docs — this file's own precedence note, top), not a new architecture
choice up for debate.

CI (PR #14, merged to `main` at `e2867de`) runs on every push and pull request via
GitHub Actions: lint (`ruff`), type check (`mypy`), `python -m pytest`, `python -m
build`. All four confirmed non-vacuous — each caught a planted violation (unused
import, bad return type) before the planting was reverted, not just a clean pass
against near-empty source. `.gitignore` covers `dist/`, `build/`, `*.egg-info`,
`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`. Required status
checks on `main` are **enabled** (`contexts: ["test"]`, `strict: true`) — confirmed
live via `gh api repos/.../branches/main/protection`, not narrated from the
Engineering Coordinator's own report of taking the action.

`[project.optional-dependencies] dev` (PR #31, WP-26/27, Honey): `ruff` and `mypy` are
**pinned exact** (`ruff==0.16.6`, `mypy==2.3.1`, read from a green CI log, not off
PATH) so the required check can't go red from an unrelated upstream release; `pytest`
and `build` stay unpinned deliberately (the Coordinator's reasoning, not re-litigated
here). The risk this closes was live, not hypothetical: `main`'s last CI before the
pin resolved `ruff-0.16.5`; a fresh unpinned venv nine hours later resolved
`ruff-0.16.6` — a second PyPI release inside the same window the fix was being built
in. Local dev environment: `.venv/` (gitignored), `python3 -m venv .venv && .venv/bin/pip
install -e ".[dev]"` documented in `CLAUDE.md` §7. A pre-existing `uv`-created `.venv/`
with no `pip`/`ruff`/`mypy` installed was found and is not the one to use if it
resurfaces — self-ignores via its own `.venv/.gitignore`, invisible to `git status`.

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
`tests/test_version.py`), one of the 20 parametrized, expanding to 32 collected cases —
the number `pytest` itself reports and CI's required check gates on. **139 as of
2026-09-04, `main` `a3e88a1`** (PR #29/WP-18 merged — `src/cric_core/knowledge_state/`
plus four test modules — followed by four more merges the same session that added no
tests: #31 linter pinning, #32 docs, #28 README, #25 CoC), re-verified directly in this
pass, `rev-parse` confirmed. **166 as of 2026-09-05, `main` `72f3fb7`** (PR #38/WP-32
merged — `src/cric_core/review/` plus its test modules, 27 new; no test-affecting
merge between `a3e88a1` and here). Verified twice, independently, the same day:
Honey's own gate on the PR branch, and separately the Engineering Coordinator's
clean-clone install-and-test run of the merged README instructions — his **first**
attempt, against the local checkout at a stale ref rather than a fresh clone of the
public repo, wrongly reported 32 and was caught and corrected before being reported
here (see `docs/LESSONS.md`). Re-derive at whatever commit is current rather than
trusting this figure forward past the next test-affecting merge.

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
| README | `README.md` | Dual-audience rebuild (Fizz, WP-23a), contact filled (D8) — merged to `main`, PR #28. **WP-33's restructure landed, PR #42, `main` `1945c2a`**: hand-written module list retired for a CI-generated `<!-- BUILD-STATUS:START/END -->` block, `contributes to`→`refines` predicate fix applied, heading renamed to "Build status" (not the Coordinator's "keep 'What exists today'" recommendation — D16's own row flags this as unconfirmed whether deliberate or overlooked, not asserted either way). Separately, D17 (funder-class naming in the existing contributor table) resolved as stands-as-shipped. | this thread, D16, D17 |
| Contributing / Governance | `CONTRIBUTING.md`, `GOVERNANCE.md` | Root pointer files to existing PRD specs (Honey, WP-19) | `docs/OPEN_QUESTIONS.md` |
| Code of Conduct | `CODE_OF_CONDUCT.md` | Contributor Covenant v2.1 verbatim; enforcement contact resolved 2026-09-04 (D8) — both addresses, per the Coordinator's ruling — merged to `main`, PR #25 (Honey, WP-19c) | D8, `docs/OPEN_QUESTIONS.md` |
| Security | `SECURITY.md` | Private Vulnerability Reporting, live, stated unconditionally (Honey, WP-19a) | `docs/OPEN_QUESTIONS.md` |
| CI | `.github/workflows/ci.yml` | ruff → mypy → pytest → build; `test` required check; **no job added without an existing subject to examine**. **Build-status freshness check added, PR #42** (`generate_build_status.py --check`, in the `test` job after Test, before Build). **Hazard found and fixed in the same PR, not left open:** the generator's first cut derived "N of 8 Freeze Points ratified" by mechanically matching the substring "Architecture Freeze Point" in a `decisions/` Status line — which would have counted `decisions/0010`'s pre-signature "Proposed — Architecture Freeze Point candidate… not yet signed" as ratified (the Coordinator caught this reviewing PR #40). Fixed to require the Status line's value be literally `Accepted` **and** contain "Architecture Freeze Point" — a positive-marker check, not a phrase future ADR authors have to write around. | ADR-0008 |
| Branch protection | GitHub repo settings | Strict mode + `enforce_admins`, unchanged; stated exit condition if a batch stalls badly | D3, `docs/OPEN_QUESTIONS.md` |
| Decision records | `decisions/`, `docs/DECISION_REGISTER.md` | Established convention, unchanged | `decisions/0001` |
| Build status (README) | — | **CI-generated, not hand-typed** — mechanism built as **WP-33** (children 33a generator/CI, 33b README restructure). **Numbering correction, 2026-09-05:** ADR-0008's text named this "Honey's WP-24," a discrepancy this file flagged as unreconciled in WP-34 (this row's own prior text, superseded here). Ruled by the Coordinator: he re-dispatched the same mechanism under a new number without checking; WP-33 is the identifier that actually ran and shipped, WP-24 its earlier working name. `decisions/0008-ci-generated-build-status.md` corrected to say so in this same records package. **Landed, PR #42, `main` `1945c2a`** — see D16. | ADR-0008, D16 |
