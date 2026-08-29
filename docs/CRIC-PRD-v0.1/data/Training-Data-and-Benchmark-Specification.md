# CRIC Training Data and Benchmark Specification

## Purpose

This document defines how CRIC converts evidence, StateSnapshots and Event Cubes into reproducible machine-learning datasets while preserving provenance, temporal integrity, uncertainty and negative-case semantics.

---

# First-Class Training Entities

CRIC must represent:

- TrainingDataset;
- DatasetVersion;
- TrainingSample;
- Label;
- Feature;
- FeatureSet;
- SplitDefinition;
- Benchmark;
- Model;
- TrainingRun;
- EvaluationRun;
- Prediction.

---

# TrainingSample

A TrainingSample is an immutable manifest referencing source knowledge.

Reference:

```yaml
id:
type: TrainingSample
task_id:
subject_id:
event_cube_id:
snapshot_ids: []
prediction_cutoff:
feature_set_id:
label_ids: []
source_nodes: []
exclusion_notes: []
quality_flags: []
created_by:
```

Training samples should reference data rather than duplicate canonical scientific facts.

---

# Label

Labels require provenance.

```yaml
id:
type: Label
sample_id:
label_type:
value:
class:
temporal_window:
epistemic_status:
confidence:
source_nodes: []
created_by:
review_status:
```

---

# Negative Labels

Required semantics:

## `confirmed_negative`

Sufficient evidence supports absence of the specified event during a defined observation interval.

## `probable_negative`

Evidence strongly suggests absence but is incomplete.

## `no_known_event`

No qualifying event was found in the evidence searched as of a stated CRIC system time.

## `unknown`

Evidence is insufficient.

## `unobserved`

The relevant interval was not adequately observed.

## `not_applicable`

The label does not apply.

`unknown`, `unobserved` and `no_known_event` must never silently become confirmed negatives.

---

# GLOF Sample Categories

Initial benchmark should include:

- confirmed historical GLOFs;
- probable/disputed GLOFs;
- dangerous-looking lakes that did not fail during adequately observed intervals;
- routine stable lakes;
- uncertain cases excluded from supervised labels but retained for research.

---

# Hard Negatives

Hard negatives are scientifically important.

Examples:

- rapidly expanding lake with no known failure;
- large moraine-dammed lake exposed to avalanche but stable during target interval;
- lake with strong susceptibility indicators but no trigger/failure.

Hard-negative status must itself have evidence.

---

# Temporal Leakage

Every predictive sample must define a prediction cutoff.

No feature may use information acquired after that cutoff unless the experiment explicitly studies retrospective reconstruction.

Required fields:

```yaml
prediction_cutoff:
allowed_observation_end:
allowed_system_knowledge_end:
future_information_policy:
```

---

# Event-Relative Tasks

Examples:

- GLOF within 24 hours;
- GLOF within 7 days;
- GLOF within 30 days;
- susceptibility over one year;
- lake expansion over one year.

Task definitions must be versioned.

---

# FeatureSet

A FeatureSet defines:

- feature names;
- derivation methods;
- units;
- missing-data handling;
- source requirements;
- code version;
- normalisation;
- temporal aggregation.

---

# Multimodal Samples

A sample may reference:

- optical imagery;
- SAR;
- DEM-derived terrain;
- precipitation;
- temperature;
- seismicity;
- lake time series;
- glacier observations;
- infrastructure/exposure.

Modalities must remain independently traceable.

---

# Dataset Splits

Random row splitting is often inappropriate for geospatial climate-risk data.

CRIC should support:

- lake-disjoint split;
- basin-disjoint split;
- geography-disjoint split;
- temporal holdout;
- event-disjoint split;
- source-disjoint split where relevant.

SplitDefinition is versioned and immutable.

---

# Leakage Across Related Lakes

Upstream/downstream or geographically adjacent lakes may share information.

Benchmarks should document whether connected systems may appear across train/test splits.

---

# Dataset Versioning

A DatasetVersion freezes:

- sample list;
- labels;
- feature versions;
- splits;
- inclusion criteria;
- exclusion criteria;
- ontology version;
- code version;
- hashes.

---

# Benchmark

A Benchmark defines:

- task;
- dataset version;
- split;
- metrics;
- baseline models;
- evaluation protocol;
- uncertainty reporting;
- prohibited information;
- reporting template.

---

# Metrics

Metrics depend on task.

Potential classification metrics:

- precision;
- recall;
- F1;
- PR-AUC;
- ROC-AUC;
- Brier score;
- calibration error.

For rare high-consequence events, accuracy alone is inadequate.

Potential segmentation metrics:

- IoU;
- Dice;
- boundary error.

Potential regression metrics:

- MAE;
- RMSE;
- interval coverage.

---

# Calibration

Risk-state models should evaluate calibration where probabilistic outputs are used.

A model score must not be described as probability unless calibration supports that interpretation.

---

# Class Imbalance

GLOFs are rare.

Strategies may include:

- class weighting;
- balanced sampling;
- focal loss;
- hard-negative mining;
- anomaly detection;
- ranking formulations.

Evaluation must preserve realistic prevalence where operational interpretation is claimed.

---

# Training Curator Agent

Responsibilities:

- identify eligible samples;
- detect label ambiguity;
- propose hard negatives;
- check leakage;
- generate dataset manifests;
- route disputed labels to HITL.

It may not silently convert unknown cases to negatives.

---

# Benchmark Freeze

A benchmark release should be immutable.

Corrections create a new benchmark version.

---

# Reconstructability

A user should be able to answer:

> Exactly which evidence trained this model?

through:

```text
Model
→ TrainingRun
→ DatasetVersion
→ TrainingSample
→ Snapshot
→ Observation
→ Asset
→ Source
```

---

# v0.1 Reference Dataset

A practical first benchmark may target approximately:

- 10 confirmed GLOF/event cases;
- 10 hard negatives;
- 20 routine negatives;

subject to evidence quality rather than fixed quotas.

The architecture must scale far beyond this initial set.

---

# v0.1 Acceptance Criteria

- TrainingSample and Label schemas exist;
- negative semantics are enforced;
- one event cube produces reproducible samples;
- prediction cutoffs prevent leakage;
- split definitions are versioned;
- hard negatives are represented;
- benchmark manifest exists;
- model-to-source reconstruction works.
