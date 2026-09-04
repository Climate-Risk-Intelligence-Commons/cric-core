# Requirements: cric-core

**Defined:** 2026-09-04
**Core Value:** Every claim traces to its source evidence with an auditable derivation chain — no value without provenance, no contradiction silently resolved.

## v1 Requirements

Requirements for Phase 1 exit: all 8 Architecture Freeze Points ratified, Pydantic-implemented, and CI green. Downstream repositories cannot safely build on cric-core until every item here is done.

### Identifier System (FP1 — Complete)

- [x] **ID-01**: `parse_id(s)` accepts exactly `CRIC:<namespace>:<type>:<ulid>` and rejects all other forms — no aliases, no case-folding, no second format
- [x] **ID-02**: Parser raises a typed `CRICIdentifierError` (not a generic exception) on any malformed input, with the offending string in the error
- [x] **ID-03**: Exactly 12 canonical namespaces are accepted; any string not in that set is rejected at parse time
- [x] **ID-04**: ULID component is validated for length (26 chars), charset (Crockford base-32), and monotonicity-safe generation
- [x] **ID-05**: `generate_id(namespace, type)` produces a unique, sortable, valid `CRIC:…` identifier without external coordination
- [x] **ID-06**: Round-trip: `parse_id(str(generate_id(...)))` succeeds and returns an equal value
- [x] **ID-07**: 32 passing unit tests covering valid, invalid, and boundary cases; zero skipped

### OKF Base Frontmatter (FP2)

- [ ] **OKF-01**: A Pydantic model `OKFBase` is defined with all mandatory header fields: `id` (CRIC identifier), `schema_version`, `created_at`, `knowledge_state`, `source_type`, and `content_hash`
- [ ] **OKF-02**: `OKFBase` rejects any document that omits a mandatory field with a `ValidationError` that names the missing field
- [ ] **OKF-03**: `OKFBase.id` accepts only a valid CRIC identifier string (delegates to FP1 parser); free-text strings are rejected
- [ ] **OKF-04**: `schema_version` is a `semver`-format string; non-semver values are rejected
- [ ] **OKF-05**: A schema fixture file provides at least one valid example, one missing-field example, and one invalid-field-type example
- [ ] **OKF-06**: Ratification negative test: a concrete scenario from the PRD that the frontmatter must represent is demonstrated parseable under the model before sign-off

### Temporal and Epistemic Model (FP3)

- [ ] **TEMP-01**: A Pydantic model `TemporalWindow` expresses observation start, end, and a nullable `unknown` sentinel — `unknown` is a first-class value, not `None` coerced to absent
- [ ] **TEMP-02**: `BeliefTimestamp` carries both the assertion time and the evidence-acquisition time as distinct fields; they may differ and neither may be silently defaulted to the other
- [ ] **TEMP-03**: Deserialising a document with `observation_state: "unknown"` does not produce a falsy Python value — `bool(doc.observation_state)` must not be `False`
- [ ] **TEMP-04**: `unknown` and `unobserved` are distinct enumeration members; coercing one to the other raises an error
- [ ] **TEMP-05**: A schema test asserts the `unknown ≠ false` invariant with a fixture that would produce a false negative if auto-coercion were permitted
- [ ] **TEMP-06**: Ratification negative test: a concrete "not yet observed" vs "confirmed absent" scenario from the cryosphere PRD is demonstrated distinguishable under the model before sign-off

### Evidence Provenance Chain (FP4)

- [ ] **PROV-01**: A Pydantic model `ProvenanceChain` represents a directed acyclic chain from derived value back to one or more source evidence nodes, with each link carrying a `derivation_method` field
- [ ] **PROV-02**: Every node in a `ProvenanceChain` is identified by a CRIC identifier (FP1); bare strings without the `CRIC:` prefix are rejected
- [ ] **PROV-03**: Appending a new link produces a new `ProvenanceChain` object; the original is unchanged (append-only / immutable-lineage semantics enforced at the model level)
- [ ] **PROV-04**: A `ProvenanceChain` with a cycle (node A → node B → node A) is rejected at validation time with a typed error
- [ ] **PROV-05**: A schema test demonstrates the immutable-lineage invariant: two `ProvenanceChain` objects produced from the same base do not share mutable state
- [ ] **PROV-06**: Ratification negative test: a synthetic multi-hop derivation (e.g. satellite image → normalised index → risk score) is representable end-to-end under the model before sign-off

### OKF Relationship Grammar (FP5)

- [ ] **REL-01**: A Pydantic model `OKFRelationship` represents a directed edge between two CRIC-identified OKF nodes with a `predicate` field drawn from a closed enum
- [ ] **REL-02**: The predicate vocabulary includes at minimum: `supports`, `contradicts`, `refines`, `supersedes`, `cites`; any string outside the enum is rejected
- [ ] **REL-03**: Both `source_id` and `target_id` must be valid CRIC identifiers; bare strings are rejected
- [ ] **REL-04**: A `contradicts` relationship between two nodes does not cause validation to fail — contradiction is valid data, not a schema error
- [ ] **REL-05**: A schema test asserts that a `contradicts` edge between two conflicting-claim nodes round-trips cleanly
- [ ] **REL-06**: Ratification negative test: a concrete inter-document contradiction from the PRD family is shown representable without silent resolution before sign-off

### Knowledge-State Vocabulary (FP6 — ratified ADR-0007, code pending WP-18)

- [ ] **KS-01**: A Python `Enum` (or Pydantic `Literal`) named `KnowledgeState` defines exactly 7 values: `confirmed`, `supported`, `contested`, `contradicted`, `unknown`, `unobserved`, `no_known_event`
- [ ] **KS-02**: `KnowledgeState.unknown` and `KnowledgeState.unobserved` and `KnowledgeState.no_known_event` are never equal to each other and never equal to any falsy Python value
- [ ] **KS-03**: Deserialising a JSON document with `"knowledge_state": "unknown"` produces `KnowledgeState.unknown`, not `None`, not `False`, not an empty string
- [ ] **KS-04**: Serialising any `KnowledgeState` member round-trips to the canonical string form defined in registry §6 — no aliases, no case variants
- [ ] **KS-05**: A schema test asserts that auto-coercion of `unknown` → `False` is impossible given the Pydantic model configuration
- [ ] **KS-06**: State-transition envelope: only the 8 edges ratified in ADR-0007 are accepted by a `validate_transition(from_state, to_state)` function; all others raise `InvalidTransitionError`

### Review Decision Schema (FP7 — ratified ADR-0007, code pending WP-18)

- [ ] **REV-01**: A Pydantic model `ReviewDecision` carries: `reviewer_id` (CRIC identifier), `subject_id` (CRIC identifier), `decision` (enum), `rationale` (non-empty string), `timestamp`, and `resulting_state` (`KnowledgeState`)
- [ ] **REV-02**: `decision` enum contains at minimum: `accept`, `reject`, `request_revision`, `escalate`
- [ ] **REV-03**: `resulting_state` must be a member of `KnowledgeState`; free strings are rejected
- [ ] **REV-04**: A `ReviewDecision` with an empty `rationale` string is rejected at validation time
- [ ] **REV-05**: A schema test verifies that a `ReviewDecision` produces a valid state transition consistent with FP6's `validate_transition` — an invalid transition in `resulting_state` is caught
- [ ] **REV-06**: Round-trip: a `ReviewDecision` serialised to JSON and deserialised produces an equal object with no field loss

### Agent Manifest Schema (FP8)

- [ ] **AGNT-01**: A Pydantic model `AgentManifest` declares: `agent_id` (CRIC identifier), `version` (semver string), `input_types` (list of CRIC identifier strings referencing schema types), `output_types` (list of CRIC identifier strings), and `review_output_types` (list referencing `ReviewDecision` or subclasses)
- [ ] **AGNT-02**: An `AgentManifest` with an empty `output_types` list is rejected — every agent must declare at least one output type
- [ ] **AGNT-03**: `input_types` and `output_types` entries must be valid CRIC identifiers; bare strings are rejected
- [ ] **AGNT-04**: Two `AgentManifest` objects can be composed: a `compose(a, b)` function succeeds iff `a.output_types` and `b.input_types` have a non-empty intersection, and raises `IncompatibleManifestError` otherwise
- [ ] **AGNT-05**: A schema test verifies that an agent declaring `review_output_types` referencing `ReviewDecision` (FP7) round-trips correctly
- [ ] **AGNT-06**: Ratification negative test: a concrete agent-composition scenario where two agents are incompatible (no shared type) is shown caught by `compose()` before sign-off

### Schema Test Suite (all models)

- [ ] **TST-01**: Every Pydantic model produced for FP2–FP8 has a dedicated test module containing at minimum: one valid fixture, one missing-required-field fixture, one wrong-type fixture, and one boundary fixture (maximum-length string, edge-case enum value, etc.)
- [ ] **TST-02**: Every model's test module contains a backwards-compat fixture: a JSON document from a prior commit (or the ratification fixture) that must still parse successfully after any change
- [ ] **TST-03**: All schema tests are collected by `pytest` under `tests/schema/` and run in CI without extra flags
- [ ] **TST-04**: No test uses `assert True` or `assert isinstance(x, Model)` as its sole assertion — each test asserts a specific field value or a specific exception type and message

### CI and Quality Gates

- [ ] **CI-01**: `ruff check` passes with zero errors on every PR; the ruff config in `pyproject.toml` is the authority — no per-file ignores that mask real issues
- [ ] **CI-02**: `mypy --strict` passes on the `src/cric_core/` tree with zero type errors
- [ ] **CI-03**: `pytest` exits 0 with no skipped tests (skip is prohibited unless annotated with a `# reason:` comment and a linked issue)
- [ ] **CI-04**: `python -m build` succeeds and produces a `dist/` wheel importable in a clean virtualenv
- [ ] **CI-05**: JSON Schema artefacts are generated from Pydantic models and written to `schema/` as part of the build step; a missing or stale artefact causes CI to fail

### Phase 1 Exit Gate

- [ ] **EXIT-01**: A canonical example OKF node document (YAML or JSON) exists in `tests/fixtures/` that validates against all 8 Freeze Point schemas simultaneously without error
- [ ] **EXIT-02**: The canonical example includes a `ProvenanceChain` (FP4), a `TemporalWindow` (FP3), a `KnowledgeState` value (FP6), and at least one `OKFRelationship` (FP5) to another identified node
- [ ] **EXIT-03**: CI runs the `EXIT-01` fixture validation as a named test (`test_phase1_exit_gate`) that fails if any schema rejects the document

## v2 Requirements

Deferred until after Phase 1 exit. Needed before Phase 4 domain repositories begin extending core types.

### Published JSON Schema Artefacts

- **SCH-01**: CI publishes versioned JSON Schema files to a GitHub Release asset on every tagged release
- **SCH-02**: Each published schema file carries a `$id` URI matching the release tag and schema name
- **SCH-03**: A TypeScript consumer can validate a JSON document against the published OKF schema without importing any Python code

### Backwards-Compatibility Guarantees

- **BACK-01**: Every released schema version is accompanied by a migration guide noting any breaking field changes
- **BACK-02**: Fixtures from the previous minor version are included in the test suite and must pass against the current model
- **BACK-03**: A `CHANGELOG.md` entry is required for every schema change; CI fails if `CHANGELOG.md` is not updated on a PR that modifies any file under `src/cric_core/`

### OKF Validation CLI

- **CLI-01**: `cric validate <path>` reads a YAML or JSON file and reports pass/fail against the OKF schema
- **CLI-02**: Validation errors include field path, expected type, and actual value — not just "ValidationError"
- **CLI-03**: Exit code 0 = valid, 1 = invalid, 2 = tool error (file not found, parse error)

## v3 Requirements

Future consideration — Phase 4+, contingent on domain repo adoption.

### Schema Migration Tooling

- **MIG-01**: `cric migrate <path> --from 1.x --to 2.x` transforms a valid v1 document to v2 in place
- **MIG-02**: Migration is idempotent — running it twice produces the same result
- **MIG-03**: A dry-run flag (`--dry-run`) prints the diff without writing

### Cross-Repo Integration Test Harness

- **INT-01**: A CI job pins a snapshot of `cric-cryosphere` and verifies it imports cleanly against `cric-core` HEAD
- **INT-02**: A failing cross-repo test blocks merge of the `cric-core` PR that caused it

## Out of Scope

| Feature | Reason |
|---------|--------|
| Domain ontologies (cryosphere, GLOF) in cric-core | Violates dependency direction — cric-core is the root; domain ontologies belong in `cric-cryosphere` / `cric-glof` (Phase 4) |
| Graph query / retrieval execution | cric-core ships schemas, not a query engine; retrieval lives in `cric-api` (Phase 6) |
| A second "human-friendly" ID format (e.g. `CRIC-LAKE-001`) | Two ID formats → two parsers → divergence bugs; explicitly prohibited by Freeze Point 1 / ADR-0004 |
| Auto-resolving contradictions | Silently drops valid evidence; violates Constitutional Rule 3 |
| Binary knowledge states (true/false) | Cannot express `unknown`, `unobserved`, `contradicted`; Rule 6 prohibits auto-converting these to false |
| `unknown` auto-coerced to negative/absent | Precisely how false negatives enter risk models; prohibited by registry §6 and Training-Data spec |
| LangGraph or any mandatory orchestration framework | Couples all agents across 12 repos to one framework's upgrade cycle; explicit PRD decision |
| Web frontend | `cric-ui`, Phase 12; TypeScript/React is out of scope for this repository |
| Data ingestion pipeline | `cric-ingest`, Phase 5; deterministic acquisition of external sources is not a cric-core concern |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ID-01 through ID-07 | Phase 0 | Complete |
| OKF-01 through OKF-06 | Phase 1 | Pending |
| TEMP-01 through TEMP-06 | Phase 1 | Pending |
| PROV-01 through PROV-06 | Phase 1 | Pending |
| REL-01 through REL-06 | Phase 1 | Pending |
| KS-01 through KS-06 | Phase 1 (WP-18) | Pending |
| REV-01 through REV-06 | Phase 1 (WP-18) | Pending |
| AGNT-01 through AGNT-06 | Phase 1 | Pending |
| TST-01 through TST-04 | Phase 1 (concurrent with each FP) | Pending |
| CI-01 through CI-05 | Phase 0 → Phase 1 (CI-05 new) | CI-01–04 Complete; CI-05 Pending |
| EXIT-01 through EXIT-03 | Phase 1 | Pending |
| SCH-01 through SCH-03 | Phase 2 | Pending |
| BACK-01 through BACK-03 | Phase 2 | Pending |
| CLI-01 through CLI-03 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 53 total
- Mapped to phases: 53
- Unmapped: 0 ✓

---
*Requirements defined: 2026-09-04*
*Last updated: 2026-09-04 — initial definition from PRD family + feature research*
