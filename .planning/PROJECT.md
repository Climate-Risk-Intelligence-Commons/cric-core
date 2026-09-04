# CRIC-Core

## What This Is

`cric-core` is the contract root of the Climate Risk Intelligence Commons (CRIC): an open-source, provenance-preserving, temporally aware knowledge/data/model/agent infrastructure for climate-risk evidence. It holds the authoritative 39-document PRD family and the Python package that ships the canonical schemas, identifiers, and base types every other CRIC repository depends on. First operational domain: Himalayan cryosphere / Glacial Lake Outburst Flood (GLOF) risk.

## Core Value

Every claim traces to its source evidence with an auditable derivation chain — no value without provenance, no contradiction silently resolved.

## Requirements

### Validated

- ✓ **Freeze Point 1: Identifier format** — `CRIC:<namespace>:<type>:<ulid>`, strict parse, 12 canonical namespaces, zero case-folding. Ratified ADR-0004 (2026-08-29), implemented in `src/cric_core/identifiers/`, 32 passing tests. — Phase 0
- ✓ **Freeze Points 6 + 7: Knowledge-state vocabulary + Review decision schema** — 7-value knowledge-state vocabulary, 8-edge state-transition envelope. Ratified ADR-0007 (2026-09-03). Schema locked; code not yet written (WP-18). — Phase 0

### Active

<!-- Current Phase 1 scope: produce the remaining Architecture Freeze Points and reach Phase 1 exit. -->

- [ ] **FP6 + FP7 code** — Implement ratified knowledge-state vocabulary and review-decision schema as Pydantic models with full schema test suite (WP-18)
- [ ] **Freeze Point 2: Base OKF frontmatter** — Define and ratify the canonical Open Knowledge Fragment header schema; validate with at least one negative counter-example
- [ ] **Freeze Point 3: Temporal model** — Define and ratify the temporal + epistemic model (observation windows, belief timestamps, `unknown` ≠ `false`)
- [ ] **Freeze Point 4: Provenance model** — Define and ratify the evidence-provenance chain schema
- [ ] **Freeze Point 5: Relationship representation** — Define and ratify the OKF relationship grammar
- [ ] **Freeze Point 8: Agent manifest schema** — Define and ratify the agent dependency/output manifest schema
- [ ] **Phase 1 exit gate** — Canonical example OKF nodes validate against all ratified schemas; CI stays green

### Out of Scope

- **Domain ontologies (cryosphere, GLOF)** — live in `cric-cryosphere` / `cric-glof` (Phase 4); cric-core must not depend on domain repos
- **Data ingestion pipeline** — `cric-ingest` repository, Phase 5; deterministic acquisition and normalisation of external sources is not a cric-core concern
- **Graph materialisation and retrieval** — retrieval engine is Phase 6, initially in `cric-api`; cric-core ships schemas, not query execution
- **Web frontend** — `cric-ui`, Phase 12; TypeScript/React work is out of scope for this repo
- **LangGraph or any mandatory orchestration framework** — explicit PRD decision; agents implement their own loops, no shared orchestration dependency
- **Human-facing short IDs as production identifiers** — `CRIC-LAKE-001` style IDs appear in fixtures only; a second ID format is prohibited by Freeze Point 1

## Context

- **39-document PRD family** in `docs/CRIC-PRD-v0.1/` is the specification baseline. Authority precedence (highest to lowest): released executable contracts → Schema-and-Vocabulary-Registry → PRD-MASTER → specialised PRDs → examples.
- **Phase 0 is complete.** Package scaffolding, CI pipeline (ruff, mypy, pytest, build), and Freeze Point 1 are all green on `main`.
- **Blocking issue D6:** `gsd-ingest-docs` was run without `--manifest` flag on 2026-09-03. `.planning/INGEST-CONFLICTS.md` does not exist. Correct re-run: `gsd-ingest-docs docs/CRIC-PRD-v0.1 --mode new --manifest gsd-ingest-manifest.yaml`. This blocks the next wave of work packages.
- **`.planning/config.json`** sets `mode: yolo` and `auto_advance: true` — these settings remove Freeze Point gates; flagged for human review before any agent relies on them.
- **Dev-host quirk:** prefix `python3`, `pip`, `pytest`, and `build` with `env -u PYTHONHOME -u PYTHONPATH` on this machine. The harness AppImage leaks those variables into venvs. CI runs on clean images and does not need this prefix.
- **Multi-agent workflow:** each work package runs in a separate git worktree at `/home/ash/Eyekyam/.worktrees/cric-core/<branch>`. Never share a working tree between agents.

## Constraints

- **Tech stack:** Python 3.12+ for all package and scientific code; TypeScript for the web frontend (Phase 12 only); Pydantic is the runtime schema authority — no duck-typed contracts
- **Dependency direction:** cric-core is the root; it may import no domain-specific repository; all dependency edges point toward this repo, never away
- **Architecture Freeze Points:** once locked, a change requires explicit migration plan plus Ashley's sign-off; a work package may not silently alter a locked Freeze Point
- **Freeze Point ratification bar:** every candidate must include a stated negative test (a concrete scenario the PRD documents, shown representable under the proposed closure) before sign-off is valid; accuracy alone is not sufficient
- **Branch protection:** `main` is branch-protected with `enforce_admins`; no direct pushes, including from the Coordinator token; every change requires a GitHub PR
- **Security:** CRIC v0.1 is a research and reference implementation; model scores, risk states, and agent outputs must never be presented as official warnings or substitute for institutional warning authority

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Single ID format `CRIC:<ns>:<type>:<ulid>` — no aliases, no second format | Prevents identifier proliferation across 12 repos; ULID provides sortability and uniqueness without coordination | ✓ Good — ADR-0004, shipped as Freeze Point 1 |
| Pydantic as runtime schema authority, not JSON Schema directly | Strict typed contracts catchable at import time; generated JSON Schema published as artefact | — Pending validation at scale |
| No mandatory orchestration framework | Avoids coupling 23 product agents to a single framework's upgrade cycle; agents own their own loops | — Pending — first agent work (Phase 8) will test this |
| 7-value knowledge-state vocabulary (not binary true/false) | `unknown` ≠ `false`; contradiction is data, not an error to resolve | ✓ Good — ADR-0007, ratified with negative test |
| `unknown` and `unobserved` are never auto-converted to negative labels | Constitutional Rule 6; prevents silent false negatives in downstream risk estimates | ✓ Good — locked in registry §6 and Training-Data spec |
| Git worktrees for concurrent multi-agent work | Single checkout collides when multiple agents work in parallel; worktree isolation is the mitigation | ✓ Good — enforced by CLAUDE.md |
| GSD workflow for doc-conflict resolution before work packages | 39 PRDs written by different roles accumulate inter-document conflicts; resolving them up front prevents agents from "picking whichever they read first" | ⚠️ Revisit — D6 shows the process broke on first run; needs verified re-run |

---
*Last updated: 2026-09-04 after repository research (brownfield init, Phase 0 complete)*
