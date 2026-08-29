# CRIC Repository and System Architecture

## Purpose

This document defines the repository boundaries, dependency hierarchy, deployment model and cross-repository contracts for the Climate Risk Intelligence Commons.

---

# Architectural Model

CRIC is a multi-repository ecosystem.

Repositories are divided by durable responsibility rather than by temporary project team.

```text
cric-core
   ↓
cric-knowledge
cric-data
cric-ingest
cric-agents
cric-cryosphere
cric-glof
cric-models
cric-api
cric-ui
cric-review
cric-docs
```

`cric-core` provides the foundational contracts on which the remaining repositories depend.

---

# Repository Dependency Rules

## `cric-core`

May not depend on any domain-specific repository.

Contains:

- base Pydantic models;
- OKF schema models;
- identifiers;
- base node types;
- temporal structures;
- epistemic structures;
- provenance structures;
- licensing structures;
- controlled vocabularies;
- climate-risk core ontology;
- validators;
- migration helpers.

## `cric-knowledge`

Depends on `cric-core`.

Contains the canonical public OKF Markdown graph.

Must be useful without running CRIC software.

## `cric-data`

Depends on `cric-core`.

Contains:

- dataset manifests;
- acquisition recipes;
- licences;
- metadata;
- STAC references;
- sample data;
- derived dataset manifests.

Large data should generally remain outside Git.

## `cric-ingest`

Depends on `cric-core` and may interact with `cric-data`.

Contains deterministic acquisition and normalisation pipelines.

## `cric-agents`

Depends on `cric-core`.

May optionally depend on published domain packages.

Contains reusable Pydantic AI agent factories, dependency types, toolsets, structured output models, workspaces, evaluations and agent manifests.

## `cric-cryosphere`

Depends on `cric-core`.

Contains cryosphere ontology and deterministic cryosphere processing.

## `cric-glof`

Depends on `cric-core` and `cric-cryosphere`.

Contains GLOF ontology, event models, state snapshots, benchmark definitions and GLOF-specific workflows.

## `cric-models`

Depends on `cric-core` and published domain packages.

Contains model training and evaluation infrastructure.

## `cric-review`

Depends on `cric-core`.

Contains human review artefacts and review workflow schemas.

## `cric-api`

Depends on published schemas and services.

Must not become the source of truth.

## `cric-ui`

Consumes APIs, static knowledge artefacts and materialised indexes.

## `cric-docs`

Documentation only.

---

# Recommended GitHub Organisation Layout

```text
github.com/climate-risk-intelligence-commons/
├── cric-core
├── cric-knowledge
├── cric-data
├── cric-ingest
├── cric-agents
├── cric-cryosphere
├── cric-glof
├── cric-models
├── cric-review
├── cric-api
├── cric-ui
└── cric-docs
```

---

# Local Deployment Model

A user may clone only the repositories required for a particular task.

Example minimal knowledge deployment:

```text
cric-core
cric-knowledge
```

Example research-agent deployment:

```text
cric-core
cric-knowledge
cric-data
cric-agents
```

Example full GLOF research deployment:

```text
cric-core
cric-knowledge
cric-data
cric-ingest
cric-agents
cric-cryosphere
cric-glof
cric-models
cric-review
cric-api
cric-ui
```

---

# Canonical Versus Materialised Data

Canonical artefacts include:

- OKF Markdown;
- schema definitions;
- immutable manifests;
- provenance records;
- source metadata;
- training dataset manifests;
- model cards;
- review decisions.

Materialised derivatives may include:

- DuckDB;
- PostgreSQL/PostGIS;
- search indexes;
- vector stores;
- graph databases;
- parquet caches;
- API caches.

Materialised representations must be regenerable.

---

# Large Data Policy

Git is not the default storage for:

- raw satellite products;
- DEM rasters;
- hydrodynamic rasters;
- large training tensors;
- model weights;
- large time-series archives.

These objects are referenced through immutable asset nodes.

Each asset record must contain:

```yaml
id:
type: DataAsset
uri:
source_uri:
sha256:
size_bytes:
media_type:
provider:
licence:
redistribution:
temporal_coverage:
spatial_coverage:
retrieved_at:
availability_status:
```

---

# Repository Releases

Each repository should use semantic versioning unless a repository-specific reason requires another model.

Every release should generate where applicable:

- Git tag;
- release notes;
- schema version;
- ontology version;
- migration notes;
- content manifest;
- checksums;
- `CITATION.cff`.

---

# Cross-Repository Identifiers

CRIC identifiers must be globally unique inside the CRIC namespace.

Recommended form:

```text
CRIC:<namespace>:<type>:<ulid>
```

Example:

```text
CRIC:core:claim:01K...
CRIC:glof:event:01K...
CRIC:knowledge:observation:01K...
```

Human-readable aliases may coexist.

---

# Interface Contracts

Cross-repository communication should occur through:

- published Pydantic models;
- JSON Schema;
- OKF Markdown;
- GeoJSON;
- GeoParquet;
- STAC;
- typed Python packages;
- REST/OpenAPI;
- optional MCP interfaces.

Repository internals should not be imported across boundaries when a public interface exists.

---

# Branching and Contribution

Recommended branches:

- `main` for released and review-complete work;
- normal feature branches;
- pull requests for all stable ontology changes.

Domain repositories may experiment freely without modifying `cric-core`.

Core ontology changes require:

- proposal;
- compatibility analysis;
- tests;
- migration impact;
- maintainer approval.

---

# Human Review Repository

`cric-review` is a first-class workflow repository.

Reference structure:

```text
review/
├── inbox/
├── assigned/
├── in-review/
├── approved/
├── rejected/
├── needs-more-evidence/
├── disputed/
├── escalated/
└── archived/
```

Each bundle must be machine-readable enough for an agent to detect its status and resume automatically.

---

# Local Agent Workspaces

Agents must not write arbitrary intermediate files into canonical repositories.

Each execution receives an isolated workspace:

```text
.workspaces/
└── <run-id>/
    ├── input/
    ├── scratch/
    ├── output/
    ├── logs/
    └── proposed-changes/
```

Only approved outputs are promoted into canonical locations.

---

# v0.1 Architectural Requirement

v0.1 must demonstrate that the multi-repository architecture is real, even if only a subset of repositories contains substantial functionality.

At minimum:

- `cric-core`;
- `cric-knowledge`;
- `cric-agents`;
- `cric-cryosphere`;
- `cric-glof`;
- `cric-review`;
- `cric-docs`

should exist with functioning interfaces and documentation.
