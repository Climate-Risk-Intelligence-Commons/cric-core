# ADR-0006: `DataAsset` is the canonical ontology type; `Asset` is prose only

- **Status:** Accepted — **propagation of an existing registry decision, not an
  amendment**
- **Approver:** Engineering Coordinator
- **Date:** 2026-08-29
- **Freeze Point?** No (not itself a Freeze Point) — but see Consequences: it is a
  **mandatory input to Freeze Point 2** (Base OKF frontmatter).
- **Evidence:** Engineering Coordinator's ruling, channel CRIC-Dev
  (`17bd72a0-4d90-4e0b-b102-f9163f0cfd4b`), event
  `1724653e311b31ade3a7a32d3a96281329e3e38e773fad6243eeb1c98812bc4b`,
  2026-08-29T15:42:00Z. Underlying finding first surfaced by Fizz during WP-8
  (`docs/CRIC-Implementation-Team/Domain-Phase-Mapping.md` citation work) and
  independently confirmed by the Engineering Coordinator during WP-5 (ADR-0004).

## Context

`CRIC-Schema-and-Vocabulary-Registry.md` §3, "Asset Resolution" (line 86), is
normative:

> Use **`DataAsset`** as the canonical ontology type. `Asset` may remain a generic
> prose term but SHOULD NOT be used as a competing schema type.

Two specialised documents never received that canonicalisation:

- `knowledge/Core-Ontology-Specification.md:78` lists `Asset` in the Root Object Type
  tree and gives it a full `# Asset` section (line 291) with core attributes — a
  competing schema type, exactly what §3 says not to have.
- `knowledge/OKF-Knowledge-Graph-Specification.md:316` still lists `Asset` (not
  `DataAsset`) in its Node Categories.

This is not two documents disagreeing by accident. `CRIC-Integration-Audit.md:11`
records the canonicalisation as a deliberate, completed act: *"Canonicalised
`DataAsset` as the schema type while retaining 'asset' as generic prose."* The
registry was updated; the two downstream documents were not. Per
`CRIC-PRD-MASTER.md`'s Implementation Authority ordering, the registry (rank 2)
outranks both specialised documents regardless.

## Decision

**`DataAsset` is the canonical ontology/schema type.** `Asset` may be used as a
generic prose term but must not appear as a competing schema type, a Root Object
Type, or a Node Category. This ADR records that decision durably; it does not make
a new one — registry §3 already decided this. What was missing was propagation, not
judgment.

## Why this is propagation, not amendment (and why that matters for who signs)

The Engineering Coordinator evaluated this exactly as it evaluated the earlier
org-layout casing question: is the registry's language binding, and does anything
here require *deciding* new PRD content? No — §3 is already normative, and both
drifted documents are simply behind it. Recognising an existing rank-2 decision
requires no material architecture change and therefore no Ashley signature, the
same reasoning `decisions/0001` applied to the `decisions/`-vs-`docs/adr/` filing
choice. If, during Freeze Point 2 assembly, it turns out the drifted documents must
actually be *edited* (not merely annotated) to resolve this cleanly, that crosses
into amending the PRD — at that point it goes to Ashley. Not yet reached.

## Alternatives considered

- **Treat `Asset` and `DataAsset` as two valid, coexisting schema types** (i.e., defer
  to whichever specialised document a reader happens to open). Rejected: registry §3
  is explicit that `Asset` "SHOULD NOT be used as a competing schema type" — this
  isn't ambiguous language inviting a permissive reading.
- **Wait and resolve this only when Freeze Point 2 forces the question.** Rejected:
  the Engineering Coordinator's stated reason is what elevates this above "note it
  and move on" — Freeze Point 1 already ratified that a minted `id_segment` is
  immutable (`decisions/0004`, decision 3 and the immutability guardrail). Frontmatter
  `type:` values feed the identifier `<type>` segment. If a Freeze Point 2 work
  package or any earlier implementation mints an ID against the drifted `Asset` type
  before this is on record, that ID is permanent and the fix becomes a migration, not
  an edit. Recording the ruling now, ahead of Freeze Point 2's assembly, is what
  keeps this cheap.
- **Amend `Core-Ontology-Specification.md` and `OKF-Knowledge-Graph-Specification.md`
  directly, now, as this ADR's own action.** Rejected for two reasons: (1) it is
  outside this role's write scope (`docs/`, `decisions/` only — not PRD content under
  `docs/CRIC-PRD-v0.1/`); (2) more fundamentally, per the ruling above, whether those
  documents get *edited* versus *annotated alongside* is itself a decision that
  belongs to whoever assembles Freeze Point 2, informed by whether the drift is
  contained enough to annotate or pervasive enough to require a source edit
  (Ashley's signature, if so).

## Consequences

- **Mandatory input to Freeze Point 2 (Base OKF frontmatter), not a standalone patch.**
  Registry §3 governs the frontmatter `type:` vocabulary; Node Categories in
  `OKF-Knowledge-Graph-Specification.md` *is* that vocabulary. Freeze Point 2's own
  ADR — whenever it is assembled — must state the `DataAsset` canonicalisation
  **self-containedly**, not merely cite this ADR or registry §3 by reference: it has
  to survive the deletion test (per `docs/PROJECT_FACTS.md`'s citation-consolidation
  convention) on its own, since a reader deciding the frontmatter `type:` vocabulary
  cannot be required to also open this ADR to get the `Asset`/`DataAsset` rule right.
- **Trigger for action, a performed event, not a date:** whoever assembles Freeze
  Point 2 (registry §4/specialised-doc candidate work, analogous to Fizz's WP-5/WP-9
  role) reads this ADR before finalising that candidate, and incorporates the
  `DataAsset` ruling into the FP2 ADR's own text. Nothing to chase in
  `docs/OPEN_QUESTIONS.md` in the meantime — there is no absence to wait on, only an
  assembly step that hasn't started yet.
- **Escalation condition, stated now rather than discovered later:** if Freeze Point
  2 assembly concludes that `Core-Ontology-Specification.md` and/or
  `OKF-Knowledge-Graph-Specification.md` must be *edited* (not merely annotated
  alongside) to resolve the drift cleanly, that is a PRD amendment and requires
  Ashley's signature — this ADR does not pre-authorise it.
- **Second drift instance on record.** `OKF-Knowledge-Graph-Specification.md:316`
  joins `Core-Ontology-Specification.md` as a second file carrying the same stale
  `Asset` reference — both traced to the same un-propagated registry canonicalisation
  (`CRIC-Integration-Audit.md:11`), not two independent errors.
- **Does not touch `docs/OPEN_QUESTIONS.md` or `docs/PROJECT_FACTS.md`** — out of
  scope for WP-10 (`files_allowed_to_change: [decisions/, docs/DECISION_REGISTER.md]`).
