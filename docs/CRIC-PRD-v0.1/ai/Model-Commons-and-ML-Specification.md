# CRIC Model Commons and Machine-Learning Specification

## Purpose

The Model Commons provides open, reproducible infrastructure for training, evaluating, comparing and deploying climate-risk models without confusing experimental model output with validated operational authority.

---

# Model Commons Principles

- provenance before leaderboard performance;
- small and medium models are first-class;
- local and sovereign deployment must remain possible;
- model architecture is replaceable;
- multimodal fusion should preserve modality provenance;
- uncertainty and calibration must be visible;
- reproducibility is mandatory for published benchmarks.

---

# First-Class Model Entities

- Model;
- ModelCard;
- TrainingRun;
- EvaluationRun;
- Prediction;
- FeatureSet;
- DatasetVersion;
- ModelArtifact.

---

# Model

Represents persistent model identity.

Fields:

- model ID;
- name;
- task;
- architecture family;
- input modalities;
- output schema;
- licence;
- intended use;
- prohibited use.

---

# Model Version / Artifact

Each weight release should identify:

- parent model;
- architecture;
- weight URI;
- hash;
- training run;
- framework version;
- quantisation;
- licence;
- hardware notes.

---

# ModelCard

Must document:

- purpose;
- training data;
- evaluation data;
- metrics;
- limitations;
- known failure modes;
- geography;
- temporal coverage;
- sensor dependencies;
- calibration;
- uncertainty;
- safety disclaimer.

---

# GLOF Model Families

## Vision Segmentation

Potential targets:

- lake;
- glacier;
- snow;
- moraine;
- debris;
- rock;
- vegetation;
- landslide scar.

## Lake Change

Input:

- temporal imagery or extracted polygons.

Output:

- area trajectory;
- growth;
- shoreline movement;
- anomaly.

## Susceptibility

Potential models:

- XGBoost;
- LightGBM;
- CatBoost;
- random forest;
- small MLP.

## Trigger Time-Series

Potential architectures:

- temporal CNN;
- GRU/LSTM;
- compact transformer;
- temporal fusion transformer where justified.

## Failure-Mode Models

Separate experts may evaluate:

- overtopping;
- moraine breach;
- ice-dam drainage;
- displacement wave;
- piping/internal erosion;
- cascading failure.

## Multimodal Fusion

Possible inputs:

- imagery embeddings;
- lake history;
- terrain;
- weather;
- seismicity;
- glacier state.

Output should include:

- state/risk score;
- uncertainty;
- explanatory feature references.

---

# Foundation Encoder Research Track

CRIC may investigate a compact Himalayan Cryosphere Foundation Encoder trained self-supervised on large volumes of unlabelled regional imagery.

Indicative size:

- approximately 50M to 300M parameters.

This is a research direction, not a v0.1 requirement.

---

# ModelRun

Every training run records:

```yaml
model_id:
code_commit:
environment:
dataset_version:
split_definition:
feature_set:
hyperparameters:
random_seeds:
hardware:
started_at:
completed_at:
artifacts: []
metrics: []
```

---

# Reproducibility

Published runs should preserve:

- code commit;
- environment lock;
- dataset version;
- seeds;
- parameters;
- weight hash.

Deterministic reproducibility may not always be achievable on all hardware, but deviations must be documented.

---

# Local Compute

CRIC should support CPU and commodity GPU experimentation where possible.

Model size and inference requirements should be reported.

Quantised variants are encouraged when scientifically acceptable.

---

# Model Registry

The registry should expose:

- task;
- domain;
- version;
- licence;
- benchmark results;
- status;
- model card;
- artifact URI;
- hash.

---

# Model Status

Suggested lifecycle:

- experimental;
- candidate;
- benchmarked;
- research_validated;
- deprecated.

Operationally validated status must require a separate governance process and should not be inferred from benchmark performance.

---

# Prediction Node

Every significant prediction records:

- model artifact;
- input sample/snapshot;
- execution time;
- output;
- confidence;
- calibration context;
- threshold;
- code version.

---

# Explainability

Where practical, model output should expose:

- influential features;
- source observations;
- modality contributions;
- uncertainty;
- missing inputs.

Explanations must not be presented as causal proof unless methodologically justified.

---

# Ensemble and Mixture-of-Experts

Because GLOF failure mechanisms differ, CRIC should permit ensembles or mixture-of-experts.

A fusion layer may combine mechanism-specific outputs.

Each expert remains independently evaluable.

---

# Uncertainty

Potential sources:

- data uncertainty;
- measurement uncertainty;
- model uncertainty;
- distribution shift;
- missing modalities;
- label uncertainty.

The interface should avoid presenting one confidence number as if it captured all uncertainty.

---

# Distribution Shift

Evaluation should monitor:

- new sensors;
- new geography;
- changed climate regime;
- different lake types;
- changed preprocessing.

---

# Human Review

Model outputs used for safety-relevant interpretation must enter the HITL process at the defined autonomy level.

---

# Model Evaluation Agent

May:

- execute registered benchmarks;
- compare model versions;
- detect regressions;
- generate candidate model cards;
- identify calibration problems.

---

# v0.1 Baselines

v0.1 should prioritise interpretable baselines:

- deterministic lake-change features;
- tree-based susceptibility classifier;
- simple segmentation baseline where data permits.

The objective is to validate the evidence-to-model pipeline before optimising model complexity.

---

# v0.1 Acceptance Criteria

- Model and ModelCard schemas exist;
- TrainingRun and EvaluationRun are reproducible;
- baseline model is benchmarked;
- model artifact is hashed;
- model-to-training-evidence traversal works;
- predictions expose version and inputs;
- safety-relevant outputs route to HITL;
- local execution is documented.
