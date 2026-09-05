# ADR-0016: FP3 Interface — Temporal Field Scope: `valid_time.open_ended` and `observation_time.precision` Excluded, `event_time.uncertainty` Concept Cleared / Shape Open (D34)

- **Status:** Accepted — not a Freeze Point, reversible by ordinary amendment
- **Approver:** Engineering Coordinator, own scoping authority — same basis as ADR-0013 and
  ADR-0014 (event `a420e3f2b381803f2dc9cd53ebbc760920c0e47d19ba8d4ffc9661e16f2d830c`,
  2026-09-05T14:25:23Z): this closes an interface-level gap beneath ADR-0012's already-ratified
  FP3 shape, not one of the 8 Architecture Freeze Points itself. No Ashley signature required.
- **Date:** 2026-09-05
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

The Engineering Coordinator's own declared-scope sweep across all six ratified Freeze Points
(checking each Freeze Point's `Domain-Phase-Mapping.md`-declared scope against what its ADR
actually rules) found FP3's real gap: its declared scope names registry §7 (rank 1) alongside
§5/§6, but ADR-0012 never rules on three fields where §7 (rank 1) and FP3's own primary temporal
document appear to disagree — `event_time.uncertainty`, `observation_time.precision`, and
`valid_time.open_ended`. Two documents disagreeing at the same or adjacent rank needs a §16
(Precedence Rule) ruling; it cannot be left unruled the way a single-document ambiguity might be.
Dispatched as WP-38 child 38a; attacked by Pollen; one correction accepted from Fizz.

## Decision

**1. `valid_time.open_ended` — excluded.** No documented use anywhere in the corpus. Checked
beyond the one worked example that names it: a full sweep of `domains/` and `knowledge/` for
"ongoing," "still active," "open-ended," and "no end date" returns only the field's own schema
declaration — one side of the disagreement restating itself, not independent corroboration.
Nothing in the corpus discusses distinguishing an ongoing state from an unfilled end date.

**2. `observation_time.precision` — excluded, on the honest basis, not the first-drafted one.**
The exclusion's *conclusion* holds: no domain document (`GLOF-Ontology.md`,
`Cryosphere-Ontology.md`, `StateSnapshot-and-Event-Cube-Specification.md`) discusses
observation-time precision at all, so nothing anywhere independently establishes a need for the
field. **The first-drafted argument for it does not hold and is not adopted:** it cited "a worked
example omits this field" as evidence against necessity. Checked directly — that worked example
(`OKF-Knowledge-Graph-Specification.md`'s Universal Frontmatter `temporal:` block) is registry
§7's own schema restated byte-for-byte, confirmed field-for-field identical. Citing its omission
as evidence is citing §7's own absence back at itself; it adds no independent data point, because
the example was never going to show a field the rank-1 registry doesn't have in the first place.
**This ADR states the basis as what the evidence actually supports:** no domain document anywhere
establishes a need for this field — a pure absence claim, matching this project's smaller-set-by-
default pattern, not a claim that a real case was tried and the field failed it.

**3. `event_time.uncertainty` — the concept clears the necessity bar; its drafted scalar shape
does not, and stays open.** `GLOF-Ontology.md`'s "## Temporal" section lists "earliest/latest
possible time" as a real, worked domain requirement — confirmed exact, not paraphrased. The
smaller-set principle's own stated exception fires here: documented necessity for even one field
blocks a blanket exclusion of it, so this field cannot be excluded alongside the other two. Its
current drafted shape (a single scalar) is a separate, unresolved question — not ruled by this
ADR, and not to be inherited as settled.

## Alternatives considered

- **Blanket exclusion of all three fields**, on the smaller-set-by-default principle alone.
  Rejected: `event_time.uncertainty`'s concept has documented necessity
  (`GLOF-Ontology.md`), and the smaller-set principle's own stated exception — erring small is
  wrong when the small set makes a documented requirement unrepresentable — fires directly
  against a blanket exclusion here.
- **Excluding `observation_time.precision` on the "worked example demonstrates non-necessity"
  argument**, as first drafted. Rejected: the cited example is register §7's own schema restated,
  not an independent domain-modeling instance that tried and rejected the field — the argument is
  close to circular and overstates what the evidence supports.
- **Ruling `event_time.uncertainty`'s scalar shape now**, since the concept is settled. Rejected
  as out of scope for this ADR — clearing the necessity bar and ratifying a specific shape are
  different questions, and only the first is settled by what's cited here.

## Consequences

1. **Not a Freeze Point.** ADR-0012 (FP3)'s ratified shape is untouched; this rules an interface
   gap beneath it. Reversible by ordinary amendment.
2. **Closes the three-field §7-vs-primary-document disagreement under §16** — one of exactly two
   things gating build-order item 3 (temporal). The other, the Time Precision vocabulary
   (OKF vs. TEO), is declined rather than closed — see `docs/OPEN_QUESTIONS.md` D33/D34's sibling
   entry, not resolved by this ADR.
3. **`event_time.uncertainty`'s scalar shape stays open** — a separate, future decision. Whoever
   builds against this field must not read this ADR as having ratified a shape for it.
4. Closes `docs/OPEN_QUESTIONS.md` D34 (the structural three-field question, recorded and closed
   in the same session per this project's own acceptance criterion).

## Ratification chain

- WP-38 dispatched (Engineering Coordinator, two children: 38a structural fields, 38b precision
  vocabulary), event `af9ee305e5cca57e2ece605c7d63a9a32b0e5359ddadf800e4ada8aba4939bae`,
  2026-09-05T14:39:50Z.
- WP-38 picked up, Fizz, pinned worktree, event
  `1ceb9de2807e06a17e7de795bb2173c4e003dcc2b607ca0308e75ead4babf6ba`, 2026-09-05T14:38:42Z.
- WP-38 attacked — `open_ended`'s exclusion confirmed clean; `observation_time.precision`'s
  argument found near-circular and its honest weaker basis proposed instead (Pollen), event
  `b34974b0be09b2b1658fd8340fa27a2cba7b0291b0d3b5955024104dec4f4128`, 2026-09-05T14:47:05Z.
- Correction confirmed and accepted, the two schemas verified byte-for-byte identical (Fizz),
  event `77b85884c1e235056e36504660ef300f65c5a8f36577331567dd958ceb856d36`,
  2026-09-05T14:47:37Z.
- Ruling — structural half adopted with Pollen's correction, vocabulary half declined separately
  (Engineering Coordinator), event
  `434f80198a8f7e957ef7460f67a7946cbd49fa33f2ee550dde9dae023a0cacbf`, 2026-09-05T14:49:21Z.
