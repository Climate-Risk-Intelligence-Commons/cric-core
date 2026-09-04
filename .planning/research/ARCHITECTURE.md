# Architecture Research

**Domain:** Provenance-preserving, temporally-aware climate-risk knowledge infrastructure (contract root library)
**Researched:** 2026-09-04
**Confidence:** HIGH — sourced directly from the 39-document PRD family, ratified ADRs, and existing Phase 0 code

---

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Human Applications / UI                        │
│                    (cric-ui — Phase 12, TypeScript/React/MapLibre)    │
├──────────────────────────────────────────────────────────────────────┤
│                          API / SDK / CLI                              │
│                   (cric-api — FastAPI + OpenAPI, Phase 6)            │
├──────────────────────────────────────────────────────────────────────┤
│              Agent Commons            │    Scientific Workflows        │
│          (cric-agents, Phase 8)       │   (cric-models, Phase 7)      │
├───────────────────────────────────────┴───────────────────────────────┤
│                  Retrieval / Graph / Search Layer                      │
│              Deterministic OKF multi-hop context retrieval             │
│        (TraversalProfile → ContextSubgraph → ContextPack → LLM)       │
├──────────────────────────────────────────────────────────────────────┤
│               Materialised Data Services                               │
│       DuckDB (local) │ PostgreSQL/PostGIS (institutional)             │
│       Full-text index │ Vector store │ Graph DB │ Parquet cache        │
├──────────────────────────────────────────────────────────────────────┤
│   OKF Knowledge Commons (cric-knowledge)  │  Data Commons (cric-data) │
│   Markdown + YAML frontmatter, Git-versioned canonical artefacts      │
├──────────────────────────────────────────────────────────────────────┤
│                         Domain Packages                                │
│        cric-cryosphere (Phase 4)  │  cric-glof (Phase 4)             │
├──────────────────────────────────────────────────────────────────────┤
│                       ★ cric-core ★  (this repo)                      │
│   identifiers │ OKF schemas │ temporal │ provenance │ relationships   │
│   knowledge-state vocab │ review contracts │ controlled vocabularies   │
├──────────────────────────────────────────────────────────────────────┤
│                           Storage                                      │
│   Git (canonical) │ DuckDB │ PostgreSQL │ S3-compatible │ STAC        │
└──────────────────────────────────────────────────────────────────────┘

Cross-cutting (present at every layer):
Pydantic schemas │ provenance │ temporal semantics │ permissions │ HITL │ ontology
```

**Dependency direction is strict and unidirectional:**
```
cric-core ← domain packages ← ingest/models/agents ← api/ui
```
`cric-core` may not import any domain-specific repository. All dependency edges point toward this repo, never away.

---

### cric-core Internal Structure

`cric-core` ships schemas, identifiers, and base types. It does not ship query execution, domain ontologies, or UI code.

```
src/cric_core/
├── identifiers/        # FP1: CRIC:<namespace>:<type>:<ulid> — DONE (ADR-0004)
├── knowledge_state/    # FP6+7: 7-value vocab + review decision schema — RATIFIED, code pending (WP-18)
├── okf/                # FP2: base OKF frontmatter schema — pending
├── temporal/           # FP3: multi-temporal model — pending
├── provenance/         # FP4: evidence-provenance chain schema — pending
├── relationships/      # FP5: OKF relationship grammar — pending
├── agents/             # FP8: agent dependency/output manifest schema — pending
├── vocabularies/       # controlled vocabularies (epistemic, negative-case, predicates)
└── validators/         # Pydantic-based validation framework
```

Each directory corresponds to exactly one Architecture Freeze Point. Once a Freeze Point is ratified, the code in its directory is locked — changes require an explicit migration plan and Ashley's sign-off.

---

### Component Responsibilities

| Component | Responsibility | Implementation |
|-----------|---------------|----------------|
| `identifiers/` | Parse and generate `CRIC:<ns>:<type>:<ulid>` — single format, no aliases | Pydantic model + ULID; 32 passing tests |
| `okf/` | Canonical OKF frontmatter base schema (all required fields, version markers) | Pydantic BaseModel; generates JSON Schema |
| `temporal/` | 4-axis temporal model: event_time, observation_time, valid_time, system_time | Pydantic models; temporal consistency validators |
| `provenance/` | Evidence-provenance chain: source_nodes, transformations, agent_run_id, sha256 | Pydantic models; immutable lineage |
| `relationships/` | Typed relationship grammar with canonical predicates | Pydantic models; predicate registry enforced |
| `knowledge_state/` | 7-value workflow status + 8-edge transition envelope | Pydantic enum + transition validator |
| `agents/` | Agent definition schema: instructions + dependency + toolsets + output + workspace + permissions | Pydantic manifest schema |
| `vocabularies/` | Canonical controlled vocabularies: epistemic status, negative-case, predicates | Enum types + registry |
| `validators/` | Multi-level OKF validation: syntax → schema → ontology → graph → temporal → provenance | Composable validator pipeline |

---

## Recommended Project Structure

```
src/
├── cric_core/
│   ├── __init__.py               # package version, public API surface
│   ├── identifiers/
│   │   ├── __init__.py
│   │   ├── _model.py             # CRICIdentifier Pydantic model
│   │   └── _parse.py             # strict parser, zero case-folding
│   ├── okf/
│   │   ├── __init__.py
│   │   ├── _frontmatter.py       # OKFBase Pydantic model (FP2)
│   │   └── _node_categories.py   # canonical node type registry
│   ├── temporal/
│   │   ├── __init__.py
│   │   ├── _model.py             # TemporalBlock, EventTime, ObservationTime…
│   │   └── _validators.py        # consistency checks (event ≤ observation ≤ system)
│   ├── provenance/
│   │   ├── __init__.py
│   │   └── _model.py             # ProvenanceRecord, lineage chain
│   ├── relationships/
│   │   ├── __init__.py
│   │   ├── _model.py             # Relationship, predicate validation
│   │   └── _predicates.py        # canonical predicate registry (§8 is authority)
│   ├── knowledge_state/
│   │   ├── __init__.py
│   │   ├── _vocabulary.py        # KnowledgeState enum (7 values)
│   │   └── _transitions.py       # allowed 8-edge transition graph
│   ├── agents/
│   │   ├── __init__.py
│   │   └── _manifest.py          # AgentManifest Pydantic model (FP8)
│   └── vocabularies/
│       ├── __init__.py
│       ├── _epistemic.py         # EpistemicStatus (8 values)
│       └── _negative_case.py     # NegativeCaseLabel (6 values; never auto-converted)
tests/
├── unit/                         # per-module logic
├── schema/                       # valid + invalid + boundary + backwards-compat fixtures
│   ├── fixtures/valid/
│   ├── fixtures/invalid/
│   └── fixtures/boundary/
├── ontology/                     # type and predicate registry checks
└── okf/                          # full OKF node round-trip tests
```

### Structure Rationale

- **One directory per Freeze Point:** keeps boundaries visible and makes "what changed" obvious in diffs.
- **`_model.py` / `_validators.py` split inside each directory:** models hold field definitions; validators hold enforcement logic. This prevents circular imports and lets validators be tested independently.
- **No `core/` or `base/` umbrella directory:** every module is already in `cric_core`; double-nesting adds noise without meaning.
- **`tests/schema/fixtures/`:** backwards-compatibility fixtures live here permanently — they are never deleted when a schema evolves, because old fixture failures are the signal that migration is required.

---

## Architectural Patterns

### Pattern 1: Pydantic as runtime schema authority

**What:** Every contract surface — OKF nodes, API request/response, agent inputs/outputs, review artefacts, provenance records — is a Pydantic model. JSON Schema is generated from Pydantic and published as a build artefact, but Pydantic is the source of truth.

**When to use:** Always. No duck-typed contracts. No dict-shaped data passed between modules.

**Trade-offs:** Import-time schema validation catches errors early; generated JSON Schema lets non-Python consumers validate without importing cric-core. Downside: Pydantic v2 migration is a breaking schema change — pin Pydantic version in `pyproject.toml` and treat it as a dependency contract.

```python
class TemporalBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")  # reject unknown fields — intentional strictness
    event_time: EventTime | None = None
    observation_time: ObservationTime | None = None
    valid_time: ValidTime | None = None
    system_time: SystemTime  # required — every node must record when CRIC knew it
```

### Pattern 2: Immutable provenance chain

**What:** Every derived value carries a `provenance` block naming its `source_nodes`, `transformations`, `agent_run_id`, and `content_sha256`. Provenance is append-only: a new node supersedes an old one, the old one stays in the graph with `status: superseded`.

**When to use:** Every time a node is created or updated. No value without provenance is a Constitutional Rule.

**Trade-offs:** Storage grows monotonically; this is intentional — historical knowledge states must be reconstructable. The supersession pattern (`superseded_by` relationship + `status: superseded`) is the only correct way to "update" a node.

```python
class ProvenanceRecord(BaseModel):
    source_nodes: list[CRICIdentifier] = Field(default_factory=list)
    source_uris: list[AnyUrl] = Field(default_factory=list)
    parent_nodes: list[CRICIdentifier] = Field(default_factory=list)
    transformations: list[str] = Field(default_factory=list)
    agent_run_id: CRICIdentifier | None = None
    content_sha256: str | None = None  # SHA-256 of the canonical content bytes
```

### Pattern 3: Contradiction coexistence, not resolution

**What:** Two validly sourced conflicting claims both live in the graph simultaneously. The relationship grammar expresses `contradicts` between them. A later assessment node may prefer one interpretation — it does not delete the other.

**When to use:** Whenever two evidence nodes disagree on the same subject-predicate-object triple.

**Trade-offs:** Query results must filter by `knowledge_state` to get "current best understanding"; returning all nodes including `disputed` / `superseded` is intentional for provenance reconstruction but requires explicit filtering in application code.

```python
# Wrong — do not do this:
if claim_a.confidence > claim_b.confidence:
    archive(claim_b)

# Correct:
Relationship(
    predicate="contradicts",
    target=claim_b.id,
    source_nodes=[assessment.id],
    status="accepted",
)
```

### Pattern 4: Deterministic code before LLM

**What:** All ingestion, hashing, validation, geospatial computation, feature generation, indexing, and graph materialisation use ordinary Python. LLMs consume an assembled `ContextPack`; they do not traverse the graph themselves.

**When to use:** Always. The retrieval pipeline is: `TraversalProfile` (defines permitted hops) → `ContextSubgraph` (resolved node/edge set) → `ContextPack` (bounded, versioned package) → LLM.

**Trade-offs:** More code to write up front; prevents the largest class of hallucination-in-retrieval bugs by construction.

### Pattern 5: Knowledge state as a state machine, not a free field

**What:** The 7-value `knowledge_state.status` vocabulary (`candidate`, `accepted`, `disputed`, `superseded`, `rejected`, `withdrawn`, `archived`) is a state machine with 8 allowed transitions (ADR-0007). The Pydantic model enforces allowed transitions; code that attempts an illegal transition raises a validation error.

**When to use:** Every time a node's knowledge state changes. The transition must be modelled as a new `ReviewDecision` node, not a silent field update.

**Trade-offs:** Slightly more ceremony than a string field; prevents knowledge lifecycle bugs that would be invisible in a free-field schema.

---

## Data Flow

### OKF Node Lifecycle

```
External Source (paper, satellite, pipeline output)
    ↓ [deterministic ingest — cric-ingest]
Raw DataAsset node + ProvenanceRecord
    ↓ [deterministic feature extraction]
Observation node (with temporal block, epistemic status, provenance)
    ↓ [optional: knowledge_state = candidate]
ReviewRequest → human HITL review → ReviewDecision
    ↓ [knowledge_state = accepted | rejected | disputed]
Claim / StateSnapshot (assembled by deterministic code)
    ↓ [ContextPack assembled]
LLM agent consumes bounded, versioned context
    ↓ [agent output is a new Pydantic-validated node, not raw text]
AgentRun node + output node → ReviewRequest (if HITL required)
```

### Retrieval Path (Constitutional Rule 13)

```
Query → TraversalProfile (permitted hop types, depth limits)
    ↓ [deterministic graph traversal — no LLM here]
ContextSubgraph (resolved nodes + edges)
    ↓ [deterministic packing — apply token budget, order by provenance weight]
ContextPack (bounded, versioned, schema-validated)
    ↓
LLM receives ContextPack — it does NOT call graph traversal tools
```

### Provenance Chain Flow

```
L0 Source Evidence (original paper, satellite pass, sensor reading)
    ↓
L1 Derived Observation (extracted, normalised, attributed)
    ↓
L2 Assessment / Claim (synthesised, method declared)
    ↓
L3 Model Prediction (trained on L0–L2 labelled data)
    ↓
L4 Review Decision (HITL acceptance / rejection)
```

Each level carries a `derived_from` relationship back to its parent. No value appears at any level without tracing to L0.

---

## Multi-Repository Dependency Map

```
cric-core  (this repo — contract root, no upstream deps)
    │
    ├── cric-knowledge  (OKF Markdown graph, parser, vault layout)
    │
    ├── cric-data  (dataset manifests, DataAsset, licence metadata, STAC refs)
    │
    ├── cric-cryosphere  (cryosphere ontology, deterministic processing)
    │   └── cric-glof  (GLOF ontology, event models, StateSnapshot, benchmarks)
    │
    ├── cric-ingest  (deterministic acquisition + normalisation pipelines)
    │
    ├── cric-agents  (Pydantic agent factories, toolsets, workspaces, manifests)
    │
    ├── cric-models  (training + evaluation infrastructure)
    │
    ├── cric-review  (HITL review artefacts and workflow schemas)
    │
    ├── cric-api  (FastAPI service, retrieval engine, graph materialisation)
    │
    ├── cric-ui  (React + Vite + MapLibre, TypeScript)
    │
    └── cric-docs  (documentation only)
```

**Higher-level repositories must not redefine core schema types.** They may extend (add fields via subclassing) but never redefine semantic meaning. A domain type that changes what `knowledge_state.status: accepted` means is a prohibited change regardless of which repo it lives in.

---

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| Single researcher | Knowledge-only profile: Obsidian vault + `cric-knowledge` checkout. No database, no API. Works offline. |
| Small team / local research | Markdown + DuckDB (local analytical store) + Python SDK + agents. DuckDB Spatial for geospatial queries. No Docker required. |
| Web workbench | FastAPI + React/MapLibre + materialised DuckDB or PostgreSQL/PostGIS graph. Docker-composed. |
| Institutional deployment | PostGIS + object storage (S3-compatible) + auth + private dataset partitions. Background job adapters (Celery, Dramatiq, k8s jobs) via interface — not hardwired. |

**First bottleneck:** OKF graph materialisation. DuckDB handles local analytical loads well; the transition point to PostgreSQL/PostGIS is when concurrent writes or multi-user graph queries exceed DuckDB's single-writer model.

**Second bottleneck:** Large asset storage. Raw satellite products, DEM rasters, and model weights must never enter Git. They are referenced through immutable `DataAsset` nodes with URI + SHA-256 + byte-size. The storage adapter is injected — switching from local filesystem to S3 changes configuration, not application logic.

**Do not prematurely introduce distributed complexity.** v0.1 explicitly forbids a mandatory distributed task queue. The interface design permits later adapters; do not add Celery or Dramatiq until there is a concrete operational reason.

---

## Anti-Patterns

### Anti-Pattern 1: Treating `unknown` as `false`

**What people do:** Auto-convert `epistemic.status: unknown`, `no_known_event`, or `unobserved` to a negative training label or a `False` boolean because "no evidence means it didn't happen."

**Why it's wrong:** Constitutional Rule 6. In climate risk, absence of observation is not evidence of absence — particularly in data-sparse Himalayan regions. Silent false negatives corrupt downstream risk estimates and training data.

**Do this instead:** Keep the negative-case vocabulary explicit: `confirmed_negative`, `probable_negative`, `no_known_event`, `unknown`, `unobserved`, `not_applicable`. Only the first two are safe to treat as negative labels. The latter three must propagate forward as-is.

### Anti-Pattern 2: Resolving contradictions in code

**What people do:** When two claims disagree, keep the higher-confidence one and archive or delete the other.

**Why it's wrong:** Constitutional Rule 3. Contradictions are data about the state of scientific knowledge. Deleting a contradicted claim destroys the record of the disagreement and makes the graph appear more certain than it is.

**Do this instead:** Represent both claims. Express `contradicts` relationships between them. Create an `Assessment` node that reasons about the contradiction. Let `knowledge_state` reflect whether a claim is `disputed`. Never delete.

### Anti-Pattern 3: LLM-driven graph traversal

**What people do:** Give an LLM a graph traversal tool and let it decide which nodes to retrieve for context assembly.

**Why it's wrong:** Constitutional Rule 13. LLM traversal is non-deterministic, non-reproducible, and subject to prompt injection via malicious node content. The LLM cannot verify provenance chains it constructs on the fly.

**Do this instead:** The deterministic retrieval engine (Phase 6, `cric-api`) assembles a `ContextPack` before the LLM is invoked. The LLM consumes a bounded, versioned, schema-validated context package. It does not hold a graph traversal tool.

### Anti-Pattern 4: Second ID format "for convenience"

**What people do:** Add human-readable aliases like `CRIC-LAKE-001` as a second canonical identifier format because ULIDs are not memorable.

**Why it's wrong:** ADR-0004, Freeze Point 1. A second identifier format creates identifier proliferation across 12 repositories. Every system that consumes a CRIC ID must then decide which format is authoritative.

**Do this instead:** Human-readable labels (`title`, `aliases`, `tags`) live in the OKF frontmatter alongside the canonical ULID-based ID. Short IDs may appear in fixtures and documentation but must never be treated as production identifiers. The `aliases` field supports Obsidian wiki-link navigation without polluting the identifier namespace.

### Anti-Pattern 5: Widening `files_allowed_to_change` during implementation

**What people do:** While implementing a work package, discover a related defect in an adjacent file and fix it in the same branch because "it's faster."

**Why it's wrong:** CLAUDE.md §4. Each work package's `files_allowed_to_change` is a hard boundary, not a hint. A fix outside it invalidates the work package and can silently alter a Freeze Point that another agent is concurrently producing.

**Do this instead:** File the defect. Do not fix it in this branch. Raise a new work package.

---

## Integration Points

### Within cric-core

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `identifiers/` ↔ all other modules | `CRICIdentifier` Pydantic model | Every schema that holds an ID imports this model — it is the one exception to the "no cross-module imports" rule |
| `knowledge_state/` ↔ `okf/` | `KnowledgeState` enum embedded in `OKFBase` | State transition validation runs at OKF parse time |
| `provenance/` ↔ `temporal/` | `ProvenanceRecord.content_sha256` is computed before `system_time.created_at` is stamped | Order matters: hash first, timestamp second |
| `relationships/` ↔ `vocabularies/` | Relationship predicate must be in canonical predicate registry | Validation at model construction time |

### With Downstream Repositories

| Downstream | Contract Surface | Notes |
|------------|-----------------|-------|
| `cric-knowledge` | OKF Pydantic schemas (published JSON Schema) | The knowledge vault validates every node against `cric-core` schemas |
| `cric-agents` | `AgentManifest` schema (FP8) | Agents declare their dependency types and output schemas using `cric-core` models |
| `cric-ingest` | `ProvenanceRecord`, `DataAsset`, identifier parser | Every ingested artefact gets a `cric-core`-validated ID and provenance chain |
| `cric-api` | All published Pydantic models + generated JSON Schema | FastAPI uses `cric-core` models as request/response types |
| Domain repos | Subclass `cric-core` base types — never redefine semantic meaning | `cric-cryosphere` adds cryosphere fields; it does not change what `Observation` means |

### External Interface Contracts

Cross-repository communication uses:
- Published Pydantic models (Python-to-Python)
- Generated JSON Schema (language-agnostic validation)
- OKF Markdown (human-readable canonical artefacts)
- GeoJSON / GeoParquet (spatial data exchange)
- STAC (large asset cataloguing)
- REST/OpenAPI via `cric-api`
- Optional MCP interfaces for agent toolsets

---

## Observability Requirements

Every workflow or agent run must generate:

```python
class RunRecord(BaseModel):
    run_id: CRICIdentifier        # CRIC:<ns>:agent_run:<ulid>
    started_at: datetime
    completed_at: datetime | None
    input_refs: list[CRICIdentifier]
    output_refs: list[CRICIdentifier]
    errors: list[str]
    provenance: ProvenanceRecord  # links run record into the provenance chain
    performance_metrics: dict[str, float] = Field(default_factory=dict)
```

This is not optional logging — it is the mechanism by which agent outputs enter the provenance chain and can be audited.

---

## Phase 1 Exit Gate (Current Objective)

The 8 Architecture Freeze Points are the architecture of `cric-core`. Phase 1 is complete when all 8 are ratified AND a canonical example OKF node validates against all ratified schemas.

| Freeze Point | Status | ADR |
|-------------|--------|-----|
| FP1: Identifier format | ✓ Ratified + implemented | ADR-0004 |
| FP2: Base OKF frontmatter | Pending | — |
| FP3: Temporal model | Pending | — |
| FP4: Provenance model | Pending | — |
| FP5: Relationship representation | Pending | — |
| FP6: Knowledge-state vocabulary | ✓ Ratified, code pending (WP-18) | ADR-0007 |
| FP7: Review decision schema | ✓ Ratified, code pending (WP-18) | ADR-0007 |
| FP8: Agent manifest schema | Pending | — |

**Ratification bar (non-negotiable):** every closed set (enum, transition graph, schema) needs a stated negative test — a concrete scenario the PRD documents, shown representable under the proposed closure — before sign-off is valid. Accuracy alone is not sufficient.

---

## Sources

- `docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md` — canonical layer diagram, language, API, storage, agent runtime
- `docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md` — multi-repo dependency rules, workspace isolation, large data policy
- `docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md` — node model, temporal semantics, relationship grammar, validation levels
- `docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md` — canonical naming, identifier form, root object types, knowledge state, epistemic status, negative-case vocab, predicates
- `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md` — phase order, dependency graph, exit criteria
- `docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md` — 13 Constitutional Product Rules
- `.planning/PROJECT.md` — ratified ADRs, Phase 0 status, current active requirements
- `CLAUDE.md` — authority precedence, freeze point ratification bar, fan-out rules

---

*Architecture research for: cric-core (Climate Risk Intelligence Commons contract root)*
*Researched: 2026-09-04*
