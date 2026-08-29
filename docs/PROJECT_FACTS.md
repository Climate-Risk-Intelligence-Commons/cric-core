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
- **Remote:** `github.com/ashley-eyekyam/cric-core.git` (current — see D1 in
  `OPEN_QUESTIONS.md`; `product/Repository-and-System-Architecture.md` names the
  eventual layout as `github.com/climate-risk-intelligence-commons/`, not yet created)
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
