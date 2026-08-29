# CRIC v0.1 Implementation Specification

## Purpose

CRIC v0.1 is the first open-source reference implementation demonstrating that heterogeneous climate-risk evidence can be transformed into a provenance-preserving, temporally aware, agent-compatible knowledge and modelling commons.

The reference scientific domain is Himalayan cryosphere risk, beginning with GLOF intelligence.

v0.1 is an experimental proof of concept, not a validated operational early-warning system.

---

# v0.1 Product Question

Can CRIC make the chain:

```text
source evidence
→ observation
→ provenance
→ state reconstruction
→ risk-relevant feature
→ model/interpretation
→ downstream consequence
→ human review
```

visible, inspectable and reproducible?

---

# v0.1 Geographic Scope

Initial focus:

- Indian Himalayan Region;
- connected transboundary Indus, Ganga and Brahmaputra cryosphere systems where relevant to selected cases.

The reference dataset may use cases outside India where needed for scientifically useful positive/negative examples.

---

# Minimum Repositories

Required:

```text
cric-core
cric-knowledge
cric-data
cric-ingest
cric-cryosphere
cric-glof
cric-agents
cric-models
cric-api
cric-ui
cric-docs
```

Recommended:

```text
cric-review
```

---

# Workstream 1: CRIC Core

Deliver:

- Pydantic core schemas;
- JSON Schemas;
- ontology registry;
- temporal schema;
- provenance schema;
- knowledge-state schema;
- validators;
- ID conventions.

---

# Workstream 2: Knowledge Commons

Deliver downloadable Obsidian-compatible OKF vault.

Minimum content:

- selected lakes;
- glaciers;
- events;
- sources;
- observations;
- claims;
- evidence;
- snapshots;
- datasets;
- provenance.

---

# Workstream 3: GLOF Reference Dataset

Target approximately:

- 10 confirmed historical GLOF cases;
- 10 hard-negative lakes;
- 20 routine negative/stable cases;

subject to evidence quality.

Do not force quotas if reliable evidence is unavailable.

---

# Workstream 4: Observation Factory

Implement deterministic pipelines for a useful subset of:

- lake polygons;
- lake area;
- lake area change;
- glacier relationship;
- DEM terrain;
- rainfall/temperature context;
- downstream exposure.

---

# Workstream 5: StateSnapshot and Event Cube

For selected cases:

- persistent lake identity;
- event-relative snapshots;
- explicit missing windows;
- pre-event observations;
- event claims;
- post-event observations;
- provenance.

---

# Workstream 6: Training Dataset

Deliver:

- TrainingSample;
- Label;
- FeatureSet;
- SplitDefinition;
- DatasetVersion;
- benchmark manifest.

Include hard negatives and explicit unknown/no-known-event semantics.

---

# Workstream 7: Baseline Models

Prioritise simple baselines.

Candidate:

- lake-change baseline;
- tree-based susceptibility classifier;
- optional segmentation baseline.

Model performance is secondary to pipeline reproducibility.

---

# Workstream 8: Agent Commons

Minimum functioning agents:

1. Evidence Extraction Agent;
2. Entity Resolution Agent;
3. Ontology Watch Agent;
4. Provenance Auditor Agent;
5. Human Review Router Agent.

Each must be reusable via injected dependencies/toolsets/workspaces.

---

# Workstream 9: HITL

Demonstrate:

```text
agent detects ambiguity
→ review bundle
→ human decision
→ workflow resumes
→ provenance updated
```

---

# Workstream 10: Search and Graph

Deliver:

- OKF parser;
- graph materialiser;
- edge index;
- deterministic bounded traversal;
- temporal filters;
- provenance traversal;
- context package generation.

---

# Workstream 11: API

Minimum:

- entity;
- observation;
- snapshot;
- event;
- provenance;
- search;
- graph endpoints.

---

# Workstream 12: UI

Minimum scientific workbench:

- map;
- lake/entity page;
- timeline;
- evidence/provenance view;
- candidate/accepted status;
- review view.

---

# Initial Source Families

Candidate sources include:

- NRSC/ISRO glacial lake inventories;
- Landsat;
- Sentinel-1;
- Sentinel-2;
- GPM IMERG;
- Copernicus DEM;
- HydroSHEDS;
- WorldPop;
- OpenStreetMap;
- peer-reviewed and institutional GLOF inventories.

Actual use depends on access and licensing.

---

# Milestone A: Schema Spine

Exit:

- core schemas;
- ontology;
- example OKF nodes;
- validators.

---

# Milestone B: First Lake Digital Record

Exit:

- one lake;
- glacier;
- observations;
- provenance;
- snapshot;
- graph traversal.

---

# Milestone C: First Event Cube

Exit:

- historical GLOF;
- pre/post snapshots;
- claims;
- contradictions;
- event manifest.

---

# Milestone D: Dataset Slice

Exit:

- positive;
- hard negative;
- routine negative;
- reproducible sample generation.

---

# Milestone E: Baseline Model

Exit:

- versioned dataset;
- training run;
- evaluation;
- model card;
- source-to-model provenance.

---

# Milestone F: Agent/HITL Loop

Exit:

- agent candidate knowledge;
- ontology watch;
- review bundle;
- human approval/rejection;
- durable resume.

---

# Milestone G: Reference Workbench

Exit:

- API;
- map;
- entity explorer;
- timeline;
- evidence lineage.

---

# Non-Goals

v0.1 does not require:

- operational warning;
- national-scale production ingestion;
- real-time sensor network;
- calibrated failure probability;
- exhaustive ontology for all climate hazards;
- distributed microservices;
- large foundation-model training.

---

# v0.1 Definition of Done

A technically competent external researcher should be able to clone CRIC, inspect the knowledge vault, reproduce a reference GLOF Event Cube, build a training sample, run a baseline model, trace the output to source evidence and inspect any human-review decisions without needing undocumented project knowledge.
