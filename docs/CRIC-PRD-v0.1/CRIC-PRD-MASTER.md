# Climate Risk Intelligence Commons (CRIC)
# Product Requirements Document Master

**Specification:** CRIC PRD v0.1 Integrated  
**Status:** Architecture and implementation baseline  
**First domain:** Cryosphere / GLOF  
**Canonical registry:** `CRIC-Schema-and-Vocabulary-Registry.md`

## Product Thesis

> **Climate Risk Intelligence Commons (CRIC) is an open-source, provenance-preserving, temporally aware knowledge, data, modelling and agentic infrastructure for representing, integrating, analysing and deriving intelligence from climate-risk evidence. It is designed for human researchers, deterministic software and autonomous agents to operate on the same inspectable evidence base. Cryosphere risk, beginning with GLOF intelligence, is its first domain implementation.**

## Constitutional Product Rules

1. Evidence lineage is immutable.
2. Every significant derived value must be traceable to source evidence.
3. Scientific contradiction is represented, not erased.
4. Historical knowledge state remains reconstructable.
5. Evidence completeness is separate from hazard/risk.
6. Unknown is not negative.
7. Deterministic computation is preferred where deterministic computation is suitable.
8. Agents operate through typed contracts and explicit permissions.
9. Agent tools, datasets, workspaces, dependencies and model configuration remain separable.
10. Human oversight increases with uncertainty, irreversibility, authority and consequence.
11. CRIC never silently assumes institutional warning authority.
12. Core architecture remains climate-risk-wide rather than GLOF-specific.

## Product Layers

```text
CRIC Core
Climate Risk Ontology
Domain Ontologies
Evidence and Data Commons
Knowledge Commons
Agent Commons
Model Commons
Computational Commons
Interfaces
Human Review and Governance
```

## Canonical Repository Family

```text
cric-core
cric-knowledge
cric-data
cric-ingest
cric-cryosphere
cric-glof
cric-models
cric-agents
cric-review
cric-api
cric-ui
cric-docs
```

## Canonical PRD Tree

```text
CRIC-PRD-v0.1/
├── CRIC-PRD-MASTER.md
├── CRIC-Schema-and-Vocabulary-Registry.md
├── CRIC-Requirements-Traceability-Matrix.md
├── CRIC-Repository-Dependency-and-Implementation-Sequence.md
├── product/
├── knowledge/
├── domains/
├── data/
├── ai/
├── interfaces/
├── engineering/
├── community/
└── implementation/
```

## Document Map

### Product

- `product/Product-Vision-and-Principles.md`
- `product/Product-Scope-and-Domain-Architecture.md`
- `product/Repository-and-System-Architecture.md`

### Knowledge

- `knowledge/OKF-Knowledge-Graph-Specification.md`
- `knowledge/Core-Ontology-Specification.md`
- `knowledge/Temporal-and-Epistemic-Ontology.md`
- `knowledge/Evidence-Provenance-and-Trust.md`
- `knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md`
- `knowledge/Ontology-Evolution-and-Governance.md`

### Domains

- `domains/Cryosphere-Ontology.md`
- `domains/GLOF-Ontology.md`
- `domains/StateSnapshot-and-Event-Cube-Specification.md`

### Data

- `data/Data-Commons-Architecture.md`
- `data/Ingestion-and-Licensing.md`
- `data/Data-Quality-and-Validation.md`
- `data/Training-Data-and-Benchmark-Specification.md`

### AI

- `ai/Agent-Commons-Architecture.md`
- `ai/Agent-Team-Specifications.md`
- `ai/Model-Commons-and-ML-Specification.md`
- `ai/Responsible-Autonomy-and-HITL.md`

### Interfaces

- `interfaces/API-and-SDK-Specification.md`
- `interfaces/Search-and-Graph-Interfaces.md`
- `interfaces/Human-Applications-and-UI.md`

### Engineering

- `engineering/Software-Architecture.md`
- `engineering/Security-and-Responsible-AI.md`
- `engineering/Testing-and-Quality-Assurance.md`
- `engineering/Deployment-Versioning-and-Releases.md`

### Community

- `community/Open-Source-Governance.md`
- `community/Volunteer-HITL-Workflow.md`
- `community/Contribution-and-Review-Process.md`

### Implementation

- `implementation/CRIC-v0.1-Implementation-Specification.md`
- `implementation/CRIC-v0.2-Implementation-Specification.md`

## First Implementation Goal

CRIC v0.1 must make the chain:

```text
source observation
→ provenance
→ normalised knowledge
→ state reconstruction
→ risk-relevant feature
→ model or rule
→ downstream consequence
→ human-reviewed interpretation
```

visible, inspectable and reproducible.

## Agent Commons

Agents are not application-specific prompt wrappers.

A CRIC agent is assembled from:

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

This enables the same agent to be reused in different scientific workflows and downstream applications.

## Knowledge Commons

The OKF knowledge graph is itself a CRIC product.

Every independently addressable piece of scientifically, evidentially, computationally or agentically valuable knowledge should be representable as an atomic node when it benefits from its own provenance, uncertainty, temporal context, relationships or lifecycle.

## Temporal Truth

CRIC preserves:

- event time;
- observation/acquisition time;
- valid time;
- system/knowledge time.

Accepted history is not edited away. New knowledge supersedes or disputes earlier knowledge through explicit graph relationships.

## Responsible Autonomy

CRIC uses six autonomy levels from unrestricted deterministic computation through external authoritative action.

Safety-significant interpretation requires human review. Authoritative emergency action remains with competent external institutions.

## v0.1 Definition of Done

An external technically competent researcher can:

1. clone the relevant CRIC repositories;
2. inspect the Obsidian-compatible knowledge commons;
3. validate canonical OKF nodes;
4. reproduce a reference GLOF Event Cube;
5. create a provenance-linked TrainingSample;
6. run a baseline model;
7. trace its output back to original evidence;
8. inspect contradiction and uncertainty;
9. observe or complete a HITL review;
10. reproduce the component versions used.

## Implementation Authority

For coding work, use the following precedence:

1. executable contracts in a released `cric-core`;
2. `CRIC-Schema-and-Vocabulary-Registry.md`;
3. this Master PRD;
4. specialised PRD documents;
5. examples and older illustrative snippets.

## Safety Statement

CRIC v0.1 and v0.2 are research and reference implementations unless separately validated and authorised for operational use. Model scores, risk states and agent outputs must not be represented as official warnings merely because they are generated by CRIC.
