# CRIC Ontology Evolution and Governance

## Purpose

CRIC must continuously evolve as new climate-risk concepts, measurements, hazards and relationships are encountered.

Ontology evolution is therefore a normal product capability.

Stable ontology changes, however, must remain reviewable, versioned and reproducible.

---

# Governance Principle

Agents may discover and propose ontology changes.

Agents may not silently mutate the stable core ontology.

Stable changes enter through pull requests.

---

# Sources of Ontology Evolution

Ontology gaps may arise from:

- new scientific literature;
- new sensor types;
- new hazards;
- new failure mechanisms;
- new climate-risk domains;
- new model features;
- new data standards;
- ambiguous terminology;
- duplicated concepts;
- cross-domain interactions.

---

# Continuous Ontology Awareness

Knowledge-processing agents should be able to ask:

- Is this concept represented?
- Is this predicate available?
- Is an existing type too broad?
- Is an existing type too narrow?
- Are these terms synonyms?
- Are apparently identical terms scientifically different?
- Is this relationship direct, causal, contributory or merely associated?
- Does this new evidence expose a missing temporal or uncertainty construct?

---

# Ontology Gap Result

Reference typed output:

```yaml
gap_id:
encountered_term:
context_nodes: []
current_best_match:
gap_type:
  - missing_type
  - missing_predicate
  - ambiguous_definition
  - synonym_collision
  - overly_broad
  - overly_narrow
  - cross_domain_gap
proposed_action:
confidence:
evidence_nodes: []
```

---

# Ontology Proposal

Every proposed stable change becomes an `OntologyProposal` node.

Required fields:

- proposal ID;
- proposer;
- proposed identifier;
- proposed name;
- definition;
- parent;
- rationale;
- evidence;
- affected types;
- affected predicates;
- backwards-compatibility impact;
- migration impact;
- example nodes;
- test cases;
- status.

---

# Lifecycle

```text
experimental
→ candidate
→ review
→ stable
→ deprecated
→ removed
```

---

# Experimental Ontology

Domain repositories and local agent workspaces may use experimental terms.

Experimental terms must be clearly namespaced.

Example:

```text
CRIC-EXP:glof:possible-new-trigger
```

Experimental types must not masquerade as stable core types.

---

# Candidate Promotion

Promotion from experimental to candidate should require:

- demonstrated need;
- definition;
- examples;
- evidence;
- parent relationship;
- conflict check against existing ontology.

---

# Human Review

Human review is required for stable changes that:

- alter semantic meaning;
- affect multiple repositories;
- change safety-relevant concepts;
- create breaking schema changes;
- deprecate widely used types.

Low-risk additions may use lighter review rules.

---

# Pull Request Workflow

```text
Agent/Human encounters gap
↓
OntologyGapResult
↓
OntologyProposal
↓
Prototype schema
↓
Validation against example nodes
↓
Impact analysis
↓
Human review where required
↓
Pull request to cric-core
↓
Automated tests
↓
Maintainer review
↓
Merge
↓
Ontology version increment
↓
Migration artefacts
↓
Dependent repositories update
```

---

# Ontology Watch Agent

Responsibilities:

- monitor candidate nodes;
- inspect unresolved vocabulary;
- detect repeated free-text terms;
- identify schema failures caused by genuine new concepts;
- compare domain ontology with core ontology;
- emit gap results.

---

# Ontology Synthesis Agent

Responsibilities:

- propose definitions;
- identify parent types;
- suggest predicates;
- generate examples;
- search for duplicates;
- draft migration impact;
- generate candidate Pydantic schema changes.

It cannot merge its own proposal.

---

# Ontology Critic Agent

A separate agent should challenge proposals by checking:

- duplication;
- excessive specificity;
- insufficient specificity;
- domain leakage into core;
- unclear definitions;
- incompatible inheritance;
- unnecessary new predicates.

---

# Parallelism

Ontology discovery and analysis should be highly parallel.

Multiple agents may independently evaluate the same candidate.

Human review should be reserved for decisions where human judgement materially improves safety, scientific validity or long-term semantic stability.

---

# Versioning

Ontology versions use semantic versioning.

## Major

Breaking semantic changes.

## Minor

Backward-compatible additions.

## Patch

Clarifications that do not change machine semantics.

---

# Deprecation

Deprecated types remain resolvable.

Required metadata:

```yaml
status: deprecated
deprecated_at:
replacement:
migration_guidance:
```

---

# Removal

Removal from active schemas should occur only after:

- deprecation period;
- migration tooling;
- documentation;
- release notes.

Historical nodes must remain interpretable.

---

# Schema Migration

Every breaking or structurally meaningful change should provide:

- migration script where feasible;
- migration record;
- before/after examples;
- affected node count;
- validation report.

---

# Community Proposals

External contributors may submit ontology proposals through pull requests.

Templates should request:

- scientific rationale;
- sources;
- examples;
- proposed hierarchy;
- impact.

---

# Governance Roles

Suggested roles:

- contributor;
- domain reviewer;
- ontology reviewer;
- maintainer;
- core maintainer.

Core maintainers approve stable `cric-core` ontology changes.

---

# Ontology Certification

CRIC should avoid using "certified" to imply universal scientific truth.

Instead, ontology states indicate governance maturity:

- experimental;
- candidate;
- stable;
- deprecated.

A stable type means CRIC has adopted its definition for interoperability.

---

# Automated Checks

Pull requests should run:

- schema generation;
- Pydantic tests;
- duplicate identifier checks;
- predicate validation;
- inheritance validation;
- example validation;
- migration tests;
- documentation generation.

---

# v0.1 Acceptance Criteria

- ontology proposal schema exists;
- experimental namespace exists;
- at least one example agent-generated proposal is demonstrated;
- proposal passes through review;
- pull request workflow is documented;
- stable ontology cannot be silently modified by agent execution;
- ontology version changes are testable;
- deprecated types remain resolvable.
