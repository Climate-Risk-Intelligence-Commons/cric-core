# CRIC Canonical Schema and Vocabulary Registry

## Status

Canonical integration registry for the CRIC PRD v0.1 specification family.

This document resolves naming choices that appeared in earlier drafting batches. Where an earlier document differs from this registry, this registry is authoritative for implementation until the relevant source document is revised.

## 1. Canonical Naming Rules

- Project name: **Climate Risk Intelligence Commons (CRIC)**.
- First domain implementation: **Cryosphere**, with **GLOF** as the first hazard workflow.
- Canonical knowledge format: **OKF Markdown**, consisting of Markdown plus YAML frontmatter.
- Runtime schema authority: **Pydantic**.
- Canonical knowledge is version-controlled OKF. Databases and indexes are materialisations.
- Significant historical knowledge is preserved. Supersession does not delete prior assertions.

## 2. Canonical Identifier Form

Canonical logical form:

```text
CRIC:<namespace>:<type>:<ulid>
```

Examples:

```text
CRIC:core:claim:01J...
CRIC:cryosphere:glacial_lake:01J...
CRIC:glof:event:01J...
```

Human-facing short IDs such as `CRIC-LAKE-001` may appear in examples and fixtures, but MUST NOT be treated as the canonical production identifier format.

## 3. Canonical Root Object Types

```text
CRICObject
├── KnowledgeObject
├── ResourceObject
├── ComputationalObject
├── GovernanceObject
└── QualityObject
```

Canonical core types include:

- Entity
- Event
- Observation
- StateSnapshot
- Claim
- Evidence
- Assessment
- Source
- Dataset
- DatasetVersion
- DataAsset
- Licence
- Workflow
- Agent
- AgentRun
- Toolset
- Model
- ModelRun
- TrainingRun
- EvaluationRun
- TrainingSample
- Label
- FeatureSet
- Prediction
- ReviewRequest
- ReviewDecision
- OntologyProposal
- MigrationRecord
- ProvenanceRecord
- QualityAssessment
- UncertaintyAssessment

### Asset Resolution

Use **`DataAsset`** as the canonical ontology type. `Asset` may remain a generic prose term but SHOULD NOT be used as a competing schema type.

### Model Run Resolution

Use:

- `TrainingRun` for model training;
- `EvaluationRun` for evaluation;
- `ModelRun` only as the generic parent or non-training/non-evaluation execution record.

## 4. Knowledge State

Canonical workflow status vocabulary:

```text
candidate
accepted
disputed
superseded
rejected
withdrawn
archived
```

Recommended structure:

```yaml
knowledge_state:
  status: candidate
  origin: agent
  verification:
    method:
    verified_by:
    verified_at:
```

`scientific_confidence` or epistemic confidence MUST remain separate from workflow status.

## 5. Epistemic Status

Canonical epistemic vocabulary:

```text
observed
reported
derived
inferred
simulated
hypothesised
disputed
unknown
```

## 6. Negative-Case Vocabulary

Canonical training/evidence semantics:

```text
confirmed_negative
probable_negative
no_known_event
unknown
unobserved
not_applicable
```

`unknown`, `unobserved`, and `no_known_event` MUST NOT be automatically converted to negative training labels.

## 7. Multi-Temporal Model

Canonical temporal block:

```yaml
temporal:
  event_time:
    start:
    end:
    precision:
  observation_time:
    start:
    end:
    acquisition_time:
  valid_time:
    from:
    to:
  system_time:
    created_at:
    updated_at:
    superseded_at:
```

CRIC describes this as **multi-temporal**, with tri-temporal truth at its core: event/world time, valid time, and system/knowledge time, while observation/acquisition time remains explicitly represented.

## 8. Canonical Relationship Predicates

Core scientific/evidential predicates include:

```text
supports
contradicts
refines
supersedes
superseded_by
corroborates
disputes
derived_from
consistent_with
inconsistent_with
```

Spatial/domain predicates may include:

```text
located_in
part_of
contains
feeds
fed_by
drains_to
upstream_of
downstream_of
adjacent_to
intersects
overlaps
within
connected_to
terminates_at
terminates_in
associated_with
dammed_by
exposed_to
experienced
impacted
triggered_by
observed_by
```

Predicates MUST be registered and versioned.

## 9. Evidence and Provenance Levels

Canonical conceptual lineage:

```text
L0 Source Evidence
L1 Normalised Data
L2 Knowledge
L3 Derived Features
L4 Model Output
L5 Interpretation
L6 Decision Intelligence
```

Every significant derived object MUST support backward traversal.

## 10. Canonical Review States

Repository queue/state vocabulary:

```text
inbox
assigned
in-review
approved
rejected
needs-more-evidence
disputed
escalated
archived
```

Canonical `ReviewDecision.decision` values:

```text
approve
reject
modify
needs_more_evidence
disputed
escalate
```

The queue folder name and decision value are deliberately different grammatical forms.

## 11. Autonomy Levels

```text
Level 0  Unrestricted deterministic computation
Level 1  Autonomous analytical generation
Level 2  Autonomous provisional knowledge
Level 3  Trusted scientific graph promotion
Level 4  Safety-significant interpretation
Level 5  Authoritative action by competent external institution
```

## 12. Canonical Repository Names

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
cric-review
```

`cric-review` is canonical in the integrated architecture because HITL is a first-class workflow layer.

## 13. Agent Composition Contract

Canonical composition:

```text
Agent Definition
+ Instructions
+ Dependency Schema
+ Toolsets
+ Datasets
+ Workspace
+ Model Configuration
+ Structured Output Schema
+ Permissions
+ Evaluation Suite
```

No mandatory orchestration framework is part of the CRIC contract.

## 14. Canonical GLOF Analytical Decomposition

```text
Lake Evolution
→ Susceptibility
→ Trigger Conditions
→ Failure State / Mechanism
→ Flood Propagation
→ Exposure
→ Vulnerability
→ Consequence
→ Decision-Support Interpretation
```

## 15. Canonical Data Formats

Preferred where appropriate:

- Markdown + YAML for OKF knowledge;
- JSON / JSON Schema for machine contracts;
- GeoJSON for small interoperable geometry;
- GeoParquet for analytical vector data;
- COG for large rasters;
- STAC for EO cataloguing and asset references.

## 16. Precedence Rule

For implementation disputes:

1. this Canonical Registry;
2. CRIC-PRD-MASTER;
3. specialised PRD document;
4. older examples or illustrative snippets.

A future schema repository release supersedes this prose registry once executable contracts are published.
