# CRIC Volunteer Human-in-the-Loop Workflow

## Purpose

This document specifies the practical workflow by which qualified volunteers and maintainers can review agent-generated or pipeline-generated work through the open-source repository.

The workflow must also work locally without a hosted platform.

---

# Review Objectives

Volunteer review should be used where human judgement materially improves:

- scientific interpretation;
- entity resolution;
- ambiguous evidence;
- ontology changes;
- training labels;
- benchmark freezes;
- safety-significant outputs.

Routine deterministic processing should remain automated.

---

# Review Repository

Reference:

```text
cric-review/
├── inbox/
├── assigned/
├── in-review/
├── approved/
├── rejected/
├── needs-more-evidence/
├── disputed/
├── escalated/
└── archived/
```

---

# Review Bundle

```text
HITL-00000421/
├── request.md
├── request.yaml
├── evidence/
│   └── references.yaml
├── candidate-changes/
│   └── changes.yaml
├── agent-analysis.md
├── instructions.md
└── decision.yaml
```

---

# Reviewer Registry

A machine-readable registry may contain:

```yaml
reviewer_id:
public_name:
expertise: []
review_permissions: []
affiliations: []
conflicts_declared: []
status:
review_history:
```

Avoid unnecessary personal data.

---

# Expertise Tags

Possible tags:

- cryosphere;
- glaciology;
- hydrology;
- remote_sensing;
- GIS;
- geotechnical;
- meteorology;
- seismicity;
- ML;
- ontology;
- data_quality;
- software_security.

---

# Assignment

The Review Router may recommend reviewers based on:

- expertise;
- availability;
- conflict;
- risk level;
- review history.

A human maintainer may override assignment.

---

# Review Instructions

Every bundle must clearly state:

- what is being reviewed;
- why;
- exact decision requested;
- evidence;
- uncertainties;
- alternatives;
- consequences of approval;
- required expertise.

---

# Review Outcomes

- approved;
- rejected;
- modified;
- needs_more_evidence;
- disputed;
- escalated.

---

# Signature

Initial implementations may use:

- Git identity;
- commit hash;
- reviewer ID.

Higher-assurance deployments may require signed commits or institutional identity.

---

# Double Review

Examples requiring multiple reviewers may include:

- benchmark ground-truth labels;
- new GLOF failure mechanism;
- safety-significant classification;
- stable core ontology change.

---

# Volunteer Reputation

CRIC may maintain transparent review history.

Reputation should not become an opaque automated truth score.

Potential signals:

- completed reviews;
- agreement/disagreement history;
- expertise;
- maintainer feedback;
- reversals.

---

# Review Quality

Maintainers may audit review decisions.

A reviewer can be suspended from particular approval classes without deleting their historical contributions.

---

# Local Workflow

A researcher running CRIC locally can use the same structure.

They may act as authorised local reviewer according to their deployment policy.

---

# GitHub Workflow

Typical:

1. agent creates bundle;
2. bundle committed to branch;
3. pull request opened;
4. reviewer comments or commits decision;
5. automated validation checks decision;
6. workflow resumes;
7. review is archived with provenance.

---

# Review of Visual Evidence

Where satellite imagery or maps are needed, the bundle should reference immutable asset IDs and provide reproducible viewing instructions.

---

# Review of Scientific Claims

Reviewer should assess:

- source support;
- alternative explanations;
- temporal scope;
- spatial scope;
- uncertainty;
- contradiction status.

---

# Review of Training Labels

Reviewer should assess:

- event identity;
- observation interval;
- evidence sufficiency;
- negative semantics;
- leakage.

---

# Review of Ontology

Reviewer should assess:

- scientific need;
- definition;
- duplicate concepts;
- inheritance;
- cross-domain implications;
- migration impact.

---

# Volunteer Safety

Volunteer reviewers must not be presented as official emergency authorities merely because they participate in CRIC.

---

# v0.1 Acceptance Criteria

- reviewer registry schema exists;
- expertise-based routing works;
- review bundle template exists;
- Git-based decision works;
- local decision works;
- double-review policy can be encoded;
- decisions are provenance-linked.
