# CRIC Contribution and Review Process

## Purpose

This document defines how contributors submit software, knowledge, data, ontology, model and agent changes across CRIC repositories.

---

# Contribution Types

- software;
- documentation;
- OKF knowledge node;
- source/evidence addition;
- dataset manifest;
- training label;
- ontology proposal;
- model;
- agent;
- evaluation;
- review decision.

---

# General Contribution Flow

```text
Issue/Proposal
↓
Branch
↓
Contribution
↓
Automated validation
↓
Review
↓
Revision
↓
Merge
↓
Release
```

Not every small change requires an issue first.

---

# Pull Request Requirements

A PR should state:

- purpose;
- affected components;
- evidence where scientific;
- schema/ontology impact;
- licence impact;
- testing;
- migration impact;
- safety impact.

---

# Knowledge Contributions

New OKF knowledge must pass:

- schema validation;
- ontology validation;
- provenance validation;
- licence validation;
- graph-link validation.

Candidate scientific interpretation may additionally require domain review.

---

# Data Contributions

Must include:

- source;
- licence;
- acquisition method;
- version;
- hash/manifests;
- quality information.

Large data should normally not be committed directly to Git.

---

# Ontology Contributions

Must use OntologyProposal.

Stable changes require designated ontology review.

---

# Agent Contributions

Must include:

- agent manifest;
- Pydantic dependencies;
- output schema;
- toolsets;
- permission profile;
- evaluation suite;
- documentation.

---

# Model Contributions

Must include:

- model card;
- training provenance;
- evaluation;
- licence;
- artifact hash;
- limitations.

---

# Training Labels

Ground-truth-like labels require evidence.

Disputed labels must remain representable rather than forced into binary consensus.

---

# Review Dimensions

Reviewers should separate:

- code correctness;
- schema correctness;
- scientific validity;
- licensing;
- security;
- safety;
- documentation.

One reviewer need not be expert in all dimensions.

---

# CODEOWNERS

Critical paths should require specialist reviewers.

Examples:

```text
ontology/      ontology maintainers
security/      security maintainers
glof/          cryosphere/GLOF reviewers
agents/        agent maintainers
```

---

# Automated Checks

PR automation should include applicable:

- lint;
- type checks;
- tests;
- schema validation;
- ontology validation;
- OKF validation;
- provenance;
- licence;
- security;
- agent evaluation.

---

# Review Comments

Scientific disagreement should be expressed with evidence and rationale.

Where disagreement itself is scientifically meaningful, the correct result may be multiple graph claims rather than forcing one textual answer.

---

# Merge Rules

Stable core changes require maintainer approval.

Agents may prepare branches and pull requests but should not autonomously merge stable core changes.

---

# Contributor Documentation

CRIC should provide templates for:

- bug;
- feature;
- data source;
- ontology proposal;
- scientific claim;
- model;
- agent;
- review request.

---

# Attribution

Contributors should receive normal Git/open-source attribution.

Scientific dataset/publication attribution may additionally follow domain norms.

---

# v0.1 Acceptance Criteria

- CONTRIBUTING document exists;
- PR templates exist;
- CODEOWNERS exists;
- knowledge/data/ontology/agent contribution paths are documented;
- automated checks block invalid merges;
- scientific disagreements can be represented without destructive resolution.
