## Conflict Detection Report

Ingest set: 39 classified documents (30 SPEC / 7 PRD / 2 DOC / 0 ADR), MODE=new.
Per-doc precedence overrides in force: `CRIC-Schema-and-Vocabulary-Registry.md` = 0,
`CRIC-PRD-MASTER.md` = 1. All other documents fall back to ADR > SPEC > PRD > DOC.

Detection passes with no candidates: LOCKED-vs-LOCKED ADR contradiction (0 ADRs in the set, no
document carries `locked: true`); ADR-vs-existing-locked-CONTEXT.md (MODE is new, no existing
`.planning/` context); UNKNOWN-confidence-low documents (0 UNKNOWN, 0 low-confidence — the set
is 9 high / 30 medium).

### BLOCKERS (2)

[BLOCKER] Cross-reference cycle: Master PRD and Canonical Registry cite each other
  Found: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md declares `CRIC-Schema-and-Vocabulary-Registry.md`
    its canonical registry and lists it first in its own Document Map and authority precedence;
    docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md §16 closes the loop by naming
    CRIC-PRD-MASTER as rank 2 in its precedence ordering. Closing edge:
    Registry §16 -> CRIC-PRD-MASTER.
  Expected: a directed acyclic cross-reference graph; DFS three-colour marking (max traversal
    depth 50, not exceeded — deepest observed path is 4) found this 2-cycle plus three longer
    cycles that all close through the same Registry -> Master edge:
    Master -> knowledge/OKF-Knowledge-Graph-Specification.md -> Registry -> Master;
    Master -> interfaces/Search-and-Graph-Interfaces.md -> Registry -> Master;
    Master -> engineering/Deterministic-Retrieval-Engine-Specification.md ->
      interfaces/Search-and-Graph-Interfaces.md -> Registry -> Master.
  Character: mutual-citation loop between reference documents, NOT a definitional deadlock.
    Neither document defines a term the other must resolve first. The Master names the Registry
    as the canonical vocabulary source; the Registry names the Master as the next authority
    below itself. Each citation is a governance-ordering statement, and the two orderings agree
    (Registry outranks Master in both). Nothing needs to be computed in a fixed order to read
    either document.
  → Judged benign, acknowledge and proceed; or, to make the graph acyclic, drop the Registry's
    §16 mention of CRIC-PRD-MASTER (the same ordering is already stated in the Master's own
    Implementation Authority section), or trim the set via --manifest.

[BLOCKER] Cross-reference cycle: retrieval engine and search interface cite each other
  Found: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md cites
    `interfaces/Search-and-Graph-Interfaces.md` as owning "what retrieval exposes";
    docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md cites the engine specification
    back in its Context Package section. Closing edge:
    Search-and-Graph-Interfaces.md -> engineering/Deterministic-Retrieval-Engine-Specification.md.
  Expected: a directed acyclic cross-reference graph. This 2-cycle sits inside the same
    strongly-connected component as the blocker above; that component is
    {CRIC-PRD-MASTER.md, CRIC-Schema-and-Vocabulary-Registry.md,
    knowledge/OKF-Knowledge-Graph-Specification.md, interfaces/Search-and-Graph-Interfaces.md,
    engineering/Deterministic-Retrieval-Engine-Specification.md} — 5 of 39 documents.
  Character: mutual-citation loop between reference documents, NOT a definitional deadlock. The
    two documents explicitly partition ownership — the engine specification states
    "`interfaces/Search-and-Graph-Interfaces.md` owns what retrieval exposes ... This document
    owns how the engine underneath that surface is built" — so each cites the other precisely
    for the half it does not own. The one shared definition, the Context Package / ContextPack
    schema, has a single declared owner (Search-and-Graph-Interfaces.md: "the YAML schema below
    is its single canonical definition"), and the engine specification maps onto those field
    names rather than restating them.
  → Judged benign, acknowledge and proceed; or trim the set via --manifest.

DEVIATION RECORDED: the default rule for a detected cycle is to exclude the cyclic set from
synthesis. That was NOT done here. On the orchestrator's explicit instruction not to silently
drop documents, all 39 documents — including all 5 in the strongly-connected component — were
synthesized into the intel files. Both cycles are reported above with their characterisation so
the decision to proceed rests with the user, not with this synthesis pass. If either cycle is
judged genuine rather than benign, the intel derived from those 5 documents should be re-checked
before routing.

### WARNINGS (1)

[WARNING] Competing ratification status for requirement R-041
  Found: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md records R-041 as
    "ACCEPTED — Engineering Coordinator, `docs/OPEN_QUESTIONS.md` U5, channel event
    `7c037f772b9bb01b6b388ca4dea1ddc980b26738b08d721f35e7b0ac539041e1`, 2026-09-03T10:04:53Z".
  Found: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md records the same requirement as
    "explicitly marked *PROPOSED — pending Ashley's decision, not yet ratified*, so its
    existence is visible for review without it being treated as an active requirement before
    that decision is made".
  Found: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md agrees with the audit — "it is not
    yet backed by its own numbered requirement. A dedicated traceability-matrix requirement for
    the write-side boundary specifically (candidate identifier \"R-041\") is under separate
    consideration; this document does not assume or cite that identifier."
  Impact: the substantive rule is not in dispute — all three documents assert the same four-step
    LLM write pipeline (structured mutation -> Pydantic validation -> human/policy check ->
    atomic write). Only R-041's ratification status differs, and that status determines whether
    a roadmapper treats the write-boundary bypass test as an active v0.1 acceptance criterion or
    as a pending decision. Resolving by type precedence alone would silently overturn a dated,
    attributed ratification annotation: Agent-Commons-Architecture.md is SPEC (rank 2) and
    outranks the Traceability Matrix, which is PRD (rank 3), so the mechanical rule would return
    "not ratified". That outcome is recorded here rather than applied, because a governance
    ratification event is not the kind of contradiction the type ordering was written to
    arbitrate, and because resolving by the annotation's later date would be a timestamp
    tiebreak, which the precedence rules forbid.
  → Confirm R-041's status (Ashley's decision per the audit's own wording), then update whichever
    of the three documents is stale. Both variants are preserved as
    REQ-R-041-status-variant-a and REQ-R-041-status-variant-b in
    `.planning/intel/requirements.md`; neither was merged or discarded.

### INFO (9)

[INFO] Precedence model applied to this ingest
  Note: two per-doc precedence overrides were supplied in the classification JSONs and applied
  as specified — `CRIC-Schema-and-Vocabulary-Registry.md` = 0 and `CRIC-PRD-MASTER.md` = 1.
  These encode the repository's own declared authority precedence and are corroborated by the
  sources themselves: CRIC-PRD-MASTER.md §Implementation Authority and
  CRIC-Schema-and-Vocabulary-Registry.md §16 independently state the same ordering (registry >
  master PRD > specialised PRD documents > older examples). The registry consequently outranks
  all 37 other documents in this ingest, and every auto-resolution below follows from that.

[INFO] Auto-resolved: Registry > Cryosphere Ontology on deprecated predicates
  Note: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md §8 removes `connected_to` and
  `associated_with` as canonical relationship predicates, naming them vague/semantically-empty
  anti-patterns. docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md still lists `associated_with`
  as a live predicate under Glacier Relationships and GlacialLake Relationships, and
  `connected_to` under GlacialLake Relationships and Spatial Relationships, with no deprecation
  notice. Registry precedence 0 wins; the deprecations stand. Both forms are preserved under
  their own sources in `.planning/intel/constraints.md`. This is the same divergence the corpus
  already flags itself in docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md, which notes Cryosphere
  is the first domain implementation so "this is not a low-priority corner case".

[INFO] Auto-resolved: Registry > OKF Knowledge Graph Specification on the predicate list
  Note: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md lists core predicates
  including `is_a`, `generated_by`, `contributes_to`, `affected`, `trained_on`, `evaluated_on`,
  `predicted_by` and `reviewed_by` that do not appear in registry §8, while most of the
  registry's spatial/domain predicates do not appear in the OKF list. No override was needed:
  the OKF document itself states "`CRIC-Schema-and-Vocabulary-Registry.md` section 8 is the sole
  authority for the canonical predicate list; the list above is illustrative, not exhaustive."
  Registry §8 governs. The corpus records this divergence as an open editorial item in
  CRIC-Integration-Audit.md.

[INFO] Auto-resolved: Registry > Core Ontology and OKF specifications on `Asset` vs `DataAsset`
  Note: registry §3 Asset Resolution states "Use `DataAsset` as the canonical ontology type.
  `Asset` may remain a generic prose term but SHOULD NOT be used as a competing schema type."
  docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md lists `Asset` as a ResourceObject
  child type and gives it a field list; docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-
  Specification.md lists `Asset` among minimum node categories. Registry wins — `DataAsset` is
  the schema type. docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md already uses
  `DataAsset` and is consistent with the registry.

[INFO] Auto-resolved: Registry > Core Ontology Specification on run record types
  Note: registry §3 Model Run Resolution requires `TrainingRun` for training, `EvaluationRun`
  for evaluation, and `ModelRun` only as the generic parent or non-training/non-evaluation
  execution record. docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md's
  ComputationalObject branch lists only `ModelRun` ("Records a training, inference or evaluation
  execution"). Registry wins. docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md and
  docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md already follow the
  registry's three-type split.

[INFO] Auto-resolved: Registry > Software Architecture and v0.1 Implementation on `cric-review`
  Note: registry §12 states "`cric-review` is canonical in the integrated architecture because
  HITL is a first-class workflow layer".
  docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md omits it from "Expected repositories"
  and calls it "recommended where shared HITL workflow warrants independent permissions and
  lifecycle"; docs/CRIC-PRD-v0.1/implementation/CRIC-v0.1-Implementation-Specification.md lists
  it under "Recommended" rather than "Required". Registry wins — `cric-review` is canonical.
  docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md and
  docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md both already
  treat it as first-class.

[INFO] Auto-resolved: Registry > Core Ontology and OKF specifications on the canonical type list
  Note: beyond the two named resolutions above, the type inventories diverge in scope. Registry
  §3 lists TrainingRun, EvaluationRun, FeatureSet, Licence, TraversalProfile, ContextSubgraph and
  ContextPack among canonical core types; Core-Ontology-Specification.md's root hierarchy omits
  all seven. OKF-Knowledge-Graph-Specification.md's node categories add Location, Organisation,
  Person, Sensor and ModelCard, which registry §3 does not list. Registry §3 governs the
  canonical set; the other documents' lists are retained under their own sources in
  `.planning/intel/constraints.md` as the type coverage each document assumes.

[INFO] Short-form identifiers in examples are conformant, not conflicting
  Note: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md uses `CRIC-LAKE-000123` and
  `CRIC-OBS-0012`, and docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md uses
  `CRIC-LAKE-001`, rather than the canonical `CRIC:<namespace>:<type>:<ulid>` form. This is not
  a contradiction: registry §2 explicitly permits short IDs "in examples and fixtures" while
  prohibiting them as the production identifier format, and every occurrence found is inside an
  illustrative snippet. Recorded for transparency because CRIC-Integration-Audit.md flags
  illustrative short IDs as material a future editorial pass may update.

[INFO] Self-declared open gap: no trust / review-status vocabulary exists
  Note: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md states
  "No controlled vocabulary for trust or review-status enum values (for example, distinguishing
  `machine-confirmed` from `human-reviewed`) currently exists anywhere in the PRD", while its own
  `by_trust` index and its ranking function's trust weight both assume such values exist and are
  comparable/orderable. Verified against the corpus: registry §10 defines review *queue states*
  and `ReviewDecision.decision` values, which are a different dimension; neither
  Evidence-Provenance-and-Trust.md nor Claims-Contradictions-and-Knowledge-Lifecycle.md
  enumerates permitted values for the "review status" trust dimension they each name. This is a
  gap the corpus declares about itself, not a contradiction between documents, so it is INFO
  rather than a blocker — but it is an unresolved dependency for the retrieval engine and is
  carried in `.planning/intel/constraints.md` under its source.
