# Project Research Summary

**Project:** cric-core — Climate Risk Intelligence Commons (contract root Python package)
**Domain:** Provenance-preserving, temporally-aware knowledge/data/model/agent infrastructure for climate-risk evidence
**Researched:** 2026-09-04
**Confidence:** HIGH — brownfield project; Phase 0 shipped; research sourced directly from 39-document PRD family, ratified ADRs, and existing codebase

---

## Executive Summary

`cric-core` is the contract root of a multi-repository, multi-agent open-source ecosystem for Himalayan cryosphere and GLOF (glacial lake outburst flood) risk intelligence. The core design philosophy is provenance preservation at every layer: no value enters the graph without a traceable lineage, no observation is silently coerced to a negative label, and no contradiction is erased. Phase 0 has shipped — the canonical identifier system (`CRIC:<ns>:<type>:<ulid>`, 32 passing tests) and CI scaffolding are in place. Phase 1 is the immediate objective: implementing Pydantic models for all eight Architecture Freeze Points so that the 12 downstream repositories can build on a stable, typed contract surface.

The recommended approach is Python 3.12+ with Pydantic v2 as the runtime schema authority. Pydantic models are the source of truth; JSON Schema is generated from them and published as build artefacts for non-Python consumers. The dependency direction is strictly unidirectional — `cric-core` may not import from any domain repository. Two Freeze Points (FP6: knowledge-state vocabulary, FP7: review-decision schema) are already ratified via ADR-0007 and their Pydantic code is the immediate next deliverable (WP-18). The remaining five freeze points (FP2–FP5, FP8) require both ratification and implementation before Phase 1 can exit.

The defining differentiators of this system are: explicit contradiction coexistence (both conflicting claims live in the graph), a 7-value epistemic vocabulary that prevents `unknown` from being silently treated as `false`, and immutable append-only provenance chains. These are not optional properties — they are Constitutional Product Rules (Rules 1, 2, 3, 6) and any implementation that shortcuts them introduces systematic false negatives into downstream risk models. The highest-risk pitfall is precisely this coercion: a Python truthiness check or an ML label encoder that receives a `KnowledgeState` value and silently converts `unknown` to a negative class label.

---

## Key Findings

### Recommended Stack

The stack is largely determined by the brownfield project state and the PRD mandates. Python 3.12+ is non-negotiable; Pydantic v2 (≥2.7) is the mandated runtime schema authority. The build toolchain (`hatchling`, `ruff`, `mypy`, `pytest ≥8`) is already configured and functioning. Three libraries need to be added to `pyproject.toml` dependencies for Phase 1 work to proceed: `pydantic>=2.7`, `python-ulid>=3.0` (for ULID generation — the existing identifier code does regex validation but has no generation library), and `pyyaml>=6.0` (for OKF frontmatter parsing in FP2).

**Core technologies:**
- **Python 3.12+**: Primary language — mandated by PRD; `@override`, `StrEnum` stdlib, faster CPython
- **Pydantic v2 (≥2.7)**: Runtime schema authority — mandated; `model_json_schema()` publishes JSON Schema without a separate step; v2 only (v1 is maintenance-only)
- **python-ulid (≥3.0)**: ULID generation for new `CRIC:<ns>:<type>:<ulid>` identifiers — actively maintained, pure Python, no C build dep
- **pyyaml (≥6.0)**: OKF frontmatter parsing — needed for FP2; `ruamel.yaml` only if comment round-trip is required (it is not)
- **hatchling**: Build backend — already in use, zero-config src-layout support
- **ruff + mypy + pytest ≥8**: Already configured; add `pydantic.mypy` plugin and `pytest-cov` for Phase 1

**Hard excludes:** LangGraph (explicit PRD prohibition — couples 23 agents to a single framework's upgrade cycle), numpy/pandas/scientific stack (belongs in domain repos, not contract root), networkx (graph materialisation is Phase 6 `cric-api`), any second ID format.

### Expected Features

**Must have — Phase 1 (table stakes, blocks all downstream repos):**
- FP1: Canonical identifier system — **done** (ADR-0004, 32 tests green)
- FP2: OKF base frontmatter schema — Pydantic model + schema tests + negative-test ratification
- FP3: Temporal + epistemic model — including `unknown ≠ false` invariant (Constitutional Rule 6)
- FP4: Evidence-provenance chain schema — immutable append-only lineage
- FP5: OKF relationship grammar — canonical predicate vocabulary locked
- FP6: Knowledge-state vocabulary (7-value) — **ratified** ADR-0007; Pydantic code is WP-18 immediate next step
- FP7: Review-decision schema — **ratified** ADR-0007; Pydantic code is WP-18
- FP8: Agent manifest schema — depends on FP6/FP7 types being settled

**Should have — before Phase 4 domain work begins:**
- Published JSON Schema artefacts from CI (low-cost CI step on top of Pydantic; needed before TypeScript frontend work)
- Backwards-compatibility fixtures for every schema (required before domain repos extend core types)
- Semantic versioning + changelog discipline (12 downstream repos will pin cric-core)

**Defer to Phase 3+:**
- OKF validation CLI (`cric validate my-fragment.yaml`) — low priority until domain repos produce real OKF content
- Schema migration tooling — needed post-v1 as FPs evolve
- Cross-repo integration test harness — needed before any stable FP changes

**Anti-features (never build into cric-core):**
- Domain ontologies (dependency direction violation — they belong in `cric-cryosphere`/`cric-glof`)
- Graph query execution (belongs in `cric-api`, Phase 6)
- Second ID format "for convenience"
- Auto-resolving contradictions
- Binary knowledge states (true/false) — the 7-value vocabulary replaces this
- LangGraph as a runtime dependency

### Architecture Approach

`cric-core` is a pure schema/identifier/vocabulary library — it ships no query execution, no UI, no HTTP surface, and no domain ontologies. The internal structure maps one-to-one to the eight Freeze Points (one directory per FP). Each directory contains a `_model.py` (Pydantic field definitions) and, where needed, a `_validators.py` (enforcement logic) — kept separate to prevent circular imports. The dependency direction is strictly unidirectional: `cric-core` is the root; all 12 downstream repositories import from it; it imports from none of them.

**Major components (in Phase 1 delivery order):**
1. `identifiers/` — FP1: CRIC identifier parsing/generation (**done**)
2. `knowledge_state/` — FP6+7: 7-value vocab + review decision schema (ratified, WP-18 code pending)
3. `okf/` — FP2: base OKF frontmatter schema (next after WP-18)
4. `temporal/` — FP3: 4-axis temporal model with `unknown ≠ false` invariant
5. `provenance/` — FP4: evidence-provenance chain, append-only lineage
6. `relationships/` — FP5: typed relationship grammar + canonical predicate registry
7. `agents/` — FP8: agent manifest schema (depends on FP6/FP7)
8. `vocabularies/` — controlled vocabularies shared across all FPs

**Key patterns:**
- Pydantic with `extra="forbid"` everywhere — reject unknown fields at import time, not query time
- `StrEnum` (Python 3.11+ stdlib) for all vocabulary types — avoids `.value` unpacking tax
- `datetime` with `timezone=UTC` always — no naive datetimes; open-ended temporal windows as `tuple[datetime, datetime | None]`
- State-transition graph as `frozenset[tuple[KnowledgeState, KnowledgeState]]` in code, not config
- Provenance: hash first, timestamp second (order is load-bearing for FP4)

### Critical Pitfalls

1. **`unknown` → `false` coercion** (Critical, Phase 1 FP6) — Python truthiness, pandas label encoders, and ML pipelines all default to treating `KnowledgeState` values as booleans. Prevention: Pydantic type makes bool coercion impossible at the type level; schema test suite must include explicit `unknown`-as-negative rejection tests; every `match`/`case` on knowledge-state must handle all 7 values with a final `case _: raise ValueError`.

2. **Silent contradiction resolution** (Critical, Phase 1 FP4 + Phase 5) — Standard deduplication/upsert patterns from data engineering assume two records for the same entity are duplicates to merge. In CRIC, two conflicting sourced claims are both data. Prevention: graph schema makes it structurally impossible to have a single "current value" field; ingest tests must assert two conflicting observations produce two claim nodes, not one.

3. **Freeze Point ratification without a negative test** (Critical, all remaining FPs) — A closure ratified without a documented break-attempt is not production-ready. Prevention: ratification checklist requires a stated negative test (a PRD-documented scenario the author *attempted* to break the closure with) and Ashley's sign-off; this is a hard PR gate.

4. **Identifier proliferation — second ID format** (Critical, Phase 1 FP2) — Human-readable short IDs (`CRIC-LAKE-001`) start in fixtures, graduate to API responses, and end up in external systems. Prevention: OKF base frontmatter (FP2) must have no short-ID field; identifier parser test rejects non-ULID formats; short IDs appear only in fixture files and documentation.

5. **`mode: yolo` / `auto_advance: true` governance gap** (Critical, immediate) — `.planning/config.json` currently sets these flags. If any agent reads them and skips Freeze Point ratification, a Freeze Point can be silently "implemented without ratification." Prevention: Ashley must review and update these settings before Phase 1 work packages read them; no automated agent may declare a Freeze Point ratified.

6. **cric-core importing from domain repositories** (High, all phases) — Creates a dependency cycle that breaks installation of `cric-core` in isolation. Prevention: CI installs `cric-core` in a clean environment with no domain packages and asserts all imports succeed; any `import cric_<domain>` line in `src/cric_core/` is an automatic PR block.

7. **LLM-driven graph traversal** (High, Phase 8) — Giving an agent live graph query access produces non-deterministic, non-reproducible context assembly. Prevention: FP8 agent manifest schema must make the context-assembly vs. model-consumption boundary explicit; agents receive a typed `ContextPack`, not a query interface.

---

## Implications for Roadmap

The eight Architecture Freeze Points *are* the architecture of `cric-core`. The roadmap is determined by their dependency graph and ratification state.

### Phase 1a: WP-18 — FP6 + FP7 Pydantic Code (Immediate)
**Rationale:** Both are ratified (ADR-0007); the Pydantic code is mechanical given a locked schema; WP-18 is already the named next step in `.planning/PROJECT.md`. FP6 types must exist before FP3 (temporal model) can reference epistemic states, and before FP8 (agent manifest) can declare output types. Unblocking this first is highest ROI.
**Delivers:** `src/cric_core/knowledge_state/` — `KnowledgeState` enum (7 values), transition validator (8 allowed edges), `ReviewDecision` Pydantic model; schema test suite with valid/invalid/boundary/backwards-compat fixtures including explicit `unknown`-as-negative rejection test.
**Avoids:** Auto-coercion pitfall (Pitfall 1); governance gap pitfall (Pitfall 5 — Ashley must approve `config.json` before dispatch).

### Phase 1b: FP2 — Base OKF Frontmatter Schema
**Rationale:** FP2 is the envelope that FP3 (temporal), FP4 (provenance), and FP5 (relationships) all annotate. It must exist before any of them can be fully specified. Also gates FP8 because agents reference OKF node types.
**Delivers:** `src/cric_core/okf/` — `OKFBase` Pydantic model (required frontmatter fields, version markers, canonical node type registry); `pyyaml` added to runtime dependencies; no short-ID field on the base model.
**Avoids:** Second ID format pitfall (Pitfall 4 — no `short_id` field on base OKF schema, even optional).

### Phase 1c: FP3 + FP4 + FP5 — Temporal, Provenance, Relationships (parallel if file-disjoint)
**Rationale:** FP3 references FP6 epistemic vocabulary (available after 1a); FP4 and FP5 reference FP2 OKF node types (available after 1b); all three are otherwise independent of each other and can be developed in parallel child work packages if `files_allowed_to_change` is disjoint.
**Delivers:**
- `src/cric_core/temporal/` — `TemporalBlock`, 4-axis model, UTC-only datetime enforcement, `unknown ≠ false` invariant tested
- `src/cric_core/provenance/` — `ProvenanceRecord`, append-only lineage, hash-before-timestamp order enforced, mutable-URL rejection tested
- `src/cric_core/relationships/` — `Relationship`, canonical predicate registry (§8 of Registry is authority), predicate-not-in-registry validation error
**Avoids:** Silent contradiction resolution (Pitfall 2 — provenance model makes append-only structurally clear); mutable-URL provenance (Pitfall, FP4 — provenance requires content-addressed snapshot).

### Phase 1d: FP8 — Agent Manifest Schema
**Rationale:** FP8 depends on FP6/FP7 types (output schema types), FP2 (OKF node type references), and FP4 (provenance for agent run records). It is last in the Freeze Point sequence and gates the first agent work (Phase 8).
**Delivers:** `src/cric_core/agents/` — `AgentManifest` Pydantic model; `tool_permissions` scope field; `input_context_schema` / `output_schema` separation (context-assembly vs. model-consumption boundary explicit); `RunRecord` with mandatory `provenance` field.
**Avoids:** LLM graph traversal pitfall (Pitfall 7 — manifest schema makes context bundle type explicit).

### Phase 1e: Phase 1 Exit Gate
**Rationale:** Phase 1 is not "done" when all 8 FPs have Pydantic code — it exits when a canonical example OKF node validates against all 8 ratified schemas with CI green.
**Delivers:** End-to-end validation fixture (`tests/okf/test_canonical_example.py`) asserting a complete OKF node round-trips through all 8 schema layers; `pytest-cov` added; coverage gate enforced; CI green on merged tree.

### Phase 2: Published Artefacts + Backwards Compatibility
**Rationale:** Downstream repos (starting with `cric-knowledge` and `cric-data`) need stable contract surfaces. Before they pin a version of `cric-core` they need JSON Schema artefacts and a clear versioning signal.
**Delivers:** CI step publishing `model_json_schema()` output per FP; semantic versioning + changelog discipline; backwards-compatibility fixtures for every schema permanently resident in `tests/schema/fixtures/`; `cric-core` isolation CI test (installs in clean env with no domain packages).

### Phase 3: Domain Extension + OKF Validation CLI
**Rationale:** Once `cric-cryosphere` and `cric-glof` (Phase 4 in the system roadmap) start building, they need to extend core types and validate OKF nodes locally.
**Delivers:** Extension guidance + base protocol interfaces for domain subclassing; optional `cric validate` CLI entry point for human contributors.

### Phase Ordering Rationale

- WP-18 first because it unblocks FP3 (temporal model needs epistemic states) and FP8 (manifest needs output type vocabulary) — a single mechanical implementation unlocks two otherwise blocked freeze points.
- FP2 before FP3/FP4/FP5 because all three use OKF as their envelope; implementing the temporal or provenance model before the frontmatter schema forces retrofitting.
- FP3/FP4/FP5 in parallel (subject to pairwise-disjoint file check per CLAUDE.md §12) because they annotate OKF nodes in orthogonal ways and have no producer/consumer edges between them.
- FP8 last because it references types from every other FP.
- Published artefacts and backwards-compat fixtures in Phase 2 (not Phase 1) because they require a stable FP set to be worth publishing — publishing partial schemas creates a false sense of completeness.

### Research Flags

**Phases likely needing deeper research during planning:**
- **FP3 (temporal model):** The 4-axis temporal model (event/observation/valid/system time) has sparse documentation in existing provenance standards; the `unknown ≠ false` invariant needs a concrete negative test scenario from the PRD before ratification sign-off.
- **FP4 (provenance chain):** Immutable append-only semantics have a performance trap at scale (~1,000 evidence nodes triggers O(n) hop materialisation if not designed correctly); the FP4 schema design must make the storage boundary decision explicit.
- **FP8 (agent manifest):** The `tool_permissions` scoping mechanism and `input_context_schema` shape need a concrete agent use case to validate against before the schema can be ratified.

**Phases with standard, well-documented patterns (skip additional research):**
- **WP-18 (FP6+FP7 Pydantic code):** Schema is ratified; implementation is mechanical — `StrEnum` + `frozenset` transition graph + Pydantic model. No research needed.
- **FP2 (OKF frontmatter):** Standard Pydantic BaseModel with `extra="forbid"`; YAML parsing with pyyaml is well-understood. Ratification (negative test) is the work, not the implementation.
- **FP5 (relationship grammar):** Predicate registry is the authority (§8 of Registry); implementation is a Pydantic `Literal` union over the registry values.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Brownfield project; pyproject.toml read directly; all core tools confirmed in place; only 3 runtime deps need adding |
| Features | HIGH | Derived from 39-document PRD family, ratified ADRs, and CLAUDE.md constitutional rules; feature set is determined, not speculative |
| Architecture | HIGH | FP dependency graph sourced from ratified ADRs and PRD; Phase 0 structure confirmed by reading existing code |
| Pitfalls | HIGH | All critical pitfalls are either named in PRD constitutional rules, ratified ADRs, or already-identified blocking issues (D6) |

**Overall confidence:** HIGH

### Gaps to Address

- **D6 (ingest run without `--manifest`):** `.planning/INGEST-CONFLICTS.md` does not exist yet; this blocks Phase 1 work package dispatch. Immediate action: re-run `gsd-ingest-docs docs/CRIC-PRD-v0.1 --mode new --manifest gsd-ingest-manifest.yaml` and verify the conflicts file exists before dispatching any FP work packages.
- **`config.json` governance:** `mode: yolo` and `auto_advance: true` must be reviewed by Ashley before Phase 1 work packages read them. No automated agent may declare a Freeze Point ratified regardless of these settings.
- **FP3 negative test scenario:** The temporal model needs a concrete PRD-documented scenario where the proposed closure is *attempted* to fail before sign-off. The `unknown ≠ false` invariant is the most natural candidate; a GLOF event with `no_known_event` epistemic status should be used as the break-attempt.
- **FP4 storage boundary decision:** The provenance chain schema must decide at design time whether provenance hops are materialised at write time or reconstructed at read time. This affects FP4 ratification (the schema must encode the decision, not leave it to the implementation).

---

## Sources

### Primary (HIGH confidence)
- `docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md` — 13 Constitutional Product Rules, authority precedence
- `docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md` — canonical vocabulary, identifier form, registry §6 (`unknown` handling), §8 (predicate registry)
- `docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md` — layer boundaries, language, dependency direction
- `docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md` — test class requirements
- `CLAUDE.md` — Freeze Point ratification bar, Constitutional Rules 1/2/3/6/11/13, fan-out rules, authority precedence
- `.planning/PROJECT.md` — ratified ADRs, Phase 0 status, WP-18 identification, D6 blocking issue
- `pyproject.toml` (read directly) — hatchling, pytest ≥8, ruff, mypy, Python ≥3.12 confirmed
- `src/cric_core/identifiers/__init__.py` (read directly) — stdlib dataclasses, regex ULID validation, no generation library yet
- ADR-0004 (2026-08-29) — Identifier format ratification record
- ADR-0007 (2026-09-03) — Knowledge-state vocabulary + review-decision schema ratification record

### Secondary (MEDIUM confidence)
- `docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md` — multi-repo dependency rules
- `docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md` — node model, temporal semantics, relationship grammar
- `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md` — phase order, dependency graph

---

*Research completed: 2026-09-04*
*Ready for roadmap: yes — pending D6 resolution and `config.json` governance review*
