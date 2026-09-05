# ADR-0010: Freeze Point 5 — Relationship Representation (Predicate Vocabulary + Direction)

- **Status:** Accepted — **Architecture Freeze Point 5** of 8 (ratified 2026-09-05
  together with Freeze Points 4 and 3; reversal requires explicit migration, not
  routine amendment)
- **Approver:** Ashley
- **Ruled by:** Engineering Coordinator, channel event
  `d95acb598e4ccb772b6eccfa350f65091397cbfcc957598e89aabf263d871140`, 2026-09-05T10:23:29Z
- **Date proposed:** 2026-09-05
- **Date signed:** 2026-09-05 — blanket approval covering this ADR together with
  ADR-0011 and ADR-0012 (D18/D21/D22), not a separate per-ADR assent; see Ratification
  chain.
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

Freeze Point 5 of 8 (per `CRIC-Repository-Dependency-and-Implementation-Sequence.md`).
FP5's subject is two things, not one: (a) which predicates are canonical for typed
relationships between core objects, and (b) how edge direction is represented. Blast
radius is not independently re-derived in this ADR — it is wherever any typed
predicate or relationship edge appears; no phase list is asserted here beyond what
FP6+7's own blast radius already covers (`decisions/0007`), since this candidate has
not had that specific check run against it yet.

`CRIC-Schema-and-Vocabulary-Registry.md` §8 lists predicates but hedges with
"include"/"may include" (no exhaustiveness claim), and separately states "Predicates
MUST be registered and versioned" without specifying a registration mechanism —
confirmed verbatim, zero exceptions, by direct reading (Pollen, WP-31 verification
pass). `OKF-Knowledge-Graph-Specification.md:269` corroborates the hedge ("§8 is the
sole authority... illustrative, not exhaustive") and `:271` supplies the missing
mechanism: "domain repositories may extend predicates through ontology proposals."

Assembled by Fizz as WP-31 from two children; attacked by Pollen, who confirmed the
direction-representation claim holds against three separate attempts to break it, and
confirmed the evidence-field gap (below) is real rather than manufactured.

## Decision

**1. Predicate vocabulary — closed at exactly 35.** The canonical set is precisely
the predicates registry §8 enumerates: 11 core relationship predicates, 23
spatial/domain predicates, 1 structural predicate (35 total, independently counted
twice — Fizz's assembly and Pollen's verification pass agree). Explicitly excluded:
the two deprecated predicates (`connected_to`, `associated_with`) and the rejected
`caused_by`. Future additions go through the extension mechanism already written into
`OKF-Knowledge-Graph-Specification.md:271` ("domain repositories may extend
predicates through ontology proposals") — this ADR transcribes that path, it does not
invent one.

**Explicitly excluded from this signature: the relationship entry schema's `evidence`
field.** `Core-Ontology-Specification.md:440` requires each edge to retain "evidence
and confidence where appropriate"; no field literally named `evidence` exists on the
schema, and `evidence_nodes` is attested corpus-wide only on the Claim schema, never
on Relationships (Pollen). This ADR does not rule on that gap — it stays open, tracked
as `docs/OPEN_QUESTIONS.md` D19 — and nothing in this Decision should be read as
having resolved it by omission.

**2. Direction representation — ratified as specified.** `OKF-Knowledge-Graph-Specification.md:241`'s
mechanism is structural: `out_edges`/`in_edges` traversal indices, generated
independently for every predicate. Named inverse pairs (e.g. `supports`/
`supported_by`, `supersedes`/`superseded_by`) are an authoring convenience layered on
top of that mechanism, not a requirement of it — only 2 of the 11 core predicates have
a registered paired inverse name at all, and nothing in the text requires the other 9
to. `consistent_with`/`inconsistent_with` each derive their own symmetric
`out_edges`/`in_edges` independently, with no cross-pairing between them, so there is
no dedup collision.

## Alternatives considered

- **Option A — leave the predicate set fully open.** Rejected. §8's "MUST be
  registered and versioned" would have no floor at all, and every relationship-bearing
  work package downstream would re-litigate the set from scratch.
- **Option B — close the set at the union including FP4's five ML-flavoured
  illustrative predicates (`generated_by, trained_on, evaluated_on, predicted_by,
  reviewed_by`) as required, on the theory that FP4 and FP5 are coupled here the way
  FP6 and FP7 were.** Rejected. Pollen's direct grep of
  `Evidence-Provenance-and-Trust.md` found zero occurrences of `derived_from` or
  `predicate` anywhere in that document — nothing documented today requires those
  five predicates for FP4's own text, so coupling FP4 into FP5's closure here would
  resolve that coupling by default rather than by a stated ruling. (Whether FP4 itself
  eventually needs some of those five is a separate, still-open question — see FP4's
  own status in `docs/PROJECT_FACTS.md`.)
- **Option C (chosen) — close at exactly the 35 §8 predicates, excluding the two
  deprecated and the one rejected, and name the amendment path already written into
  the OKF spec.** Smaller-set principle: enlarging an enum later is a routine
  amendment; shrinking one is a migration, because by the time a value is minted into
  a record, this project's identifier-immutability rule (ADR-0004) makes it
  permanent. The counterweight was checked explicitly — erring small is the wrong
  call the moment it makes a *documented* requirement unrepresentable — and it does
  not fire against anything found in the corpus as of this ruling.

## Consequences

1. **`affected` is invalid; `impacted` is canonical.** `OKF-Knowledge-Graph-Specification.md:262`
   uses `affected`, registry §8:223 uses `impacted`. Registry is rank 1
   (`CRIC-PRD-MASTER.md` Implementation Authority ordering), so this is a
   propagation — the same shape as ADR-0006's `DataAsset`/`Asset` ruling — not a new
   decision.
2. **This closure makes existing domain content non-conformant on day one, by
   design.** `Cryosphere-Ontology.md` uses `associated_with` at `:116`/`:198` and
   `connected_to` at `:205`/`:388` — confirmed as the only four live uses of either
   deprecated predicate anywhere across all 39 PRD documents (whole-corpus search,
   Engineering Coordinator). Fixing that content is out of this ADR's scope and needs
   an assigned owner — tracked as `docs/OPEN_QUESTIONS.md` D20, not silently implied
   as already handled.
3. **The relationship entry schema's `evidence` field is carved out, not ratified by
   this ADR.** `Core-Ontology-Specification.md:440` requires each edge to retain
   "evidence and confidence where appropriate"; the entry schema (`predicate, target,
   confidence, status, source_nodes, valid_time.{from,to}`) has `confidence` but no
   field literally named `evidence`. Pollen confirmed `evidence_nodes` exists at 7
   locations corpus-wide, all on the Claim schema, zero on Relationships; `evidence.node_ids`
   has zero hits anywhere. This ADR's signature covers the predicate vocabulary and
   direction representation only — the evidence-field gap remains open, tracked as
   `docs/OPEN_QUESTIONS.md` D19. A document carrying an item marked "needs
   ratification" cannot simultaneously be clear for signature on that item, so it is
   excluded rather than waved through.
4. Once signed, reversal requires an explicit migration per this project's Freeze
   Point rule (`docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` §2) — not
   a routine amendment.

## Ratification chain

- WP-31 assembled (Fizz), event `a8480a1e5f677b922c8ddb916fc09541e92074bbba810f34b7e6178ea60f4eaa`,
  2026-09-05T10:07:38Z.
- WP-31 attacked and direction-representation claim confirmed to hold; evidence-field
  gap confirmed real (Pollen), event `3239ebfa7c476d20aa136195baeddcfceaaeae2cf0affb964a4ce5f1d5203fb8`,
  2026-09-05T10:16:54Z.
- Ruling — Option C chosen, both consequences and the evidence-field carve-out stated
  explicitly (Engineering Coordinator), event
  `d95acb598e4ccb772b6eccfa350f65091397cbfcc957598e89aabf263d871140`, 2026-09-05T10:23:29Z.
- Ashley's signature — **blanket approval**, event
  `524472fa44b27d8f732d4033e444891120a5b7f155bef69e4ab21a19738482a3`, 2026-09-05T13:38:43Z:
  *"Please consider all my signatures and all of the decisions as done. Go ahead."*
  This event does not name D18 individually — it covers D18, D21 and D22 together as
  one act, per the Engineering Coordinator's own instruction not to record it as three
  separate per-ADR assents that did not happen. Recorded as what it is.
