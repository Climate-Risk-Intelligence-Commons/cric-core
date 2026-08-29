# CRIC Software Architecture Specification

## Purpose

This document defines the implementation architecture supporting the CRIC knowledge, data, model, agent and interface layers.

The architecture should favour open standards, replaceable components, deterministic computation and local deployment.

---

# Architectural Layers

```text
Human Applications
API / SDK / CLI
Agent Commons
Scientific Workflows
Model Commons
Retrieval / Graph / Search
Materialised Data Services
OKF Knowledge Commons + Data Commons
Storage
```

Cross-cutting:

- Pydantic schemas;
- provenance;
- temporal semantics;
- permissions;
- validation;
- HITL;
- ontology.

---

# Language

Python 3.12+ is the primary backend/scientific language.

TypeScript is preferred for the web frontend.

---

# Schema Authority

Pydantic is the runtime schema authority.

Uses:

- OKF validation;
- API contracts;
- agent dependencies;
- agent outputs;
- review artefacts;
- dataset manifests;
- ontology proposals;
- model metadata.

Generated JSON Schema should be published.

---

# Agent Runtime

CRIC should use modular Pydantic-based agents.

No mandatory orchestration framework such as LangGraph is required.

Agent execution should compose:

```text
Agent Definition
+ Instructions
+ Dependency Object
+ Toolsets
+ Dataset Context
+ Workspace
+ Model Provider
+ Output Schema
+ Permission Profile
```

This keeps agents reusable across applications and workflows.

---

# Deterministic Workflow Layer

Use ordinary Python for:

- ingestion;
- hashing;
- validation;
- geospatial computation;
- feature generation;
- indexing;
- graph materialisation;
- dataset construction.

LLM agents should not replace deterministic code where deterministic code is suitable.

---

# Backend API

FastAPI is preferred.

Benefits:

- Pydantic integration;
- OpenAPI;
- asynchronous interfaces;
- typed request/response contracts.

---

# Geospatial Stack

Preferred:

- GeoPandas;
- Shapely;
- Rasterio;
- Xarray;
- PyProj;
- PySTAC / pystac-client.

---

# Analytical Storage

Initial local analytical store:

- DuckDB;
- DuckDB spatial where suitable.

Larger deployments:

- PostgreSQL;
- PostGIS.

The application layer should minimise backend-specific coupling.

---

# Knowledge Storage

Canonical:

```text
Markdown + YAML frontmatter
```

Materialised:

- relational tables;
- edge indexes;
- search indexes;
- vector indexes.

---

# Large Asset Storage

Supported adapters should include:

- local filesystem;
- S3-compatible object storage;
- remote HTTP/STAC reference.

---

# Frontend

Preferred:

- React;
- Vite;
- TypeScript;
- MapLibre GL JS.

---

# Repository Architecture

Expected repositories include:

```text
cric-core
cric-knowledge
cric-data
cric-ingest
cric-cryosphere
cric-glof
cric-models
cric-agents
cric-api
cric-ui
cric-docs
```

`cric-review` is recommended where shared HITL workflow warrants independent permissions and lifecycle.

---

# Dependency Direction

Preferred:

```text
cric-core
↑
domain packages
↑
ingest/models/agents
↑
api/ui
```

Higher-level repositories must not redefine core schemas.

---

# Workspace Isolation

Agent runs should receive isolated workspaces.

Suggested:

```text
workspaces/
  <run-id>/
    input/
    working/
    output/
    logs/
    state/
```

Agents should not receive unrestricted repository write access by default.

---

# Dependency Injection

Runtime dependencies should be injected.

Examples:

- graph store;
- dataset registry;
- object storage;
- model provider;
- review repository;
- Git service.

This supports local and institutional deployment without rewriting agent logic.

---

# Configuration

Configuration precedence may be:

1. defaults;
2. repository profile;
3. deployment profile;
4. environment;
5. explicit runtime overrides.

Secrets must not enter committed configuration.

---

# Observability

Every workflow/agent run should generate:

- run ID;
- timestamps;
- structured logs;
- input/output references;
- errors;
- provenance;
- performance metrics where useful.

---

# Durable Workflow State

Long-running workflows should persist state.

Especially when waiting for HITL, the process should terminate cleanly and resume later.

---

# Background Processing

CRIC should not require a distributed task queue in v0.1.

Interfaces should permit later adapters to:

- Celery;
- Dramatiq;
- cloud queues;
- Kubernetes jobs.

---

# Containers

Docker should support reproducible development and deployment.

Avoid making containers mandatory for simple local knowledge-base use.

---

# CI/CD

GitHub Actions should initially run:

- formatting/linting;
- unit tests;
- schema tests;
- ontology validation;
- OKF validation;
- provenance checks;
- licence checks;
- security scanning;
- build tests.

---

# Testing Pyramid

- unit tests;
- schema fixtures;
- deterministic integration tests;
- agent tests with mocked models;
- limited live-model evaluations;
- end-to-end reference workflows.

---

# Model Provider Abstraction

Agents should not be tied to one LLM provider.

Provider configuration belongs in runtime dependencies/configuration.

Local models should be supported where compatible.

---

# Reproducible Environments

Projects should pin dependencies through an appropriate Python package-management workflow and lock files.

Model and scientific runs should record environment information.

---

# Performance

Optimise first for:

- correctness;
- reproducibility;
- bounded retrieval;
- batch efficiency.

Do not prematurely introduce distributed complexity.

---

# v0.1 Deployment Profiles

## Knowledge-Only

Obsidian + Markdown.

## Local Research Workstation

Markdown + DuckDB + Python SDK + agents + local assets.

## Web Workbench

API + UI + materialised graph.

## Institutional

PostGIS/object storage/auth/private datasets.

---

# v0.1 Acceptance Criteria

- repository dependency direction is documented;
- Pydantic schemas are shared;
- local workstation profile works;
- graph materialisation is regenerable;
- agent workspaces are isolated;
- model provider is replaceable;
- HITL state is durable;
- Docker and non-Docker workflows are documented.
