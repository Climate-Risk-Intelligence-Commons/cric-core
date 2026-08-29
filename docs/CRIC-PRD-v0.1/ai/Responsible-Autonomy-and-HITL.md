# CRIC Responsible Autonomy and Human-in-the-Loop Specification

## Purpose

CRIC is designed to maximise useful machine autonomy without treating all tasks as equally risky.

Human review is a durable repository workflow, not a manual checkpoint inserted into every agent action.

---

# Core Principle

Maximise machine autonomy in reversible, inspectable and non-safety-critical operations.

Increase human oversight as:

- uncertainty rises;
- scientific authority rises;
- consequence rises;
- irreversibility rises;
- public-safety significance rises.

---

# Autonomy Levels

## Level 0: Unrestricted Deterministic Computation

Examples:

- parsing;
- hashing;
- schema validation;
- geometry validation;
- unit conversion;
- deterministic feature extraction;
- index generation.

No routine HITL.

## Level 1: Autonomous Analytical Generation

Examples:

- source relevance ranking;
- candidate relationships;
- similarity;
- clustering;
- ontology-gap detection;
- contradiction candidates.

Outputs remain analytical/candidate.

## Level 2: Autonomous Provisional Knowledge

Agents may create:

- candidate nodes;
- candidate claims;
- candidate event reconstructions;
- provisional labels;
- ontology proposals.

They may not automatically represent these as reviewed scientific consensus.

## Level 3: Trusted Scientific Graph Promotion

Promotion may occur through:

- deterministic authoritative-source rules;
- defined corroboration rules;
- human review;
- maintainer-approved workflows.

Not every node requires manual review.

## Level 4: Safety-Significant Interpretation

Human review required for outputs intended to influence:

- operational warning;
- evacuation;
- critical infrastructure action;
- official risk certification;
- safety-critical public communication.

## Level 5: Authoritative Action

External competent institutions retain authority.

CRIC does not autonomously assume government warning powers.

---

# Review as Repository State

Reference `cric-review` structure:

```text
inbox/
assigned/
in-review/
approved/
rejected/
needs-more-evidence/
disputed/
escalated/
archived/
```

The filesystem/Git state is part of the workflow protocol.

---

# Review Bundle

Each request is self-contained.

```text
review-<id>/
├── request.yaml
├── README.md
├── evidence/
│   └── references.yaml
├── proposed/
│   └── changes.yaml
├── agent/
│   └── analysis.yaml
└── decision.yaml
```

Large evidence remains referenced rather than copied unnecessarily.

---

# ReviewRequest

Required fields:

```yaml
review_id:
type: ReviewRequest
status:
created_at:
created_by:
workflow_run_id:
subject_ids: []
review_type:
risk_level:
required_expertise: []
question:
options: []
evidence_nodes: []
proposed_action:
blocking: true
```

---

# ReviewDecision

```yaml
review_id:
decision:
  - approve
  - reject
  - modify
  - needs_more_evidence
  - disputed
  - escalate
reviewer:
reviewer_role:
decided_at:
rationale:
conditions: []
modified_values:
signature_method:
```

---

# Volunteer Review

Open-source volunteers may participate according to role and expertise.

Potential reviewer classes:

- general contributor;
- data reviewer;
- geospatial reviewer;
- cryosphere reviewer;
- hydrology reviewer;
- ontology reviewer;
- ML reviewer;
- maintainer.

Repository permissions should enforce what each class may approve.

---

# Review Assignment

The Human Review Router Agent may classify a request by:

- domain;
- expertise;
- urgency;
- safety consequence;
- ambiguity;
- required number of reviewers.

---

# Multi-Reviewer Decisions

High-impact decisions may require:

- two independent reviews;
- domain expert plus maintainer;
- consensus;
- majority;
- escalation.

The required policy should be encoded in the ReviewRequest.

---

# Agent Pause

When blocked:

1. agent persists run state;
2. agent creates review bundle;
3. workflow status becomes `waiting_for_review`;
4. execution exits cleanly.

No long-running process must remain alive.

---

# Agent Resume

A later invocation:

1. scans review status;
2. validates decision;
3. verifies reviewer authority;
4. loads persisted run state;
5. applies decision;
6. continues workflow;
7. records review in provenance.

---

# Local Deployment

A local CRIC user may interact with review folders directly through:

- Obsidian;
- text editor;
- Git client;
- CLI;
- CRIC UI.

The review protocol must not require a hosted service.

---

# GitHub Workflow

For shared repositories:

```text
Agent creates review bundle
↓
commit / branch / PR
↓
volunteer reviews
↓
decision committed
↓
agent sees decision
↓
workflow resumes
```

---

# Ontology Review

Ontology changes should use the same review mechanism.

Stable changes to `cric-core` ultimately enter through pull requests approved by maintainers.

---

# Safety-Significant Review

A safety-relevant review bundle should additionally expose:

- intended audience;
- intended action;
- model limitations;
- missing evidence;
- uncertainty;
- alternative interpretations;
- applicable authority.

---

# Review Provenance

Every decision must be linked to downstream outputs affected by it.

Example:

```text
ReviewDecision
→ accepted Claim
→ StateSnapshot
→ Training Label
→ DatasetVersion
```

---

# Conflict of Interest

Future governance should permit declaration of:

- contributor affiliation;
- source ownership;
- competing interest.

This is particularly important for formal scientific review.

---

# Privacy

Public review artefacts should avoid unnecessary personal information.

Reviewer identity may be represented by stable contributor ID where appropriate.

---

# Reversibility

A human approval is not immutable scientific truth.

Later evidence may:

- dispute;
- supersede;
- withdraw;
- trigger re-review.

The original decision remains historically visible.

---

# Review Queue Health

Agents may monitor:

- stale requests;
- blocked workflows;
- expertise shortages;
- repeated ontology gaps;
- disputed decisions.

They may suggest prioritisation but should not fabricate approval.

---

# HITL Failure Modes

CRIC must defend against:

- rubber-stamp approval;
- reviewer impersonation;
- unqualified approval;
- stale evidence;
- approval of a different node version;
- post-approval mutation;
- ambiguous decision records.

---

# Cryptographic and Git Integrity

Where useful, review decisions may leverage:

- Git commit identity;
- signed commits;
- release signatures;
- hashes of reviewed artefacts.

This proves review-object integrity, not scientific correctness.

---

# Acceptance Criteria

- review bundles are machine-readable;
- agents can pause without remaining alive;
- agents can resume from durable state;
- reviewer authority can be checked;
- multiple review policies are supported;
- local/offline review works;
- review decisions enter provenance;
- ontology PR review uses the same architecture;
- Level 4 outputs cannot bypass required human review.
