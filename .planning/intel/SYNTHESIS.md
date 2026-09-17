# Synthesis Summary

Entry point for downstream consumers. Produced by `gsd-doc-synthesizer` from the per-doc
classifications in `.planning/intel/classifications/` and the source documents themselves.

MODE: new. Precedence: ADR > SPEC > PRD > DOC, with two per-doc overrides applied
(`CRIC-Schema-and-Vocabulary-Registry.md` = 0, `CRIC-PRD-MASTER.md` = 1).

---

## Corpus

39 classified documents, all under `docs/CRIC-PRD-v0.1/`. This is one coherent PRD family
(CRIC PRD v0.1), not a pile of independent documents.

- SPEC: 30
- PRD: 7
- DOC: 2
- ADR: 0

Confidence: 9 high, 30 medium. No UNKNOWN classifications and no low-confidence
classifications, so no document was excluded for being untypeable.

All 39 documents were consumed and are represented in the intel files: 30 SPEC documents in
`constraints.md`, 7 PRD documents in `requirements.md`, 2 DOC documents in `context.md`, with
`decisions.md` drawing on the Master PRD, the Registry, the implementation-sequence document
and three others.

## Decisions

`.planning/intel/decisions.md` — 29 entries.

**Decisions locked: 0.** The ingest set contains no ADR-classified document and no document
carrying `locked: true`, so no entry can be marked `locked` without misrepresenting the
classification. Every entry is `status: proposed`. This is a statement about classification
state, not about how binding the corpus considers its own content — where a source declares
content constitutional, canonical or non-negotiable, that wording is preserved verbatim inside
the entry's `decision:` field.

Highest-value content for planning:

- The 13 Constitutional Product Rules (CPR-01..CPR-13), source
  `docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md`.
- The 8 Architecture Freeze Points (ID format; base OKF frontmatter; temporal model; provenance
  model; relationship representation; knowledge-state vocabulary; review decision schema; agent
  manifest schema), source
  `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md`.
- The registry's canonical resolutions (identifier form, `DataAsset`, `TrainingRun`/
  `EvaluationRun`, the three retrieval artefact types, deprecated predicates, `cric-review`
  canonical, the closed vocabularies), source
  `docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md` (precedence 0).
- The Coding-Agent Work Package Rule and the Phase 0-14 build order with per-phase exit
  criteria.

## Requirements

`.planning/intel/requirements.md` — 56 entries.

- 41 carry the corpus's own numbering, `REQ-R-001-*` through `REQ-R-041-*`, extracted from
  `CRIC-Requirements-Traceability-Matrix.md`. Their `acceptance:` is that document's own
  "v0.1 Verification" column. The R-nnn identifiers are preserved inside the slug because
  cross-document traceability in this corpus depends on them.
- 2 are the competing ratification-status variants for R-041 (see Conflicts below); both are
  preserved, neither merged.
- 13 are PRD-level requirements not in the matrix: the v0.1 Definition of Done and first
  implementation goal, the safety statement, product mission, success criteria, design
  invariants, product values, product non-goals, domain architecture, governance model,
  contribution process, and the v0.2 objectives and non-goals.

## Constraints

`.planning/intel/constraints.md` — 243 entries across all 30 SPEC documents.

Type breakdown:

- schema: 85
- protocol: 93
- nfr: 42
- api-contract: 23

Where a document's content diverges from the registry, both forms are retained under their own
sources and the divergence is recorded in the conflicts report rather than silently rewritten.
Entries affected by a divergence carry an inline NOTE pointing at the report.

## Context

`.planning/intel/context.md` — 8 topics from the 2 DOC documents: the batch 07 and batch 08
integration resolutions, three open items the corpus flags about itself (predicate-list
divergence, Cryosphere's use of deprecated predicates, R-041's status), the authority deferral
by the audit document, and the corpus integrity manifest.

## Conflicts

`.planning/INGEST-CONFLICTS.md` — **2 blockers, 1 competing variant, 9 auto-resolved.**

Blockers are both cross-reference cycles, characterised in the report as mutual-citation loops
between reference documents rather than definitional deadlocks. The strongly-connected component
is 5 of 39 documents: `CRIC-PRD-MASTER.md`, `CRIC-Schema-and-Vocabulary-Registry.md`,
`knowledge/OKF-Knowledge-Graph-Specification.md`, `interfaces/Search-and-Graph-Interfaces.md`,
`engineering/Deterministic-Retrieval-Engine-Specification.md`.

**Deviation from default behaviour, recorded explicitly:** the default rule excludes a cyclic
set from synthesis. That was not done. On the orchestrator's instruction not to silently drop
documents, all 39 — including all 5 cyclic ones — were synthesized. The cycles are reported in
full so the judgement rests with the user. If either cycle is judged genuine rather than benign,
re-check the intel derived from those 5 documents before routing.

The one warning is R-041's ratification status, which three documents disagree about. The
substantive rule (the four-step LLM write pipeline) is not in dispute; only whether the
requirement is ratified. It was not auto-resolved: type precedence alone would return "not
ratified" and thereby overturn a dated, attributed ratification annotation, and resolving by
that annotation's date would be a forbidden timestamp tiebreak.

The 9 auto-resolved entries are almost all the registry (precedence 0) overriding a specialised
document — deprecated predicates still live in the Cryosphere ontology, `Asset` vs `DataAsset`,
`ModelRun` vs `TrainingRun`/`EvaluationRun`, `cric-review` canonical vs recommended, and type-list
scope divergences — plus one conformant-not-conflicting note on short-form example IDs and one
self-declared open gap (no trust/review-status vocabulary exists anywhere in the corpus, though
the retrieval engine's `by_trust` index and ranking trust weight both assume one).

## Files

- `.planning/intel/decisions.md`
- `.planning/intel/requirements.md`
- `.planning/intel/constraints.md`
- `.planning/intel/context.md`
- `.planning/INGEST-CONFLICTS.md`
