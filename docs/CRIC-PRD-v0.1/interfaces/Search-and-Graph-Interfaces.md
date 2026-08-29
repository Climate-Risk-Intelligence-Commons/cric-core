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
contradictions: []
provenance_roots: []
temporal_scope:
spatial_scope:
retrieval_policy:
truncation:
```

This package itself should be inspectable.

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
