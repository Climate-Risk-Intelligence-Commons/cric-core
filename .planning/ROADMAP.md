# Roadmap: cric-core

## Overview

cric-core ships in four phases: the package foundation and canonical identifier system are complete (Phase 0); all eight Architecture Freeze Points must be ratified, Pydantic-implemented, and CI-green before any downstream repository can safely build on core (Phase 1, current); once the contract surface is stable, versioned JSON Schema artefacts and backwards-compatibility guarantees give downstream consumers a safe pinning target (Phase 2); and an optional developer-facing validation CLI rounds out the toolchain (Phase 3). Every other CRIC repository is blocked on Phase 1 exit.

## Phases

- [x] **Phase 0: Foundation** — Package scaffolding, CI pipeline, and Freeze Point 1 (identifier system)
- [ ] **Phase 1: Architecture Freeze Points** — All 8 FPs ratified and Pydantic-implemented; Phase 1 exit gate passes
- [ ] **Phase 2: Published Contracts** — Versioned JSON Schema artefacts and backwards-compatibility guarantees for downstream consumers
- [ ] **Phase 3: Developer Tooling** — `cric validate` CLI for local OKF node validation

## Phase Details

### Phase 0: Foundation
**Goal**: Package is importable, CI is green, and Freeze Point 1 (canonical identifier form) is locked — the minimum basis for every downstream CRIC repository
**Depends on**: Nothing (first phase)
**Requirements**: ID-01, ID-02, ID-03, ID-04, ID-05, ID-06, ID-07, CI-01, CI-02, CI-03, CI-04
**Success Criteria** (what must be TRUE):
  1. Package installs cleanly from a wheel in a fresh virtualenv with zero import errors
  2. `parse_id("CRIC:<ns>:<type>:<ulid>")` succeeds; any other form raises `CRICIdentifierError` naming the offending string
  3. `generate_id(namespace, type)` produces a valid, unique, sortable identifier without external coordination
  4. 32 unit tests pass; ruff, mypy --strict, and build all exit 0 on every PR
**Plans**: Complete

### Phase 1: Architecture Freeze Points
**Goal**: All eight Architecture Freeze Points ratified and Pydantic-implemented so that every downstream CRIC repository can build on a typed, stable contract surface — 12 repositories cannot safely extend cric-core until this phase exits
**Depends on**: Phase 0
**Requirements**: KS-01, KS-02, KS-03, KS-04, KS-05, KS-06, REV-01, REV-02, REV-03, REV-04, REV-05, REV-06, OKF-01, OKF-02, OKF-03, OKF-04, OKF-05, OKF-06, TEMP-01, TEMP-02, TEMP-03, TEMP-04, TEMP-05, TEMP-06, PROV-01, PROV-02, PROV-03, PROV-04, PROV-05, PROV-06, REL-01, REL-02, REL-03, REL-04, REL-05, REL-06, AGNT-01, AGNT-02, AGNT-03, AGNT-04, AGNT-05, AGNT-06, TST-01, TST-02, TST-03, TST-04, CI-05, EXIT-01, EXIT-02, EXIT-03
**Success Criteria** (what must be TRUE):
  1. Any Freeze Point model (OKFBase, TemporalWindow, ProvenanceChain, OKFRelationship, KnowledgeState, ReviewDecision, AgentManifest) imports and validates a well-formed document without error
  2. A document with `"knowledge_state": "unknown"` deserialises to `KnowledgeState.unknown` — never `None`, `False`, or an empty string; `bool(doc.knowledge_state)` is not `False`
  3. A `ProvenanceChain` with a cycle is rejected at validation time with a typed error; appending to a chain produces a new object that does not share mutable state with the original
  4. The named test `test_phase1_exit_gate` passes: a canonical OKF node fixture validates against all 8 Freeze Point schemas simultaneously
  5. CI exits 0: ruff (zero errors), mypy --strict (zero type errors on `src/cric_core/`), pytest (no skips, no bare `assert True`), build (importable wheel), JSON Schema generation (no stale artefacts in `schema/`)
**Plans**: 7 plans

Plans:
- [ ] 01-01: FP6 + FP7 — KnowledgeState enum (7 values), validate_transition (8 edges), ReviewDecision model (WP-18; unblocks FP3 and FP8)
- [ ] 01-02: FP2 — OKFBase frontmatter Pydantic model with semver field, CRIC-id field, ratification negative test
- [ ] 01-03: FP3 — TemporalWindow + BeliefTimestamp with UTC enforcement and `unknown ≠ false` invariant tested
- [ ] 01-04: FP4 — ProvenanceChain with append-only immutable lineage semantics; cycle detection at validation time
- [ ] 01-05: FP5 — OKFRelationship with closed predicate enum (supports, contradicts, refines, supersedes, cites)
- [ ] 01-06: FP8 — AgentManifest schema with output_types enforcement and compose() incompatibility check
- [ ] 01-07: Phase 1 exit gate — canonical OKF node fixture + JSON Schema generation step for CI (CI-05)

### Phase 2: Published Contracts
**Goal**: Stable versioned JSON Schema artefacts and backwards-compatibility guarantees let downstream repositories safely pin `cric-core` without risk of silent breakage
**Depends on**: Phase 1
**Requirements**: SCH-01, SCH-02, SCH-03, BACK-01, BACK-02, BACK-03
**Success Criteria** (what must be TRUE):
  1. A TypeScript consumer validates a JSON document against the published OKF schema without importing any Python code
  2. A PR that modifies any file under `src/cric_core/` without updating `CHANGELOG.md` is blocked by CI
  3. Every release tag publishes versioned JSON Schema files in GitHub Release assets with `$id` URIs matching the tag and schema name
**Plans**: 2 plans

Plans:
- [ ] 02-01: JSON Schema CI publication — `model_json_schema()` output per FP written to `schema/`; versioned GitHub Release artefacts on tag push
- [ ] 02-02: Backwards-compatibility fixture harness and CHANGELOG enforcement gate

### Phase 3: Developer Tooling
**Goal**: `cric validate` CLI enables domain repository contributors to validate OKF nodes locally without writing Python
**Depends on**: Phase 1
**Requirements**: CLI-01, CLI-02, CLI-03
**Success Criteria** (what must be TRUE):
  1. `cric validate my-fragment.yaml` reports pass/fail with field path, expected type, and actual value — not just "ValidationError"
  2. Exit codes are deterministic: 0 = valid, 1 = invalid, 2 = tool error (file not found, parse failure)
**Plans**: 1 plan

Plans:
- [ ] 03-01: `cric validate` CLI entry point with structured error reporting and deterministic exit codes

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 0. Foundation | —/— | Complete | 2026-08-29 |
| 1. Architecture Freeze Points | 0/7 | Not started | - |
| 2. Published Contracts | 0/2 | Not started | - |
| 3. Developer Tooling | 0/1 | Not started | - |
