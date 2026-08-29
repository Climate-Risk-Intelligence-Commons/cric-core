# CRIC GLOF Ontology Specification

## Purpose

This document defines the Glacial Lake Outburst Flood domain ontology used by the first operationally relevant CRIC hazard vertical.

The ontology is intended for historical event reconstruction, scientific evidence integration, machine-learning dataset construction, susceptibility analysis, trigger analysis, consequence modelling and decision-support research.

It does not imply that CRIC outputs are validated operational warnings.

---

# Conceptual Decomposition

GLOF intelligence should not be represented as one monolithic prediction problem.

CRIC separates:

1. lake evolution;
2. susceptibility;
3. trigger conditions;
4. failure state/mechanism;
5. flood propagation;
6. exposure;
7. vulnerability;
8. consequence;
9. decision-support interpretation.

---

# Type Hierarchy

```text
GLOFEvent
├── MoraineDamFailureGLOF
├── IceDamFailureGLOF
├── OvertoppingGLOF
├── DisplacementWaveGLOF
├── CascadingLakeFailureGLOF
├── CompoundMechanismGLOF
└── UnknownMechanismGLOF

GLOFTrigger
├── ExtremePrecipitationTrigger
├── SnowmeltTrigger
├── IceAvalancheTrigger
├── SnowAvalancheTrigger
├── RockAvalancheTrigger
├── LandslideTrigger
├── GlacierCalvingTrigger
├── SeismicTrigger
├── PipingTrigger
├── DamDegradationTrigger
├── UpstreamLakeFailureTrigger
└── UnknownTrigger

GLOFFailureProcess
├── Overtopping
├── BreachErosion
├── Piping
├── InternalErosion
├── StructuralCollapse
├── IceDamDrainage
└── UnknownFailureProcess
```

Multiple triggers and processes may apply to one event.

---

# `GLOFEvent`

Required or recommended fields:

## Identity

- event ID;
- event name;
- aliases;
- source event IDs;
- lake ID;
- glacier ID where relevant;
- basin;
- country;
- administrative region.

## Temporal

- event start;
- event end;
- temporal precision;
- earliest/latest possible time;
- CRIC knowledge time.

## Mechanism

- failure mode claims;
- trigger claims;
- trigger confidence;
- breach mechanism;
- compound/cascading status.

## Hydraulic properties

Where available:

- released volume;
- peak discharge;
- breach dimensions;
- flood depth;
- velocity;
- travel time;
- runout distance.

Each value must be independently sourced or derived.

## Consequences

- fatalities;
- injuries;
- missing persons;
- displaced population;
- settlement impacts;
- road impacts;
- bridge impacts;
- hydropower impacts;
- communication impacts;
- agricultural impacts;
- geomorphic impacts.

Reported consequence values may conflict and must be represented as claims/observations rather than overwritten.

---

# Trigger Representation

A trigger is not automatically a proven cause.

CRIC should distinguish:

- observed precursor;
- candidate trigger;
- inferred trigger;
- reported trigger;
- preferred interpretation;
- disputed trigger;
- unknown trigger.

---

# Multi-Trigger Events

A GLOF may involve:

```text
heavy precipitation
+
high lake level
+
ice avalanche
→ displacement wave
→ overtopping
→ breach
```

CRIC must represent this as a graph rather than force one categorical trigger.

---

# Failure Mechanisms

Minimum vocabulary:

- moraine_breach;
- overtopping;
- ice_dam_failure;
- landslide_displacement_wave;
- avalanche_displacement_wave;
- glacier_calving;
- piping;
- internal_erosion;
- seismic_destabilisation;
- cascading_lake_failure;
- compound;
- unknown.

---

# Event Reconstruction

Historical events should link to temporal snapshots.

Recommended windows:

- T-10 years;
- T-5 years;
- T-2 years;
- T-1 year;
- T-6 months;
- T-1 month;
- T-7 days;
- T-24 hours;
- event;
- post-event.

These are target windows, not mandatory data availability.

---

# Pre-Event Variables

Potential features:

## Lake

- area;
- volume;
- estimated depth;
- growth rate;
- shoreline migration;
- outlet state;
- freeboard;
- glacier contact.

## Glacier

- retreat;
- terminus position;
- velocity;
- calving front;
- thinning.

## Terrain and Dam

- dam geometry;
- slope;
- erosion;
- deformation;
- avalanche paths;
- landslide source areas.

## Meteorology

- precipitation;
- accumulated precipitation;
- temperature;
- temperature anomaly;
- snowmelt indicators.

## Seismic and Mass Movement

- earthquake events;
- landslide observations;
- SAR coherence change;
- deformation indicators.

---

# Post-Event Variables

- lake area reduction;
- lake level change;
- breach geometry;
- flood footprint;
- sediment deposition;
- channel change;
- infrastructure damage;
- downstream geomorphic change.

---

# GLOF Susceptibility Assessment

Susceptibility must be distinct from trigger likelihood.

Potential indicators:

- lake growth;
- dam type;
- glacier contact;
- dam geometry;
- surrounding slope;
- avalanche exposure;
- landslide exposure;
- lake volume;
- historical instability.

---

# Trigger-State Assessment

Potential short-term indicators:

- recent precipitation;
- snowmelt;
- temperature anomaly;
- seismic event;
- detected mass movement;
- rapid lake-level change;
- deformation.

---

# Lake Stability State

CRIC should favour interpretable states over unsupported exact-date failure claims.

Possible research states:

- normal;
- elevated;
- high;
- critical;
- indeterminate.

Every state must expose:

- reasons;
- evidence;
- uncertainty;
- completeness;
- model/rule version;
- operational disclaimer.

---

# Cascading GLOF

CRIC must represent sequences such as:

```text
upstream lake failure
→ downstream lake loading
→ second lake breach
→ combined flood
```

Each event remains separately addressable.

---

# Compound GLOF

A compound event may involve interacting precipitation, snowmelt, slope failure and lake instability.

Compound mechanisms must not be collapsed into a single trigger merely for classifier convenience.

---

# Downstream Exposure

Link GLOF scenarios to:

- population;
- settlements;
- roads;
- bridges;
- hydropower;
- dams;
- communications;
- health facilities;
- schools;
- emergency facilities;
- agriculture.

Exposure is not consequence. Consequence depends additionally on hazard intensity and vulnerability.

---

# Evidence and Claims

Every event should support multiple competing claims regarding:

- date;
- trigger;
- breach process;
- released volume;
- peak discharge;
- casualties;
- infrastructure damage.

---

# Training Labels

Event labels should distinguish:

- confirmed_glof;
- probable_glof;
- disputed_glof;
- non_glof;
- unknown.

Failure-mode labels and trigger labels should be separate.

---

# Model Task Separation

Potential model families:

- lake segmentation;
- glacier segmentation;
- lake-change model;
- susceptibility model;
- trigger-state model;
- failure-mode model;
- multimodal fusion model;
- consequence model.

---

# v0.1 Acceptance Criteria

- historical GLOF event can be represented;
- multiple triggers can coexist;
- conflicting trigger claims can coexist;
- failure process is distinct from trigger;
- pre/post snapshots can be linked;
- consequences can contain conflicting reports;
- cascading events can be represented;
- training labels preserve uncertainty;
- risk state exposes evidence completeness separately.
