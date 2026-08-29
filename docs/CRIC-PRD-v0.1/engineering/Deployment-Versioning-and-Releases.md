# CRIC Deployment, Versioning and Release Specification

## Purpose

This document defines how CRIC components are packaged, versioned, deployed and released while preserving compatibility across a multi-repository ecosystem.

---

# Version Dimensions

CRIC has several independent versions:

- software package version;
- API version;
- schema version;
- ontology version;
- knowledge release;
- dataset version;
- model version;
- agent version.

These must not be conflated.

---

# Semantic Versioning

Software, schemas, ontology packages and agents should generally use semantic versioning.

## Major

Breaking compatibility.

## Minor

Backward-compatible capabilities.

## Patch

Compatible fixes or clarifications.

---

# Knowledge Releases

`cric-knowledge` releases should have immutable identifiers.

Example:

```text
CRIC-KNOWLEDGE-2026.09.0
```

A release records:

- Git commit;
- schema version;
- ontology version;
- included nodes;
- hashes;
- validation report.

---

# Dataset Versions

Datasets must use immutable versions independent of repository tags.

A new sample, corrected label or changed split requires a new DatasetVersion.

---

# Model Versions

Model artifacts require:

- semantic/release version;
- weight hash;
- training run;
- dataset version;
- code version.

---

# Agent Versions

Breaking changes include:

- output schema changes;
- dependency-contract changes;
- tool-signature changes;
- permission-semantic changes.

Prompt refinements may be patch or minor changes depending on behavioural impact.

---

# Multi-Repository Release Manifest

A CRIC coordinated release should publish:

```yaml
release_id:
released_at:
components:
  cric-core:
    version:
    commit:
  cric-knowledge:
    version:
    commit:
  cric-agents:
    version:
    commit:
  cric-glof:
    version:
    commit:
schemas:
ontology:
datasets: []
models: []
```

---

# Compatibility Matrix

CRIC should publish compatibility between:

- core schema;
- ontology;
- domain packages;
- agents;
- API.

---

# Deployment Profiles

## Knowledge-Only

Requirements:

- Git;
- Markdown reader or Obsidian.

## Research Workstation

Adds:

- Python;
- local environment;
- DuckDB;
- scientific libraries;
- optional agents;
- local data cache.

## Web Workbench

Adds:

- API;
- UI;
- database/materialised indexes.

## Institutional

May add:

- PostGIS;
- S3-compatible storage;
- identity provider;
- private datasets;
- local model serving;
- controlled network.

---

# Offline Deployment

A release may create an offline bundle:

```text
cric-offline-bundle/
├── knowledge/
├── indexes/
├── datasets/
├── models/
├── schemas/
├── manifests/
└── README.md
```

Every included artefact must retain provenance and licence metadata.

---

# Container Images

Where published, images should be:

- version pinned;
- reproducibly built where feasible;
- scanned;
- signed where practical;
- linked to source commit.

---

# Database Migrations

Materialised databases are rebuildable, but operational deployments may use migrations for efficiency.

Canonical knowledge remains outside the database.

---

# Schema Migrations

Breaking schema changes require:

- migration documentation;
- migration tooling where feasible;
- before/after fixtures;
- MigrationRecord.

---

# Rollback

A deployment should be able to roll back software independently of canonical knowledge.

Knowledge rollback must not erase historical records.

---

# Release Channels

Suggested:

- experimental;
- alpha;
- beta;
- stable.

Scientific dataset/model maturity should use its own status rather than being inferred from software channel.

---

# Release Checklist

- tests pass;
- ontology validates;
- OKF validates;
- provenance validates;
- licences checked;
- security scan;
- migration notes;
- compatibility matrix;
- release manifest;
- documentation;
- model cards;
- dataset cards;
- known limitations.

---

# Release Signing

Stable releases should support cryptographic signing of:

- tags;
- manifests;
- selected artifacts.

---

# Reproducibility

A user should be able to identify the exact CRIC component set used for a scientific result.

---

# v0.1 Acceptance Criteria

- independent version dimensions documented;
- coordinated release manifest generated;
- compatibility matrix exists;
- local research deployment works;
- offline bundle can be generated;
- release checklist is automated where possible.
