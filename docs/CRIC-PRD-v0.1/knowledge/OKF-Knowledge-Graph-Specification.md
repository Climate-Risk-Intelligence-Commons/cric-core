# CRIC OKF Knowledge Graph Specification

## Purpose

This document defines the canonical Open Knowledge Format representation used by the Climate Risk Intelligence Commons.

The CRIC knowledge graph is stored as Obsidian-compatible Markdown with typed YAML frontmatter.

The Markdown repository itself is a first-class scientific artefact.

It must remain:

- human-readable;
- machine-parseable;
- Git-diffable;
- Obsidian-compatible;
- programmatically traversable;
- agent-friendly;
- versionable;
- provenance-preserving.

---

# Canonical Node Model

Every knowledge node consists of:

```text
YAML frontmatter
+
human-readable Markdown body
+
typed links to other CRIC nodes
```

The YAML frontmatter carries machine-critical structure.

The Markdown body provides:

- human-readable explanation;
- scientific context;
- interpretation;
- notes;
- quotations permitted by licence;
- review commentary;
- supporting explanation.

---

# Universal Frontmatter

Reference base structure:

```yaml
---
okf_version: "0.1"
cric_schema_version: "0.1"
ontology_version: "0.1"

id: "CRIC:knowledge:observation:..."
type: "Observation"
subtype: "LakeAreaObservation"

title: "Lake area observation for ..."
aliases: []

knowledge_state:
  status: candidate
  origin: deterministic_pipeline
  accepted_at:
  rejected_at:
  superseded_at:

temporal:
  event_time:
    start:
    end:
    precision:
  observation_time:
    start:
    end:
    acquisition_time:
  valid_time:
    from:
    to:
  system_time:
    created_at:
    updated_at:
    superseded_at:

spatial:
  geometry:
  geometry_ref:
  centroid:
  bbox:
  crs:
  elevation_m:
  administrative_units: []
  basin_ids: []

epistemic:
  status: observed
  confidence:
  confidence_method:
  uncertainty:
  completeness:

provenance:
  source_nodes: []
  source_uris: []
  parent_nodes: []
  transformations: []
  software:
  software_version:
  agent_run_id:
  human_review_ids: []
  content_sha256:

licensing:
  licence:
  licence_uri:
  attribution:
  redistribution:
  derivative_use:
  notes:

relationships: []

tags: []
---
```

---

# Temporal Semantics

CRIC uses a multi-temporal representation.

## Event Time

Represents when the real-world event occurred.

## Observation Time

Represents when the observation was made or acquired.

## Valid Time

Represents the time interval during which an assertion or state is intended to apply.

## System Time

Represents when CRIC created, changed or superseded the node.

This allows the graph to distinguish:

```text
when something happened
from
when it was observed
from
when it was true
from
when CRIC knew it
```

---

# Time Precision

Allowed values should include:

- exact;
- second;
- minute;
- hour;
- day;
- month;
- year;
- approximate;
- estimated;
- inferred;
- bounded;
- unknown.

---

# Epistemic Status

Recommended controlled vocabulary:

- observed;
- reported;
- derived;
- inferred;
- simulated;
- hypothesised;
- disputed;
- unknown.

Epistemic status is distinct from knowledge workflow status.

---

# Knowledge Workflow Status

Recommended values:

- candidate;
- accepted;
- disputed;
- superseded;
- rejected;
- withdrawn;
- archived.

An accepted claim may still be scientifically uncertain.

A disputed claim remains valid knowledge about an existing scientific disagreement.

---

# Relationship Grammar

Every relationship must support:

```yaml
relationships:
  - predicate: "derived_from"
    target: "CRIC:..."
    confidence: 1.0
    status: accepted
    source_nodes: []
    valid_time:
      from:
      to:
```

## Adjacency Derivation

A relationship needs to be declared on only one of its two participating nodes. The runtime graph compiler derives both directions — `out_edges` on the source and `in_edges` on the target — automatically from that single declaration; an author is never required to also write the paired predicate on the other node. Paired predicate names (e.g. `feeds` / `fed_by`, `supports` / `supported_by`) remain in the vocabulary purely as an authoring convenience, so a relationship can be phrased from whichever node the author happens to be editing. If both directions of what is semantically the same relationship are ever declared independently, the compiler must treat this as a duplicate edge and resolve it through canonical-direction deduplication, not materialise it as two live edges.

Core predicates should include:

- is_a;
- part_of;
- located_in;
- upstream_of;
- downstream_of;
- observed_by;
- derived_from;
- generated_by;
- supports;
- contradicts;
- disputes;
- corroborates;
- refines;
- supersedes;
- superseded_by;
- triggered_by;
- contributes_to;
- affected;
- exposed_to;
- trained_on;
- evaluated_on;
- predicted_by;
- reviewed_by.

`CRIC-Schema-and-Vocabulary-Registry.md` section 8 is the sole authority for the canonical predicate list; the list above is illustrative, not exhaustive.

Domain repositories may extend predicates through ontology proposals.

---

# Atomicity Rule

A separate node should be created when the information has independent:

- provenance;
- temporal validity;
- scientific significance;
- uncertainty;
- contradiction potential;
- graph connectivity;
- training relevance;
- review status.

A scalar field should not automatically become a node.

Example:

```yaml
elevation_m: 5100
```

may remain embedded where appropriate.

However:

> Lake area was measured as 1.42 km² from Sentinel-2 on a specific date

should normally become an observation node because the measurement has independent provenance, time, method and uncertainty.

---

# Node Categories

Minimum CRIC Core categories:

- Entity;
- Event;
- Observation;
- StateSnapshot;
- Dataset;
- DatasetVersion;
- Asset;
- Source;
- Claim;
- Evidence;
- Location;
- Organisation;
- Person;
- Sensor;
- Model;
- ModelCard;
- TrainingSample;
- Label;
- TrainingRun;
- EvaluationRun;
- Prediction;
- Workflow;
- Agent;
- AgentRun;
- Toolset;
- ReviewRequest;
- ReviewDecision;
- ProvenanceRecord;
- Licence;
- QualityAssessment;
- UncertaintyAssessment;
- OntologyProposal.

---

# Persistent Identity Versus State

Persistent entities must not accumulate changing state directly when that state has independent scientific meaning.

Example:

```text
Lake Node
  |
  ├── Observation
  ├── Observation
  ├── Observation
  ├── StateSnapshot
  ├── Claim
  └── Event
```

The lake node represents identity.

Observation nodes represent measured state.

StateSnapshot nodes represent coherent temporal context.

Claim nodes represent scientific assertions.

Event nodes represent real-world occurrences.

---

# StateSnapshot Node

A snapshot should represent a meaningful state of a subject at a defined time.

Reference structure:

```yaml
---
id:
type: StateSnapshot
subject_id:
snapshot_time:
snapshot_window:

included_observations: []
derived_features: []

upstream_context:
  node_ids: []

downstream_context:
  node_ids: []

evidence:
  node_ids: []

quality:
  completeness:
  unresolved_conflicts: []
---
```

Snapshots should be immutable once published. Corrections create a new version or superseding snapshot.

---

# Claims

A claim should support:

```yaml
subject:
predicate:
object:
value:
unit:
claim_text:
claimant:
evidence_nodes:
confidence:
status:
```

CRIC must allow multiple claims about the same subject and predicate.

---

# Contradiction Handling

Contradictory claims must coexist.

Example:

```text
CLAIM-A: trigger = intense precipitation
CLAIM-B: trigger = ice avalanche
```

Relationships may express:

```text
CLAIM-A contradicts CLAIM-B
```

A later assessment may prefer one interpretation without deleting the alternative.

---

# Supersession

A superseded node remains in the graph.

Example:

```yaml
knowledge_state:
  status: superseded
  superseded_at: 2027-03-14

relationships:
  - predicate: superseded_by
    target: CRIC:claim:...
```

This permits reconstruction of historical knowledge states.

---

# Data Asset Nodes

Large files remain outside Git but must have OKF nodes.

Required fields:

- canonical URI;
- original source URI;
- SHA-256;
- byte size;
- media type;
- provider;
- licence;
- acquisition time;
- spatial coverage;
- temporal coverage;
- availability status.

---

# Copyrighted Publications

Scientific papers may be represented as source nodes even when the paper itself cannot be redistributed.

Allowed:

- title;
- authors;
- DOI;
- bibliographic metadata;
- licence;
- source URI;
- CRIC-generated summary;
- structured claims;
- relationships;
- provenance.

Protected content must not be copied beyond lawful limits.

---

# Obsidian Compatibility

The repository should provide:

- wiki-link compatible identifiers or aliases;
- stable filenames;
- optional graph view conventions;
- folder-level indexes;
- generated Maps of Content;
- human-readable titles;
- no proprietary Obsidian plugin dependency for basic reading.

A user should be able to clone `cric-knowledge`, open it as an Obsidian vault and immediately navigate the graph.

---

# Programmatic Parsing

A reference parser must:

- parse YAML safely;
- validate against Pydantic schemas;
- resolve node IDs;
- build adjacency indexes;
- detect broken edges;
- detect duplicate IDs;
- validate temporal structures;
- expose relationship traversal;
- preserve source line/file locations for diagnostics.

---

# Graph Materialisation

Optional materialisations may include:

- DuckDB;
- PostgreSQL/PostGIS;
- NetworkX;
- graph databases;
- full-text indexes;
- vector stores.

None are canonical.

All should be rebuildable from CRIC source artefacts.

---

# Search Modes

CRIC should support:

- filename search;
- ID search;
- field search;
- full-text search;
- relationship traversal;
- temporal query;
- spatial query;
- semantic search;
- provenance-chain traversal;
- contradiction search.

---

# Validation Levels

## Syntax Validation

YAML parses and required fields exist.

## Schema Validation

Pydantic schema passes.

## Ontology Validation

Types and predicates are allowed.

## Graph Validation

Targets resolve.

## Temporal Validation

Times are internally consistent.

## Provenance Validation

Required lineage exists.

## Scientific Review

Separate from structural validation.

---

# File Naming

Recommended pattern:

```text
<type>--<short-human-name>--<id-fragment>.md
```

Example:

```text
lake--south-lhonak--01KXYZ.md
observation--lake-area--01KABC.md
claim--glof-trigger--01KDEF.md
```

Node IDs, not filenames, are the authoritative identifiers.

---

# Versioning

Each node carries:

- OKF version;
- CRIC schema version;
- ontology version.

Schema migrations must not silently rewrite semantic meaning.

---

# Minimum v0.1 Deliverables

- base OKF schema;
- Pydantic validators;
- node parser;
- graph builder;
- broken-edge detector;
- temporal validator;
- example lake;
- example observations;
- example claims;
- example contradiction;
- example event;
- example StateSnapshot;
- example review-linked node;
- Obsidian-ready vault layout.
