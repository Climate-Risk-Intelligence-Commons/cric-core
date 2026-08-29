# CRIC Agent Commons Architecture

## Purpose

The Agent Commons is a first-class CRIC product layer.

Its purpose is to allow agents to be created once and reused across climate-risk research, data engineering, ontology evolution, scientific review, model curation and downstream applications.

Agents must not be tightly coupled to a single application, model provider, dataset, toolset, workspace or credential source.

The reference implementation uses Pydantic AI.

---

# Architectural Principle

A reusable agent is an assembly of independently configurable artefacts:

```text
Agent Definition
+
Instructions
+
Dependency Schema
+
Toolsets
+
Datasets
+
Workspace
+
Model Configuration
+
Structured Output Schema
+
Permissions
+
Evaluation Suite
```

The agent definition should remain as stateless as practical.

Runtime state is injected.

---

# Reference Package Structure

```text
cric-agents/
├── pyproject.toml
├── README.md
├── docs/
├── src/
│   └── cric_agents/
│       ├── __init__.py
│       ├── py.typed
│       ├── deps/
│       ├── models/
│       ├── toolsets/
│       ├── agents/
│       ├── workspaces/
│       ├── permissions/
│       ├── prompts/
│       ├── manifests/
│       └── runtime/
├── tests/
├── evaluations/
└── examples/
```

---

# Agent Factory Pattern

Agents should be instantiated through factory functions rather than globally mutable singletons.

Reference conceptual API:

```python
def create_agent(
    model,
    instructions=None,
    toolsets=None,
    output_type=None,
    dependency_type=None,
    permissions=None,
    workspace_policy=None,
):
    ...
```

Benefits:

- isolation;
- runtime configurability;
- model swapping;
- multi-user safety;
- testing;
- reuse.

---

# Dependency Injection

Runtime dependencies may include:

- HTTP clients;
- database sessions;
- object-store clients;
- authentication tokens;
- local repository paths;
- OKF graph handles;
- materialised search indexes;
- model registries;
- review repository handles;
- logging/tracing contexts;
- user identity;
- workspace identity.

Dependencies must not be hidden in global state.

---

# Toolsets

Tools should be packaged as reusable suites.

Examples:

```text
okf_read_toolset
okf_write_candidate_toolset
provenance_toolset
geospatial_toolset
literature_toolset
dataset_toolset
ontology_toolset
review_toolset
github_toolset
model_registry_toolset
```

Toolsets should expose their own instructions when required.

---

# MCP Integration

CRIC agents may attach external tools through MCP.

MCP must remain optional.

Examples:

- institutional databases;
- remote geospatial services;
- local filesystem services;
- scientific computing services;
- government data gateways;
- specialised model services.

Agent definitions should not assume the presence of a specific MCP server.

---

# Agent Datasets

Datasets must be injected separately from the agent definition.

An agent manifest may state:

```yaml
required_datasets:
  - type: knowledge_graph
    minimum_schema_version: "0.1"

optional_datasets:
  - type: cryosphere_catalogue
  - type: glof_events
```

The same agent should be reusable against:

- local datasets;
- public CRIC datasets;
- private institutional datasets;
- synthetic test datasets.

---

# Agent Workspace

Every agent run receives an isolated workspace.

Reference structure:

```text
run/
├── input/
├── scratch/
├── output/
├── logs/
├── proposed-changes/
└── review-bundles/
```

Agents should not write directly into stable knowledge repositories unless the permission policy explicitly allows it.

---

# Structured Outputs

All consequential agent outputs should use typed Pydantic schemas.

Example classes:

- `EvidenceExtractionResult`;
- `OntologyGapResult`;
- `EntityResolutionResult`;
- `ContradictionAssessment`;
- `ReviewRoutingDecision`;
- `TrainingCandidateResult`.

Unstructured prose may accompany typed output but must not replace it.

---

# Self-Correction Through Validation

Where appropriate, invalid structured output may be returned to the model for correction.

Validation failures should be logged as part of the agent run.

Repeated failures must not result in silently malformed canonical knowledge.

---

# Agent Manifest

Every reusable agent should publish an `agent.yaml`.

Reference:

```yaml
agent_id:
name:
version:
purpose:
domain:
risk_class:
factory:
dependency_schema:
output_schema:
default_model:
supported_models:
required_toolsets:
optional_toolsets:
required_datasets:
optional_datasets:
workspace_policy:
permissions:
human_review_policy:
evaluation_suite:
```

---

# Model Independence

Agents should support runtime model selection.

The agent contract must not require one vendor.

Examples may include:

- OpenAI;
- Anthropic;
- local Ollama-compatible models;
- other Pydantic AI-supported providers.

Evaluation results should be model-specific.

---

# Agent Permissions

Permissions must be explicit.

Possible capabilities:

- read canonical graph;
- search data registry;
- read external sources;
- write scratch files;
- create candidate nodes;
- create review bundles;
- propose ontology changes;
- open pull requests;
- modify canonical knowledge;
- publish risk assessment;
- invoke external actions.

Most research agents should not receive the final two permissions.

---

# Agent Risk Classes

## Class A: Deterministic Support

Examples:

- schema validator;
- hash generator;
- format converter.

## Class B: Low-Risk Analytical Agent

Examples:

- literature classifier;
- ontology gap detector;
- relationship candidate generator.

## Class C: Provisional Knowledge Agent

Examples:

- evidence extractor;
- event reconstruction assistant;
- entity resolver.

May create candidate knowledge.

## Class D: Safety-Relevant Interpretation Agent

Examples:

- GLOF risk interpretation;
- hazard escalation assessment.

Requires human review before trusted publication or operational use.

## Class E: Authoritative Action

CRIC agents must not autonomously claim authoritative emergency powers.

---

# Agent Teams

Agent teams are compositions of reusable agents.

Example research team:

```text
Scout
↓
Source Qualification
↓
Licence Review
↓
Acquisition
↓
Evidence Extraction
↓
Entity Resolution
↓
Contradiction Detection
↓
Ontology Watch
↓
Provenance Audit
↓
Human Review Router
```

Parallel execution is encouraged where tasks are independent.

---

# Continuous Ontology Awareness

Every knowledge-processing agent should be capable of emitting an `OntologyGapResult`.

This allows agents to report:

- unknown node types;
- missing predicates;
- ambiguous terms;
- duplicate concepts;
- overly broad concepts;
- overly narrow concepts;
- new cross-domain relationships.

Ontology evolution should therefore emerge naturally from normal agent work.

---

# Human Review Integration

Agents may pause by creating a review bundle.

A paused workflow should persist:

- run ID;
- agent state;
- unresolved question;
- evidence;
- proposed change;
- required reviewer expertise.

The agent should later detect an approved `decision.yaml` and resume.

No ephemeral conversational memory should be required to resume.

---

# Agent Run Provenance

Every run should record:

- agent ID;
- agent version;
- model provider;
- model identifier;
- instructions version;
- toolset versions;
- dependency configuration excluding secrets;
- dataset versions;
- input nodes;
- output nodes;
- started at;
- completed at;
- token/cost metadata where available;
- errors;
- human reviews;
- Git commit hashes.

---

# Observability

Production wrappers may use Pydantic Logfire or equivalent observability.

Observability should include:

- agent execution;
- tool calls;
- validation failures;
- retries;
- latency;
- token use;
- exception traces.

No observability platform is canonical.

---

# Testing

## Tool Unit Tests

Tools should be testable without LLM invocation.

## Agent Contract Tests

Validate:

- dependency compatibility;
- tool registration;
- output schemas;
- permissions.

## Deterministic Agent Tests

Use Pydantic AI test or mock models where possible.

## Evaluation Suites

Each agent should maintain evaluation cases representing its intended responsibilities.

## Regression Tests

Prompt, model and tool changes should not silently degrade critical behaviours.

---

# Versioning

Semantic versioning applies to agents.

## Major

Breaking:

- output schema;
- dependency schema;
- permission semantics;
- removed tools.

## Minor

Non-breaking:

- added toolsets;
- optional dependency fields;
- expanded capabilities;
- new compatible models.

## Patch

- prompt refinements;
- bug fixes;
- documentation;
- internal implementation corrections.

---

# Reusable Agent Catalogue

`cric-agents` should publish a machine-readable catalogue.

Example agent classes:

- Research Scout Agent;
- Source Qualification Agent;
- Licence Agent;
- Acquisition Agent;
- Metadata Agent;
- Evidence Extraction Agent;
- Entity Resolution Agent;
- Temporal Reconciliation Agent;
- Spatial Reconciliation Agent;
- Contradiction Agent;
- Data Quality Agent;
- Ontology Watch Agent;
- Ontology Synthesis Agent;
- Training Curator Agent;
- Scientific Critic Agent;
- Provenance Auditor Agent;
- Human Review Router Agent;
- Repository Maintenance Agent.

---

# Downstream Reuse

External projects should be able to install and compose CRIC agents as normal Python packages.

Example:

```python
from cric_agents import create_evidence_agent
```

A downstream application should be able to provide:

- its own model;
- its own dataset;
- its own credentials;
- its own workspace;
- its own output destination.

CRIC should therefore become a reusable agent engineering commons in addition to a climate-risk knowledge commons.

---

# v0.1 Deliverables

At minimum:

- package structure;
- one generic dependency model;
- toolset interfaces;
- workspace abstraction;
- agent manifest schema;
- permissions schema;
- at least three reusable agents;
- test-model evaluation examples;
- review-bundle integration;
- one MCP toolset example;
- model swapping example;
- documentation for downstream reuse.
