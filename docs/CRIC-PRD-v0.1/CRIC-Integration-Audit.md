# CRIC Batch 07 Integration Audit

## Scope

Integrated 36 Markdown specification files into the canonical PRD tree.

## Resolutions Applied

- Added the previously planned `Product-Scope-and-Domain-Architecture.md`.
- Canonicalised production identifier form as `CRIC:<namespace>:<type>:<ulid>`.
- Canonicalised `DataAsset` as the schema type while retaining “asset” as generic prose.
- Distinguished `TrainingRun` and `EvaluationRun` from generic `ModelRun`.
- Canonicalised knowledge-state, epistemic-state, negative-case and review vocabularies.
- Made `cric-review` canonical rather than merely optional in the integrated repository family.
- Established precedence rules so older examples cannot override the canonical registry.
- Added requirements traceability and coding implementation sequence.

## Known Integration Note

Earlier batch documents are preserved substantially as authored. Some contain illustrative short IDs or generic `Asset` wording. The Canonical Schema and Vocabulary Registry resolves these for implementation. A later editorial pass may mechanically update every example, but coding agents should already follow the registry.

## File Inventory

- `CRIC-PRD-MASTER.md`
- `CRIC-Repository-Dependency-and-Implementation-Sequence.md`
- `CRIC-Requirements-Traceability-Matrix.md`
- `CRIC-Schema-and-Vocabulary-Registry.md`
- `ai/Agent-Commons-Architecture.md`
- `ai/Agent-Team-Specifications.md`
- `ai/Model-Commons-and-ML-Specification.md`
- `ai/Responsible-Autonomy-and-HITL.md`
- `community/Contribution-and-Review-Process.md`
- `community/Open-Source-Governance.md`
- `community/Volunteer-HITL-Workflow.md`
- `data/Data-Commons-Architecture.md`
- `data/Data-Quality-and-Validation.md`
- `data/Ingestion-and-Licensing.md`
- `data/Training-Data-and-Benchmark-Specification.md`
- `domains/Cryosphere-Ontology.md`
- `domains/GLOF-Ontology.md`
- `domains/StateSnapshot-and-Event-Cube-Specification.md`
- `engineering/Deployment-Versioning-and-Releases.md`
- `engineering/Security-and-Responsible-AI.md`
- `engineering/Software-Architecture.md`
- `engineering/Testing-and-Quality-Assurance.md`
- `implementation/CRIC-v0.1-Implementation-Specification.md`
- `implementation/CRIC-v0.2-Implementation-Specification.md`
- `interfaces/API-and-SDK-Specification.md`
- `interfaces/Human-Applications-and-UI.md`
- `interfaces/Search-and-Graph-Interfaces.md`
- `knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md`
- `knowledge/Core-Ontology-Specification.md`
- `knowledge/Evidence-Provenance-and-Trust.md`
- `knowledge/OKF-Knowledge-Graph-Specification.md`
- `knowledge/Ontology-Evolution-and-Governance.md`
- `knowledge/Temporal-and-Epistemic-Ontology.md`
- `product/Product-Scope-and-Domain-Architecture.md`
- `product/Product-Vision-and-Principles.md`
- `product/Repository-and-System-Architecture.md`

---

# CRIC Batch 08 Integration Audit

## Scope

Integrated the deterministic OKF multi-hop context-retrieval architecture (a hybrid graph-plus-vector retrieval design assembling bounded, inspectable LLM context deterministically, ahead of any LLM reasoning) into the canonical PRD tree: one new engineering-tier specification and six amended files.

## Resolutions Applied

- Added `engineering/Deterministic-Retrieval-Engine-Specification.md` — the engine-level design (package responsibilities, node/edge indexes, deterministic traversal ordering, compiled-graph incremental recompilation, versioned ranking function, five-way failure classification) underneath the already-committed requirements R-025 and R-026.
- Formalised `interfaces/Search-and-Graph-Interfaces.md`'s previously ad hoc navigation/policy examples into named, versioned Traversal Profiles and a structured Query Template catalogue; extended the Context Package schema with `uncertainty`, `missing_expected_information`, `exclusions`, `evidence`, `sources`, `traversal_profile`, and `engine_version`; added a Retrieval Completeness section.
- Added an explicit adjacency-derivation rule to `knowledge/OKF-Knowledge-Graph-Specification.md`'s Relationship Grammar: a relationship is declared once, the compiler derives both `out_edges` and `in_edges`; paired predicate names remain for authoring ergonomics only, not as a dual-declaration requirement.
- Deprecated `connected_to` and `associated_with` as canonical relationship predicates (`CRIC-Schema-and-Vocabulary-Registry.md` §8 and `OKF-Knowledge-Graph-Specification.md`) as vague/semantically-empty; added `exposes`, `supported_by`, `threatens`, `depends_on`, `has_snapshot`; considered and rejected `caused_by` as redundant with the existing `triggered_by`.
- Registered `TraversalProfile`, `ContextSubgraph`, and `ContextPack` as canonical `ComputationalObject` types (`CRIC-Schema-and-Vocabulary-Registry.md` §3).
- Added an "LLM Knowledge Boundary" (read only via Context Pack API; write only via structured mutation → validation → human/policy check → atomic write) and an "LLM Prompt Contract" section to `ai/Agent-Commons-Architecture.md`.
- Added a five-way retrieval-failure classification (knowledge / retrieval / context-construction / reasoning / generation) and a ranking-reproducibility test to `engineering/Testing-and-Quality-Assurance.md`.
- Added traversal-profile-selected retrieval as a named Graph API request mode in `interfaces/API-and-SDK-Specification.md`.
- Promoted "the LLM must not perform graph traversal; deterministic software assembles context first" from architecture guidance to Constitutional Product Rule 13 (see `CRIC-PRD-MASTER.md`).

## Known Integration Note

`OKF-Knowledge-Graph-Specification.md`'s "Core predicates should include" list was already a representative/illustrative subset of `CRIC-Schema-and-Vocabulary-Registry.md` §8's full predicate list before this batch — the two lists have never been identical (e.g. `is_a`, `generated_by`, `contributes_to`, `trained_on`, `evaluated_on`, `predicted_by`, `reviewed_by` appear only in the former; most spatial/domain predicates appear only in the latter). This batch removed `associated_with` from both, but did not otherwise reconcile the pre-existing divergence — that remains open for a future editorial pass, same disposition as the general "Known Integration Note" from Batch 07 above.

A candidate requirement R-041 (an explicit LLM write-side knowledge-boundary requirement, parallel to how R-026 covers reads) was identified during this integration and is pending a decision; it has not been added to `CRIC-Requirements-Traceability-Matrix.md`.

## File Inventory

- `CRIC-Schema-and-Vocabulary-Registry.md` (amended)
- `ai/Agent-Commons-Architecture.md` (amended)
- `engineering/Deterministic-Retrieval-Engine-Specification.md` (new)
- `engineering/Testing-and-Quality-Assurance.md` (amended)
- `interfaces/API-and-SDK-Specification.md` (amended)
- `interfaces/Search-and-Graph-Interfaces.md` (amended)
- `knowledge/OKF-Knowledge-Graph-Specification.md` (amended)
