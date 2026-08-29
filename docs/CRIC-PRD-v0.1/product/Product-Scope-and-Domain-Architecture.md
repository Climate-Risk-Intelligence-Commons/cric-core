# CRIC Product Scope and Domain Architecture

## Purpose

This document defines the boundary between the domain-independent Climate Risk Intelligence Commons and its domain implementations.

## Product Scope

CRIC is infrastructure for representing, integrating, validating, analysing and deriving intelligence from climate-risk evidence.

It includes:

- knowledge representation;
- data cataloguing;
- provenance;
- temporal truth;
- scientific claims and contradictions;
- domain ontologies;
- deterministic workflows;
- reusable AI agents;
- model development;
- review;
- search;
- APIs;
- human workbenches.

It does not require every CRIC deployment to install every layer.

## Domain Architecture

```text
CRIC Core
↓
Climate Risk Ontology
↓
Domain Ontology
↓
Hazard / Application Package
```

Example:

```text
CRIC Core
↓
Climate Risk
↓
Cryosphere
↓
GLOF
```

Future examples:

```text
Climate Risk → Hydrometeorology → Flood
Climate Risk → Slope Processes → Landslide
Climate Risk → Fire → Wildfire
Climate Risk → Heat → Heatwave
Climate Risk → Coastal → Coastal Flooding
```

## Core Invariance Rule

Nothing in `cric-core` should unnecessarily assume:

- glacier;
- glacial lake;
- GLOF;
- Himalayan geography;
- satellite-only observation;
- one risk equation;
- one model family.

## Climate Risk Shared Concepts

Shared concepts include:

- Hazard;
- HazardProcess;
- Trigger;
- Exposure;
- Vulnerability;
- Consequence;
- Risk;
- Scenario;
- Indicator;
- Threshold;
- Alert;
- Intervention;
- Control;
- Cascade;
- CompoundEvent.

## Domain Package Responsibilities

A domain package defines:

- specialised entities;
- observations;
- processes;
- controlled vocabularies;
- domain relationships;
- validation rules;
- domain retrieval policies;
- domain agent/tool extensions;
- domain benchmark tasks.

## Cross-Domain Relationships

Domains must be able to reference each other without copying entities.

Example:

```text
ExtremePrecipitationEvent
→ triggers
LandslideEvent
→ impacts
GlacialLake
→ contributes_to
GLOFEvent
```

## Cascading and Compound Risk

Cascading and compound events belong to shared climate-risk semantics because interactions may cross domain boundaries.

## Domain Registration

Each domain should publish a manifest:

```yaml
domain_id:
name:
version:
parent_ontology:
schema_dependencies: []
types: []
predicates: []
controlled_vocabularies: []
validators: []
migrations: []
```

## Domain Independence

A user should be able to install:

```text
cric-core + cric-knowledge + another future domain
```

without installing cryosphere/GLOF packages.

## First Reference Domain

Cryosphere/GLOF is first because it exercises:

- multimodal EO;
- temporal evolution;
- rare events;
- cascading mechanisms;
- downstream exposure;
- scientific uncertainty;
- historical reconstruction.

Its complexity makes it a strong architectural test.

## Product Non-Goals

CRIC is not:

- a single hazard dashboard;
- a single AI model;
- a single agent;
- a proprietary data warehouse;
- an autonomous government warning authority.

## Acceptance Criteria

- domain-neutral core schemas exist;
- Cryosphere extends rather than modifies core semantics;
- GLOF extends Cryosphere and Climate Risk;
- cross-domain predicates are possible;
- domain manifests are versioned;
- a second domain can be prototyped without redesigning core.
