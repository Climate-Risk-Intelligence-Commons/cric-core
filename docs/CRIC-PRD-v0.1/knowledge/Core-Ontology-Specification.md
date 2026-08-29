# CRIC Core Ontology Specification

## Purpose

This document defines the domain-independent ontology of the Climate Risk Intelligence Commons.

CRIC Core provides the smallest stable semantic layer upon which domain ontologies, including cryosphere and GLOF, are built. Domain repositories may extend the core ontology but must not redefine the semantic meaning of stable core types.

The core ontology is designed for:

- OKF Markdown knowledge graphs;
- Pydantic validation;
- deterministic graph traversal;
- temporal reasoning;
- evidence lineage;
- agentic retrieval;
- scientific disagreement;
- machine-learning provenance;
- human review.

---

# Ontology Design Rules

## Stable Core, Extensible Domains

CRIC Core should remain deliberately small.

Domain-specific meaning belongs in domain repositories.

## Type Identity is Versioned

Every type has:

- canonical identifier;
- canonical name;
- definition;
- parent type;
- ontology version introduced;
- status;
- aliases;
- constraints.

## Inheritance Must Be Semantically Meaningful

Inheritance means that every instance of the child satisfies the semantic definition of the parent.

Do not use inheritance merely to organise files.

## Relationships are First-Class Semantics

Important relationships must use controlled predicates rather than being hidden only in prose.

## Fields and Nodes Serve Different Purposes

A value remains an embedded field when it has no independent scientific lifecycle.

A value becomes a node when it has independent provenance, uncertainty, temporal validity, contradiction potential, review state, graph relationships or training value.

---

# Root Types

```text
CRICObject
├── KnowledgeObject
│   ├── Entity
│   ├── Event
│   ├── Observation
│   ├── StateSnapshot
│   ├── Claim
│   ├── Evidence
│   └── Assessment
├── ResourceObject
│   ├── Source
│   ├── Dataset
│   ├── DatasetVersion
│   ├── Asset
│   └── Licence
├── ComputationalObject
│   ├── Workflow
│   ├── Agent
│   ├── AgentRun
│   ├── Toolset
│   ├── Model
│   ├── ModelRun
│   ├── TrainingSample
│   ├── Label
│   └── Prediction
├── GovernanceObject
│   ├── ReviewRequest
│   ├── ReviewDecision
│   ├── OntologyProposal
│   └── MigrationRecord
└── QualityObject
    ├── ProvenanceRecord
    ├── QualityAssessment
    └── UncertaintyAssessment
```

---

# `CRICObject`

Every canonical CRIC object inherits:

- `id`;
- `type`;
- `subtype`;
- `title`;
- `aliases`;
- `schema_version`;
- `ontology_version`;
- `knowledge_state`;
- `temporal`;
- `provenance`;
- `licensing`;
- `relationships`;
- `tags`.

---

# `Entity`

Represents a persistent identifiable thing whose identity can continue while its state changes.

Examples:

- lake;
- glacier;
- river;
- settlement;
- bridge;
- sensor;
- organisation.

An Entity should not be overwritten with historical measurements. Measurements belong in Observation or StateSnapshot nodes.

---

# `Event`

Represents an occurrence or process episode situated in time.

Examples:

- GLOF;
- landslide;
- avalanche;
- earthquake;
- extreme rainfall episode;
- dam breach.

Required semantic characteristics:

- temporal extent or temporal uncertainty;
- participating entities where known;
- evidence;
- location or spatial footprint where relevant.

---

# `Observation`

Represents a measured, reported or extracted observation about a subject.

Core attributes:

- `subject_id`;
- `variable`;
- `value`;
- `unit`;
- `method`;
- `observation_time`;
- `source`;
- `quality`;
- `uncertainty`.

Observation values must not be silently changed. Corrections create a superseding observation.

---

# `StateSnapshot`

Represents a coherent state of an entity or system for a specific temporal point or interval.

A snapshot references observations rather than duplicating their provenance.

Core attributes:

- `subject_id`;
- `snapshot_time`;
- `included_observations`;
- `derived_features`;
- `context_nodes`;
- `completeness`;
- `conflicts`.

---

# `Claim`

Represents an assertion that can be supported, disputed, refined or superseded.

Core attributes:

- `subject`;
- `predicate`;
- `object` or `value`;
- `claim_text`;
- `claimant`;
- `evidence_nodes`;
- `confidence`;
- `status`;
- `spatial_scope`;
- `temporal_scope`.

Claims must be independently addressable where contradiction is scientifically relevant.

---

# `Evidence`

Represents an evidential object used to support or challenge a claim, assessment or decision.

Evidence may point to:

- observation;
- publication;
- dataset;
- image;
- field record;
- model output;
- government record;
- review.

Evidence does not automatically imply truth.

---

# `Assessment`

Represents an interpreted evaluation.

Examples:

- quality assessment;
- hazard susceptibility assessment;
- risk assessment;
- scientific review.

An assessment must identify:

- subject;
- method;
- evidence;
- assumptions;
- uncertainty;
- assessor;
- assessment time;
- operational status.

---

# `Source`

Represents an origin of information.

Examples:

- scientific paper;
- government report;
- satellite provider;
- web resource;
- field notebook.

A Source node may exist even when the underlying protected source document cannot be redistributed.

---

# `Dataset` and `DatasetVersion`

`Dataset` represents persistent dataset identity.

`DatasetVersion` represents an immutable release or acquisition state.

Every training or modelling workflow must depend on DatasetVersion rather than mutable Dataset identity.

---

# `Asset`

Represents a concrete file, object, raster, table, image, archive or externally stored data object.

Core attributes:

- URI;
- hash;
- size;
- media type;
- licence;
- temporal coverage;
- spatial coverage;
- acquisition metadata.

---

# Computational Types

## `Workflow`

Defines a reusable computational or scientific procedure.

## `Agent`

Defines a reusable agent specification.

## `AgentRun`

Records a concrete execution of an agent.

## `Toolset`

Defines a reusable collection of tools.

## `Model`

Defines model identity and architecture.

## `ModelRun`

Records a training, inference or evaluation execution.

## `TrainingSample`

Defines a reproducible training unit.

## `Label`

Represents a training or evaluation label with provenance and epistemic status.

## `Prediction`

Represents a model output tied to model version, inputs and time.

---

# Governance Types

## `ReviewRequest`

A machine-readable request for human review.

## `ReviewDecision`

The human response to a review request.

## `OntologyProposal`

A proposed ontology addition, modification or deprecation.

## `MigrationRecord`

Records how canonical knowledge was migrated between schema or ontology versions.

---

# Quality Types

## `ProvenanceRecord`

Captures lineage.

## `QualityAssessment`

Captures quality evaluation.

## `UncertaintyAssessment`

Captures quantified or qualitative uncertainty.

---

# Climate Risk Extension Types

CRIC Core should define general climate-risk concepts without domain-specific implementation.

```text
Hazard
HazardProcess
Trigger
Exposure
Vulnerability
Consequence
Risk
Scenario
Indicator
Threshold
Alert
Intervention
Control
Cascade
CompoundEvent
```

---

# Hazard

A potentially damaging physical process, phenomenon or condition.

Hazard must be separated from exposure, vulnerability and consequence.

---

# Trigger

A condition or event contributing to initiation or escalation of a hazard process.

A trigger may itself be another hazard event.

---

# Cascade

Represents causal or contributory propagation across multiple events or processes.

Example:

```text
ice avalanche
→ displacement wave
→ overtopping
→ moraine breach
→ GLOF
→ bridge failure
→ road isolation
```

Each edge must retain evidence and confidence where appropriate.

---

# Compound Event

Represents interacting hazards or drivers whose combined behaviour is materially different from considering them independently.

---

# Controlled Vocabulary Governance

Controlled vocabularies must have:

- stable IDs;
- definitions;
- aliases;
- status;
- source;
- version introduced;
- deprecation metadata.

Free-text values should not be used where a stable controlled vocabulary is necessary for programmatic comparison.

---

# Pydantic Representation

Every stable core type should have:

- Pydantic model;
- generated JSON Schema;
- OKF mapping;
- example fixture;
- validation tests.

Schema generation must be deterministic.

---

# Ontology Registry

`cric-core` should publish a machine-readable ontology registry:

```yaml
ontology_id: cric-core
version: "0.1.0"
types:
  - id: CRIC-TYPE-ENTITY
    name: Entity
    parent: CRICObject
    status: stable
predicates:
  - id: CRIC-PRED-DERIVED-FROM
    name: derived_from
    status: stable
```

---

# v0.1 Acceptance Criteria

- core type registry exists;
- Pydantic models validate example nodes;
- inheritance is documented;
- predicates are registered;
- unknown types fail validation unless explicitly allowed as experimental;
- domain extensions can register child types without modifying core code;
- ontology version is embedded in canonical OKF nodes.
