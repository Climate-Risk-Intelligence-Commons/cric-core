# ADR-0007: Freeze Points 6 + 7 — Knowledge-State Vocabulary and Review Decision Schema

- **Status:** Accepted — **Architecture Freeze Points** (second and third of the 8 to
  lock, ratified together as one unit; reversal requires explicit migration, not
  routine amendment)
- **Approver:** Ashley
- **Date:** 2026-09-03
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

Freeze Points 6 and 7 of 8 (per `CRIC-Repository-Dependency-and-Implementation-Sequence.md`):
knowledge-state vocabulary (registry §4) and the review decision schema. Ratified as
one unit because Freeze Point 6's transition graph is the image of Freeze Point 7's
`ReviewDecision.decision` vocabulary — neither is independently closable. Blast radius:
phases 4, 6, 7, 8, 9, 13, verified independently by both Pollen and the Engineering
Coordinator against `Domain-Phase-Mapping.md`'s actual rows.

**Freeze Point 4 (provenance model) is explicitly not part of this unit.** It looked
coupled in during assembly — the trust/`review_status` vocabulary that might have
pulled it in turned out to govern a different field entirely (see Alternatives). The
freeze-point count this ADR locks is two (6 and 7), not three.

Ratification checkpoint per `docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md`
§2: Fizz assembles and cites the candidate → Pollen does blast-radius verification and
tries to break it → Ashley signs. This was the first Freeze Point to go through the
checkpoint's full adversarial cycle more than once: four assembly rounds (WP-9, WP-11,
WP-13, WP-14), the Engineering Coordinator holding signature once mid-flight over
carried-but-unattacked items, and a fifth targeted round (WP-15) that found one real
gap before signature.

## Decision

**The seven-value knowledge-state vocabulary** (unanimous everywhere it appears in the
corpus, zero drift): `candidate, accepted, disputed, superseded, rejected, withdrawn,
archived`.

**The eight-edge transition envelope**, universal across all 31 OKF node categories
(`OKF-Knowledge-Graph-Specification.md:306`), per-type narrowing permitted:

```
candidate  → accepted
candidate  → rejected
candidate  → disputed
accepted   → disputed
accepted   → withdrawn
disputed   → accepted
disputed   → superseded
superseded → archived
```

No OKF node type may use a transition outside these eight. Negative test required for
every type: `superseded → candidate` and `withdrawn → accepted` must both fail
validation.

**`modify` is a compound transition, not a ninth edge.** A `ReviewDecision.decision:
modify` triggers supersede-plus-create: the source node moves to `superseded`, a new
node carrying the modification enters at `accepted`. `modified_values` may name a
field on the evidentiary side of the split (`value`, `claim_text`, `subject`,
`predicate`, `object`, `confidence`, `evidence_nodes`, `claimant`, `spatial_scope`,
`temporal_scope`) but **never a state field** — `status` is excluded outright,
regardless of category, because state changes happen exclusively through the
eight-edge graph above and nothing else. The exclusion names both `Claim.status` and
`Claim.knowledge_state.status` explicitly (`Claim` is the only one of the 31 node
types with both — `Core-Ontology-Specification.md:214` plus the inherited
`CRICObject:103-117` block), so an implementer cannot honestly exclude one while
permitting the other.

**`origin` is closed at three values:** `agent`, `deterministic_pipeline`, `human`.

**`knowledge_state.verification.method` is closed at four values:**
`deterministic_authoritative_source`, `corroboration_rules`, `human_review`,
`maintainer_approved_workflow` — the exhaustive list of
`Responsible-Autonomy-and-HITL.md`'s Level 3 promotion mechanisms (the only autonomy
level that defines promotion at all). Negative test required: an unrecognised string
must fail.

**`ReviewDecision.origin` is human-only**, and **`ReviewDecision` enters directly at
`accepted`**, not `candidate` — its schema (`reviewer`, `reviewer_role`,
`signature_method`) is an act of record, not something itself promoted through review.
Whether `disputed`/`superseded`/`rejected`/`withdrawn` are reachable from there is
carried, not settled — see open items below.

## Alternatives considered

- **Scoping Freeze Point 6 to `KnowledgeObject`-family types only** (Pollen's reading,
  built on "Model-Commons mentions `knowledge_state` zero times"). Genuinely
  incompatible with the Engineering Coordinator's independently-withheld reading
  (record-standing vs. thing-maturity orthogonality) — the two diverged, not
  converged, when compared. Neither side's framing settled it; a third citation
  neither had used, `OKF-Knowledge-Graph-Specification.md:306`'s Node Categories
  enumeration, did: every type under dispute (`Model`, `Prediction`, `ReviewDecision`,
  `Licence`, `OntologyProposal`) is an OKF node category governed by the universal
  frontmatter that carries `knowledge_state`. Rejected because it would leave thirty
  other types carrying an inherited, typed, ungoverned field — worse than either
  original position — and because scoping the field elsewhere would require moving
  `knowledge_state` off `CRICObject` in the ontology, a PRD amendment requiring
  Ashley's signature that this ruling avoids triggering.
- **Orthogonality as an empirical claim — "no counter-example exists in the corpus."**
  Its author (the Engineering Coordinator) could not verify his own reasoning per
  WP-12's rule and asked Pollen to attack it. Pollen's attack found that
  `ProvenanceRecord` and `MigrationRecord` — the hardest cases available — are both
  single-axis, with no documented second lifecycle anywhere in the corpus (event
  `be2c80454b187863fb9bbaa8b7f1c397414290f64a12648a2241a277c15b18f2`, 2026-08-29T16:00:39Z):
  a single-axis type cannot falsify orthogonality by construction, so that check could
  not settle the claim either way — it is why the first attempt did not close this,
  not evidence that it did. **Rejected in this form.** The Engineering Coordinator
  ruled explicitly against treating "no counter-example found" as the basis: *"That
  claim is unfalsifiable by reading… We are not claiming 'no counter-example exists in
  the corpus'"* (event `0dd3a435f6ce79178324af6a64e26c6d2c3a136a77da1d285d843a7cbe451686`,
  2026-08-29T16:02:52Z).
  **Ratified instead as an imposed invariant, not an empirical finding:** `knowledge_state`
  is orthogonal to any domain lifecycle by rule, not by exhaustive search — *"a type
  whose second axis would have to move in lockstep with `knowledge_state` is a defect
  in that type's specification, not a refutation of FP6"* (same event). This form is
  enforceable at type-design time; the rejected empirical form was not, and a future
  counter-example under it would have read as FP6 being broken rather than as a bug in
  the type that carries it. The invariant was exercised, not merely asserted, against
  two dual-axis types: `OntologyProposal` — inherited `knowledge_state` alongside its
  own `experimental → candidate → review → stable → deprecated → removed` lifecycle,
  zero cross-reference between the two anywhere in the corpus (Pollen, event
  `47d5bd1a217a715e56ffe15733fb5b155b332308585e8e0af48cecdfb4331962`, identified as the
  sharpest real conflict, not a hypothetical) — and, on adversarial re-attempt to
  construct a counter-example, held (`be2c8045…`, above); and `Licence` — its own
  status vocabulary at `Ingestion-and-Licensing.md:89` and
  `Evidence-Provenance-and-Trust.md:265`, independently found and verified against
  both citations by the Engineering Coordinator (`0dd3a435…`, above), decisively
  separable from `knowledge_state.status`. Ratified as applied to this Freeze Point's
  scope question; not extended further than that.
- **`review_status` / the trust vocabulary as part of this unit** (the reason Freeze
  Point 4 briefly looked coupled in). Confirmed a genuinely distinct field:
  `Label.review_status` is a top-level field sibling to `epistemic_status`, which
  would be redundant if it lived inside `knowledge_state.verification.method`.
  `verification.method` records a categorical *kind*; `review_status` is one of nine
  **gradable** Trust Dimensions requiring an orderable value — a categorical field
  cannot be forced into an order without producing plausible-but-wrong rankings.
  Deferred to Freeze Point 4 when it assembles, not folded in here.
- **Treating `status` and `knowledge_state.status` as interchangeable in the `modify`
  exclusion.** Rejected once found: naming only one lets an implementer honestly
  permit `modified_values: [knowledge_state.status]` while believing the exclusion
  was satisfied. Both are named.
- **The evidentiary/presentational split as the only category for `modify` fields.**
  Rejected as incomplete: `status` is neither — it is a third case, a field governed
  by a mechanism other than `modify` at all. A related but explicitly unratified
  generalisation (the Engineering Coordinator's own reasoning, not attacked by
  anyone): `id` and `provenance` may belong to the same class. Not ratified here;
  routed to the next relevant ratification as a named open item.

## Ratification chain

- **WP-9 (FP6 candidate) and WP-11 (transition graph):** Fizz, in-channel, 2026-08-29
  (same day as Freeze Point 1).
- **Scope/orthogonality question — ruled:** Engineering Coordinator, event
  `090f5e242e0f57eb40055b5099ccfc55adf66028f6ab6482f655c7e3b4e84e35`, 2026-08-29 —
  "Our two readings diverged, and the deciding citation was in neither," naming
  `OKF-Knowledge-Graph-Specification.md:306` as the deciding citation.
- **WP-13 (re-assembly, scope settled) and WP-14 (final assembly, Freeze Points 6+7 as
  one unit):** Fizz, in-channel, 2026-08-29.
- **Held:** Engineering Coordinator flagged three carried-but-unattacked items in
  WP-14 (`modify`'s evidentiary/presentational split, `ReviewDecision`'s entry point,
  the four dual-axis exclusions) and dispatched WP-15 rather than let them ride into
  signature unattacked, in-channel, 2026-08-29.
- **WP-15 (targeted attack):** Pollen, in-channel, 2026-08-29 — found one real gap
  (`status` reachable through `modified_values` without exclusion), confirmed the
  four exclusions independently, flagged the multi-reviewer question as open but
  non-blocking.
- **`status`-exclusion fix and duplicate-declaration finding:** Fizz accepted the fix;
  Engineering Coordinator sharpened it to name both `Claim.status` and
  `Claim.knowledge_state.status`, in-channel, 2026-08-29.
- **Ratified:** Engineering Coordinator, event
  `0eae51c3f2c98b0ffae59993f8c64d78ac0943ee9f133369f0ded3ed653b2e45`, 2026-08-29T16:18:29Z
  — full ruling, the five items below named explicitly open.
- **Confirmed:** Pollen, event
  `3a6430be79ce41b842428658bb51a101adf5db73ca21884fb878edf201c5898c`, 2026-08-29T16:19:21Z.
- **D7 registered** in `docs/OPEN_QUESTIONS.md` ahead of the decision digest to Ashley
  (PR #21, later corrected for three citation defects across two review rounds — see
  `docs/LESSONS.md`).
- **Signature — the interpretive chain, stated plainly:** Ashley's message, event
  `499a634d66626912c4621492fe56c792541bfdbe401c4f2ddb715787a40ff428`, 2026-09-03T10:01:01Z,
  said "Please consider my sign on other decisions" without naming D7 specifically.
  The Memory & Knowledge Manager asked him directly to confirm this covered D7 before
  any ADR was written, event
  `e516692b6570a77d26d44b6fe92693ebbc3e643496d0abc1aa70d7ebf8b28cea`,
  2026-09-03T10:02:54Z. The Engineering Coordinator then recorded it as covering D7,
  event `7c037f772b9bb01b6b388ca4dea1ddc980b26738b08d721f35e7b0ac539041e1`,
  2026-09-03T10:04:53Z, explicitly offering to unwind before this ADR committed if
  Ashley meant something narrower — and dispatched this ADR to be written after PR #21
  merged, event `3036b8213a0720996d8d91755abaaa65f6fa09b663a9420140099b8d88e3a0c7`,
  2026-09-03T10:10:10Z. No narrower reading was raised in that window. Recorded here so
  the chain is auditable rather than asserted as a plain signature — if Ashley later
  states he meant something narrower, this ADR is what gets unwound, not the channel
  record.

## Consequences

- **Locked.** Changing the seven-value vocabulary, the eight-edge graph, the `origin`
  or `verification.method` closed sets, `ReviewDecision`'s human-only/`accepted`-entry
  rule, or the `modify`/`status` exclusion after this point requires an explicit
  migration, not a routine amendment.
- **Explicitly open, staying open rather than guessed — not blocking this signature:**
  whether `maintainer_approved_workflow` counts as human-originated; **whether
  `ReviewDecision` narrows the envelope for any non-entry state — `disputed`,
  `superseded`, `rejected`, `withdrawn` — is undetermined. Absent a per-type narrowing
  the universal envelope governs; whether `ReviewDecision`'s own specification should
  narrow it belongs to that type's design;** whether multiple reviewers produce one
  `ReviewDecision` node each or share one; `Claim.status` versus
  `Claim.knowledge_state.status` as one field or two (routed to the base-object-
  hierarchy work, build-order item 6); excluding `id`/`provenance` from
  `modified_values` generally (the Engineering Coordinator's own reasoning,
  explicitly not ratified because nobody has attacked it).
- **Freeze Point 4 (provenance model) is unaffected** — it looked coupled in during
  assembly and was found not to be; it ratifies separately, on its own evidence, when
  it assembles.
- **Critical path unblocked.** Before this ADR, the ratified text existed only in the
  channel thread. Honey's build-order item 2 (knowledge-state models, WP-18) can now
  implement from a committed artefact instead of chat messages.
- **This is the second Freeze Point to lock**, and the first to go through more than
  one adversarial round before signature (WP-9 → WP-15) — recorded as the checkpoint
  working under real pressure, not as a defect in the work.
