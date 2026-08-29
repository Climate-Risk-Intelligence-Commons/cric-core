# CRIC Ingestion and Licensing Specification

## Purpose

This document defines how CRIC discovers, evaluates, acquires, normalises and registers external data and knowledge sources while preserving provenance and respecting licensing and copyright constraints.

---

# Ingestion Philosophy

Ingestion is a controlled evidence pipeline, not merely a download operation.

Reference flow:

```text
Discover
↓
Qualify Source
↓
Assess Licence
↓
Acquire or Reference
↓
Hash
↓
Extract Metadata
↓
Normalise
↓
Validate
↓
Create OKF Nodes
↓
Create Provenance
↓
Publish Candidate Knowledge
```

---

# Source Discovery

Sources may include:

- scientific literature;
- government datasets;
- satellite catalogues;
- sensor feeds;
- geospatial services;
- institutional reports;
- historical archives;
- field observations;
- community contributions.

---

# Source Qualification

Qualification may evaluate:

- source identity;
- publisher;
- scientific relevance;
- authority;
- recency;
- spatial relevance;
- temporal relevance;
- methodological transparency.

Qualification is an assessment, not a truth declaration.

---

# Licence Assessment

Before redistribution, CRIC must determine:

- licence;
- attribution requirements;
- redistribution permission;
- derivative-use permission;
- commercial-use restrictions;
- share-alike obligations;
- API terms;
- storage restrictions.

---

# Licence Status Vocabulary

- open_redistribution;
- attribution_required;
- share_alike;
- noncommercial;
- reference_only;
- restricted;
- permission_required;
- unknown.

Unknown should default to conservative handling.

---

# Copyrighted Scientific Literature

CRIC may ingest knowledge from a protected paper while retaining only a reference to the protected document.

Permitted CRIC artefacts may include:

- bibliographic metadata;
- DOI;
- source URI;
- CRIC-authored summary;
- structured factual extraction;
- claims;
- relationships;
- provenance.

Protected PDFs, figures, tables and extended copied text must not be redistributed without permission.

---

# Acquisition Modes

## Copy Permitted

Acquire and store according to licence.

## Cache Permitted

Temporarily cache for processing but do not redistribute.

## Reference Only

Store metadata and URI.

## Permission Required

Do not acquire into shared infrastructure until permission exists.

---

# Deterministic Ingestion

Where possible, ingestion should be implemented deterministically.

Agents may assist with:

- source discovery;
- semantic extraction;
- licence interpretation;
- metadata reconciliation.

Agents must not bypass explicit licence restrictions.

---

# Ingestion Manifest

Every ingestion run should record:

```yaml
ingestion_run_id:
workflow_version:
started_at:
completed_at:
sources: []
assets_acquired: []
assets_referenced: []
licence_decisions: []
created_nodes: []
failed_items: []
warnings: []
```

---

# Idempotency

Repeated ingestion of the same immutable source should not create uncontrolled duplicates.

Use:

- source IDs;
- provider IDs;
- hashes;
- canonical URIs;
- temporal/version metadata.

---

# Source Change Detection

For mutable external sources, CRIC should detect:

- changed bytes;
- changed metadata;
- new version;
- removed source;
- licence change.

A changed source should create a new version rather than silently replacing previous provenance.

---

# Metadata Extraction

Minimum metadata where available:

- title/name;
- provider;
- source URI;
- retrieval time;
- publication/release time;
- spatial extent;
- temporal extent;
- format;
- licence;
- identifiers;
- checksum.

---

# Normalisation

Normalisation should be separate from acquisition.

The raw acquired object remains immutable.

Normalised outputs become derived assets with parent links.

---

# Scientific Literature Extraction

Suggested agent team:

```text
Scout Agent
↓
Source Qualification Agent
↓
Licence Agent
↓
Acquisition/Reference Agent
↓
Metadata Agent
↓
Evidence Extraction Agent
↓
Entity Resolution Agent
↓
Contradiction Agent
↓
Ontology Watch Agent
↓
Provenance Auditor
```

Parallelism should be used where dependencies permit.

---

# Human Review Triggers

Human review may be required for:

- unclear licence;
- ambiguous source identity;
- high-impact scientific claim;
- unresolved entity collision;
- safety-significant interpretation;
- ontology change affecting stable core.

Routine open-data ingestion should not require human approval for every item.

---

# Community-Contributed Data

Community data must record:

- contributor identity or pseudonymous identifier where appropriate;
- contribution time;
- consent/licence;
- collection method;
- location precision policy;
- quality status;
- verification status.

Sensitive locations may require controlled access.

---

# Security

Ingestion must defend against:

- malicious files;
- prompt injection in documents;
- oversized payloads;
- path traversal;
- embedded executable content;
- poisoned metadata;
- untrusted archives.

Agent instructions embedded in source material must be treated as data, not system instructions.

---

# Quarantine

Suspicious or unvalidated assets should enter quarantine.

Reference states:

- discovered;
- licence_pending;
- quarantined;
- acquired;
- validated;
- rejected;
- archived.

---

# Failure Handling

Ingestion failures should create structured records.

Do not silently skip sources when the missing source materially affects completeness.

---

# v0.1 Acceptance Criteria

- source registry exists;
- licence status is machine-readable;
- open and reference-only sources are distinguishable;
- raw and normalised assets are separate;
- ingestion runs produce manifests;
- duplicate acquisition is controlled;
- protected-paper workflow is demonstrated;
- malicious-content handling is documented;
- agents cannot override licence policy;
- human review is triggered selectively rather than universally.
