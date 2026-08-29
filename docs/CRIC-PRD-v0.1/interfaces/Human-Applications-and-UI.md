# CRIC Human Applications and UI Specification

## Purpose

CRIC human interfaces must make scientific evidence, provenance, uncertainty, temporal change, contradictions and agent activity understandable without hiding the underlying machine-readable commons.

The UI is a lens over CRIC, not a separate source of truth.

---

# Primary User Groups

- climate scientists;
- cryosphere researchers;
- hydrologists;
- geospatial analysts;
- ML researchers;
- government technical officers;
- infrastructure risk teams;
- open-source contributors;
- volunteer reviewers;
- ontology maintainers;
- developers.

---

# Application Modules

Recommended modules:

1. Knowledge Explorer;
2. Climate Risk Map;
3. Entity Explorer;
4. Timeline Explorer;
5. Evidence Explorer;
6. Contradiction Explorer;
7. Provenance Explorer;
8. Dataset Explorer;
9. Model Explorer;
10. Agent Commons Console;
11. HITL Review Console;
12. Ontology Explorer.

---

# Knowledge Explorer

Displays:

- node title;
- type;
- status;
- summary;
- YAML-derived structured metadata;
- relationships;
- evidence;
- temporal information;
- provenance;
- linked Markdown.

Users should be able to switch between:

- human-readable view;
- raw OKF Markdown;
- graph neighbourhood.

---

# Climate Risk Map

MapLibre GL JS is the preferred open-source mapping layer for the web application.

Capabilities:

- lake/glacier layers;
- event locations;
- exposure;
- catchments;
- temporal filtering;
- dataset overlays;
- selectable StateSnapshots;
- provenance-aware layer metadata.

---

# Entity Explorer

For a GlacialLake, for example:

- identity;
- aliases;
- geometry;
- glacier relationship;
- lake type;
- observations;
- area history;
- StateSnapshots;
- GLOF events;
- claims;
- contradictions;
- evidence;
- downstream context.

---

# Timeline Explorer

A central CRIC interface.

It should display separate tracks for:

- real-world events;
- observations;
- publications;
- CRIC ingestion;
- claim changes;
- review decisions;
- model predictions.

This visually communicates CRIC's multi-temporal architecture.

---

# Evidence Explorer

Users should be able to start from a claim or output and answer:

> Where did this come from?

The UI should traverse:

```text
interpretation
→ claim
→ feature
→ observation
→ asset
→ source
```

---

# Contradiction Explorer

Displays competing claims side by side.

Should show:

- claim;
- source;
- evidence;
- temporal scope;
- confidence;
- review state;
- reconciliation assessments.

The UI must avoid visually treating one claim as settled unless its status supports that interpretation.

---

# Provenance Explorer

Graph visualisation of:

- parentage;
- transformations;
- software;
- agents;
- reviews;
- hashes.

---

# Dataset Explorer

Displays:

- dataset identity;
- version;
- spatial/temporal coverage;
- licence;
- quality;
- sample counts;
- asset manifests;
- derived datasets;
- downstream model usage.

---

# Model Explorer

Displays:

- model card;
- architecture;
- version;
- training dataset;
- benchmark results;
- limitations;
- calibration;
- model lineage;
- predictions.

---

# Agent Commons Console

Users should be able to inspect reusable agents as product artefacts.

For each agent:

- purpose;
- version;
- Pydantic dependency contract;
- tools;
- datasets;
- workspace policy;
- model provider;
- output schema;
- permission level;
- evaluations.

Users may create application-specific agent compositions by selecting compatible components.

---

# Agent Run View

Show:

- run ID;
- agent version;
- dependencies;
- tool calls;
- created candidate artefacts;
- provenance;
- status;
- HITL pauses;
- final structured output.

Sensitive secrets must never be displayed.

---

# HITL Review Console

The UI is a view over repository-native review artefacts.

Review screen:

- question;
- why review is needed;
- risk level;
- required expertise;
- evidence;
- proposed changes;
- agent analysis;
- alternative interpretations;
- decision controls;
- rationale.

---

# Ontology Explorer

Capabilities:

- hierarchy;
- definitions;
- predicates;
- versions;
- experimental concepts;
- candidate proposals;
- deprecated types;
- migration history.

---

# Scientific Confidence Display

Avoid deceptive precision.

Where confidence is qualitative, display it qualitatively.

Where numerical, display:

- value;
- method;
- meaning.

---

# Evidence Completeness

Evidence completeness must be visually distinct from risk state.

A user should not infer:

```text
low evidence = low risk
```

---

# Candidate Knowledge

Candidate/agent-generated knowledge must be visually distinguishable from accepted knowledge.

---

# Accessibility

UI should target:

- keyboard navigation;
- sufficient contrast;
- screen-reader semantics;
- non-colour-only status indicators;
- scalable typography.

---

# Mobile

The first scientific workbench is desktop-first, but review and inspection interfaces should remain responsive.

---

# Obsidian

The downloadable `cric-knowledge` repository itself is a supported human interface.

CRIC should provide:

- Obsidian-compatible links;
- generated indexes;
- graph-friendly naming;
- templates;
- optional CSS/snippets only where nonessential.

The knowledge base must remain useful without CRIC's web UI.

---

# Export

Users should be able to export appropriate views as:

- Markdown;
- JSON;
- GeoJSON;
- CSV;
- GeoParquet references;
- provenance bundle.

---

# v0.1 Acceptance Criteria

- lake/entity explorer works;
- map displays reference lakes/events;
- timeline distinguishes observation and knowledge time;
- evidence lineage is navigable;
- candidate knowledge is marked;
- review console can read/write valid review decisions;
- Obsidian remains independently usable.
