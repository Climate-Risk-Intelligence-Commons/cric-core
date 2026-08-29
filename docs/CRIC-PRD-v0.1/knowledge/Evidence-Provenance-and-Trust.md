# CRIC Evidence, Provenance and Trust Specification

## Purpose

Evidence lineage is a constitutional requirement of CRIC.

This document defines how CRIC records where information came from, what happened to it, how it was transformed, what licensing applies, and how downstream users can determine the basis of a claim, feature, model output or assessment.

---

# Core Principle

Every consequential output should support traversal back to source evidence.

Reference chain:

```text
Source
→ Acquired Asset
→ Normalised Asset
→ Observation
→ Feature
→ Claim
→ Assessment
→ Prediction / Decision-Support Output
```

Not every workflow uses every stage, but missing stages must not be invented.

---

# Provenance Requirements

A provenance record should answer:

- what object is being described;
- source URI or source node;
- acquisition time;
- source provider;
- source version;
- source hash where available;
- parent objects;
- transformation;
- software;
- software version;
- agent;
- agent version;
- human reviewer;
- output hash;
- licence;
- epistemic status.

---

# Provenance Record

Reference structure:

```yaml
id:
type: ProvenanceRecord
object_id:

source:
  node_ids: []
  uris: []
  provider:
  version:

acquisition:
  retrieved_at:
  method:
  actor:

parents: []

transformation:
  workflow_id:
  step_id:
  software:
  software_version:
  parameters:
  deterministic:

agent:
  agent_id:
  agent_version:
  run_id:
  model:

human_reviews: []

integrity:
  content_sha256:
  parent_hashes: []

licensing:
  licence:
  redistribution:
  derivative_use:
```

---

# Immutable Lineage

Lineage records must not be rewritten to make a later workflow appear cleaner.

If provenance metadata was incorrect:

- create a corrected record;
- link with `supersedes`;
- preserve the original.

---

# Hashing

SHA-256 is the minimum reference algorithm for v0.1.

Hashes should be generated for:

- canonical files;
- externally acquired assets where bytes are available;
- dataset manifests;
- model artefacts;
- release manifests.

For externally changing URLs, URI identity is insufficient. Store acquisition time and content hash where legally and technically possible.

---

# Parentage

Derived objects must list their parent objects.

Example:

```text
Sentinel asset
→ lake polygon
→ lake area observation
→ lake growth feature
→ susceptibility assessment
```

Each step should be independently inspectable.

---

# Provenance Granularity

A provenance record should exist at the smallest level that materially affects scientific reproducibility.

Do not create meaningless provenance nodes for every trivial formatting operation.

Do create them for:

- scientific transformations;
- feature extraction;
- aggregation;
- filtering that changes sample composition;
- label creation;
- model training;
- simulation;
- agent-generated scientific interpretation.

---

# Evidence Classes

Recommended controlled vocabulary:

- instrument_observation;
- satellite_observation;
- field_observation;
- government_dataset;
- peer_reviewed_publication;
- preprint;
- technical_report;
- institutional_record;
- news_report;
- eyewitness_report;
- community_report;
- model_output;
- simulation_output;
- agent_inference;
- human_expert_assessment.

---

# Source Authority

CRIC may store source-authority assessments, but authority must not be confused with truth.

A high-authority source can still be wrong.

A lower-authority source may contain valuable primary evidence.

Authority assessments should state the rubric used.

---

# Trust Dimensions

Trust should be decomposed rather than collapsed into one opaque score.

Possible dimensions:

- source authority;
- provenance completeness;
- measurement quality;
- temporal relevance;
- spatial relevance;
- reproducibility;
- corroboration;
- uncertainty;
- review status.

---

# Evidence Completeness

Evidence completeness must remain separate from hazard or risk.

Missing evidence does not imply low hazard.

A completeness assessment may consider:

- expected evidence categories;
- available categories;
- temporal recency;
- spatial coverage;
- unresolved conflicts;
- source accessibility.

---

# Copyrighted Scientific Papers

CRIC may represent knowledge extracted from copyrighted papers when lawful.

CRIC should store:

- bibliographic metadata;
- DOI;
- source URL;
- authors;
- publication details;
- licence where known;
- CRIC-authored structured factual extraction;
- claims;
- relationships;
- provenance.

Unless permitted, CRIC must not redistribute:

- full PDF;
- copied figures;
- copied tables;
- extended protected text.

---

# Licence Status

Recommended values:

- open_redistribution;
- attribution_required;
- share_alike;
- noncommercial;
- reference_only;
- restricted;
- unknown;
- permission_required.

Unknown licence status should default to conservative handling.

---

# Integrity Versus Scientific Validity

Cryptographic integrity proves that bytes or manifests have not changed.

It does not prove:

- scientific correctness;
- sensor calibration;
- causal validity;
- absence of bias.

CRIC documentation and UI must preserve this distinction.

---

# Agent Provenance

Agent-generated knowledge must record:

- agent ID;
- agent version;
- model;
- model provider;
- prompt/instructions version;
- toolsets;
- datasets;
- run ID;
- output validation;
- human review where applicable.

---

# Model Provenance

Every model output should identify:

- model ID;
- model version;
- training dataset version;
- inference code version;
- feature version;
- threshold/configuration;
- input nodes;
- execution time.

---

# Release Manifests

Each major knowledge or dataset release should provide a manifest containing:

- release identifier;
- Git commit;
- included artefacts;
- hashes;
- ontology version;
- schema version;
- generated time.

---

# Provenance Audit Agent

CRIC should include an agent or deterministic audit workflow capable of identifying:

- missing parent links;
- missing source references;
- unhashed assets;
- licence gaps;
- incompatible source versions;
- broken provenance chains;
- agent outputs without run records.

---

# v0.1 Acceptance Criteria

- every sample observation has provenance;
- every derived feature identifies parents;
- protected-source handling is documented;
- release manifest generation works;
- provenance graph traversal is testable;
- agent runs generate provenance;
- hashes are visible;
- evidence completeness is separate from risk;
- missing provenance fails publication validation for node classes where lineage is mandatory.
