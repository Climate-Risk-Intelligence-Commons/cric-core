# CRIC Data Quality and Validation Specification

## Purpose

This document defines the quality model, validation layers, acceptance gates and quality artefacts used throughout the Climate Risk Intelligence Commons.

CRIC must never collapse structural validity, provenance completeness, scientific quality, evidence completeness and operational suitability into one score.

---

# Quality Dimensions

Every consequential object may be assessed across independent dimensions:

- schema validity;
- ontology validity;
- graph integrity;
- temporal integrity;
- spatial integrity;
- provenance completeness;
- licence clarity;
- source quality;
- measurement quality;
- scientific plausibility;
- reproducibility;
- evidence completeness;
- contradiction status;
- human-review status;
- fitness for intended use.

A node may be structurally perfect and scientifically weak. It may also be scientifically valuable while incomplete.

---

# Validation Layers

## V0 File Integrity

Checks:

- file exists;
- readable encoding;
- valid YAML frontmatter;
- expected file type;
- hash generated where required.

## V1 Schema Validation

Pydantic validation of:

- required fields;
- types;
- enums;
- units;
- identifier format;
- nested structures.

## V2 Ontology Validation

Checks:

- registered type;
- valid parent;
- allowed predicate;
- controlled vocabulary;
- ontology version compatibility.

## V3 Graph Validation

Checks:

- relationship targets resolve;
- duplicate IDs absent;
- reciprocal relationships where required;
- orphan nodes identified;
- circularity rules where applicable.

## V4 Temporal Validation

Checks:

- valid temporal syntax;
- no invented precision;
- temporal order;
- observation time versus event time;
- supersession chronology;
- training cutoff rules.

## V5 Spatial Validation

Checks:

- valid CRS;
- geometry validity;
- coordinate ranges;
- topology;
- basin consistency;
- impossible spatial relationships.

## V6 Provenance Validation

Checks:

- required source nodes;
- parentage;
- hashes;
- transformation records;
- software/agent run;
- licence state.

## V7 Scientific Quality Assessment

May evaluate:

- measurement method;
- sensor limitations;
- scientific plausibility;
- uncertainty;
- methodological transparency;
- corroboration.

This layer may require expert review.

## V8 Fitness-for-Use

Assesses whether an object is suitable for a particular use such as:

- exploratory research;
- training;
- benchmarking;
- publication;
- risk assessment;
- operational decision support.

---

# QualityAssessment Node

Reference:

```yaml
id:
type: QualityAssessment
subject_id:
assessment_type:
dimensions:
  schema_validity:
  provenance_completeness:
  measurement_quality:
  temporal_quality:
  spatial_quality:
  scientific_plausibility:
  reproducibility:
  evidence_completeness:
fitness_for_use: []
assessor:
method:
evidence_nodes: []
created_at:
```

---

# Quality Flags

Suggested flags:

- missing_provenance;
- uncertain_licence;
- temporal_ambiguity;
- spatial_ambiguity;
- low_resolution;
- cloud_contamination;
- shadow_contamination;
- sensor_artifact;
- estimated_not_measured;
- unresolved_contradiction;
- insufficient_negative_evidence;
- possible_label_leakage;
- stale_source;
- unverifiable_source;
- manual_digitisation;
- low_inter_rater_agreement.

---

# Evidence Completeness

Completeness must be represented separately from risk.

Example:

```yaml
evidence_completeness:
  expected_categories: 8
  available_categories: 5
  score: 0.625
  missing:
    - recent_precipitation
    - lake_level
    - dam_deformation
```

A low completeness score must never automatically lower hazard classification.

---

# Measurement Quality

Measurements should retain:

- method;
- resolution;
- sensor;
- processing level;
- positional uncertainty;
- numerical uncertainty;
- calibration status where applicable.

---

# Source Quality

Source quality may consider:

- primary versus secondary evidence;
- methodological transparency;
- peer review;
- institutional provenance;
- reproducibility;
- recency.

Source quality must not be treated as automatic truth.

---

# Contradiction-Aware Validation

Conflicting observations do not necessarily invalidate the graph.

The validator should distinguish:

- structural conflict;
- scientific contradiction;
- temporal mismatch;
- expected methodological difference.

Scientific contradiction should normally generate a review or contradiction artefact, not a schema failure.

---

# Validation Reports

Every pipeline should be able to emit:

```yaml
validation_run_id:
target_ids: []
validator_version:
started_at:
completed_at:
passed:
errors: []
warnings: []
quality_flags: []
review_requests: []
```

---

# Promotion Gates

Suggested gates:

## Candidate Knowledge

Must pass V0-V3.

## Accepted Deterministic Knowledge

Must pass V0-V6 and applicable deterministic scientific checks.

## Training-Eligible

Must additionally pass training-specific provenance, label and leakage rules.

## Benchmark-Eligible

Requires stronger review, frozen version and documented inclusion criteria.

## Safety-Relevant Interpretation

Requires defined human-review policy.

---

# Automated Repair

Validators may automatically repair only semantically safe issues such as:

- formatting;
- canonical ordering;
- harmless whitespace;
- generated index refresh.

Scientific values, temporal precision, ontology meaning or provenance must not be silently repaired.

---

# Data Quality Agent

The Data Quality Agent may:

- aggregate validator results;
- identify anomalies;
- compare related observations;
- suggest quality flags;
- route ambiguous cases.

It must not convert low-quality data into high-quality data by assertion.

---

# Quality Regression

Every release should compare:

- broken links;
- validation failures;
- missing provenance;
- unresolved licences;
- benchmark composition;
- unresolved contradictions.

Quality degradation should fail CI where thresholds are exceeded.

---

# v0.1 Acceptance Criteria

- layered validators exist;
- QualityAssessment schema exists;
- evidence completeness is independent of hazard;
- training eligibility has explicit gates;
- scientific contradictions do not become generic schema errors;
- validation reports are machine-readable;
- CI detects quality regressions.
