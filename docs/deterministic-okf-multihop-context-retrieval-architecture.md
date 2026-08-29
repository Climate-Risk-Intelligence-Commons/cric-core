# Deterministic Multi-Hop Context Retrieval for an OKF Obsidian Vault

## Purpose

This document defines an architecture for collecting sufficient context from an Open Knowledge Format (OKF) Markdown knowledge base stored in an Obsidian vault, using deterministic multi-hop graph traversal before any context is passed to a Large Language Model (LLM).

The central design principle is:

> **The LLM must not perform graph traversal. Deterministic software must assemble the relevant subgraph first, then hand the resulting context package to the LLM.**

This separates knowledge storage, graph retrieval, provenance management and reasoning into distinct layers.

The result is a system that is more reproducible, auditable, bounded, testable and suitable for evidence-grade scientific, forensic, safety and risk analysis.

---

## Core Architectural Principle

The architecture should be divided into two zones.

### Deterministic zone

This performs:

- Markdown parsing
- YAML frontmatter parsing
- Pydantic schema validation
- Node resolution
- Edge resolution
- Ontology validation
- Multi-hop traversal
- Temporal filtering
- Trust filtering
- Provenance expansion
- Deduplication
- Ranking
- Completeness checks
- Contradiction retrieval
- Missing-information detection
- Token budgeting
- Context package construction

### LLM reasoning zone

This performs:

- Interpretation
- Synthesis
- Explanation
- Hypothesis generation
- Comparison
- Causal reasoning
- Scientific reasoning
- Risk reasoning
- Natural-language output

The LLM should not decide which Markdown file to open next.

The LLM should receive a resolved and bounded knowledge subgraph.

---

## Recommended Overall Architecture

```text
Obsidian / OKF Markdown Vault
            │
            ▼
     Deterministic Parser
            │
            ▼
       Graph Compiler
            │
            ▼
   Persistent Graph Index
            │
            ▼
     Query + Traversal Engine
            │
            ▼
     Context Pack Builder
            │
            ▼
            LLM
```

An extended implementation could look like:

```text
                    OBSIDIAN
                Human knowledge UI
                       │
                       ▼
               OKF Markdown Vault
                       │
                       ▼
                OKF COMPILER
               Python + Pydantic
                       │
          ┌────────────┼─────────────┐
          │            │             │
        schema      ontology      lineage
       validation   validation    validation
          │            │             │
          └────────────┼─────────────┘
                       ▼
                 GRAPH INDEX
                       │
       ┌───────────────┼────────────────┐
       │               │                │
    topology        temporal        provenance
     index           index            index
       │               │                │
       └───────────────┼────────────────┘
                       ▼
              RETRIEVAL ENGINE
                       │
              Traversal Profiles
                       │
                deterministic
                       │
                       ▼
                CONTEXT ENGINE
                       │
              completeness check
                       │
              token-budget pruning
                       │
                       ▼
                  CONTEXT PACK
                       │
             ┌─────────┴─────────┐
             │                   │
            LLM                Human
         reasoning             review
```

---

## Treat the Markdown Vault as the Source of Truth

The Obsidian vault should remain the canonical human-readable knowledge store.

A simplified vault may look like:

```text
Vault/
├── glaciers/
├── lakes/
├── events/
├── settlements/
├── infrastructure/
├── evidence/
├── claims/
├── sources/
└── .obsidian/
```

Each Markdown file represents a node or a structured knowledge object.

Example:

```yaml
---
id: lake:imja
type: GlacialLake
title: Imja Tsho

relations:
  fed_by:
    - glacier:imja
  upstream_of:
    - settlement:dingboche

created_at: 2026-08-28T10:00:00Z
valid_from: 2026-08-26T00:00:00Z
valid_to:

sources:
  - source:sentinel2:2026-08-26
---
```

This representation is excellent for persistence and human inspection.

It should not, however, be used directly as the runtime graph traversal mechanism.

---

## Compile Markdown into a Runtime Graph

The vault should be parsed and compiled into canonical runtime objects.

Example node:

```python
Node(
    id="lake:imja",
    type="GlacialLake",
    attributes={...}
)
```

Example edges:

```python
Edge(
    source="lake:imja",
    predicate="fed_by",
    target="glacier:imja"
)

Edge(
    source="lake:imja",
    predicate="upstream_of",
    target="settlement:dingboche"
)
```

The Markdown parser should therefore be used during indexing or change processing, not during every graph query.

---

## Recommended Python Package Structure

A clean implementation could use:

```text
okf/
├── parser.py
├── schemas.py
├── compiler.py
├── graph.py
├── traversal.py
├── context.py
├── provenance.py
├── temporal.py
├── ranking.py
├── completeness.py
└── validator.py
```

The high-level workflow becomes:

```python
documents = parser.scan(vault)

validated = validator.validate(documents)

graph = compiler.compile(validated)
```

---

## Build Explicit Node and Edge Indexes

The runtime graph should maintain fast indexes.

Recommended structures:

```python
graph.nodes
graph.out_edges
graph.in_edges
graph.by_type
graph.by_tag
graph.by_time
graph.by_source
graph.by_trust
```

Example:

```python
graph.out_edges["lake:imja"]
```

may return:

```python
[
    ("fed_by", "glacier:imja"),
    ("upstream_of", "settlement:dingboche"),
    ("observed_by", "satellite:sentinel2")
]
```

The application should not need to reopen YAML frontmatter to determine those relationships.

---

## Maintain Both Forward and Reverse Adjacency

For every relationship:

```text
A → B
```

maintain both:

```text
A → B
B ← A
```

Recommended structure:

```python
out_edges[source][predicate] -> target IDs
in_edges[target][predicate] -> source IDs
```

This makes forward and reverse graph navigation equally efficient.

Example:

```python
graph.out_edges["lake:imja"]
```

supports questions such as:

> What lies downstream of this lake?

While:

```python
graph.in_edges["lake:imja"]
```

supports questions such as:

> Which glaciers or catchments feed this lake?

---

## Use a Controlled Relationship Ontology

Deterministic traversal requires canonical predicates.

Avoid allowing agents or users to invent arbitrary equivalents such as:

```text
connected_to
linked_to
related_with
associated_with
impacts
affects
near
```

Instead define a controlled vocabulary.

Example predicates:

```text
feeds
drains_to
upstream_of
downstream_of
adjacent_to
located_in
observed_by
derived_from
triggered_by
caused_by
contributes_to
exposes
threatens
contains
depends_on
corroborates
contradicts
supersedes
supported_by
has_snapshot
```

These should be validated through Pydantic.

Example:

```python
from enum import Enum

class RelationType(str, Enum):
    FEEDS = "feeds"
    DRAINS_TO = "drains_to"
    UPSTREAM_OF = "upstream_of"
    DOWNSTREAM_OF = "downstream_of"
    DERIVED_FROM = "derived_from"
    CORROBORATES = "corroborates"
    CONTRADICTS = "contradicts"
```

Unknown predicates should either:

- fail validation, or
- be explicitly placed into an extension namespace.

---

## Do Not Use Blind N-Hop Traversal

A generic operation such as:

```python
get_everything_within_4_hops(node)
```

will rapidly produce graph explosion.

Instead use explicit **Traversal Profiles**.

A traversal profile defines the permitted semantic paths for a particular analytical task.

Example:

```yaml
profile: glacial_lake_risk_assessment

start_types:
  - GlacialLake

allowed_paths:

  - [fed_by, Glacier]

  - [downstream_to, RiverReach]

  - [downstream_to, RiverReach, intersects, Settlement]

  - [downstream_to, RiverReach, intersects, Infrastructure]

  - [has_snapshot, LakeSnapshot]

  - [supported_by, Evidence]

  - [derived_from, Source]

max_depth: 4
```

A query such as:

> Assess downstream GLOF exposure from Imja Tsho.

would invoke:

```python
traverse(
    start="lake:imja",
    profile="glacial_lake_risk_assessment"
)
```

The traversal engine decides what graph paths are legal.

The LLM does not.

---

## Use Graph Query Templates

Over time, the system should maintain a library of deterministic graph query templates.

Examples:

```text
Lake Hazard Profile
Lake Temporal History
Lake Evidence Lineage
Downstream Exposure
Upstream Drivers
Event Reconstruction
Source Corroboration
Claim Verification
Infrastructure Dependency
Settlement Exposure
Sensor History
Model Prediction History
Contradictory Evidence
```

Each query template should define:

- allowed seed node types
- allowed edge types
- edge direction
- maximum depth
- mandatory node types
- optional node types
- temporal constraints
- trust constraints
- provenance requirements
- maximum nodes
- maximum edges
- token budget
- completeness criteria

This makes retrieval reproducible and testable.

---

## Make Temporal Traversal First-Class

Time should be part of graph retrieval rather than a post-processing step.

Recommended metadata:

```yaml
created_at:
valid_from:
valid_to:
```

For a historical query such as:

> What was known about Imja Tsho on 1 August 2026?

apply:

```python
valid_from <= query_time
AND
(
    valid_to is None
    OR valid_to > query_time
)
```

This enables deterministic reconstruction of historical knowledge states.

For example:

```text
2025 snapshot        INCLUDE
2026-07 snapshot     INCLUDE
2026-08-26 snapshot  EXCLUDE
2026-09 snapshot     EXCLUDE
```

This is particularly valuable for:

- accident investigation
- disaster reconstruction
- regulatory analysis
- scientific change detection
- model validation
- decision audit trails

---

## Use Immutable Event and Observation Snapshots

Persistent entities and observations should be separated.

Example persistent entity:

```text
lake:imja
```

Example immutable observations:

```text
lake-snapshot:imja:2026-08-01
lake-snapshot:imja:2026-08-15
lake-snapshot:imja:2026-08-26
```

Graph:

```text
                 lake:imja
                    │
               has_snapshot
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Aug 01      Aug 15      Aug 26
```

Old observations should not be overwritten.

A latest-state query becomes:

```python
latest(
    snapshots_of="lake:imja",
    before=query_time
)
```

This preserves historical evidence.

---

## Separate the Domain Graph from the Evidence Graph

A sophisticated OKF system should treat the domain graph and evidence graph as related but distinct structures.

### Domain graph

```text
Glacier
   ↓ feeds
Lake
   ↓ drains_to
River
   ↓ threatens
Village
```

### Evidence graph

```text
SatelliteImage
       ↓
    Evidence
       ↓
      Claim
       ↓
    Assessment
```

Context retrieval should often traverse both.

Example:

```text
Lake
 ↓
has_snapshot
 ↓
LakeSnapshot
 ↓
supported_by
 ↓
Evidence
 ↓
derived_from
 ↓
Sentinel-2 scene
```

This gives the LLM structured evidence rather than unsupported statements.

A context item may therefore include:

```text
CLAIM
Lake area increased 14%

EVIDENCE
Derived lake polygon comparison

SOURCE
Sentinel-2 scenes

DATES
2025-08-21
2026-08-26

PROCESS
water-boundary-v3

VERIFICATION
human-reviewed
```

---

## Use Deterministic Retrieval Phases

Retrieval should be a pipeline rather than a single graph search.

Recommended phases:

```text
Question
   │
   ▼
Seed Resolution
   │
   ▼
Traversal Profile Selection
   │
   ▼
Graph Expansion
   │
   ▼
Temporal Filtering
   │
   ▼
Trust Filtering
   │
   ▼
Provenance Expansion
   │
   ▼
Deduplication
   │
   ▼
Context Prioritisation
   │
   ▼
Completeness Check
   │
   ▼
Token Budgeting
   │
   ▼
Context Package
```

Each phase should emit logs and machine-readable diagnostics.

---

## Restrict LLM Use During Retrieval

The only potentially non-deterministic step should be the interpretation of natural language into a structured query.

Example:

User asks:

> Could this lake threaten hydropower downstream?

The LLM may transform that into:

```json
{
  "intent": "downstream_infrastructure_exposure",
  "entity": "lake:imja",
  "infrastructure_type": "hydropower"
}
```

After this step, deterministic code should take over.

Where possible, even this intent mapping should be performed through conventional code, rules or an explicit schema.

---

## Return a Structured Context Subgraph

The graph traversal engine should return a typed object, not concatenated Markdown.

Example:

```python
ContextSubgraph(
    query_id="...",
    seed_nodes=[...],
    nodes=[...],
    edges=[...],
    provenance=[...],
    temporal_scope=...,
    exclusions=[...]
)
```

Example serialised form:

```json
{
  "seed": ["lake:imja"],

  "nodes": [
    "lake:imja",
    "snapshot:imja:2026-08-26",
    "glacier:imja",
    "river:imja-khola",
    "settlement:dingboche"
  ],

  "edges": [
    ["glacier:imja", "feeds", "lake:imja"],
    ["lake:imja", "drains_to", "river:imja-khola"],
    ["river:imja-khola", "passes_near", "settlement:dingboche"]
  ]
}
```

Only after this should the application render an LLM-facing context.

---

## Build a Deterministic Context Pack

The final object provided to the LLM should be a bounded context package.

Recommended structure:

```text
CONTEXT PACK

Query
------

Seed entities
-------------

Temporal scope
--------------

Known facts
-----------

Relevant nodes
--------------

Relevant relationships
----------------------

Evidence
--------

Sources
-------

Contradictory evidence
----------------------

Uncertainty
-----------

Missing expected evidence
-------------------------

Traversal metadata
------------------
```

This should be generated programmatically from the ContextSubgraph object.

---

## Preserve Graph Structure in the Prompt

Do not flatten all graph information into prose.

Use an explicit representation such as:

```text
[NODE]
id: lake:imja
type: GlacialLake

[EDGE]
glacier:imja
--feeds-->
lake:imja

[EDGE]
lake:imja
--drains_to-->
river:imja-khola
```

This allows the LLM to reason over topology without being responsible for discovering topology.

---

## Include Traversal Provenance

Every context pack should include retrieval metadata.

Example:

```yaml
retrieval:
  engine_version: 0.3.1

  query_profile:
    downstream_exposure_v2

  seed_nodes:
    - lake:imja

  max_depth: 4

  nodes_considered: 143

  nodes_selected: 31

  edges_selected: 52

  temporal_cutoff:
    2026-08-26T23:59:59Z

  trust_minimum:
    machine_confirmed
```

This allows failures to be classified.

For example:

```text
retrieval failure
```

versus:

```text
reasoning failure
```

This distinction is essential for forensic and evidence-grade AI.

---

## Define Retrieval Completeness

It is impossible to guarantee omniscience.

It is possible to define deterministic retrieval completeness.

Each traversal profile should specify required evidence or context categories.

Example:

```yaml
profile: glacial_lake_risk

required_context:

  - lake_geometry
  - temporal_lake_area
  - upstream_glacier
  - dam_type
  - downstream_topography
  - exposed_settlements
  - exposed_infrastructure
  - meteorology
  - seismic_context
  - historical_events
```

The retrieval engine should then report:

```text
Context completeness

Lake geometry             ✓
Temporal lake area        ✓
Upstream glacier          ✓
Dam type                  ✓
Downstream topography     ✓
Settlements               ✓
Infrastructure            ✓
Meteorology               ✗
Seismic context           ✓
Historical events         ✓
```

The LLM should therefore know that meteorological context was unavailable.

This prevents silent reasoning over absent information.

---

## Detect Missing Expected Nodes

The ontology can define expected relationships or node categories.

Example:

```text
GlacialLake
    SHOULD HAVE
        geometry_snapshot
        dam_type
        downstream_reach
        observation_source
```

If a required object is missing, the context engine should explicitly return:

```text
EXPECTED BUT ABSENT

dam_type
```

This tells the model not to infer the missing fact.

Absence should be represented as information.

---

## Retrieve Contradictory Evidence Deliberately

The retrieval engine should not optimise only for supporting evidence.

If a claim has:

```text
evidence:E1 → corroborates
evidence:E2 → corroborates
evidence:E3 → contradicts
```

all relevant evidence should be retrieved.

Traversal profiles can explicitly require:

```yaml
evidence_edges:
  - supports
  - corroborates
  - contradicts
  - disputes
```

This is especially important in:

- forensic analysis
- scientific research
- safety investigations
- intelligence analysis
- regulatory review
- model validation

---

## Use Graph Retrieval Before Vector Retrieval

Embeddings should not be the primary retrieval mechanism.

A better conceptual priority is:

```text
Graph retrieval
    +
Metadata filtering
    +
Temporal filtering
    +
Full-text retrieval
    +
Vector retrieval
```

Graph retrieval answers:

> What is structurally relevant?

Vector retrieval answers:

> What semantically similar information may also be useful?

Vector retrieval should therefore augment the evidence architecture rather than define it.

---

## Recommended Hybrid Retrieval Strategy

```text
               User query
                   │
           Entity resolution
                   │
                   ▼
             Graph traversal
                   │
          ┌────────┴────────┐
          │                 │
     deterministic       semantic
       neighbours        candidates
          │                 │
          └────────┬────────┘
                   │
             merge + filter
                   │
             provenance
                   │
             Context Pack
                   │
                  LLM
```

An additional safeguard can require semantic candidates to attach to a known graph entity or evidence object before admission into the final context.

---

## Deterministic Ranking

If too much context is available, do not ask an LLM to choose what to keep.

Use a documented scoring function.

Example:

```text
score =
    path_weight
  + node_type_weight
  + evidence_weight
  + trust_weight
  + temporal_weight
  + directness_weight
```

Possible weights:

```text
Direct evidence         +10
One-hop node             +8
Two-hop node             +5
Three-hop node           +2
Human-reviewed           +5
Machine-confirmed        +3
Current snapshot         +4
Superseded snapshot      -4
Contradictory evidence   +6
```

The exact coefficients can evolve.

What matters is that they are:

- documented
- versioned
- testable
- reproducible

---

## Deterministic Multi-Hop Traversal Algorithm

A simple traversal engine may look like:

```python
def traverse(
    graph,
    seeds,
    profile,
    query_time=None
):

    visited = set()
    frontier = list(seeds)
    results = []

    for depth in range(profile.max_depth):

        next_frontier = []

        for node_id in sorted(frontier):

            if node_id in visited:
                continue

            visited.add(node_id)

            node = graph.nodes[node_id]

            if not temporal_valid(
                node,
                query_time
            ):
                continue

            results.append(node)

            edges = allowed_edges(
                graph,
                node_id,
                profile
            )

            for edge in sorted(edges):

                if edge.target not in visited:
                    next_frontier.append(
                        edge.target
                    )

        frontier = next_frontier

    return results
```

The use of deterministic ordering such as:

```python
sorted(...)
```

is important.

If reproducibility matters, traversal ordering should also be reproducible.

---

## Start with Simple Graph Storage

A specialised graph database is not initially required.

Python dictionaries can support very large graphs efficiently.

Example:

```python
nodes: dict[str, Node]

out_edges:
dict[str, dict[str, set[str]]]

in_edges:
dict[str, dict[str, set[str]]]
```

Example:

```python
out_edges = {
    "lake:imja": {
        "drains_to": {
            "river:imja-khola"
        },

        "has_snapshot": {
            "snapshot:imja:2026-08-26"
        }
    }
}
```

Possible later backends include:

```text
SQLite
DuckDB
NetworkX
Kùzu
Neo4j
PostgreSQL
```

The persistence format and runtime graph engine should remain separable.

---

## Create a Compiled Graph Artefact

A compiled graph cache can be stored separately from the Markdown vault.

Example:

```text
.vault-index/
    nodes.msgpack
    edges.msgpack
    temporal.idx
    types.idx
    provenance.idx
    hashes.json
```

The system becomes:

```text
Markdown vault
      │
      │ changes
      ▼
incremental compiler
      │
      ▼
compiled graph
```

Queries operate against the compiled graph rather than directly against Markdown.

---

## Use Incremental Recompilation

The whole vault should not need to be reparsed after every edit.

Maintain a hash such as:

```text
SHA-256(file contents)
```

Example index entry:

```yaml
events/imja.md:
  hash: e47...
  compiled_at: ...
```

When Obsidian saves a note:

```text
file changed
    ↓
hash changed
    ↓
reparse file
    ↓
remove old edges
    ↓
insert new edges
    ↓
validate
```

This allows the graph index to remain synchronised with the vault efficiently.

---

## Recommended LLM Boundary

The LLM should have read access only through the context retrieval service.

Preferred architecture:

```text
LLM READ ACCESS
      ↓
Context Pack API only

NOT

LLM
 ↓
filesystem
 ↓
vault
```

The same principle should be applied to writes.

Preferred flow:

```text
LLM WRITE REQUEST
       ↓
Structured proposed mutation
       ↓
Pydantic
       ↓
validation
       ↓
human / policy check
       ↓
atomic Markdown write
```

This protects the knowledge graph from uncontrolled model behaviour.

---

## Recommended LLM Prompt Contract

The LLM can be told:

```text
You are provided with a deterministically assembled
knowledge subgraph.

Do not assume information outside this context.

Distinguish:

- observed facts
- derived facts
- claims
- hypotheses
- missing evidence
- contradictory evidence

Reference node IDs when making material claims.
```

Then provide:

```text
<context-pack>
...
</context-pack>
```

The model becomes a reasoner over evidence rather than a retrieval agent.

---

## Retrieval Engine Responsibilities

The deterministic retrieval layer should therefore be responsible for:

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

## Context Pack Responsibilities

The Context Pack should expose:

```text
Query
Seed entities
Temporal scope
Relevant nodes
Relevant edges
Observed facts
Derived facts
Claims
Evidence
Sources
Contradictory evidence
Uncertainty
Missing expected information
Completeness assessment
Retrieval metadata
Traversal profile
Engine version
```

The context pack should be independently inspectable before it reaches the LLM.

---

## Why This Architecture Matters

This architecture provides several important properties.

### Reproducibility

The same:

```text
query
+
vault state
+
traversal profile
+
retrieval engine version
```

should generate the same context package.

### Auditability

A reviewer can inspect:

- which nodes were selected
- which nodes were excluded
- which paths were followed
- which evidence was used
- which evidence contradicted the result
- what information was missing

### Model independence

Claude, GPT, Gemini, local models or future models can be replaced without redesigning the knowledge infrastructure.

### Reduced hallucination risk

The model is not navigating arbitrary files or inventing graph paths.

### Evidence integrity

Every material claim can remain connected to evidence, provenance and source nodes.

### Temporal reconstruction

Historical states can be recreated without overwriting prior evidence.

### Controlled context size

Token budgets can be handled programmatically and reproducibly.

### Better failure analysis

Failures can be classified as:

```text
knowledge failure
retrieval failure
context construction failure
reasoning failure
generation failure
```

This is much more valuable than treating every incorrect model answer as a generic hallucination.

---

## Recommended Design Principle

The final design principle should be:

> **The Obsidian vault is the human-readable source of truth. The compiled graph is the machine retrieval representation. The Context Pack is the only knowledge interface presented to the LLM.**

This creates three clean layers:

```text
Knowledge persistence
      ↓
OKF Markdown

Machine retrieval
      ↓
Compiled deterministic graph

Machine reasoning
      ↓
LLM over Context Pack
```

The resulting system should not be thought of merely as an Obsidian vault that an AI can read.

It should be treated as a deterministic, provenance-aware knowledge infrastructure over which AI performs bounded reasoning.

---

## Recommended Next Architectural Components

The natural next components to define are:

```text
OKF Node Schema
OKF Edge Schema
Relationship Ontology
Traversal Profile Schema
ContextSubgraph Schema
Context Pack Schema
Completeness Rules
Trust Model
Temporal Model
Evidence and Provenance Model
Incremental Graph Compiler
Retrieval Engine API
LLM Context Contract
```

These components can all be expressed using Pydantic models and versioned as first-class artefacts of the knowledge platform.
