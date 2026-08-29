# CRIC Agent Team Specifications

## Purpose

This document defines the initial reusable agent catalogue and how individual Pydantic agents compose into teams.

Agents are first-class reusable CRIC artefacts. Teams are compositions, not monolithic super-agents.

---

# Agent Construction Contract

Each agent must define:

- agent ID;
- version;
- purpose;
- typed dependencies;
- typed output;
- required toolsets;
- optional toolsets;
- required datasets;
- workspace policy;
- permissions;
- risk class;
- HITL policy;
- evaluation suite.

---

# Team Design Principles

- prefer specialised agents;
- parallelise independent work;
- keep deterministic operations outside LLM reasoning;
- persist intermediate outputs;
- make handoffs typed;
- make every agent replaceable;
- preserve run provenance;
- avoid hidden shared memory.

---

# 1. Research Scout Agent

## Purpose

Discover potentially relevant sources.

## Inputs

- research topic;
- entity IDs;
- temporal/spatial scope;
- ontology context.

## Outputs

- candidate source list;
- relevance rationale;
- search provenance.

## Permissions

Read/search only.

---

# 2. Source Qualification Agent

Evaluates:

- relevance;
- source identity;
- likely authority;
- primary/secondary status;
- recency;
- methodological transparency.

Produces candidate SourceQualityAssessment.

---

# 3. Licence Agent

Determines candidate licence state and permitted CRIC handling.

Outputs:

- redistribution classification;
- attribution requirements;
- uncertainty;
- HITL request if ambiguous.

Must never authorise beyond evidence.

---

# 4. Acquisition Agent

Uses deterministic acquisition tools.

Responsibilities:

- fetch permitted assets;
- register reference-only sources;
- hash bytes;
- generate acquisition manifest.

---

# 5. Metadata Agent

Extracts and normalises:

- title;
- authors/provider;
- DOI/identifier;
- publication time;
- spatial/temporal coverage;
- sensor;
- format.

---

# 6. Evidence Extraction Agent

Extracts candidate scientific facts and claims from sources.

Outputs typed:

- candidate observations;
- claims;
- evidence links;
- uncertainties;
- quoted snippets only where legally permitted.

All outputs remain candidate until applicable promotion rules are satisfied.

---

# 7. Entity Resolution Agent

Matches extracted references to canonical CRIC entities.

Outputs:

- exact match;
- probable match;
- new entity candidate;
- ambiguity set.

High-impact ambiguous merges route to review.

---

# 8. Temporal Reconciliation Agent

Compares:

- event dates;
- acquisition dates;
- valid intervals;
- system knowledge.

Detects temporal contradictions and false precision.

---

# 9. Spatial Reconciliation Agent

Handles:

- geometry matching;
- lake aliases;
- coordinate disagreement;
- basin membership;
- upstream/downstream relationships.

Uses deterministic GIS tools wherever possible.

---

# 10. Contradiction Agent

Searches graph neighbourhoods for:

- direct conflicts;
- partial conflicts;
- causal disagreement;
- temporal disagreement;
- measurement disagreement.

Creates candidate contradiction assessments.

---

# 11. Data Quality Agent

Aggregates validators and scientific quality signals.

Does not silently modify scientific data.

---

# 12. Ontology Watch Agent

Runs during knowledge interactions to detect ontology gaps.

Outputs `OntologyGapResult`.

This agent is intentionally pervasive and may be attached as a sidecar capability to many workflows.

---

# 13. Ontology Synthesis Agent

Turns recurring gaps into candidate ontology proposals.

May draft:

- definition;
- hierarchy;
- predicates;
- examples;
- Pydantic changes;
- migration impact.

---

# 14. Ontology Critic Agent

Independently challenges proposals.

Checks:

- duplication;
- overfitting to one paper;
- domain leakage;
- semantic ambiguity;
- unnecessary type proliferation.

---

# 15. Provenance Auditor Agent

Checks:

- source links;
- hashes;
- parent chains;
- agent-run records;
- licence;
- model provenance.

---

# 16. StateSnapshot Builder Agent

Coordinates deterministic queries and derivations to assemble candidate snapshots.

It references canonical observations rather than copying them.

---

# 17. Event Reconstruction Agent

Builds candidate Event Cubes from:

- historical event registry;
- temporal observations;
- claims;
- post-event evidence.

Must expose missing windows and contradictions.

---

# 18. Training Curator Agent

Selects candidate training samples.

Checks:

- label eligibility;
- negative semantics;
- leakage;
- split contamination;
- quality gates.

---

# 19. Scientific Critic Agent

Acts as an adversarial reviewer.

Questions:

- unsupported causal inference;
- missing alternative explanation;
- inappropriate certainty;
- data limitations;
- extrapolation.

---

# 20. Model Evaluation Agent

Runs benchmark/evaluation tools and drafts structured evaluation reports.

---

# 21. Human Review Router Agent

Determines whether an unresolved item requires:

- no review;
- domain volunteer;
- ontology reviewer;
- scientific expert;
- maintainer;
- safety escalation.

Creates self-contained review bundles.

---

# 22. Review Resumption Agent

Scans approved/rejected review artefacts and resumes eligible paused workflows.

Must use durable run IDs rather than conversational memory.

---

# 23. Repository Maintenance Agent

May:

- regenerate indexes;
- run validators;
- prepare release manifests;
- identify stale candidate branches;
- draft pull requests.

Stable merges remain governed by repository permissions.

---

# Agent Team: Literature-to-Knowledge

```text
Scout
├── Source Qualification
├── Licence
└── Ontology Watch
     ↓
Acquisition/Reference
     ↓
Metadata
     ↓
Evidence Extraction
├── Entity Resolution
├── Temporal Reconciliation
├── Contradiction
└── Ontology Watch
     ↓
Provenance Audit
     ↓
Promotion or HITL
```

---

# Agent Team: Event Reconstruction

```text
Event candidate
├── Identity Resolution
├── Temporal Reconciliation
├── Spatial Reconciliation
├── Evidence Retrieval
└── Ontology Watch
        ↓
StateSnapshot Builder
        ↓
Event Reconstruction
├── Contradiction
├── Data Quality
└── Scientific Critic
        ↓
HITL where required
```

---

# Agent Team: Training Dataset

```text
Event Cubes / Negative Cubes
↓
Training Curator
├── Data Quality
├── Leakage Checker
├── Provenance Auditor
└── Ontology Watch
↓
Dataset Manifest
↓
Benchmark Freeze Review
```

---

# Agent Team: Ontology Evolution

```text
Many normal workflows
↓
OntologyGapResults
↓
Gap clustering
├── Ontology Synthesis
└── Ontology Critic
↓
Candidate proposal
↓
Automated compatibility tests
↓
HITL if required
↓
Pull request
```

---

# Shared Toolsets

Suggested reusable toolsets:

- OKF read;
- OKF candidate write;
- graph traversal;
- provenance;
- geospatial;
- STAC;
- literature;
- dataset registry;
- Git/GitHub;
- review;
- model registry;
- validation.

---

# Parallel Execution

Parallelism is preferred for:

- independent source reviews;
- competing scientific interpretations;
- ontology critics;
- geographic partitions;
- quality checks.

Sequential execution is required where a later task depends on validated output from an earlier stage.

---

# Agent Dependencies

Example Pydantic dependency bundle:

```python
class CRICAgentDeps(BaseModel):
    workspace: WorkspaceHandle
    graph: KnowledgeGraphHandle
    dataset_registry: DatasetRegistryHandle
    review_repo: ReviewRepositoryHandle
    identity: RuntimeIdentity
```

Secrets should be injected through runtime providers, not serialised into manifests.

---

# Evaluation

Each agent must have:

- unit-tested tools;
- structured-output tests;
- mock-model tests;
- adversarial cases;
- regression fixtures;
- permission tests.

---

# v0.1 Minimum Agent Set

The first functioning release should implement at least:

- Evidence Extraction Agent;
- Entity Resolution Agent;
- Ontology Watch Agent;
- Provenance Auditor Agent;
- Human Review Router Agent.

Additional agents may initially exist as specifications and test stubs.

---

# Acceptance Criteria

- agents are independently installable/reusable;
- teams exchange typed artefacts;
- no hidden shared memory is required;
- ontology awareness is attachable to workflows;
- review pause/resume is durable;
- model provider is replaceable;
- permission boundaries are testable.
