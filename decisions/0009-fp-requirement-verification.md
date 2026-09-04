# ADR-0009: Any requirement naming a Freeze Point resolves to exactly one of three verification states

- **Status:** Accepted
- **Approver:** Engineering Coordinator (process/quality-gate ruling, not a Freeze
  Point — no Ashley signature required; same delegated basis as ADR-0008)
- **Date:** 2026-09-04
- **Evidence:** channel event `9a363b593a4f069f1b353025ec3b3d5beb7678b037f8a65fc15e1965f878ddba`
  (2026-09-04T06:57:16Z, defects 1–2 found), event
  `2099ffdf67f1957fde63a4af528c067192d120502f8642830f10bdf3a6a2772f`
  (06:59:41Z, defect 3 found), event
  `3068ea02f93c90422375b18939ec24d3b5125b43f62558cce9cce6a81bc158f1`
  (07:01:09Z, defect 3 amplified), event
  `5e981019100d454f2888e6f6bbb986249ad08fb6c29f23a4d58888e0479f2a98`
  (07:06:56Z, rule proposed and tested against itself, ruling stated).

## Context

A `/gsd-ingest-docs` bootstrap run of `docs/CRIC-PRD-v0.1` (2026-09-04, without the
precedence manifest — `docs/OPEN_QUESTIONS.md` D6 tracks that separately) produced
`.planning/ROADMAP.md` and `.planning/REQUIREMENTS.md`, checkpointed at the local-only
ref `planning/ingest-bootstrap-rescue` @ `74ac966edbd3260fb035b9ec41512fe3de4e598d`.

Reading those artefacts for claims that contradict `CRIC-Schema-and-Vocabulary-Registry.md`
found three defects, full detail in `docs/OPEN_QUESTIONS.md` D6:

1. `ROADMAP.md`'s Phase 1 exit criterion asserts `KnowledgeState.unknown` — not a
   member of the Registry's locked seven-value `knowledge_state` vocabulary (§4).
2. A five-value predicate enum inventing `cites`, present in both `ROADMAP.md` and
   `REQUIREMENTS.md`'s `REL-02` (the roadmap inherited it from the requirements file,
   not the other way round), omitting the ~35 real predicates in §8.
3. `REQUIREMENTS.md`'s `KS-01` defines a `KnowledgeState` enum with **zero overlap**
   against both the Registry's ratified seven values **and** `KnowledgeStateStatus`,
   the enum already shipped as tested code (`src/cric_core/knowledge_state/__init__.py`,
   PR #29, 139 tests) — internally self-contradicting (`KS-04` names the wrong Registry
   section explicitly; `KS-06` requires transition edges whose states aren't `KS-01`'s
   own members), and marked "pending WP-18" for work that had already merged when the
   artefact was generated.

Defect 3 is the most severe of the three, and it was found only because a second
reader (Pollen) opened `REQUIREMENTS.md` — the file an implementer actually builds
from — which the first pass had not.

The Engineering Coordinator proposed a standing check inside the same finding that
motivated it: *"any generated requirement naming a Freeze Point must be verified
against the ADR and against the shipped code."* The Memory & Knowledge Manager
declined to record it as adopted, on the stated ground that a remedy proposed inside
the finding it responds to inherits that finding's credibility without earning its
own — routing it back to the Coordinator to test rather than adopt. This ADR is the
result of that test.

## Decision

**Any requirement that names a Freeze Point must be resolved into exactly one of
three states before it can be treated as build-ready:**

1. **Shipped code exists for that Freeze Point.** The requirement must match the
   code. A mismatch is a **blocker**, not a note — the shipped code is the ratified
   decision in executable form, and a requirement describing something else is
   describing a different, unratified system.
2. **A signed ADR exists, no code yet.** The requirement must match the ADR.
3. **Neither an ADR nor shipped code exists.** The requirement is unratified content
   and **must be marked as such** — it may not be stated as a requirement. It is a
   proposal awaiting a Freeze Point, not a Freeze Point requirement.

The rule is **provenance-independent** — it applies to any requirement naming a
Freeze Point, not only ones confirmed to have been machine-generated. Classifying
whether a hand-edited generated file is "still generated" is a judgement call someone
will get wrong, and the population of requirements naming a Freeze Point is small
enough that the stricter, unconditional rule costs nothing.

## Alternatives considered

- **The Coordinator's original two-branch proposal** — verify against the ADR and the
  shipped code, with no third branch for Freeze Points that have neither. **Rejected
  by test, not by argument.** Applied against `.planning/REQUIREMENTS.md`'s eight
  Freeze-Point blocks: only FP1 (ADR-0004, `identifiers/`) and FP6/FP7 (ADR-0007,
  `knowledge_state/`) have anything to check against. For FP2, FP3, FP4, FP5, and FP8
  — five of eight — the two-branch rule passes by having no subject to examine, which
  is the identical failure this project already ruled against in ADR-0008 (a check
  with nothing to verify manufactures confidence rather than earning it). Defect 3
  (`KS-01`) was catchable only because FP6 happens to be ratified; the identical
  defect shape in an unratified Freeze Point's block — confirmed present, see
  Consequences — is invisible to the two-branch version of this rule.
- **Scoping the rule to artefacts confirmed machine-generated, excluding hand-edited
  ones.** Rejected: the population is small, the judgement call is genuinely hard to
  make reliably, and nothing about *why* a requirement should match its governing
  artefact depends on how the requirement's text was produced.
- **Leaving the check as a one-off finding rather than a standing rule.** Rejected:
  the project now has two Freeze Points in code (FP1, FP6+FP7) and expects more; every
  future generation of planning artefacts can now contradict working software, not
  merely a specification, and the failure mode (internally coherent, wrong source) is
  the kind that survives casual review.

## Consequences

- **Not a Freeze Point.** Reversible by ordinary amendment; no migration required.
- **Immediately falsifiable, and it was tested rather than assumed correct on
  adoption:** verifying branch 3 against `.planning/REQUIREMENTS.md`'s `OKF-01`
  (FP2, unratified) found a real defect the two-branch version would have missed
  entirely — two of six proposed mandatory header fields (`source_type`,
  `content_hash`) are not both simple inventions (`content_hash`'s underlying concept,
  `content_sha256`, is real and doubly attested, nested under `provenance:`, but
  claimed as a differently-named top-level field — a distinct failure mode from
  `source_type`'s outright invention), and ten of the twelve fields the other two
  canonical declarations agree on are omitted. Recorded as its own open item,
  `docs/OPEN_QUESTIONS.md` D10, attacked and confirmed by Pollen the same day — not
  folded into this ADR as settled, since this ADR is about the rule, not that
  specific finding's content.
- **`.planning/`'s generated output does not merge to `main` as-is.** The FP6
  requirements block is unsafe to build from per branch 1; unratified blocks (FP2/3/4/5/8)
  must be re-marked as proposals per branch 3 before anything is built from them.
- **Applies going forward to every future `/gsd-ingest-docs` run and any other
  requirement-generation mechanism this project adopts**, not only this one.
- **A rule derived from a single caught defect is shaped like that defect** — the
  reformulation exists because the original was tested against its own motivating
  case rather than adopted on the strength of having just caught something real.
