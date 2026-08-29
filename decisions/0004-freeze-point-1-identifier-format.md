# ADR-0004: Freeze Point 1 — Object Identifier Format

- **Status:** Accepted — **Architecture Freeze Point** (the first of 8 to lock; reversal
  requires explicit migration, not routine amendment)
- **Approver:** Ashley
- **Date:** 2026-08-29
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

Freeze Point 1 of 8 (per `CRIC-Repository-Dependency-and-Implementation-Sequence.md`).
Blast radius: **all phases** — every node, edge, and predicate reference in every
repository depends on this. Build-order item 1 of 11 in Phase 1.

`CRIC-Schema-and-Vocabulary-Registry.md` §2 gives only the form
`CRIC:<namespace>:<type>:<ulid>`, three examples, and a prohibition on short IDs being
canonical. It does not settle the namespace set, the type/registry relationship, which
ULID specification, case sensitivity, or separator handling. Ratification checkpoint
per `docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` §2: Fizz assembles and
cites the candidate → Pollen does blast-radius verification and tries to break it →
Ashley signs.

## Decision

**Grammar (locked):**

```
CRIC-OBJECT-ID      = "CRIC" ":" namespace ":" type ":" ulid
namespace           = lower-alpha *( lower-alnum )
type                = lower-alpha *( lower-alnum / "_" )
ulid                = 26( crockford-b32-char )
crockford-b32-char  = "0"-"9" / "A"-"H" / "J" / "K" / "M" / "N" / "P"-"T" / "V"-"Z"
```

Regex: `^CRIC:[a-z][a-z0-9]*:[a-z][a-z0-9_]*:[0-9A-HJKMNPQRSTVWXYZ]{26}$`

A validator built from this must reject: `cric:core:claim:...` (lowercase prefix),
`CRIC:Core:claim:...` (uppercase namespace), `CRIC:core:glacial-lake:...` (hyphen where
the vocabulary uses underscore), `CRIC:core:claim:01ARZ3` (short ULID), any ULID
containing `I`/`L`/`O`/`U`, and `CRIC-LAKE-001` (the short form — must not parse at all).

**Six ratified sub-decisions**, per the Engineering Coordinator's ruling:

1. **ULID.** Adopt the community spec at `github.com/ulid/spec`: 26 characters,
   Crockford Base32, uppercase canonical. **UUIDv7 (RFC 9562) was the real alternative**
   and has the stronger open-standards pedigree — rejected because the PRD's own
   placeholder is spelled `<ulid>` and both example sets carry ULID timestamp prefixes.
   This is the one sub-decision with a genuine alternative; Ashley was asked explicitly
   to overturn it at signature if he wanted the IETF standard, and did not (see
   Ratification chain).
2. **Namespace — closed.** The legal set is the registry §12 canonical repository-name
   stems. Extension requires amending §12. Every namespace across all three PRD
   mentions of the identifier form matches a stem, with no counterexample.
3. **Case and comparison.** Lowercase `namespace` and `type`; uppercase `ulid`;
   comparison is byte-exact, no normalisation on read. Normalising would let two
   byte-different strings compare equal — Constitutional Rule 1 makes evidence lineage
   immutable, and an identifier that is "the same" under one comparison and different
   under another corrupts a provenance closure quietly.
4. **Separators.** Segments cannot contain `:`. The character classes above already
   enforce this; there is no escape mechanism and none will be added. A future name
   that needs one is an amendment, not a runtime escape.
5. **Type-registry dependency — in scope for this Freeze Point.** A first,
   intentionally-incomplete Root/domain Type registry ships with Freeze Point 1 to
   validate the `<type>` segment against. The alternative — a validator that accepts any
   string as `<type>` — defeats `Core-Ontology-Specification.md`'s own v0.1 acceptance
   criterion, "unknown types fail validation unless explicitly allowed as experimental."
   **Finding, not actioned by this ADR:** `Domain-Phase-Mapping.md`'s Freeze Point 1 row
   cites only registry §2 as primary spec; it should be corrected to also cite §3. That
   edit is outside this role's write scope (not `docs/DECISION_REGISTER.md`,
   `OPEN_QUESTIONS.md`, `LESSONS.md`, or `PROJECT_FACTS.md`) and is not made here.
6. **The PascalCase→snake_case transform is not authoritative.** The ontology registry
   carries the `id_segment` explicitly per type. A converter still ships, demoted to a
   registration-time suggestion — the stored value is authoritative, not a derivation.

**Accepted alongside the six, not itself an open decision:** Fizz's minting-immutability
guardrail — once an `id_segment` has been used in a minted ID, it is immutable.
Renaming a type's display `name:` later adds an alias; it never rewrites the segment. A
segment changing after objects exist under it would silently break resolution for
everything already minted — the same Constitutional Rule 1 basis as decision 3's
byte-exact comparison requirement.

## Alternatives considered

- **UUIDv7 instead of ULID** for the `ulid` segment (decision 1). Genuinely close: the
  IETF-standardised alternative, arguably the better choice on pure standards grounds
  for a project whose architecture doc says "favour open standards." Rejected on the
  PRD's own placeholder spelling and both example sets' timestamp-prefixed shape, not
  on technical merit — recorded as the one sub-decision a future re-opening should
  start from.
- **Namespace as an open/extensible set**, inferred from whatever strings are already in
  use. Rejected: no PRD text states a rule, and the PRD's own two identifier-form
  mentions with examples don't even agree with each other on which namespaces to show —
  inferring a set from examples that disagree would be unprincipled. The closed set
  anchored to registry §12 is the only citable option.
- **Case-insensitive or normalised comparison.** Rejected on Constitutional Rule 1
  grounds (above) — silent provenance corruption is a worse failure mode than the
  inconvenience of strict comparison.
- **An in-segment escape mechanism** for `:` or other reserved characters. Rejected:
  nothing in the current vocabulary needs one, and adding an escape surface ahead of a
  real need is an amendment risk with no offsetting benefit today.
- **Deriving `<type>` algorithmically from the registry's PascalCase `name:` field**,
  used as the authoritative value at ID-validation time. This was the position all of
  Fizz, Pollen, and Honey converged toward independently — Fizz recommended an
  acronym-aware converter, Pollen implemented and verified one against the whole
  corpus. The convergence itself is what the Coordinator flagged as the signal:
  everyone solved "make the converter correct" and nobody asked whether a converter
  should be the source of truth. Rejected because the failure mode is silent (a wrong
  derivation produces a well-formed ID that simply fails to resolve, undetectable until
  then) and the corpus already contains ambiguous acronym cases (`GLOFEvent`, and two
  more Pollen found while verifying, one of which is the root of the type tree) that no
  fixed algorithm can be proven correct against as the vocabulary grows into the
  hundreds. The converter is retained as a registration-time suggestion — the
  verification work by Fizz and Pollen is not wasted, it just stops being the source of
  truth.

## Ratification chain

- **Dispatched:** Engineering Coordinator, WP-5, event
  `7c645c42b6ade526512b035b00fd6957a8102ae43b8ac6622898b26fdbbeaf7f`, 2026-08-29T14:39:35Z.
- **Assembled and cited:** Fizz, event
  `7d3117eae73d53bf3b489387dc05f066774cbbcecc263d521d2550f9c30513ae`, 2026-08-29T14:42:59Z.
  Amended twice more: incorporating the Coordinator's evidence corrections (ULID-grep
  framing, a third identifier-form citation, the Asset/DataAsset drift's known cause),
  event `c360d888679ee8078ccf1719e94a9b2bfba9032ba2204b888cfb7a6abfe03c7f`; and folding
  in Pollen's decision-6 finding, event
  `2790ba9c9b90fa626e72a1eac4185eb2032743d6fd50e14710fe0cd819557c73`, 2026-08-29T14:46:50Z.
- **Blast-radius verified and attacked:** Pollen, event
  `8d0c3e567dc8f0250cf139e74ab20fab4beef25b62b1c28e90bd4649a4a66628`, 2026-08-29T14:45:58Z
  (every citation checked at source, nothing broke under attack, decision 6 discovered
  independently as a real gap) and mechanical re-verification event
  `0edf726875a44d92a927930e9bc84c14ff04a6a06df9751496a237b59c2141f9`, 2026-08-29T14:47:35Z
  (both PascalCase→snake_case transforms coded and run against the whole corpus, not
  traced by eye).
- **Ruled:** Engineering Coordinator, event
  `c32f57f60ae85ebf4bdbb2c48b3b8750b8b02e03623b89999673f4c728bb02a3`, 2026-08-29T14:49:29Z
  — decisions 1–5 as Fizz recommended; decision 6 against both Fizz's and Pollen's
  converged position, for the reason stated above.
- **Accepted:** Ashley, event
  `1426b5ec5f0bb8bc571322b44e9cbce025fee3d4eb70997ff7677e602316c62a`, 2026-08-29T14:58:22Z
  — in response to the Memory & Knowledge Manager's decision digest (event
  `e48e8ecf2a2eb7136e9372dbf932a2639f5c2aab4ecbb93621cbdafc417376b7`), Ashley asked to
  "go ahead with [the Engineering Coordinator's] prudent decision... as my accepted
  responses," without separately overturning the flagged ULID/UUIDv7 alternative.
- **Recorded as signed:** Engineering Coordinator, event
  `7b26ab2c4447e9f203f165698e87cc4c936c5f61c6d0b67985e9d61ef53fe495`, 2026-08-29T14:59:53Z
  — states explicitly that Ashley "accepted my recommendation over UUIDv7 rather than
  overturning it," recorded that way because it was the one sub-decision with a real
  alternative.

## Consequences

- **Locked.** Changing the identifier grammar, any of the six sub-decisions, or the
  immutability guardrail after this point requires an explicit migration, not a routine
  amendment — per `CRIC-Repository-Dependency-and-Implementation-Sequence.md`'s Freeze
  Point rule.
- **WP-6 (Phase 1, build-order item 1: identifier types)** is dispatched against this
  ADR — `src/cric_core/identifiers/**`, TDD, rejection tests for every malformed example
  Fizz enumerated, `CRIC-LAKE-001` must not parse. Does not implement the type registry
  (decision 5) — that is a separate, later work package.
- **`Domain-Phase-Mapping.md`'s Freeze Point 1 row is now known-incomplete** (cites only
  §2, needs §3 added per decision 5) — flagged here as a finding for whoever owns that
  document; not corrected by this ADR or this role.
- **The PascalCase→snake_case converter code Pollen wrote during verification is not
  wasted** — it ships as the registration-time suggestion tool per decision 6, just not
  as the authoritative resolver.
- **This is the first of 8 Freeze Points to lock** and the first live exercise of the
  three-way ratification checkpoint (assemble → verify/attack → sign). No process defect
  surfaced in the exercise; recorded here as a precedent for the remaining seven.
