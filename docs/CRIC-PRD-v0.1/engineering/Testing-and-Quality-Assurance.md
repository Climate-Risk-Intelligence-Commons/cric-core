# CRIC Testing and Quality Assurance Specification

## Purpose

This document defines the verification, validation, evaluation and regression framework for the Climate Risk Intelligence Commons.

CRIC combines deterministic software, geospatial processing, scientific knowledge, machine-learning models, reusable AI agents and human-review workflows. Quality assurance must therefore test each layer independently and test the complete evidence chain end to end.

Passing software tests does not establish scientific validity. Scientific validation is an additional activity.

---

# Quality Assurance Objectives

CRIC QA must detect:

- broken schemas;
- invalid ontology use;
- broken graph relationships;
- temporal inconsistencies;
- spatial inconsistencies;
- missing provenance;
- licensing violations;
- training leakage;
- model regressions;
- agent output regressions;
- permission violations;
- unsafe autonomy;
- broken HITL pause/resume;
- release incompatibilities.

---

# Test Classes

## Unit Tests

Test isolated deterministic functions.

Examples:

- identifier generation;
- unit conversion;
- hash calculation;
- temporal parsing;
- graph edge construction;
- geometry validation;
- manifest generation.

## Schema Tests

Every Pydantic model requires:

- valid fixture;
- invalid fixture;
- boundary cases;
- backwards-compatibility cases.

## Ontology Tests

Test:

- type registry;
- inheritance;
- predicates;
- controlled vocabularies;
- deprecation;
- version compatibility.

## OKF Tests

Test:

- frontmatter parsing;
- Markdown body preservation;
- links;
- canonical IDs;
- relationships;
- round-trip serialisation.

## Graph Tests

Test:

- deterministic edge materialisation;
- bounded traversal;
- contradiction retrieval;
- dependency impact;
- temporal graph slices.

## Geospatial Tests

Test:

- CRS conversion;
- geometry validity;
- topology;
- raster/vector alignment;
- basin membership;
- upstream/downstream relationships.

## Provenance Tests

Test complete trace chains.

Example:

```text
Source
→ Asset
→ Observation
→ Feature
→ TrainingSample
→ Model
→ Prediction
```

---

# Golden Scientific Fixtures

CRIC should maintain small, manually reviewed reference cases.

A golden fixture contains:

- canonical nodes;
- expected relationships;
- source references;
- expected derived values;
- known contradictions;
- expected validation outcome.

Golden fixtures provide regression protection without pretending to represent the full scientific domain.

---

# Agent Testing

Each agent requires:

- tool unit tests;
- dependency-contract tests;
- structured-output validation;
- mock-model tests;
- adversarial prompts;
- permission tests;
- regression cases.

Live-model evaluation should supplement, not replace, deterministic tests.

---

# Agent Evaluation Dimensions

Potential dimensions:

- factual grounding;
- provenance completeness;
- schema compliance;
- contradiction awareness;
- temporal correctness;
- ontology compliance;
- unnecessary escalation;
- missed escalation;
- tool-selection correctness;
- unsupported certainty.

---

# Prompt Injection Tests

Fixtures should include malicious text embedded inside:

- papers;
- Markdown;
- metadata;
- web content;
- dataset descriptions.

Agents must treat these as data.

---

# HITL Tests

Test:

- review bundle creation;
- blocking state;
- clean process termination;
- valid approval;
- invalid approval;
- unauthorised reviewer;
- modified artefact after review;
- rejected decision;
- needs-more-evidence;
- workflow resumption;
- provenance of decision.

---

# Training Data Tests

Test:

- unknown is not negative;
- event-relative cutoffs;
- no future leakage;
- split integrity;
- duplicate contamination;
- label provenance;
- hard-negative eligibility.

---

# Model Tests

Test:

- model loading;
- artifact hashes;
- deterministic preprocessing;
- benchmark execution;
- output schema;
- calibration reporting;
- regression thresholds.

---

# Scientific Validation

Scientific validation may include:

- expert review;
- comparison with published measurements;
- inter-rater agreement;
- field validation;
- cross-dataset comparison;
- retrospective event reconstruction.

Results must be stored as CRIC evidence/assessment artefacts.

---

# End-to-End Reference Test

At least one v0.1 workflow should run:

```text
Acquire/reference source
↓
Create provenance
↓
Create observation
↓
Create StateSnapshot
↓
Build Event Cube
↓
Create TrainingSample
↓
Train/evaluate baseline
↓
Generate prediction
↓
Trace prediction back to source
```

---

# Continuous Integration

Required CI categories:

- lint;
- type check;
- unit tests;
- schema tests;
- ontology tests;
- OKF validation;
- provenance validation;
- licence checks;
- security checks;
- agent mocked evaluations;
- build/package tests.

---

# Quality Gates

Suggested:

## Pull Request Gate

Fast deterministic suite.

## Main Branch Gate

Full integration suite.

## Release Candidate Gate

End-to-end reference workflows plus benchmark checks.

## Stable Release Gate

Release manifest, signatures, documentation, migrations and reproducibility checks.

---

# Regression Budgets

A release should define acceptable regression thresholds.

Examples:

- zero new broken graph links;
- zero unlicensed redistributed assets;
- zero Level 4 HITL bypasses;
- zero provenance breaks in benchmark samples;
- bounded model metric regression.

---

# Test Artefact Provenance

Test results themselves should be version-addressable for releases.

---

# v0.1 Acceptance Criteria

- CI executes core deterministic tests;
- golden GLOF fixture exists;
- agent mock evaluations exist;
- HITL pause/resume is tested;
- training leakage tests exist;
- end-to-end provenance test passes;
- release candidate gate is automated.
