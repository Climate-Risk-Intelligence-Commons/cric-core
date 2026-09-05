# ADR-0013: FP4 Interface — `acquisition.retrieved_at` vs. `observation_time.acquisition_time` (D24)

- **Status:** Accepted — not a Freeze Point, reversible by ordinary amendment
- **Approver:** Engineering Coordinator, ruling this explicitly as his own scoping authority
  rather than leaving it inferred (event
  `a420e3f2b381803f2dc9cd53ebbc760920c0e47d19ba8d4ffc9661e16f2d830c`, 2026-09-05T14:25:23Z) —
  this closes a carve-out beneath ADR-0011's already-ratified shape, not one of the 8
  Architecture Freeze Points itself. Ashley's 13:38:43Z blanket approval cannot cover this
  ruling — it was made at 13:57:21Z, after the blanket named nothing on this subject — so the
  basis is the Coordinator's own scoping authority, not an inherited signature. No Ashley
  signature required.
- **Date:** 2026-09-05
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

Carve-out #1 from WP-30's assembly of Freeze Point 4 (provenance model): `ProvenanceRecord`'s
`acquisition.retrieved_at` (`Evidence-Provenance-and-Trust.md:71`, FP4's own primary spec, part
of the shape ADR-0011 already ratified) and registry §7's `observation_time.acquisition_time`
(rank-1) name what reads as the same instant. The Coordinator reserved this pair to himself in
the original data-layer scoping dispatch (event `9d83ccb905ab0f6a2183f127220600ba22cb35a6c3ce8de51fbd153d34363e03`,
08:30:46Z) rather than leaving it in either WP-30 child's scope, then did not rule on it —
found unruled and recorded as `docs/OPEN_QUESTIONS.md` D24 (event
`10fce8a88246fbcf04ec31ff42431c49cb3c7961baedc537e44807488407c14e`, 11:14:10Z). Assembled by
Fizz as WP-36 child 36a; attacked by Pollen.

## Decision

**Option C — distinct concepts, distinct scopes, mandatory cross-reference sentences in both
documents, no required equality.**

**Strongest evidence, corpus-derived:** the OKF spec's own worked `Observation` example
(`OKF-Knowledge-Graph-Specification.md:60-124`) carries `temporal.observation_time.acquisition_time`
**and** a separate embedded `provenance:` block with **no** `acquisition`/`retrieved_at` key at
all — the two fields don't even co-occur on the same node in the ordinary case, because
`acquisition.retrieved_at` exists only inside the standalone `ProvenanceRecord` node type
(created only via the field-vs-node promotion trigger ADR-0011 already ratified). Corroborated
three more ways: the Reference Chain structurally separates "Acquired Asset" from "Observation"
as different lineage stages; `Temporal-and-Epistemic-Ontology.md` keeps "System Time" (ingestion
time) and "Observation Time" (satellite acquisition/sensor timestamp/field survey date) as
explicitly distinct axes; and the corpus's own worked archival example — a 1994 GLOF, reported
2002, ingested by CRIC in 2026, referenced again in 2028 — reasons about exactly this gap as two
necessary, different facts, confirmed by Pollen against the example's full four-fact chain, not
just the 2002-vs-2026 pair first cited.

**Domain-convention corroboration, labelled as such, not corpus text (Pollen):** in
remote-sensing/EO metadata convention, "acquisition time" nested under `observation_time` means
*when an instrument captured a scene* (satellite pass time, sensor timestamp — the sense STAC
and most EO metadata standards use); `ProvenanceRecord.acquisition.retrieved_at` is a different
verb sense — *when CRIC's pipeline fetched/downloaded a file*, an operational ingestion fact.
The same distinction as "when the photo was taken" versus "when you downloaded the photo." This
corroborates Option C; it is not load-bearing on its own, and is recorded here explicitly as
domain convention rather than a corpus citation.

## Alternatives considered

- **Option A — dedupe to one canonical field.** Rejected: destroys the archival-gap distinction
  the corpus explicitly wants preserved — the 1994/2002/2026/2028 chain requires the two
  timestamps to be able to differ, sometimes by decades.
- **Option B — keep both fields independent with no stated relationship.** Rejected as
  under-using what is already known: viable on its own, but leaves every future implementer to
  re-derive the object-class distinction (`Observation` vs. `ProvenanceRecord`) from scratch
  rather than stating it once.
- **Option C (chosen) — distinct concepts, distinct scopes, cross-reference, no required
  equality.** The only option that doesn't require reopening ADR-0011 or registry §7, and
  directly matches the object-class evidence above.

## Consequences

1. **Not a Freeze Point.** Reversible by ordinary amendment; ADR-0011's own ratified shape is
   untouched.
2. **Enforceable invariant, not just documentation:** a validator requiring
   `retrieved_at == acquisition_time` must be rejected — a live sensor feed may make them
   numerically equal by coincidence, which this ruling already permits ("no required equality"),
   but nothing may require it. The 2002-vs-2026 case is the correct shape, not an inconsistency.
3. **`DataAsset.retrieved_at` (flat, `Repository-and-System-Architecture.md:247`) is a third,
   differently-shaped occurrence of the acquisition-time concept** — confirmed by Pollen, out of
   this ADR's scope, flagged explicitly so it is not silently conflated with either field ruled
   on here.
4. Closes `docs/OPEN_QUESTIONS.md` D24.

## Ratification chain

- WP-36 assembled (Fizz), event `8271a7ab02e0419c1664e985a11f1b3a4b62a6f88728a243ced64330016369de`,
  2026-09-05T13:50:42Z.
- WP-36 attacked — Option C confirmed to hold, the EO-convention argument added (Pollen), event
  `adf3046d3bdf4d89469fd9c1f1e3acba61ffbf8f2f1d1c88ea65f408bc184663`, 2026-09-05T13:53:57Z.
- Fizz confirmed no correction needed for D24, agreed the domain-convention argument should be
  labelled as such, event `c7ab1e323b1c34f4ea03a3ee7ad151d89bf6dc8cd4b0d7bc060d1cbad6e21866`,
  2026-09-05T13:54:29Z.
- Ruling — Option C ratified as stated (Engineering Coordinator), event
  `f127c71c53d1c4ba5afd7d0870dc3e73f3175fa043f94f265b71876b5cc1f9af`, 2026-09-05T13:57:21Z.
