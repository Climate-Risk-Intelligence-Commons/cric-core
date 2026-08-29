# CRIC StateSnapshot and Event Cube Specification

## Purpose

This document defines how CRIC captures temporally coherent states of climate-risk entities and reconstructs the evolution surrounding significant events.

The first implementation is the GLOF Event Cube, but the design is intended to generalise to other climate hazards.

---

# `StateSnapshot`

A StateSnapshot is an immutable graph node representing the best available description of a subject and its relevant context for a specified time or interval.

A snapshot is not a copy of all source data.

It is a structured index into observations, features, claims and evidence.

---

# Snapshot Identity

Required fields:

```yaml
id:
type: StateSnapshot
subject_id:
snapshot_time:
snapshot_window:
snapshot_purpose:
schema_version:
ontology_version:
```

---

# Snapshot Temporal Semantics

A snapshot must identify whether it represents:

- exact acquisition time;
- nearest available observation;
- reconstructed state;
- aggregated interval;
- event-relative window.

---

# Snapshot Components

## Subject State

References direct observations about the primary subject.

## Upstream Context

May include:

- parent glacier;
- upstream lakes;
- avalanche paths;
- mass-movement source areas;
- precipitation catchment;
- seismic events.

## Downstream Context

May include:

- drainage network;
- settlements;
- population;
- bridges;
- roads;
- hydropower;
- dams;
- critical facilities.

## Environmental Context

- precipitation;
- temperature;
- snow;
- soil/frozen-ground state;
- river conditions.

## Derived Features

Features computed from observations.

## Evidence Completeness

Explicit record of what is available and missing.

## Conflicts

References unresolved contradictory nodes.

---

# Snapshot Immutability

Accepted snapshots must not be edited to reflect later knowledge.

If reconstruction improves:

```text
Snapshot v1
↓ superseded_by
Snapshot v2
```

Both remain retrievable.

---

# Event Cube Concept

An Event Cube is a structured collection of temporal snapshots, event records and post-event evidence surrounding a significant event.

For GLOF:

```text
Identity
+
Pre-event snapshots
+
Event
+
Post-event snapshots
+
Consequences
+
Evidence
+
Claims
+
Provenance
```

---

# Event Cube Identity Layer

Capture:

- lake;
- aliases;
- coordinates;
- basin;
- country;
- glacier;
- lake type;
- dam type;
- external identifiers.

---

# Recommended Temporal Windows

```text
T-10y
T-5y
T-2y
T-1y
T-6m
T-1m
T-7d
T-24h
T-event
T+24h
T+7d
T+1m
T+6m
```

These are target analysis windows.

The actual snapshot should record the distance between requested and available observation time.

---

# Nearest-Observation Semantics

If T-7d imagery is unavailable and T-10d is used:

```yaml
requested_relative_time: "-7d"
actual_relative_time: "-10d"
temporal_offset_days: -3
selection_method: nearest_usable_observation
```

This prevents false temporal precision.

---

# Lake State Block

Potential linked observations:

- area;
- perimeter;
- volume;
- depth;
- water level;
- growth rate;
- shoreline change;
- outlet position;
- glacier contact.

---

# Glacier State Block

- terminus;
- retreat;
- velocity;
- surface elevation;
- calving;
- snow/ice conditions.

---

# Dam and Terrain Block

- dam geometry;
- freeboard;
- slope;
- erosion;
- seepage;
- deformation;
- breach precursor;
- surrounding relief.

---

# Trigger Context Block

- precipitation;
- accumulated precipitation;
- temperature;
- temperature anomaly;
- snowmelt;
- earthquake;
- landslide;
- avalanche;
- SAR coherence/deformation.

---

# Downstream Context Block

- drainage path;
- settlements;
- population;
- roads;
- bridges;
- hydropower;
- critical infrastructure;
- exposure estimates.

---

# Event Block

- event time;
- trigger claims;
- failure process;
- released volume;
- peak discharge;
- breach geometry;
- propagation;
- runout.

---

# Post-Event Block

- residual lake;
- breach scar;
- inundation;
- sediment;
- channel change;
- damaged infrastructure;
- recovery observations.

---

# Event Cube Manifest

Each cube should have a manifest:

```yaml
event_cube_id:
event_id:
subject_id:
snapshot_ids: []
source_assets: []
derived_features: []
claims: []
conflicts: []
dataset_version:
created_at:
content_manifest_sha256:
```

---

# Training Use

An Event Cube can produce multiple TrainingSamples.

Example:

```text
T-1y → T-6m → T-1m → T-7d
               ↓
       target = GLOF within 7 days
```

Training sample generation must record:

- cube version;
- included snapshots;
- excluded data;
- label source;
- leakage controls;
- feature generation code.

---

# Negative Event Cubes

CRIC should also create cubes for non-event lakes.

Types:

- hard negative;
- routine negative;
- confirmed negative;
- no-known-event;
- unknown.

Negative cubes must define the observation interval over which absence is asserted.

---

# Leakage Prevention

For predictive experiments, post-event information must never leak into pre-event training features.

The TrainingSample manifest must define:

- prediction cutoff;
- allowed source times;
- prohibited future information.

---

# Generalisation Beyond GLOF

The Event Cube abstraction should later support:

- flood;
- wildfire;
- drought;
- landslide;
- heatwave;
- cyclone;
- coastal event.

The domain package defines which contextual blocks apply.

---

# v0.1 Acceptance Criteria

- StateSnapshot schema exists;
- event-relative time is represented;
- nearest-observation offsets are explicit;
- snapshots are immutable;
- one GLOF cube is constructible;
- one negative cube is constructible;
- training samples can reference cube snapshots;
- leakage controls are represented;
- missing data is explicit.
