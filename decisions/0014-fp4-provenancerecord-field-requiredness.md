# ADR-0014: FP4 Interface — `ProvenanceRecord` Field Requiredness, Three Tiers (D29)

- **Status:** Accepted — not a Freeze Point, reversible by ordinary amendment
- **Approver:** Engineering Coordinator (within his own delegated scoping authority — this
  rules a field-obligation layer beneath ADR-0011's already-ratified shape, not one of the 8
  Architecture Freeze Points itself; no Ashley signature required)
- **Date:** 2026-09-05
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

ADR-0011 (Freeze Point 4) ratified `ProvenanceRecord`'s full field shape but not each field's
obligation level. WP-30 child 30a found that of roughly 26 fields in the reference structure
(`Evidence-Provenance-and-Trust.md:32-51`), **exactly one** — `parents` — carries unambiguous
mandatory language (`:135` and the v0.1 acceptance criterion at `:360`); the rest are genuinely
undetermined, not a search failure — the text simply never states an obligation level for them.
Tracked as `docs/OPEN_QUESTIONS.md` D29. Assembled by Fizz as WP-36 child 36b; attacked by
Pollen, who found one real defect in the assembled tiering.

## Decision

**Three tiers, not two — the third corrected from Fizz's original assembly during attack:**

1. **Required (scoped): `parents`.** The one field with unambiguous mandatory language.
2. **Required-whenever-applicable: `source.*`, `acquisition.*`, `integrity.*` (output hash),
   `licensing.*`.** All four carry the same unqualified "should" as every other item in the
   Requirements list, with no conditional language attached — unlike "source hash where
   available" (`:36`), which does carry one. For `integrity.*` and `licensing.*`, "applicable"
   is **unconditionally true**: every provenance record describes some actual output (a hash is
   always computable in principle), and every record has some licence status, with `unknown`
   as a legitimate, always-available value under the Licence Status vocabulary's own
   conservative-handling rule (`:265-275`, `:271`, `:278` — "Unknown licence status should
   default to conservative handling"). Licence is never *inapplicable*, only sometimes
   *unresolved*.
3. **Conditional on triggering event: `agent.*`, `transformation.*`, `human_reviews`.**
   Genuinely event-gated (`:46`, `:48`) — the block does not apply if no agent ran or no human
   reviewed. This tier held unattacked.

**Cite the contrast, not the absence.** Sixteen items sit under one blanket "A provenance record
should answer:" (`:32-51`), and exactly one — "source hash **where available**" — carries a
conditional qualifier. That is not an absence to read an obligation into; it is the document
demonstrating it knows how to write a conditional and using it exactly once in sixteen. That
contrast is positive evidence about the drafters' intent for the other fifteen, which is why
`integrity.*`/`licensing.*` sit in the required-whenever-applicable tier rather than "optional":
demoting them there would treat "no explicit conditional stated" as if it meant "low priority,"
which is the opposite of what the one genuine conditional in the list implies for everything
else.

**Falsification stated explicitly, so the lock carries a documented hole rather than an
undocumented one:** if a legitimate provenance record is found whose output genuinely cannot be
hashed, `integrity.content_sha256` moves from required-whenever-applicable to conditional. The
asymmetry between licence and output hash is named, not smoothed over: licence has a documented
escape value (`unknown`, with its own conservative-handling rule), so "always required" is
always satisfiable; `content_sha256` rests on "a hash is always computable in principle," which
is an inference nobody has tested against a real counter-example.

## Alternatives considered

- **Option A — global-optional/permissive.** Rejected: too thin — would let a record validate
  with only `id`/`type`/`object_id`/`parents`, defeating the document's own stated purpose.
- **Option B — global-required/strict.** Rejected: manufactures a "must" the text never states
  for roughly 20 fields, and is impractical — it would force `transformation.*`/`agent.*` on
  records where nothing was transformed and no agent was involved.
- **Option C (chosen, as corrected) — tier by field-group semantics.** Fizz's original assembly
  placed `integrity.*`/`licensing.*` in an "optional" tier alongside the genuinely
  event-conditional fields. Pollen's attack found this backward: event-conditional
  ("doesn't apply if the event didn't happen") and universally-applicable-but-unqualified
  ("applies to every record, nothing says otherwise") are different shapes, and
  `integrity.*`/`licensing.*` are the second shape, not the first — they belong with
  `source.*`/`acquisition.*`. Fizz confirmed the correction directly against the text before
  this ruling. The `agent.*`/`transformation.*`/`human_reviews` tier held unattacked throughout.

## Consequences

1. **Not a Freeze Point.** ADR-0011 already ratified FP4's field shape; this ADR rules the
   obligation layer beneath it. Reversible by ordinary amendment.
2. The falsification condition above is part of this ruling, not a footnote — if it fires,
   `content_sha256`'s tier changes without reopening the rest of this ADR.
3. **A related, unruled finding surfaced during assembly, not adopted here:** WP-36 child 36b
   found that the Provenance Requirements list's "epistemic status" item (`:51`, carve-out #3 /
   `docs/OPEN_QUESTIONS.md` D26 — no corresponding field anywhere in `ProvenanceRecord`'s YAML
   skeleton) may be answered by the target object's own `epistemic_status` tag, reachable via
   `object_id`, rather than needing a dedicated `ProvenanceRecord` field at all. Stated
   explicitly by its own finder as "a plausible cross-doc reading, not a ruling." Not adopted as
   part of this ADR; D26 stays open, this reading recorded there as candidate content for
   whoever rules on it.
4. Closes `docs/OPEN_QUESTIONS.md` D29.

## Ratification chain

- WP-36 assembled (Fizz), event `8271a7ab02e0419c1664e985a11f1b3a4b62a6f88728a243ced64330016369de`,
  2026-09-05T13:50:42Z.
- WP-36 attacked — the `integrity.*`/`licensing.*` tier placement found backward and corrected
  (Pollen), event `adf3046d3bdf4d89469fd9c1f1e3acba61ffbf8f2f1d1c88ea65f408bc184663`,
  2026-09-05T13:53:57Z.
- Fizz confirmed the tier correction against the text directly, net effect stated as three
  tiers, event `c7ab1e323b1c34f4ea03a3ee7ad151d89bf6dc8cd4b0d7bc060d1cbad6e21866`,
  2026-09-05T13:54:29Z.
- Ruling — three tiers as corrected, falsification stated (Engineering Coordinator), event
  `f127c71c53d1c4ba5afd7d0870dc3e73f3175fa043f94f265b71876b5cc1f9af`, 2026-09-05T14:04:04Z.
