# CRIC API and SDK Specification

## Purpose

This document defines the programmatic interfaces through which humans, applications, deterministic pipelines, external models and reusable agents interact with the Climate Risk Intelligence Commons.

The interface layer must preserve CRIC's core guarantees:

- typed schemas;
- provenance;
- temporal semantics;
- knowledge-state visibility;
- deterministic retrieval;
- permission boundaries;
- reproducible graph traversal;
- replaceable storage backends.

The API is not the canonical knowledge store. Canonical knowledge remains represented through CRIC's versioned OKF and data artefacts. API and SDK layers expose controlled views and operations over those artefacts and their materialised indexes.

---

# Interface Principles

## Schema First

Public request and response contracts must be generated from or validated against Pydantic models.

## Stable Identity

Clients interact using CRIC IDs rather than storage paths wherever possible.

## Explicit Knowledge State

Responses must not silently mix:

- candidate;
- accepted;
- disputed;
- superseded;
- rejected

knowledge.

## Temporal Explicitness

Time-sensitive queries must state which temporal dimension is being filtered:

- event time;
- observation time;
- valid time;
- system time.

## Provenance Traversability

Consequential objects returned by the API should expose or link to provenance.

## Storage Independence

Clients should not depend on whether the underlying materialisation is:

- Markdown/OKF;
- DuckDB;
- PostgreSQL/PostGIS;
- object storage;
- search index;
- vector index.

---

# Interface Surfaces

CRIC should provide:

1. Python SDK;
2. REST API;
3. CLI;
4. batch interfaces;
5. event/webhook interfaces where useful;
6. future MCP-compatible interfaces where justified.

---

# Python SDK

Suggested package:

```text
cric-sdk
```

Illustrative usage:

```python
from cric import CRIC

cric = CRIC.from_profile("local")

lake = cric.entities.get("CRIC-LAKE-000123")

observations = cric.observations.query(
    subject_id=lake.id,
    variable="lake_area",
    observation_time=("2020-01-01", "2026-01-01"),
    knowledge_state=["accepted", "disputed"],
)

lineage = cric.provenance.trace(observations[0].id)
```

---

# SDK Modules

Suggested namespaces:

```text
cric.entities
cric.events
cric.observations
cric.snapshots
cric.claims
cric.evidence
cric.datasets
cric.assets
cric.models
cric.agents
cric.reviews
cric.ontology
cric.provenance
cric.search
cric.graph
cric.geo
cric.temporal
```

---

# REST API

Suggested base:

```text
/api/v1/
```

Core resource endpoints:

```text
/entities
/events
/observations
/snapshots
/claims
/evidence
/datasets
/assets
/models
/agents
/reviews
/ontology
/provenance
/search
/graph
```

---

# Resource Retrieval

Example:

```text
GET /api/v1/entities/{id}
```

Response should include:

- canonical ID;
- type;
- title;
- knowledge state;
- temporal metadata;
- relevant relationships;
- schema/ontology version;
- provenance reference.

---

# Observation Query

Example:

```text
GET /api/v1/observations
```

Filters may include:

- subject ID;
- variable;
- method;
- observation-time range;
- system-time range;
- spatial bounds;
- source;
- quality;
- knowledge state.

---

# Historical Knowledge Query

CRIC must support queries equivalent to:

```text
What did CRIC know about lake X on 2026-01-01?
```

This should use system time rather than silently returning today's graph.

---

# Provenance API

Example:

```text
GET /api/v1/provenance/{object_id}/trace
```

Options:

- ancestors;
- descendants;
- depth;
- include transformations;
- include review decisions;
- include model runs.

---

# Graph API

Example operations:

- neighbours;
- bounded traversal;
- shortest semantic path;
- predicate-constrained traversal;
- traversal-profile-selected retrieval;
- temporal graph slice;
- provenance traversal;
- dependency impact traversal.

Predicate-constrained traversal specifies allowed predicates directly. Traversal-profile-selected retrieval instead selects a named, versioned Traversal Profile and lets the profile define the permitted paths:

```python
cric.graph.traverse(
    seed="CRIC-LAKE-001",
    traversal_profile="glacial_lake_risk_assessment",
)
```

Arbitrary unbounded graph traversal should be restricted.

---

# Snapshot API

Operations:

```text
GET /snapshots/{id}
GET /entities/{id}/snapshots
POST /snapshots/build-candidate
```

Candidate snapshot construction may invoke deterministic workflows or authorised agents.

---

# Dataset API

Expose:

- Dataset;
- DatasetVersion;
- manifest;
- assets;
- licence;
- quality;
- spatial/temporal coverage.

Large assets should normally be accessed through signed/local/object-store URLs or storage adapters rather than streamed blindly through the API.

---

# Model API

Expose:

- model registry;
- model card;
- versions;
- training runs;
- evaluation runs;
- predictions;
- provenance.

Inference endpoints should be optional deployment capabilities rather than assumed core behaviour.

---

# Agent API

Agents are first-class resources.

Possible operations:

```text
GET /agents
GET /agents/{agent_id}
POST /agent-runs
GET /agent-runs/{run_id}
POST /agent-runs/{run_id}/resume
```

Agent execution requests must specify or resolve:

- agent version;
- dependency profile;
- toolset;
- dataset context;
- workspace;
- model provider;
- permission profile.

---

# Review API

Expose:

- review queues;
- review requests;
- decisions;
- workflow linkage.

Repository-native review remains canonical where configured. The API may be a view/controller over it.

---

# CLI

Suggested commands:

```text
cric validate
cric search
cric graph
cric provenance
cric dataset
cric agent
cric review
cric ontology
cric snapshot
cric materialise
```

Examples:

```text
cric validate knowledge/
cric provenance trace CRIC-OBS-0012
cric graph neighbours CRIC-LAKE-001 --predicate fed_by
cric search "moraine dam overtopping"
```

---

# Pagination

All list endpoints must support bounded pagination.

Cursor-based pagination is preferred for large mutable indexes.

---

# Errors

Machine-readable error structure:

```yaml
error:
  code:
  message:
  details:
  trace_id:
```

Scientific uncertainty is not an API error.

---

# Authentication and Authorisation

Deployment profiles may include:

- anonymous read-only public access;
- authenticated contributor;
- reviewer;
- maintainer;
- local trusted mode;
- institutional deployment.

Permissions must be capability based where practical.

---

# OpenAPI

FastAPI should generate OpenAPI documentation from typed routes.

Generated documentation must not replace semantic PRD documentation.

---

# Compatibility

API versions and ontology versions are separate.

A client must be able to determine:

- API version;
- schema version;
- ontology version;
- knowledge release version.

---

# Future MCP Interface

A future MCP server may expose CRIC resources and reusable Agent Commons capabilities to external AI clients.

It should reuse the same:

- Pydantic contracts;
- permission system;
- provenance;
- deterministic retrieval layer.

MCP must remain an adapter, not the canonical CRIC architecture.

---

# v0.1 Acceptance Criteria

- Python SDK reads canonical entities;
- REST API exposes core resources;
- OpenAPI is generated;
- graph traversal is bounded;
- historical knowledge queries are possible;
- provenance trace endpoint works;
- agent runs are version-addressable;
- API/storage separation is demonstrated.
