# CRIC Deterministic Retrieval Engine Specification

## Purpose

This document defines the implementation architecture of the deterministic multi-hop graph retrieval engine that assembles bounded, inspectable context for an LLM from the OKF Markdown vault.

`interfaces/Search-and-Graph-Interfaces.md` owns what retrieval exposes: search modes, the traversal request shape, the context package contract and the v0.1 acceptance criteria for retrieval as a product/API surface. This document owns how the engine underneath that surface is built: package responsibilities, index structures, the traversal algorithm, the compiled graph artefact, ranking mechanics and failure classification. The relationship mirrors how `engineering/Software-Architecture.md` provides the implementation architecture underlying the CRIC knowledge, data, model, agent and interface layers described elsewhere in the PRD; this document does the same for the retrieval slice of that architecture.

This document is the detailed engine-level design for two already-committed requirements in `CRIC-Requirements-Traceability-Matrix.md`:

- **R-025** — Graph retrieval is deterministic and bounded.
- **R-026** — LLMs receive inspectable context packages.

It is also the concrete instance of Constitutional Product Rule #13:

> **The LLM must not perform graph traversal; deterministic software assembles context first.**

Everything below exists to make that rule enforceable rather than aspirational: a named, testable pipeline stage for every step between a question and an LLM-facing context pack.

---

# Package/Module Responsibility Layout

The engine should be organised as named responsibilities rather than a single monolithic retrieval function. Each responsibility should be independently testable and independently versioned.

```text
parser
compiler
graph
traversal
context
ranking
completeness
```

- **parser** — reads Markdown files and YAML frontmatter from the vault into intermediate, unvalidated document representations. Runs during indexing and change processing, never during a live query.
- **compiler** — validates parsed documents against Pydantic schemas and the relationship ontology, resolves them into canonical `Node` and `Edge` objects, and writes them into the persistent graph index.
- **graph** — owns the runtime graph representation and its indexes (see below); answers structural questions without reparsing Markdown.
- **traversal** — implements traversal profiles and the deterministic multi-hop expansion algorithm; decides which paths are legal for a given analytical task.
- **context** — assembles the `ContextSubgraph` and renders it into the structured Context Pack; owns token budgeting and structure-preserving (non-flattened) rendering.
- **ranking** — scores candidate nodes/edges when more context is available than the token budget permits, using the documented, versioned scoring function.
- **completeness** — evaluates a traversal profile's required-context checklist against what was actually retrieved, and detects expected-but-absent nodes.

Provenance and temporal handling are cross-cutting concerns exercised by `compiler`, `traversal` and `context` rather than isolated packages, consistent with the cross-cutting list in `Software-Architecture.md`.

---

# Node and Edge Index Structures

The compiled graph maintains explicit indexes so that queries operate against precomputed structures rather than rescanning documents.

```text
out_edges
in_edges
by_type
by_time
by_trust
```

- **out_edges** — keyed by source node ID, supports forward traversal ("what does this node connect to") without inspecting the source document.
- **in_edges** — keyed by target node ID, supports reverse traversal ("what connects to this node") with equal efficiency to the forward direction. Every canonical relationship materialises into both `out_edges` and `in_edges`.
- **by_type** — supports type-scoped seed resolution and traversal-profile validation (e.g. restricting a profile's `start_types` or `allowed_paths` to specific node types without a full scan).
- **by_time** — supports temporal filtering against `created_at`/`valid_from`/`valid_to`, enabling point-in-time graph reconstruction for historical queries.
- **by_trust** — supports trust-tier filtering (for example, a minimum provenance-completeness or review-status threshold) without re-evaluating a node's full provenance chain on every query.

Additional indexes (by tag, by source) may be added where a retrieval policy needs them, following the same pattern: an index exists because a defined query pattern needs it, not speculatively.

---

# Deterministic Multi-Hop Traversal

Traversal proceeds from one or more seed nodes, expanding outward hop by hop, constrained by a traversal profile's allowed predicates, allowed node types, direction and maximum depth. At each hop the engine:

1. filters the current frontier to nodes not yet visited;
2. applies temporal validity against the query time;
3. accepts the node into the result set;
4. resolves the allowed outgoing (or incoming, per profile direction) edges via `out_edges`/`in_edges`;
5. adds unvisited targets to the next frontier.

This repeats until the profile's `max_depth` is reached or the frontier is exhausted.

## Ordering requirement

At every step where the algorithm iterates over a frontier or a set of edges, that iteration must proceed in a fixed, deterministic order (for example, lexicographic ordering of node and edge identifiers) rather than relying on incidental data-structure iteration order.

This matters because:

- **Reproducibility** — the same query against the same vault state and the same traversal profile must produce byte-identical selected nodes, edges and ordering on every run, on every machine. Non-deterministic ordering silently breaks this even when the *set* of selected nodes is correct.
- **Deterministic truncation** — traversal profiles bound results by `max_nodes`/`max_depth`. When a boundary is reached mid-frontier, which nodes get admitted before the cutoff depends entirely on iteration order. Undefined ordering makes truncation effectively random.
- **Auditability** — a reviewer replaying a past query for forensic or scientific verification needs the same context package the original run produced, not an equivalent-but-different one.
- **Stable input to ranking and token budgeting** — downstream ranking and token-budget pruning (below) operate over the candidate list traversal produces; a stable, ordered candidate list is a precondition for those stages themselves being reproducible.

---

# Compiled Graph Artefact and Incremental Recompilation

The vault (Markdown + YAML frontmatter) remains the canonical, human-readable source of truth. The engine never traverses it directly at query time. Instead, `compiler` produces a compiled graph artefact — a persisted, versioned representation of nodes, edges and their indexes — and all queries run against that artefact.

The compiled artefact should not require a full-vault reparse after every edit. Incremental recompilation keeps it synchronised at bounded cost:

```text
file changed
    ↓
hash changed
    ↓
reparse only the changed file
    ↓
remove edges sourced from that file
    ↓
insert newly parsed edges
    ↓
revalidate (schema + ontology)
    ↓
update indexes
```

A per-file content hash (e.g. SHA-256) is the change-detection mechanism: if a file's hash is unchanged since the last compilation, it is skipped entirely. Only files whose hash has changed are reparsed, and only the edges sourced from those specific files are removed and reinserted — the rest of the compiled graph is untouched. Revalidation after reinsertion confirms the updated file still satisfies schema and ontology constraints before the compiled artefact is considered current.

The compiled artefact and its persistence backend are separable concerns: an initial implementation may use in-process structures, with SQLite, DuckDB or a dedicated graph engine as later options, without changing the traversal or ranking logic built on top.

---

# Retrieval Phase Pipeline

`Search-and-Graph-Interfaces.md` defines the retrieval capability's product-level pipeline under "Retrieval Principle":

```text
User/Agent question → Query planning → Deterministic candidate retrieval →
Graph expansion → Temporal/spatial filtering → Evidence/provenance expansion →
Ranking → Context package → LLM reasoning
```

This document defines the implementing detail underneath that pipeline — the full sequence of deterministic phases the engine executes between candidate retrieval and context package delivery:

```text
Seed resolution
    ↓
Traversal profile selection
    ↓
Graph expansion
    ↓
Temporal filtering
    ↓
Trust filtering
    ↓
Provenance expansion
    ↓
Deduplication
    ↓
Context prioritisation
    ↓
Completeness check
    ↓
Token budgeting
    ↓
Context package
```

Each phase corresponds to a named responsibility above (traversal, ranking, completeness, context) and each should emit logs and machine-readable diagnostics, so that a failure can be attributed to a specific phase rather than to "retrieval" as an undifferentiated whole. This document's pipeline does not replace the interface-level pipeline; it is the engine-internal expansion of its "Deterministic candidate retrieval" through "Ranking" stages.

---

# Deterministic Ranking Function

When more context is available than the token budget permits, selection among candidates must not be delegated to the LLM. Ranking uses a documented, versioned scoring function rather than an ad hoc or model-driven cutoff:

```text
score =
    path_proximity_weight
  + node_type_weight
  + evidence_weight
  + trust_weight
  + temporal_weight
  + directness_weight
  + contradiction_weight
```

- **path/proximity weight** — rewards nodes closer to the seed (fewer hops) over more distant ones.
- **node-type weight** — reflects how central a node's ontology type is to the traversal profile's analytical intent.
- **evidence weight** — rewards nodes that carry direct supporting evidence over nodes reached only through intermediate structural links.
- **trust weight** — reflects the node's trust dimensions (see `Evidence-Provenance-and-Trust.md`), such as source authority and provenance completeness.
- **temporal weight** — rewards current, temporally relevant snapshots over superseded or stale ones.
- **directness weight** — distinguishes directly asserted facts from inferred or derived ones.
- **contradiction weight** — ensures contradictory evidence is not suppressed simply because it scores lower on other dimensions; see the interface specification's contradiction-aware retrieval policy.

The exact coefficients for these components are deliberately not fixed by this document. They must be:

- **documented** — the coefficients in force for a given retrieval must be recorded, not implicit;
- **versioned** — recorded as a `ranking_version` alongside the other retrieval-reproducibility fields already required by `Search-and-Graph-Interfaces.md` (index version, graph release, traversal policy, embedding version);
- **testable** — subject to regression tests against reference queries so a coefficient change is a reviewable, evaluable event rather than a silent behavioural shift.

No specific numeric weights are prescribed here; any concrete values elsewhere in draft material are illustrative only and must not be treated as final without their own versioned specification.

---

# Five-Way Failure Classification

The Product Thesis in `CRIC-PRD-MASTER.md` frames CRIC as infrastructure over which "human researchers, deterministic software and autonomous agents operate on the same inspectable evidence base." An incorrect or incomplete answer is only genuinely inspectable if the system can say *where* it went wrong. Collapsing every bad answer into a single "hallucination" bucket is incompatible with that thesis and with forensic, scientific, safety and regulatory use. Because retrieval is now a deterministic, logged pipeline rather than an LLM improvising over files, a failure can and should be attributed to one of five distinct layers:

- **Knowledge failure** — the relevant evidence does not exist anywhere in the vault. This is a gap in what CRIC knows, not a defect in retrieval or reasoning.
- **Retrieval failure** — the evidence exists in the compiled graph, but the deterministic pipeline did not select it (for example: wrong traversal profile, an over-restrictive filter, or a seed-resolution error).
- **Context-construction failure** — the correct nodes and edges were selected, but were mis-rendered, incorrectly prioritised, or dropped during token-budget pruning before reaching the LLM.
- **Reasoning failure** — the LLM received correct, complete context but reasoned incorrectly over it.
- **Generation failure** — the LLM reasoned correctly but its natural-language output misrepresents that reasoning.

This classification is what makes evidence-grade AI auditable in practice: each layer maps to a distinct owner (vault content, traversal/ranking code, context rendering code, the model's reasoning, the model's generation), a distinct remediation, and a distinct test suite. It also underwrites Constitutional Product Rule #2 (traceability of derived values) and Rule #10 (human oversight scaling with uncertainty) by making it possible to say precisely which layer a human reviewer needs to inspect.

---

# Open Gap: Trust / Review-Status Vocabulary

No controlled vocabulary for trust or review-status enum values (for example, distinguishing `machine-confirmed` from `human-reviewed`) currently exists anywhere in the PRD. `Evidence-Provenance-and-Trust.md` and `Claims-Contradictions-and-Knowledge-Lifecycle.md` each list "review status" as a trust or state dimension, but neither enumerates its permitted values. (`Temporal-and-Epistemic-Ontology.md` was also checked — it defines a `review_time` timestamp and describes a "Reviewed and not accepted" case within its `Rejected` knowledge-state, but does not itself carry a "review status" dimension.)

The `by_trust` index and the ranking function's trust weight above both assume such values exist and are comparable/orderable. This document does not invent that enumeration — doing so here, outside the ontology/trust specifications that own the concept, would create a competing and likely inconsistent definition. This is flagged as an open gap and future work: a controlled review-status/trust vocabulary should be specified in the knowledge-tier documents that already own the "review status" dimension, then consumed here.

---

# Retrieval Engine Responsibilities

The deterministic retrieval layer is responsible for:

```text
Seed resolution
Traversal profile selection
Graph traversal
Reverse-edge traversal
Temporal filtering
Trust filtering
Provenance expansion
Evidence expansion
Contradiction retrieval
Deduplication
Relevance scoring
Completeness assessment
Missing-information identification
Token budgeting
Context rendering
Retrieval logging
```

These are software-engineering responsibilities, not LLM responsibilities.

---

# Context Pack Responsibilities

`interfaces/Search-and-Graph-Interfaces.md`'s "Context Package" YAML schema is the single canonical definition of this artefact — registered as the `ContextPack` type in `CRIC-Schema-and-Vocabulary-Registry.md` §3 ("Context Pack" and "Context Package" name the same object; "ContextPack" is its canonical type identifier). This section maps engine-level responsibilities onto that canonical schema's actual field names, rather than restating a parallel list under different names:

| Responsibility | Canonical field(s) |
|---|---|
| Query | `query_id`, `question` |
| Seed entities | `seed_nodes` |
| Temporal scope | `temporal_scope` |
| Relevant nodes | `selected_nodes` |
| Relevant edges | `selected_edges` |
| Observed facts / Derived facts | `claims` and `evidence` entries, each carrying the existing `epistemic_status` tag (observed / derived / etc., per `Temporal-and-Epistemic-Ontology.md`) rather than separate fields |
| Claims | `claims` |
| Evidence | `evidence` |
| Sources | `sources` |
| Contradictory evidence | `contradictions` |
| Uncertainty | `uncertainty` |
| Missing expected information | `missing_expected_information` |
| Completeness assessment | the Retrieval Completeness ✓/✗ table accompanying the pack (a report, not a single field) |
| Retrieval metadata | `retrieval_policy` plus the Retrieval Reproducibility fields (index version, graph release, ranking version, embedding version) |
| Traversal profile | `traversal_profile` |
| Engine version | `engine_version` |

A Pydantic `ContextPack` model must be built against these canonical field names; this table exists so that model and the schema in `Search-and-Graph-Interfaces.md` cannot drift apart. The context pack must be independently inspectable before it reaches the LLM.
