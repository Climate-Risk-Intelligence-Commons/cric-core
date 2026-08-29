# CRIC Repository Dependency and Implementation Sequence

## Purpose

This document converts the PRD family into a coding order suitable for human engineering teams and coding agents.

## Dependency Graph

```text
cric-core
├── cric-knowledge
├── cric-data
├── cric-cryosphere
│   └── cric-glof
├── cric-ingest
├── cric-agents
├── cric-models
├── cric-review
├── cric-api
└── cric-ui
```

Operationally, several repositories depend on more than one upstream package. The diagram expresses the architectural spine rather than every package-manager dependency.

## Phase 0: Organisation and Contracts

Create repositories, branch protection, licences, contribution templates, CI skeletons and coordinated release metadata.

Exit criterion: repositories exist and `cric-core` can publish a versioned Python package.

## Phase 1: `cric-core`

Implement first because every other repository consumes its contracts.

Build order:

1. identifier types;
2. knowledge-state models;
3. temporal models;
4. spatial models;
5. provenance;
6. base object hierarchy;
7. relationship model;
8. ontology registry;
9. review contracts;
10. validation framework;
11. JSON Schema export.

Exit criterion: canonical example OKF nodes validate.

## Phase 2: `cric-knowledge`

Implement:

- OKF parser/serializer;
- vault layout;
- example nodes;
- graph link validator;
- Obsidian indexes.

Exit criterion: knowledge-only deployment works without API/database.

## Phase 3: `cric-data`

Implement:

- Dataset;
- DatasetVersion;
- DataAsset;
- manifests;
- licence metadata;
- storage URI abstraction;
- reference dataset registry.

Exit criterion: small and large assets can be represented without ambiguity.

## Phase 4: `cric-cryosphere` and `cric-glof`

Implement domain schemas and controlled vocabularies.

Start with:

- Glacier;
- GlacialLake;
- Moraine/MoraineDam;
- cryosphere observations;
- GLOFEvent;
- trigger/failure mechanism;
- StateSnapshot extensions;
- Event Cube manifests.

Exit criterion: one manually curated historical event validates.

## Phase 5: `cric-ingest`

Implement deterministic acquisition and normalisation.

Initial pipelines:

- literature/reference ingestion;
- lake inventory ingestion;
- EO/STAC reference ingestion;
- DEM context;
- meteorological context;
- provenance generation.

Exit criterion: one source-to-observation workflow is reproducible.

## Phase 6: Graph Materialisation and Retrieval

This may initially live in `cric-core`/`cric-api` libraries before being separated if needed.

Implement:

- edge table;
- node index;
- temporal filters;
- spatial filters;
- bounded traversal;
- context package.

Exit criterion: multi-hop retrieval requires no manual LLM file crawling.

## Phase 7: `cric-review`

Implement:

- review bundle schema;
- queue states;
- reviewer registry;
- decision validation;
- durable pause/resume state.

Exit criterion: a synthetic workflow pauses and resumes through Git/local review.

## Phase 8: `cric-agents`

Implement reusable infrastructure before a large catalogue.

First agents:

1. Evidence Extraction;
2. Entity Resolution;
3. Ontology Watch;
4. Provenance Auditor;
5. Human Review Router.

Exit criterion: the same agent can run with different injected dataset/workspace/model configurations.

## Phase 9: Event Cube Pipeline

Integrate domain, ingestion, retrieval and agents.

Exit criterion: first positive Event Cube and first negative cube are reproducible.

## Phase 10: `cric-models`

Implement:

- TrainingSample;
- Label;
- FeatureSet;
- split definitions;
- baseline training;
- evaluation;
- model cards;
- model registry.

Exit criterion: model output traces to original source evidence.

## Phase 11: `cric-api`

Implement only after core contracts stabilise sufficiently.

Initial endpoints:

- entity;
- observation;
- event;
- snapshot;
- provenance;
- search;
- graph;
- agent run;
- review.

## Phase 12: `cric-ui`

Implement:

- map;
- entity explorer;
- timeline;
- evidence/provenance explorer;
- contradiction view;
- HITL review view.

## Phase 13: Reference Dataset Expansion

Scale toward the v0.1 target dataset while continuously running ontology-gap detection and quality validation.

## Phase 14: Coordinated v0.1 Release

Required evidence:

- tests;
- release manifest;
- compatibility matrix;
- reference Event Cube;
- reference benchmark;
- baseline model;
- agent/HITL demonstration;
- workbench;
- reproducibility instructions.

## Coding-Agent Work Package Rule

Every implementation task handed to a coding agent SHOULD contain:

```yaml
work_package:
  repository:
  objective:
  authoritative_prd_sections: []
  upstream_contracts: []
  files_allowed_to_change: []
  tests_required: []
  acceptance_criteria: []
  prohibited_changes: []
  review_required:
```

This prevents coding agents from opportunistically redesigning CRIC architecture while implementing a narrow task.

## Critical Path

```text
Core schemas
→ OKF parser
→ domain schemas
→ ingestion/provenance
→ StateSnapshot/Event Cube
→ training dataset
→ baseline model
```

Agent Commons and HITL can progress in parallel once `cric-core` contracts exist.

## Parallel Workstreams

After Phase 1:

- Knowledge Commons;
- Data Commons;
- Cryosphere ontology;
- Agent runtime;
- review protocol;
- documentation

can progress substantially in parallel.

## Architecture Freeze Points

Before v0.1 coding accelerates, freeze candidate versions of:

1. ID format;
2. base OKF frontmatter;
3. temporal model;
4. provenance model;
5. relationship representation;
6. knowledge-state vocabulary;
7. review decision schema;
8. agent manifest schema.

Changes remain possible but require explicit migration after the freeze.
