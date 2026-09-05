# ADR-0011: Freeze Point 4 — Provenance Model (Promotion Rule, Record Shape, Source-Hash Rule)

- **Status:** Accepted — **Architecture Freeze Point 4** of 8 (ratified 2026-09-05
  together with Freeze Points 5 and 3; reversal requires explicit migration, not
  routine amendment)
- **Approver:** Ashley
- **Ruled by:** Engineering Coordinator, channel event
  `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`, 2026-09-05T10:33:53Z
- **Date proposed:** 2026-09-05
- **Date signed:** 2026-09-05 — blanket approval covering this ADR together with
  ADR-0010 and ADR-0012 (D18/D21/D22), not a separate per-ADR assent; see Ratification
  chain.
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

Freeze Point 4 of 8. Subject: when provenance is a standalone node versus an embedded
field, what a promoted `ProvenanceRecord` contains, and how the source-hash
requirement is satisfied. Assembled by Fizz as WP-30 from three children; attacked by
Pollen, who closed the carve-out on whether FP4 implies a relationship predicate and
found the field-count claim underneath the candidate's most confident line was
borrowed from a disputed source.

This morning's framing — "FP4 is Phase 3's gate" — is corrected by this ADR's own
scope. See Consequences.

## Decision

**1. The promotion rule.** Provenance becomes a standalone `ProvenanceRecord` node
when it meets the ontology's own field-vs-node trigger
(`Core-Ontology-Specification.md:54-58`): independent lifecycle, contradiction
potential, review state, and the rest of that document's stated conditions. This is a
general condition already written into a document nobody disputes, not a hand-picked
list assembled for this ADR.

**2. `ProvenanceRecord`'s full shape when promoted**, per the reference structure at
`Evidence-Provenance-and-Trust.md`'s own field definitions.

**3. "Significant" (§9's "every significant derived object MUST support backward
traversal") means a non-empty `parents` list.** Chosen over the alternative that
"significant" is a separately-declared property, on Pollen's evidence: `Source` is
both a promoted registry §3 type and the root of the corpus's own lineage chain, with
nothing upstream by design. The alternative makes the MUST either vacuous or
unsatisfiable for `Source`, and the corpus never states which; treating "significant"
as "has a non-empty `parents` list" excludes `Source` by construction, with no ad-hoc
exception needed for the one case that actually tests the rule.

**4. The source-hash rule is conditional, not a single missing field.** If
`source.node_ids` is populated, the hash requirement (`:41`, "source hash where
available") is satisfied by dereferencing the `Asset`/`DataAsset` the node id points
to. If only `source.uris` is populated, a hash is required on the record itself —
exactly the externally-changing-URL case `:129` already anticipates, where the
upstream asset has no stable node to dereference.

**Explicitly excluded from this signature: the embedded-baseline field count.** The
claim that every `CRICObject` carries a nine-flat-field embedded `provenance:` block
comes entirely from `OKF-Knowledge-Graph-Specification.md`'s Universal Frontmatter —
one side of D10's still-unresolved three-way disagreement about FP2's own subject.
`Evidence-Provenance-and-Trust.md` itself states no embedded shape anywhere. **FP4
does not settle an FP2 question as a side effect of answering its own.** That number
is tracked at `docs/OPEN_QUESTIONS.md` D10, not here.

## Alternatives considered

- **"Significant" as a separately-declared property (Fizz's original Option 1).**
  Rejected — see Decision 3. It needed an ad-hoc exception for `Source`, the one case
  in the corpus that actually tests the rule, and the corpus never states what that
  exception would be. An option that needs an ad-hoc exception for the case that
  tests it is the weaker option, regardless of which sounds more principled on paper.
- **Folding the OKF spec's nine-field embedded-provenance block into this ADR as
  FP4's own baseline**, since it was the most readily available field count.
  Rejected — the field count's actual source is one side of D10's disagreement about
  FP2's subject, not FP4's. Adopting it here would resolve an FP2 question as an
  uncredited side effect of ratifying FP4, the exact hazard this project named twice
  in one round (see `docs/LESSONS.md`'s "absence of prohibition read as presence of
  support" entry).
- **Treating the source-hash rule as a single missing field to add.** Rejected —
  `:129`'s externally-changing-URL scenario shows the requirement is genuinely
  conditional on which of `source.node_ids`/`source.uris` is populated, not a gap
  fixable by adding one field unconditionally.

## Consequences

1. **Phase 3's gate is FP4 *and* FP2, not FP4 alone.** FP4 as ratified unblocks the
   standalone `ProvenanceRecord` and the promotion logic; it does not settle what a
   `DataAsset`'s own embedded `provenance` field contains, because that number was
   excluded above and belongs to FP2 (D10). This corrects the Coordinator's own
   earlier statement to Ashley that FP4 alone gates Phase 3 — the data layer's
   critical path runs through both.
2. Reversal, once signed, requires an explicit migration per this project's Freeze
   Point rule.

## Ratification chain

- WP-30 assembled (Fizz), event `6f4893bc51d94331dcd2ca9b7178c7fc1fe80d1b0b6731b8bd87d52baa1a5f9e`,
  2026-09-05T10:05:35Z.
- WP-30 attacked — carve-out #4 confirmed closed, field-count borrow flagged (Pollen),
  event `a1aeb8bc4aaf7749a0f5fbc2ca031c452a5525ce357ca6e3886189009a3d9907`, 2026-09-05T10:14:07Z.
- Ruling — promotion rule, record shape, "significant" = non-empty `parents`,
  conditional source-hash rule, field-count exclusion, Phase-3-gate correction to
  Ashley (Engineering Coordinator), event
  `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`, 2026-09-05T10:33:53Z.
- Ashley's signature — **blanket approval**, event
  `524472fa44b27d8f732d4033e444891120a5b7f155bef69e4ab21a19738482a3`, 2026-09-05T13:38:43Z:
  *"Please consider all my signatures and all of the decisions as done. Go ahead."*
  This event does not name D21 individually — it covers D18, D21 and D22 together as
  one act, per the Engineering Coordinator's own instruction not to record it as three
  separate per-ADR assents that did not happen. Recorded as what it is.
