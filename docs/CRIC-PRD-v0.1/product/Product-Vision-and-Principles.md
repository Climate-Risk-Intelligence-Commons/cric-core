# CRIC Product Vision and Principles

## Purpose

This document defines the long-term product intent, design philosophy and non-negotiable principles of the Climate Risk Intelligence Commons.

CRIC is intended to become an open scientific infrastructure through which heterogeneous climate-risk evidence can be collected, represented, analysed, challenged, recombined and reused by humans and machines.

Cryosphere risk is the first implementation domain. GLOF intelligence is the first hazard vertical.

---

# Vision

CRIC should become a durable, open and machine-readable memory of climate-risk evidence.

The system should allow a future researcher, public institution, community organisation, modeller or AI agent to ask not only:

> What is the current assessment?

but also:

> What evidence produced it?

> What did the system know at an earlier time?

> Which sources disagree?

> Which transformation created this feature?

> Which samples trained this model?

> Which assumptions remain unresolved?

> Which ontology definitions changed after the original analysis?

This ability to reconstruct reasoning and evidence is central to CRIC.

---

# Product Mission

CRIC shall provide reusable infrastructure for:

- climate-risk evidence integration;
- knowledge graph construction;
- temporal knowledge preservation;
- scientific provenance;
- data quality;
- contradiction management;
- reusable agent creation;
- model training and evaluation;
- cascading hazard reasoning;
- exposure and consequence analysis;
- open scientific collaboration.

---

# Primary Users

CRIC is designed for:

- climate scientists;
- cryosphere scientists;
- hydrologists;
- geologists;
- remote-sensing researchers;
- disaster-risk practitioners;
- data scientists;
- machine-learning researchers;
- software engineers;
- open-source contributors;
- government technical teams;
- academic institutions;
- humanitarian organisations;
- infrastructure-risk teams;
- AI-agent developers.

---

# Funders and Resourcing Partners

Primary Users, above, describes who operates CRIC. This section describes who resources it — a distinct relationship, and folding one into the other would misstate both.

CRIC does not name any specific funder, partner or beneficiary institution in this document, or in any public-facing material derived from it, whether committed, prospective or aspirational, without that party's explicit consent.

## Funder and Grantor Classes

CRIC's own architecture and values, not marketing framing, are what make it creditable to at least four distinct classes:

- public research and government science funders, who evaluate methodology, reproducibility and named institutional partnership rather than narrative alone;
- philanthropic and mission-driven funders working in climate, disaster risk or open science, who evaluate a credible, evidenced pathway from source observation to populations exposed to downstream hazard;
- open-source and digital-infrastructure sustainability funders, who evaluate shipped, maintained, openly governed software as the deliverable, not a roadmap;
- multilateral and development-finance climate bodies, who evaluate whether a piece of infrastructure strengthens institutional decision-making without displacing institutional authority.

Individual and community giving is deliberately out of scope for this section. CRIC intends a dedicated funding surface for that relationship later; until it exists, this document does not treat individual giving as a funder class to design for.

## What Each Class Can Already Verify Against This PRD

- Reproducibility and provenance discipline (Product Values: Evidence Before Interpretation, Provenance Before Convenience) is the primary claim for research and government funders.
- Disaster-risk practitioners named as Primary Users, above, and downstream exposure named as a GLOF Product Objective, is the primary claim for philanthropic and mission-driven funders.
- Open by Default, Replaceability and Modularity (Product Values), plus the open governance model in `community/Open-Source-Governance.md`, is the primary claim for open-source sustainability funders.
- The Non-Goals of this document — CRIC does not replace government warning systems — and Constitutional Product Rule 11 (`CRIC-PRD-MASTER.md`: "CRIC never silently assumes institutional warning authority") is the primary claim for multilateral and development-finance bodies, who cannot resource anything that competes with the institutions they answer to.

## What CRIC Owes Every Funding Relationship

- No funding relationship may create a closed fork, exclusive licence, or private branch of otherwise-open material. AGPL-3.0 already makes this structural; this states it as a standing commitment, not only a licence default.
- No funded output may be represented as an institutional warning, consistent with Constitutional Product Rule 11.
- No funding relationship is represented as committed, prospective or under discussion in any public material until the funder named has agreed to that disclosure.

---

# Product Values

## Evidence Before Interpretation

Interpretation must remain traceable to evidence.

## Provenance Before Convenience

A convenient output without inspectable lineage is inferior to a slower but reproducible result.

## Open by Default

Schemas, interfaces, ontology and reproducible methods should be open unless there is a defensible reason otherwise.

## Uncertainty is Data

Unknown, disputed and incomplete states must be represented explicitly.

## Contradiction is Valuable

Conflicting scientific claims are part of the knowledge graph and must not be silently reconciled.

## Temporal Context is Mandatory

A fact without temporal context may be scientifically misleading.

## Human and Machine Readability

The canonical knowledge representation must remain usable without specialised proprietary software.

## Modularity

CRIC components should be reusable independently.

## Replaceability

No single model provider, database engine, orchestration framework or cloud vendor should be structurally required.

## Scientific Modesty

The system must distinguish experimental models from validated operational capability.

---

# Product Scope

CRIC Core is climate-hazard agnostic.

It must eventually support:

- cryosphere;
- flood;
- drought;
- landslide;
- wildfire;
- heat;
- coastal hazard;
- storm surge;
- cyclone;
- extreme rainfall;
- erosion;
- groundwater;
- ecosystem degradation;
- cascading hazards;
- compound hazards;
- multi-hazard interactions.

Domain packages extend the core ontology.

---

# First Domain: Cryosphere

The first implementation shall cover:

- glaciers;
- snow and ice;
- glacial lakes;
- glacier-lake interaction;
- moraine systems;
- ice dams;
- slope instability;
- avalanche;
- rockfall;
- permafrost;
- glacier retreat;
- GLOF events;
- flood propagation;
- downstream exposure.

---

# GLOF Product Objectives

The first GLOF implementation should support:

- historical event registry;
- lake identity;
- glacier identity;
- lake state snapshots;
- remote-sensing observations;
- hydrometeorological context;
- terrain context;
- upstream triggers;
- downstream exposure;
- failure mode;
- event reconstruction;
- candidate risk indicators;
- training datasets;
- positive, negative and unknown cases;
- evidence chains;
- retrospective model experiments.

---

# Non-Goals

CRIC Core is not required to:

- make emergency declarations;
- replace government warning systems;
- guarantee model predictions;
- provide autonomous evacuation instructions;
- ingest every possible dataset into Git;
- impose one graph database;
- impose one LLM provider;
- impose one agent orchestration system;
- eliminate scientific disagreement.

---

# Success Criteria

CRIC succeeds when:

- a knowledge repository can be cloned and opened in Obsidian;
- all important nodes validate against published schemas;
- a deterministic parser can reconstruct the graph;
- an agent can traverse relevant nodes without ad hoc file parsing assumptions;
- every derived output exposes provenance;
- historic knowledge states remain reconstructable;
- contradictory claims are preserved;
- reusable agents can be composed with different tools and datasets;
- model runs are reproducible;
- human review can resume paused workflows through repository artefacts;
- ontology changes can be proposed, reviewed and merged through standard pull requests.

---

# Design Invariants

The following must remain true across all CRIC releases.

- No significant evidence is destroyed by correction.
- No missing value is silently interpreted as low risk.
- No inferred claim is silently promoted to observed fact.
- No model output is confused with scientific consensus.
- No copyrighted source is redistributed without permission.
- No agent depends on globally mutable runtime state.
- No stable ontology change occurs without versioning.
- No safety-critical decision is delegated merely because an agent can technically execute it.
