# ADR-0012: Freeze Point 3 — Temporal Model (Negative-Value Exclusion, Scope Precedence)

- **Status:** Proposed — Architecture Freeze Point candidate (third of 8), **ruled by
  the Engineering Coordinator, not yet signed by Ashley.** Becomes
  `Accepted — Architecture Freeze Point (third of 8 to lock; reversal requires
  explicit migration, not routine amendment)` only after Ashley signs, matching
  ADR-0004/ADR-0007's exact phrasing (see `decisions/0008`'s CI-parsing note).
- **Approver:** Ashley (signature pending)
- **Ruled by:** Engineering Coordinator, channel event
  `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`, 2026-09-05T10:33:53Z
- **Date proposed:** 2026-09-05
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

Freeze Point 3 of 8. Subject includes where `false`/`absent`/`not detected` sit
relative to registry §5 (Epistemic Status) and §6 (Negative-Case Vocabulary), and
which document's negative-case scope governs when two disagree. Assembled by Fizz as
WP-29 from three children; attacked by Pollen, who found the routing citation
(Domain-Phase-Mapping.md row 3 → §5/§6) resolves textually but its own supporting
claim — that §6 "overlaps at coarser granularity" the ontology's "Unknown Versus
Negative" list — does not hold against the text it describes.

## Decision

**Ratified — the exclusion.** `false`, `absent`, and `not detected` are **not**
members of registry §5 or §6. Both Fizz and Pollen independently swept the whole
corpus for controlled-vocabulary use of any of the three and found none anywhere;
`:365`'s explicit prohibition on collapsing `unknown` into `false` is positive
evidence the two concepts must stay distinct, not merely an absence of a contrary
rule. FP3's closure rejects all three from both vocabularies.

**Explicitly declined, not ratified, and stated here so nobody applies it as if it
were: the placement of those three tokens on `Observation.value`.** That they belong
there is, in Pollen's finding and Fizz's own acceptance of it, unconstrained by
omission rather than affirmatively supported — the corpus states no type for
`Observation.value` at all, and `unit` sitting beside it in the schema reads at least
as naturally as numeric. **A Freeze Point may not rest on "nothing forbids it."**
Where these tokens actually live is `Observation`'s own specification's business, not
FP3's, and it stays open — tracked at `docs/OPEN_QUESTIONS.md` D23.

**Ratified — scope precedence.** Registry §6's wider scope governs over
`Training-Data-and-Benchmark-Specification.md`'s narrower restatement. §6's
MUST-NOT covers "negative training labels" unqualified — which includes
`probable_negative`, not only `confirmed_negative`. Training-Data's own restatement
narrows this to "confirmed negatives," which is a specialised document under registry
§16 and loses to §6 on precedence. FP3's candidate states the §6 scope, not the
narrower one.

**Explicitly excluded from this signature: "no known evidence" as a new value on
`Evidence` or `Claim`.** This is invention, not transcription — `Evidence` has no
extension point for it today, and treating it as already-covered would be exactly the
"absence of prohibition read as presence of support" pattern this round produced
twice elsewhere (see `docs/LESSONS.md`). It becomes an open item, tracked at
`docs/OPEN_QUESTIONS.md` D23 alongside the `Observation.value` placement question,
since both concern the same undefined specification.

**D13 (the intra-registry `unknown`/`disputed` collision) is carried as established
precedent, not re-attacked here.** The field path determines which vocabulary governs
a bare token — the same ruling that already settled `epistemic.status` versus
`knowledge_state.status` for the identical shape of problem. D13 stays a recorded
question in `docs/OPEN_QUESTIONS.md`, not a blocker on this signature.

## Alternatives considered

- **Adopting Fizz's Option 1 whole** (both the negative-value exclusion and the
  `Observation.value` placement together). Rejected as a package — the two halves are
  not equally supported. The exclusion is a well-supported negative (whole-corpus
  sweep, twice, zero hits, plus `:365`'s positive prohibition). The placement is an
  inference from an untyped field having no stated alternative, which is a different
  and weaker kind of evidence. Splitting them lets FP3 close on the half that holds.
- **Treating "nothing says otherwise" as sufficient to place the three tokens on
  `Observation.value`.** Rejected on the same reasoning as FP4's field-count
  exclusion in `decisions/0011` — the same pattern, found twice in one round.
- **Adopting Training-Data's narrower "confirmed negatives" restatement as FP3's own
  scope**, since it is the more specific document. Rejected — registry §16's
  precedence rule runs the other way for a specialised document narrowing a rank-1
  rule; §6's unqualified scope governs.

## Consequences

1. FP3's candidate is closed on the negative-value exclusion and the scope-precedence
   ruling; it is silent on where those tokens are typed, which remains
   `Observation`'s own specification's business (D23).
2. Reversal, once signed, requires an explicit migration per this project's Freeze
   Point rule.

## Ratification chain

- WP-29 assembled (Fizz), event `6739900881d9c9fe1956f7217d42dd6354bfc8df700edb69f3fe5696b74dd485`,
  2026-09-05T10:06:50Z.
- WP-29 attacked — routing citation's supporting claim found not to hold, intra-document
  `unknown` collision found (Pollen), event
  `e5ea70ce178de59d29f2e4255e7c25184611bbe7fd6e833924cb2b6fd3c71e4b`, 2026-09-05T10:16:00Z.
- Fizz's confirmation and retraction of the citation-label-vs-content gap, event
  `9e501d8c5a775e6aa6135a6a1d1c83a12fe9a911c54cb9cd3dd038a28a8637dc`, 2026-09-05T10:17:15Z.
- Ruling — exclusion ratified, placement declined, scope precedence ratified,
  "no known evidence" excluded, D13 carried as precedent (Engineering Coordinator),
  event `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`,
  2026-09-05T10:33:53Z.
- Ashley's signature: **pending** — not yet requested-and-received as of this ADR's
  creation. Do not treat this ADR as ratified until this line is updated with his
  acceptance event.
