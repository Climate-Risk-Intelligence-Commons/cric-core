# CRIC Search and Graph Interfaces Specification

## Purpose

This document defines how humans, applications and agents retrieve relevant CRIC knowledge deterministically without requiring an LLM to manually open individual Markdown files and improvise multi-hop navigation.

The retrieval architecture must exploit the explicit graph, ontology, temporal model, spatial model and provenance encoded in OKF.

---

# Retrieval Principle

The LLM should receive a bounded evidence package produced by deterministic retrieval wherever possible.

Reference pattern:

```text
User/Agent question
↓
Query planning
↓
Deterministic candidate retrieval
↓
Graph expansion
↓
Temporal/spatial filtering
↓
Evidence/provenance expansion
↓
Ranking
↓
Context package
↓
LLM reasoning
```

The LLM is not the primary graph crawler.

---

# Canonical and Materialised Graph

Canonical knowledge:

```text
OKF Markdown nodes
```

Materialised indexes may include:

- DuckDB;
- PostgreSQL/PostGIS;
- adjacency index;
- full-text index;
- vector index;
- geospatial index.

All materialisations must be regenerable.

---

# Search Modes

CRIC should support:

- ID lookup;
- exact metadata lookup;
- full-text search;
- ontology/type search;
- graph search;
- spatial search;
- temporal search;
- provenance search;
- semantic/vector search;
- hybrid search.

---

# Deterministic Multi-Hop Navigation

A graph traversal request should specify:

- seed nodes;
- allowed predicates;
- allowed node types;
- maximum depth;
- direction;
- temporal filters;
- knowledge-state filters;
- maximum nodes;
- evidence-expansion policy.

Example:

```yaml
seed:
  - CRIC-LAKE-001
max_depth: 3
allowed_predicates:
  - fed_by
  - exposed_to
  - experienced
  - supported_by
knowledge_state:
  - accepted
  - disputed
max_nodes: 100
```

## Traversal Profiles

Ad hoc traversal requests do not scale to reproducible, auditable retrieval. A production traversal request should reference a named, versioned **Traversal Profile** rather than restating seed, path and depth parameters inline each time.

A traversal profile declares:

- profile name;
- profile version;
- start_types (permitted seed node types);
- allowed_paths (permitted sequences of predicate and node type);
- max_depth.

`allowed_paths` enumerates the legal predicate/node-type sequences a traversal may follow from a seed node; any path not listed is not traversed. Changing `allowed_paths` or `max_depth` for a named profile requires a new profile version, so that a context package can always be reproduced from the `(query, vault state, traversal profile, engine version)` tuple recorded in its retrieval metadata.

Example profile:

```yaml
profile: glacial_lake_risk_assessment
version: 1

start_types:
  - GlacialLake

allowed_paths:
  - [fed_by, Glacier]
  - [drains_to, RiverReach]
  - [drains_to, RiverReach, exposed_to, Settlement]
  - [drains_to, RiverReach, exposed_to, Infrastructure]
  - [has_snapshot, StateSnapshot]
  - [supported_by, Evidence]
  - [derived_from, Source]

max_depth: 4
```

A traversal request then reduces to a profile reference plus concrete seeds:

```yaml
seed:
  - CRIC-LAKE-001
profile: glacial_lake_risk_assessment
profile_version: 1
```

The traversal engine, not the LLM, decides which of the profile's paths are legal for a given request.

---

# Edge Index

Every canonical relationship should materialise into an edge table:

```text
source_id
predicate
target_id
edge_metadata
source_file
ontology_version
knowledge_state
```

This allows deterministic traversal without parsing every YAML frontmatter block during each request.

---

# Per-Node Edge Pages

CRIC knowledge exports may generate Obsidian-friendly edge/index pages for human navigation.

These are derived artefacts and can be regenerated.

---

# Search Result Object

Every result should expose:

- node ID;
- title;
- type;
- score;
- match reason;
- knowledge state;
- relevant time;
- provenance status;
- graph path where applicable.

---

# Context Package

The retrieval layer should produce a structured context package for an LLM or agent.

Example:

```yaml
query_id:
question:
seed_nodes: []
selected_nodes: []
selected_edges: []
claims: []
evidence: []
sources: []
contradictions: []
provenance_roots: []
temporal_scope:
spatial_scope:
retrieval_policy:
traversal_profile:
engine_version:
truncation:
uncertainty: []
missing_expected_information: []
exclusions: []
```

This package itself should be inspectable.

`evidence` and `sources` are exposed as explicit top-level fields rather than being reachable only indirectly through `provenance_roots` or nested inside `claims`, so supporting evidence and the sources it derives from can be inspected directly.

`traversal_profile` records the name and version of the Traversal Profile (see Traversal Profiles) used to produce this package, and `engine_version` records the version of the retrieval engine that produced it; together with `query_id` these support the `(query, vault state, traversal profile, engine version)` reproducibility tuple described above.

Each entry in `claims` and `evidence` carries the `epistemic_status` tag already defined in `Temporal-and-Epistemic-Ontology.md` (observed / reported / derived / inferred / simulated / hypothesised / disputed / unknown), so the LLM can distinguish observed from derived facts using that existing controlled vocabulary rather than a new one.

`uncertainty`, `missing_expected_information` and `exclusions` make explicit what the retrieval engine could not resolve or deliberately left out, so the LLM is told what context was unavailable rather than being left to infer completeness silently.

---

# Retrieval Policies

Different tasks require different graph expansions.

Examples:

## Scientific Claim Review

Expand:

- claim;
- supporting evidence;
- contradicting claims;
- sources;
- provenance;
- reviews.

## Lake State Review

Expand:

- lake;
- relevant snapshots;
- observations;
- glacier;
- dam;
- trigger context;
- provenance.

## Model Audit

Expand:

- model;
- training run;
- dataset version;
- samples;
- labels;
- source evidence.

## Query Templates

Each retrieval policy should be maintained as a named, versioned **Query Template** rather than an informal expansion list. A query template declares:

- allowed seed node types;
- allowed edge types;
- edge direction;
- maximum depth;
- mandatory node types;
- optional node types;
- temporal constraints;
- trust constraints;
- provenance requirements;
- maximum nodes;
- maximum edges;
- token budget;
- completeness criteria.

The three retrieval policies above restate in this structured form as follows.

## Query Template: Scientific Claim Review

```yaml
query_template: scientific_claim_review
version: 1
allowed_seed_types:
  - Claim
allowed_edge_types:
  - supported_by
  - contradicts
  - corroborates
  - derived_from
  - observed_by
edge_direction: both
max_depth: 3
mandatory_node_types:
  - Evidence
  - Source
optional_node_types:
  - Claim
  - Assessment
temporal_constraints:
  respect_valid_time: true
trust_constraints:
  minimum_knowledge_state: disputed
provenance_requirements:
  minimum_provenance: complete
max_nodes: 150
max_edges: 300
token_budget: 4000
completeness_criteria:
  - supporting_evidence_present
  - contradicting_claims_checked
  - source_chain_resolved
```

## Query Template: Lake State Review

```yaml
query_template: lake_state_review
version: 1
allowed_seed_types:
  - GlacialLake
allowed_edge_types:
  - has_snapshot
  - fed_by
  - dammed_by
  - triggered_by
  - observed_by
  - derived_from
edge_direction: both
max_depth: 3
mandatory_node_types:
  - StateSnapshot
  - Observation
optional_node_types:
  - Glacier
  - MoraineDam
  - IceDam
  - Trigger
temporal_constraints:
  valid_at: query_time
trust_constraints:
  minimum_knowledge_state: accepted
provenance_requirements:
  minimum_provenance: complete
max_nodes: 120
max_edges: 250
token_budget: 3500
completeness_criteria:
  - latest_snapshot_included
  - glacier_context_checked
  - dam_type_known
```

## Query Template: Model Audit

```yaml
query_template: model_audit
version: 1
allowed_seed_types:
  - Model
allowed_edge_types:
  - derived_from
  - observed_by
  - supported_by
edge_direction: forward
max_depth: 4
mandatory_node_types:
  - ModelRun
  - DatasetVersion
optional_node_types:
  - TrainingSample
  - Label
  - Evidence
temporal_constraints:
  respect_valid_time: true
trust_constraints:
  include_unverified: true
  mark_unverified: true
provenance_requirements:
  minimum_provenance: complete
max_nodes: 200
max_edges: 400
token_budget: 5000
completeness_criteria:
  - training_run_resolved
  - dataset_version_resolved
  - sample_lineage_traceable
```

---

# Temporal Search

Queries must distinguish:

- event-time interval;
- observation-time interval;
- valid-time interval;
- system-time interval.

Example:

```text
Find observations acquired before the GLOF but only using evidence CRIC possessed by 1 January 2026.
```

---

# Spatial Search

Capabilities:

- bounding box;
- radius;
- polygon;
- basin;
- upstream/downstream network;
- intersection;
- nearest feature.

Spatial predicates should use deterministic GIS.

---

# Hybrid Retrieval

Semantic embeddings may improve recall.

They must not replace exact graph constraints.

Recommended sequence:

1. metadata/ontology filter;
2. lexical/vector candidate retrieval;
3. graph expansion;
4. provenance/evidence enrichment;
5. bounded ranking.

---

# Vector Index

Embeddings are derived indexes.

Each embedding should identify:

- source node;
- text representation version;
- embedding model;
- model version;
- generated time.

Vector indexes must be rebuildable.

---

# Contradiction-Aware Retrieval

When a selected claim has known contradictions, retrieval policy should normally include them.

The system should not present only the highest-ranked claim and conceal known disagreement.

---

# Provenance-Aware Retrieval

High-impact retrieval may require minimum provenance completeness.

Example policy:

```yaml
minimum_provenance: complete
include_unverified: true
mark_unverified: true
```

---

# Evidence Budget

Context construction must operate within bounded token/data budgets.

Ranking should prioritise:

- direct evidence;
- graph proximity;
- temporal relevance;
- source relevance;
- contradiction coverage;
- provenance completeness.

---

# Retrieval Completeness

Retrieval cannot guarantee omniscience, but it can guarantee a deterministic account of what was and was not found.

Each traversal profile or query template may declare a `required_context` checklist naming the context categories a complete answer should be able to draw on. Example, for the `glacial_lake_risk_assessment` traversal profile:

```yaml
profile: glacial_lake_risk_assessment
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

For every retrieval, the engine should report a completeness table against this checklist rather than leaving gaps implicit:

```text
Context completeness

Lake geometry             ✓
Temporal lake area        ✓
Upstream glacier          ✓
Dam type                  ✓
Downstream topography     ✓
Exposed settlements       ✓
Exposed infrastructure    ✓
Meteorology               ✗
Seismic context           ✓
Historical events         ✓
```

This table should be carried in the context package alongside `missing_expected_information`, so the LLM is told explicitly that, for example, meteorological context was unavailable rather than being left to reason silently over the gap.

Retrieval completeness is a property of the retrieval engine and its declared checklist; it does not certify that the underlying evidence itself is complete.

---

# Retrieval Reproducibility

A context package should record enough information to reproduce:

- index version;
- graph release;
- query;
- traversal policy;
- ranking version;
- embedding version where used.

---

# Agent Tool

The Agent Commons should expose retrieval as a reusable typed tool rather than allowing each agent to invent its own vault-navigation logic.

---

# Example Queries

CRIC should support:

- all observations used to derive feature X;
- all claims contradicting trigger interpretation Y;
- what CRIC knew about event E on date X;
- all StateSnapshots used to train model M;
- all lakes exposed to avalanche paths in basin B;
- all derived nodes dependent on retracted source S;
- all candidate ontology concepts encountered during GLOF ingestion.

---

# v0.1 Acceptance Criteria

- OKF graph materialises into an edge index;
- deterministic multi-hop traversal works;
- traversal is bounded;
- context packages are machine-readable;
- contradictions are retrievable;
- temporal and spatial filters work;
- vector search is optional rather than required;
- an LLM can receive relevant graph context without opening files one by one.
