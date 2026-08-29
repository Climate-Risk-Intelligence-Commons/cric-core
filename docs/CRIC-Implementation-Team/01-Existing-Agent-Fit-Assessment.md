# Existing Agent Fit Assessment

## 1. The finding, stated plainly

This project's Buzz channel already has four persistent specialist agent identities as
members:

- **Fizz** — Product/Requirements Analyst
- **Honey** — Implementation Engineer
- **Pollen** — Independent Verifier
- **Memory & Knowledge Manager** — decisions/documentation

These are confirmed to be the **same cross-project persistent identities** used on a
separate project (EnergyMatrix) — not new agents invented for CRIC. Fizz has already
demonstrated CRIC-specific work under this identity (the `Domain-Phase-Mapping.md`
companion to this study), which is direct evidence the identity *can* pick up
CRIC-specific context when handed it — but that is different from knowing whether the
identity's standing mandate (the system prompt/instructions that persist across
sessions and projects) already generalizes to a 12-repo OKF/graph/agent-commons build,
or was tuned against EnergyMatrix's shape of work and needs CRIC-specific scoping.

**Hard limitation, stated honestly:** there is no CLI command in this environment to
read an agent's actual configured system-prompt text (no `buzz agents get` or
equivalent read command exists). Everything below is therefore reasoning about
*plausible* fit from the roles' names, their demonstrated outputs, and this project's
own written requirements — not verified fact about what their prompts actually say.
Where this document recommends "confirm with Ashley/the agents themselves," that is a
literal recommendation to close a gap this study cannot close by reading files, not a
rhetorical hedge.

---

## 2. Per-role reasoning

### Fizz — Product/Requirements Analyst

**Plausible fit:** Strong. Fizz's demonstrated output on this exact project
(`Domain-Phase-Mapping.md`) required reading and correctly citing over a dozen PRD
documents, resolving an authority-precedence rule (`CRIC-Schema-and-Vocabulary-Registry.md`
outranks specialised docs per `CRIC-PRD-MASTER.md`), and reasoning about an 8-item
Freeze Point dependency graph — that is exactly the shape of work a "Requirements
Analyst" identity should do well regardless of which project it's pointed at, since
requirements analysis is inherently about reading and reconciling written specs.

**Open question worth confirming:** whether Fizz's standing mandate already includes
"when a specialised doc and a registry/schema doc disagree, the registry wins" as a
default reflex, or whether that reasoning had to be freshly derived (correctly, this
time) from `CRIC-PRD-MASTER.md`'s own text each time. If it's the latter, that's fine —
it means the identity is doing genuine analysis rather than working from a stale
EnergyMatrix-tuned assumption — but it's worth Ashley confirming rather than assuming,
since a subtly wrong default (e.g. "most recently edited doc wins," which might be a
reasonable EnergyMatrix-style heuristic) would be a quiet correctness risk across all
14 phases, not just one.

### Honey — Implementation Engineer

**Plausible fit:** Likely strong on general software engineering competence; the
open question is whether CRIC's specific implementation discipline is already a
reflex or needs explicit scoping. Two concrete points this project asserts that a
generic "Implementation Engineer" mandate might not automatically encode:

1. **The Coding-Agent Work Package Rule** (`00-Overview-and-Superpowers-Codex-Pathway.md`
   §5) treats `files_allowed_to_change` and `prohibited_changes` as hard constraints,
   explicitly to stop an implementer from "opportunistically redesigning CRIC
   architecture while implementing a narrow task." A generic implementation mandate
   optimized for a single-repo project (EnergyMatrix, per the confirmed cross-project
   identity) may default to holistic judgment calls ("I noticed X was suboptimal so I
   also fixed it") that are normal good practice in a single-repo context but are the
   exact failure mode this project's own PRD names as a risk in a 12-repo,
   contract-first build.
2. **Typed-contract discipline.** `Agent-Commons-Architecture.md`'s reference
   implementation is Pydantic AI with typed dependencies and typed outputs throughout;
   the Repository Dependency doc's Phase 1 build order is itself a sequence of typed
   contracts (identifier types, knowledge-state models, temporal models, spatial
   models, provenance, base object hierarchy, relationship model). Whether Honey's
   default coding style already leans this strictly typed/contract-first, or would
   need to be told explicitly to avoid duck-typed or loosely-validated shortcuts, is
   unverified.

**Recommendation, not a finding:** confirm with Ashley/Honey directly whether Honey's
mandate already treats a work package's `files_allowed_to_change` list as a hard
boundary and defaults to `test-driven-development` (see `00-...`) as the implementation
discipline, or whether this needs to be stated explicitly per work package (which the
Work Package Rule already does by construction — so this may be moot in practice even
if Honey's base mandate doesn't say it, provided every task actually uses the YAML
shape).

### Pollen — Independent Verifier

**Plausible fit:** Likely strong on the general discipline of independent
verification; the open question is whether Pollen's verification checklist already
knows CRIC's specific escalation boundary. `knowledge/Ontology-Evolution-and-Governance.md`
defines a **Human Review** gate that is not a generic "get a second opinion" step — it
names five specific triggers:

- alters semantic meaning;
- affects multiple repositories;
- changes safety-relevant concepts;
- creates breaking schema changes;
- deprecates widely used types.

And states elsewhere that changes to a locked Architecture Freeze Point "remain
possible but require explicit migration after the freeze." A generic Independent
Verifier mandate should already know how to check "does this code do what the
acceptance criteria say" — that part is domain-agnostic. What is CRIC-specific is
knowing to **stop and escalate to a human** rather than approve-and-move-on when a
change trips one of those five triggers, or touches a Freeze Point. This is a
plausible scoping gap, not a confirmed one: it is equally possible Pollen's mandate
already generalizes "escalate destructive/broad-blast-radius changes to a human," in
which case CRIC's specific trigger list is just an instance of a rule Pollen already
follows.

**Recommendation, not a finding:** confirm with Ashley/Pollen whether Pollen's
verification pass explicitly checks a work package's stated `acceptance_criteria` field
(from the Work Package Rule) as the primary pass/fail bar, and whether it knows to
route to Ashley (human review) rather than self-approve when a change matches any of
the five Human Review triggers above or touches a Freeze Point.

### Memory & Knowledge Manager — decisions/documentation

**Plausible fit:** Likely strong and closest to domain-agnostic of the four, since
"record decisions and keep documentation current" transfers cleanly across projects
by nature. The one CRIC-specific nuance worth flagging: this project distinguishes
ordinary decisions from **Architecture Freeze Point** decisions, which the PRD says
"require explicit migration" once locked — i.e., they are not just decisions to log,
they are decisions whose reversal has a defined, heavier process. Similarly,
`Ontology-Evolution-and-Governance.md` specifies semantic versioning for the ontology
itself. Whether this role's standing mandate already distinguishes "log this decision"
from "log this decision AND flag that reversing it means a formal migration" is
unverified, but the gap (if any) is narrower here than for Honey or Pollen — it is a
matter of granularity in an already-appropriate function, not a missing capability.

---

## 3. Recommendation

**Reuse these four as the core build-time team rather than creating parallel new
identities for the same functions.** Every open question above is a scoping/tuning
question — "does the existing mandate already know this CRIC-specific detail" — not a
capability gap that would require a different kind of agent. Standing up new
identities to duplicate Requirements/Implementation/Verification/Memory functions
that already exist and have already produced correct CRIC-specific output (Fizz's
`Domain-Phase-Mapping.md`) would be redundant. The genuine gaps, if any, are in
*what new roles cover work these four don't touch at all* — that is the subject of
`02-New-Role-Gap-Analysis.md`, not a case for replacing or duplicating these four.

The concrete next step this document recommends is a short confirmation pass with
Ashley (or with each agent directly, if that's possible) on the four open questions
above, before the first Phase 1 work package is dispatched — not because there is
reason to believe the mandates are wrong, but because the cost of confirming is one
short conversation and the cost of a wrong assumption compounds across 14 phases and
12 repositories.
