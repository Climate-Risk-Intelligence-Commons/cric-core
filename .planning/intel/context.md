# Context

Running notes from the 2 DOC-classified documents in the ingest set. These carry no
requirements, decisions or technical contracts of their own — both defer authority elsewhere —
but they record integration history and corpus state that downstream planning needs.

---

## Topic: PRD integration batch 07 — what was resolved
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md
Batch 07 integrated 36 Markdown specification files into the canonical PRD tree and applied
these resolutions: added the previously planned `Product-Scope-and-Domain-Architecture.md`;
canonicalised the production identifier form as `CRIC:<namespace>:<type>:<ulid>`; canonicalised
`DataAsset` as the schema type while retaining "asset" as generic prose; distinguished
`TrainingRun` and `EvaluationRun` from generic `ModelRun`; canonicalised the knowledge-state,
epistemic-state, negative-case and review vocabularies; made `cric-review` canonical rather than
merely optional; established precedence rules so older examples cannot override the canonical
registry; added requirements traceability and a coding implementation sequence.

## Topic: PRD integration batch 08 — deterministic retrieval architecture
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md
Batch 08 integrated the deterministic OKF multi-hop context-retrieval architecture — described
in the source as "a hybrid graph-plus-vector retrieval design assembling bounded, inspectable
LLM context deterministically, ahead of any LLM reasoning" — as one new engineering-tier
specification plus six amended files. Resolutions: added
`engineering/Deterministic-Retrieval-Engine-Specification.md` beneath the already-committed
R-025 and R-026; formalised ad hoc navigation/policy examples in
`interfaces/Search-and-Graph-Interfaces.md` into named, versioned Traversal Profiles and a
structured Query Template catalogue, and extended the Context Package schema with `uncertainty`,
`missing_expected_information`, `exclusions`, `evidence`, `sources`, `traversal_profile` and
`engine_version`; added the adjacency-derivation rule to the OKF Relationship Grammar;
deprecated `connected_to` and `associated_with`; added `exposes`, `supported_by`, `threatens`,
`depends_on`, `has_snapshot`; considered and rejected `caused_by`; registered `TraversalProfile`,
`ContextSubgraph` and `ContextPack` as canonical `ComputationalObject` types; added the LLM
Knowledge Boundary and LLM Prompt Contract to `ai/Agent-Commons-Architecture.md`; added the
five-way retrieval-failure classification and the ranking-reproducibility test to
`engineering/Testing-and-Quality-Assurance.md`; added traversal-profile-selected retrieval as a
named Graph API request mode; and promoted "the LLM must not perform graph traversal" to
Constitutional Product Rule 13.

## Topic: Known integration note — illustrative material not yet mechanically updated
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md
"Earlier batch documents are preserved substantially as authored. Some contain illustrative
short IDs or generic `Asset` wording. The Canonical Schema and Vocabulary Registry resolves
these for implementation. A later editorial pass may mechanically update every example, but
coding agents should already follow the registry."

## Topic: Open item — OKF vs registry predicate-list divergence
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md
The audit records that `OKF-Knowledge-Graph-Specification.md`'s "Core predicates should include"
list "was already a representative/illustrative subset of `CRIC-Schema-and-Vocabulary-Registry.md`
§8's full predicate list before this batch — the two lists have never been identical (e.g.
`is_a`, `generated_by`, `contributes_to`, `trained_on`, `evaluated_on`, `predicted_by`,
`reviewed_by` appear only in the former; most spatial/domain predicates appear only in the
latter). This batch removed `associated_with` from both, but did not otherwise reconcile the
pre-existing divergence — that remains open for a future editorial pass."

## Topic: Open item — Cryosphere ontology still uses deprecated predicates
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md
"`domains/Cryosphere-Ontology.md` (not touched by this batch) still lists `associated_with`
(twice) and `connected_to` (twice) as live predicates for Glacier/GlacierTerminus/spatial
relationships, with no deprecation notice, even though both were just deprecated project-wide in
this batch. Cryosphere is CRIC's first domain implementation, so this is not a low-priority
corner case — it is flagged here rather than silently fixed, since editing domain-specific
predicate usage is outside this batch's reviewed scope and belongs to whoever owns that file's
next revision." Verified against the source: `associated_with` appears under Glacier
Relationships and GlacialLake Relationships; `connected_to` appears under GlacialLake
Relationships and Spatial Relationships.

## Topic: Open item — R-041 ratification status
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md
The audit states R-041 (the LLM write-side knowledge-boundary requirement, parallel to how R-026
covers reads) "is pending Ashley's decision. It has been added to
`CRIC-Requirements-Traceability-Matrix.md`, explicitly marked *PROPOSED — pending Ashley's
decision, not yet ratified*". The traceability matrix as it currently stands instead marks R-041
"ACCEPTED — Engineering Coordinator ... 2026-09-03T10:04:53Z". This divergence is raised as a
WARNING in `.planning/INGEST-CONFLICTS.md`; both variants are preserved in
`.planning/intel/requirements.md`.

## Topic: Authority deferral by this document
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md
The audit's own text defers authority to `CRIC-Schema-and-Vocabulary-Registry.md`, "where the
binding decisions live". Its "Resolutions Applied" entries read decision-like but the document
has no frontmatter, no status field, no Context/Decision/Consequences structure and covers many
decisions across two batches; it was classified DOC, not ADR, on that basis.

## Topic: Corpus integrity manifest
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-File-Manifest.md
A two-column table of the 38 CRIC PRD v0.1 documents and their SHA-256 checksums. It contains no
requirements, decisions, schemas or endpoint definitions. Its value to downstream consumers is
as (a) an integrity manifest for the corpus and (b) a complete index of the PRD file set. Note
the count arithmetic: the manifest lists 38 files (it includes `CRIC-Integration-Audit.md` but
not itself); the ingest set is 39 documents, being those 38 plus the manifest itself.
