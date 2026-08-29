# CRIC Temporal and Epistemic Ontology

## Purpose

Climate-risk knowledge changes through time, and the time at which something occurred is not necessarily the time at which it was observed, became valid, or entered the CRIC knowledge base.

This document defines CRIC's temporal and epistemic model.

---

# Temporal Model

CRIC uses four distinct temporal dimensions.

## Event Time

When the real-world phenomenon occurred.

Examples:

- time of GLOF initiation;
- duration of rainfall event;
- date of avalanche.

## Observation Time

When an observation was acquired or made.

Examples:

- satellite acquisition time;
- sensor timestamp;
- field survey date.

## Valid Time

The period for which a state, claim or interpretation applies.

Examples:

- a lake polygon valid for an acquisition date;
- a road alignment valid between two dates;
- a scientific interpretation considered applicable to an event interval.

## System Time

When CRIC knew or stored the information.

Includes:

- `created_at`;
- `updated_at`;
- `superseded_at`;
- review time;
- ingestion time.

---

# Why Four Times Matter

Suppose a GLOF occurred in 1994.

A paper published in 2002 may reconstruct the event.

CRIC may ingest that paper in 2026.

A later paper in 2028 may revise the trigger interpretation.

These are different temporal facts:

```text
event_time = 1994
observation/report time = 2002
CRIC system_time = 2026
later superseding knowledge = 2028
```

CRIC must preserve all four.

---

# Temporal Structure

Reference schema:

```yaml
temporal:
  event_time:
    start:
    end:
    precision:
    uncertainty:
  observation_time:
    start:
    end:
    acquisition_time:
    precision:
  valid_time:
    from:
    to:
    open_ended: false
  system_time:
    created_at:
    updated_at:
    superseded_at:
```

---

# Partial and Uncertain Dates

CRIC must support:

- exact timestamp;
- date only;
- month only;
- year only;
- bounded interval;
- before;
- after;
- approximately;
- inferred interval;
- unknown.

Do not invent a precise timestamp to satisfy a schema.

---

# Temporal Precision Vocabulary

Recommended values:

- second;
- minute;
- hour;
- day;
- month;
- year;
- interval;
- approximate;
- estimated;
- inferred;
- unknown.

---

# Temporal Uncertainty

Uncertainty may be represented by:

- confidence;
- lower/upper bounds;
- earliest/latest possible time;
- textual notes;
- method used to infer time.

---

# Temporal Conflict

Conflicting dates must be preserved.

Example:

```text
Source A: event occurred 3 August
Source B: event occurred 4 August
```

CRIC should create separate claim or event-time assertion nodes where the disagreement is scientifically relevant.

A reconciliation assessment may later state a preferred date while retaining both sources.

---

# Bitemporal Query Requirement

At minimum CRIC must support questions equivalent to:

> What was considered valid on date X?

and:

> What did CRIC know on date Y?

This is the basis of historical knowledge reconstruction.

---

# Temporal Snapshot Rules

A `StateSnapshot` is immutable once accepted.

If additional evidence changes the reconstructed state:

- create a new snapshot;
- link it with `supersedes`;
- preserve the earlier snapshot.

---

# Epistemic Model

Temporal truth and epistemic status are separate.

Recommended epistemic states:

## `observed`

Directly measured or sensed.

## `reported`

Reported by a source without CRIC independently observing it.

## `derived`

Calculated deterministically from one or more inputs.

## `inferred`

Reasoned from evidence where the conclusion is not directly measured.

## `simulated`

Produced by a simulation or synthetic process.

## `hypothesised`

Proposed explanation requiring further evidence.

## `disputed`

Explicitly contested.

## `unknown`

Insufficient information.

---

# Evidence Status Versus Workflow Status

Example:

```yaml
epistemic:
  status: inferred

knowledge_state:
  status: accepted
```

This means CRIC accepts that the node is a valid representation of an inference. It does not convert the inference into an observation.

---

# Confidence

Confidence should not be treated as a universal probability.

Every confidence value should identify its meaning or method.

Example:

```yaml
confidence:
  value: 0.82
  scale: 0_to_1
  method: expert_assessment
```

Other methods may include:

- model probability;
- inter-rater agreement;
- source reliability rubric;
- measurement uncertainty;
- deterministic certainty.

---

# Unknown Versus Negative

CRIC must distinguish:

- false;
- absent;
- not detected;
- no known evidence;
- unknown;
- unobserved;
- not applicable.

This distinction is mandatory for training-data construction.

---

# Knowledge State

Recommended lifecycle:

```text
candidate
accepted
disputed
superseded
rejected
withdrawn
archived
```

## Candidate

Created but not promoted to accepted knowledge.

## Accepted

Structurally and procedurally accepted according to applicable rules.

## Disputed

Accepted as a representation of unresolved disagreement.

## Superseded

Replaced by a newer representation but preserved.

## Rejected

Reviewed and not accepted.

## Withdrawn

Removed from active use by its proposer or maintainer while retained historically.

---

# Three-Way Reconciliation of Changing Knowledge

CRIC should analyse conflicting or updated information using three simultaneous perspectives:

## World-Time Perspective

What appears to have happened in the real world and when?

## Evidence-Time Perspective

What observations or publications existed, and when were they produced?

## Knowledge-System Perspective

When did CRIC ingest, accept, dispute or supersede each representation?

This prevents retrospective knowledge from being incorrectly projected backwards.

---

# Agent Requirements

Temporal reconciliation agents must never:

- overwrite an earlier assertion merely because a later source exists;
- invent precision;
- collapse `unknown` into `false`;
- convert inference into observation.

They may:

- create candidate reconciliations;
- identify temporal conflicts;
- propose supersession;
- request human review.

---

# v0.1 Acceptance Criteria

- all canonical nodes support system time;
- time-bearing scientific nodes support relevant event/observation/valid times;
- partial dates validate;
- temporal conflicts can coexist;
- historical knowledge-state queries are possible;
- snapshots are immutable;
- epistemic and workflow statuses are separate;
- unknown and negative are structurally distinct.
