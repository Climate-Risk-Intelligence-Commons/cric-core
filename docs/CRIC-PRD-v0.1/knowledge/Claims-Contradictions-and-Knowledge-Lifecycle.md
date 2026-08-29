# CRIC Claims, Contradictions and Knowledge Lifecycle

## Purpose

Scientific knowledge is not a flat set of facts.

CRIC must preserve competing claims, revisions, uncertainty, retractions and evolving interpretations without erasing historical states.

---

# Claim Model

A claim is an independently addressable assertion.

Reference:

```yaml
id:
type: Claim

subject:
predicate:
object:
value:
unit:

claim_text:

claimant:
source_nodes: []
evidence_nodes: []

temporal_scope:
spatial_scope:

epistemic:
  status:
  confidence:

knowledge_state:
  status:
```

---

# When to Create a Claim Node

Create a separate claim when:

- the assertion may be disputed;
- multiple sources make different assertions;
- the assertion is scientifically important;
- temporal applicability matters;
- evidence may change;
- the assertion influences risk assessment;
- an agent or human may need to accept/reject/refine it.

---

# Claim Relationships

Core predicates:

- supports;
- contradicts;
- disputes;
- corroborates;
- refines;
- supersedes;
- consistent_with;
- inconsistent_with;
- derived_from.

---

# Contradiction

Contradiction is a first-class graph condition.

CRIC must not automatically choose a winner merely to simplify retrieval.

Example:

```text
Claim A:
"The event was triggered by intense rainfall."

Claim B:
"The event was initiated by an ice avalanche."
```

Both may remain active.

A third assessment can analyse whether:

- one is better supported;
- both contributed;
- the evidence is insufficient;
- terminology differs.

---

# Contradiction Record

A contradiction may itself be represented as an assessment when valuable.

Fields:

- claims compared;
- contradiction type;
- degree;
- evidence;
- possible reconciliation;
- reviewer;
- status.

---

# Contradiction Types

Suggested vocabulary:

- direct;
- partial;
- temporal;
- spatial;
- definitional;
- methodological;
- measurement;
- causal;
- classification;
- apparent;
- unresolved.

---

# Reconciliation

Reconciliation does not mean deletion.

Possible outcomes:

- claim A preferred;
- claim B preferred;
- both valid in different contexts;
- both partially valid;
- terminology mismatch;
- insufficient evidence;
- unresolved.

---

# Knowledge Lifecycle

```text
candidate
→ accepted
→ disputed
→ superseded
→ archived
```

Alternative branches:

```text
candidate → rejected
accepted → withdrawn
```

---

# Candidate Knowledge

Agents may generate candidate nodes freely within permission boundaries.

Candidate nodes must be visibly distinguishable from accepted knowledge.

---

# Promotion to Accepted

Acceptance requirements depend on node class and risk.

Possible promotion mechanisms:

- deterministic validation;
- authoritative source;
- multi-source corroboration;
- qualified human review;
- maintainer approval.

The promotion mechanism must be recorded.

---

# Disputed State

A disputed node remains searchable and traversable.

It should identify:

- disputing claims;
- disputing source;
- dispute reason;
- review status.

---

# Supersession

Supersession is used when a newer representation replaces an older representation for active use.

The old node remains addressable.

---

# Rejection

Rejected candidate knowledge remains available in review/history areas where useful for auditability.

It must not appear as accepted knowledge.

---

# Retractions and Withdrawals

If a source paper is retracted or a contributor withdraws a claim:

- preserve the original source node;
- update source status;
- create relevant relationships;
- flag dependent claims for re-evaluation;
- do not silently erase historical use.

---

# Dependency Impact

When a claim is superseded, disputed or withdrawn, CRIC should identify downstream dependencies:

- assessments;
- training labels;
- features;
- model runs;
- reports;
- other claims.

An impact-analysis workflow should produce candidate review tasks.

---

# Scientific Minority Views

A minority interpretation supported by defensible evidence should not be removed merely because another interpretation is dominant.

CRIC should represent:

- evidence strength;
- source;
- confidence;
- review status.

---

# Agent Behaviour

Agents may:

- detect contradictions;
- propose reconciliation;
- identify dependent nodes;
- create candidate claims;
- route conflicts to review.

Agents must not:

- erase competing claims;
- silently convert uncertainty into consensus;
- promote a high-impact disputed claim without applicable review.

---

# Retrieval Requirements

Users and agents should be able to query:

- all claims about a subject;
- accepted claims;
- disputed claims;
- superseded claims;
- evidence supporting a claim;
- evidence contradicting a claim;
- claim history;
- downstream objects dependent on a claim.

---

# v0.1 Acceptance Criteria

- two contradictory claims can coexist;
- contradiction relationships validate;
- superseded nodes remain retrievable;
- downstream dependency search works;
- candidate and accepted knowledge are distinguishable;
- retracted-source status can propagate review flags;
- no automatic conflict resolution is required for graph validity.
