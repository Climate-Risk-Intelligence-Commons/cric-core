# Decisions

Synthesized from classified docs in `.planning/intel/classifications/`.

**Provenance note.** The ingest set contains **zero ADR-classified documents** (30 SPEC / 7 PRD
/ 2 DOC) and **no document carries `locked: true`**. Every entry below is therefore
`status: proposed` — that is the classification's state, not a judgement about how binding the
source considers itself. Where a source declares its own content constitutional, canonical or
non-negotiable, that wording is preserved verbatim inside the `decision:` field so the
distinction is not lost downstream.

Two per-doc precedence overrides are in force for this ingest and are reflected in the entries
below: `CRIC-Schema-and-Vocabulary-Registry.md` = 0 (highest), `CRIC-PRD-MASTER.md` = 1. All
other docs fall back to the type ordering ADR > SPEC > PRD > DOC.

---

## CPR-01: Evidence lineage is immutable
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 1 — "Evidence lineage is immutable."
- scope: provenance, evidence lineage, all derived objects

## CPR-02: Every significant derived value must be traceable to source evidence
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 2 — "Every significant derived value must be traceable to source evidence."
- scope: provenance, derived features, model outputs, assessments

## CPR-03: Scientific contradiction is represented, not erased
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 3 — "Scientific contradiction is represented, not erased."
- scope: claims, contradictions, knowledge graph, retrieval

## CPR-04: Historical knowledge state remains reconstructable
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 4 — "Historical knowledge state remains reconstructable."
- scope: temporal model, system time, supersession, bitemporal query

## CPR-05: Evidence completeness is separate from hazard/risk
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 5 — "Evidence completeness is separate from hazard/risk."
- scope: data quality, UI display, risk state, evidence completeness scoring

## CPR-06: Unknown is not negative
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 6 — "Unknown is not negative."
- scope: training labels, negative-case vocabulary, epistemic status

## CPR-07: Deterministic computation is preferred where suitable
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 7 — "Deterministic computation is preferred where deterministic computation is suitable."
- scope: workflow layer, ingestion, geospatial, agent design

## CPR-08: Agents operate through typed contracts and explicit permissions
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 8 — "Agents operate through typed contracts and explicit permissions."
- scope: Agent Commons, agent manifest, permissions, Pydantic output schemas

## CPR-09: Agent components remain separable
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 9 — "Agent tools, datasets, workspaces, dependencies and model configuration remain separable."
- scope: Agent Commons, dependency injection, agent composition contract

## CPR-10: Human oversight scales with uncertainty, irreversibility, authority and consequence
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 10 — "Human oversight increases with uncertainty, irreversibility, authority and consequence."
- scope: autonomy levels, HITL, review routing

## CPR-11: CRIC never silently assumes institutional warning authority
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 11 — "CRIC never silently assumes institutional warning authority."
- scope: safety, prohibited autonomous actions, Level 5 autonomy, public communication

## CPR-12: Core architecture remains climate-risk-wide rather than GLOF-specific
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 12 — "Core architecture remains climate-risk-wide rather than GLOF-specific."
- scope: cric-core, core invariance rule, domain packages

## CPR-13: The LLM must not perform graph traversal
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: Constitutional Product Rule 13 — "The LLM must not perform graph traversal; deterministic software assembles context first." Promoted from architecture guidance to a Constitutional Product Rule in PRD integration batch 08 (docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md).
- scope: deterministic retrieval engine, Context Pack, LLM knowledge boundary, agent read access

## Implementation authority precedence
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- status: proposed
- decision: For coding work, resolve conflicts in this order — (1) executable contracts in a released `cric-core`; (2) `CRIC-Schema-and-Vocabulary-Registry.md`; (3) this Master PRD; (4) specialised PRD documents; (5) examples and older illustrative snippets.
- scope: conflict resolution across the whole PRD family

## Registry precedence rule (self-declared)
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Section 16 — for implementation disputes: (1) this Canonical Registry; (2) CRIC-PRD-MASTER; (3) specialised PRD document; (4) older examples or illustrative snippets. "A future schema repository release supersedes this prose registry once executable contracts are published." Section Status adds: "Where an earlier document differs from this registry, this registry is authoritative for implementation until the relevant source document is revised."
- scope: conflict resolution, registry authority, future supersession by executable schemas

## Canonical identifier form
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Section 2 — canonical logical form is `CRIC:<namespace>:<type>:<ulid>`. "Human-facing short IDs such as `CRIC-LAKE-001` may appear in examples and fixtures, but MUST NOT be treated as the canonical production identifier format."
- scope: identifiers, all object types, cross-repository identity

## Asset resolution: DataAsset is canonical
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Section 3 Asset Resolution — "Use `DataAsset` as the canonical ontology type. `Asset` may remain a generic prose term but SHOULD NOT be used as a competing schema type."
- scope: core ontology, ResourceObject types, data commons

## Model run resolution: TrainingRun / EvaluationRun / ModelRun
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Section 3 Model Run Resolution — use `TrainingRun` for model training; `EvaluationRun` for evaluation; `ModelRun` only as the generic parent or non-training/non-evaluation execution record.
- scope: core ontology, ComputationalObject types, Model Commons

## Retrieval artefact resolution: TraversalProfile / ContextSubgraph / ContextPack
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Section 3 Retrieval Artefact Resolution — `TraversalProfile`, `ContextSubgraph` and `ContextPack` are canonical `ComputationalObject` types introduced by the deterministic OKF multi-hop context-retrieval architecture. `TraversalProfile` defines permitted traversal paths (analogous to `Workflow`); `ContextSubgraph` is the resolved node/edge subgraph returned by traversal; `ContextPack` is the bounded, versioned context package built from it for LLM consumption.
- scope: core ontology, retrieval engine, Context Pack

## Deprecated relationship predicates
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Section 8 Deprecated Predicates — `connected_to` removed (vague/semantically-empty, named an anti-pattern predicate alongside `linked_to`, `related_with`, `associated_with`, `impacts`, `affects`, `near`); `associated_with` removed for the same reason. `caused_by` was considered as a new predicate and rejected as redundant with the existing `triggered_by` at CRIC's current level of ontological granularity. "Predicates MUST be registered and versioned."
- scope: relationship predicates, ontology registry, domain ontologies

## cric-review is canonical, not optional
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Section 12 — "`cric-review` is canonical in the integrated architecture because HITL is a first-class workflow layer."
- scope: repository family, HITL, review workflow

## Vocabulary closures fixed by the registry
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Sections 4-11 fix the canonical closed vocabularies: knowledge state (candidate/accepted/disputed/superseded/rejected/withdrawn/archived); epistemic status (observed/reported/derived/inferred/simulated/hypothesised/disputed/unknown); negative-case (confirmed_negative/probable_negative/no_known_event/unknown/unobserved/not_applicable, with "`unknown`, `unobserved`, and `no_known_event` MUST NOT be automatically converted to negative training labels"); multi-temporal block (event/observation/valid/system time); evidence and provenance levels L0-L6; review queue states and `ReviewDecision.decision` values; six autonomy levels 0-5.
- scope: controlled vocabularies, schema authority, training data, review, autonomy

## No mandatory agent orchestration framework
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- status: proposed
- decision: Section 13 — the canonical agent composition contract is Agent Definition + Instructions + Dependency Schema + Toolsets + Datasets + Workspace + Model Configuration + Structured Output Schema + Permissions + Evaluation Suite. "No mandatory orchestration framework is part of the CRIC contract." Restated in `engineering/Software-Architecture.md`: "No mandatory orchestration framework such as LangGraph is required."
- scope: Agent Commons, agent runtime, software architecture

## Eight Architecture Freeze Points
- source: docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md
- status: proposed
- decision: "Before v0.1 coding accelerates, freeze candidate versions of: 1. ID format; 2. base OKF frontmatter; 3. temporal model; 4. provenance model; 5. relationship representation; 6. knowledge-state vocabulary; 7. review decision schema; 8. agent manifest schema. Changes remain possible but require explicit migration after the freeze."
- scope: cric-core Phase 1 contracts, all downstream phases and repositories

## Coding-Agent Work Package Rule
- source: docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md
- status: proposed
- decision: Every implementation task handed to a coding agent SHOULD contain a `work_package` block with fields: repository, objective, authoritative_prd_sections, upstream_contracts, files_allowed_to_change, tests_required, acceptance_criteria, prohibited_changes, review_required. Stated rationale: "This prevents coding agents from opportunistically redesigning CRIC architecture while implementing a narrow task."
- scope: task shape for all implementation work across repositories

## Phased build order and critical path
- source: docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md
- status: proposed
- decision: Phases 0-14 with per-phase exit criteria: 0 organisation/contracts; 1 cric-core (11-step build order, exit = canonical example OKF nodes validate); 2 cric-knowledge; 3 cric-data; 4 cric-cryosphere + cric-glof; 5 cric-ingest; 6 graph materialisation and retrieval; 7 cric-review; 8 cric-agents; 9 Event Cube pipeline; 10 cric-models; 11 cric-api; 12 cric-ui; 13 reference dataset expansion; 14 coordinated v0.1 release. Critical path: core schemas → OKF parser → domain schemas → ingestion/provenance → StateSnapshot/Event Cube → training dataset → baseline model. "Agent Commons and HITL can progress in parallel once `cric-core` contracts exist."
- scope: implementation sequencing, repository dependency order, parallel workstreams

## Merge rule: agents prepare, humans merge stable core
- source: docs/CRIC-PRD-v0.1/community/Contribution-and-Review-Process.md
- status: proposed
- decision: Merge Rules — "Stable core changes require maintainer approval. Agents may prepare branches and pull requests but should not autonomously merge stable core changes."
- scope: contribution process, merge policy, agent permissions

## Ontology governance: agents propose, they do not mutate the stable core
- source: docs/CRIC-PRD-v0.1/knowledge/Ontology-Evolution-and-Governance.md
- status: proposed
- decision: Governance Principle — "Agents may discover and propose ontology changes. Agents may not silently mutate the stable core ontology. Stable changes enter through pull requests." Human review is required for stable changes that alter semantic meaning, affect multiple repositories, change safety-relevant concepts, create breaking schema changes, or deprecate widely used types.
- scope: ontology evolution, OntologyProposal, human review triggers, cric-core

## PRD integration batch resolutions (record only)
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md
- status: proposed
- decision: Batch 07 recorded these resolutions — added `Product-Scope-and-Domain-Architecture.md`; canonicalised the identifier form; canonicalised `DataAsset`; distinguished `TrainingRun`/`EvaluationRun` from `ModelRun`; canonicalised the knowledge-state, epistemic-state, negative-case and review vocabularies; made `cric-review` canonical; established precedence rules; added traceability and implementation sequence. Batch 08 added the Deterministic Retrieval Engine specification, formalised Traversal Profiles and Query Templates, added the adjacency-derivation rule, deprecated `connected_to`/`associated_with`, added `exposes`/`supported_by`/`threatens`/`depends_on`/`has_snapshot`, rejected `caused_by`, registered the three retrieval artefact types, added the LLM Knowledge Boundary and LLM Prompt Contract, added the five-way retrieval-failure classification, and promoted Rule 13. This document is a per-batch integration record classified DOC; its own text defers authority to `CRIC-Schema-and-Vocabulary-Registry.md`, which is where the binding form of each resolution lives.
- scope: PRD integration history, batch 07 and 08 change record
