# New Role Gap Analysis

## Restraint principle

Stated up front because it governs every conclusion below: **a role only earns
creation when a specific named phase or task needs it and the four existing
generalists (Fizz, Honey, Pollen, Memory & Knowledge Manager) provably don't cover
it.** The default answer to "should we add a role" is no. This document is not trying
to produce a complete-looking org chart — it is trying to name the smallest set of
exceptions to "the four generalists handle everything," and to reframe as much as
possible as a temporary or rotating responsibility of an existing role rather than a
new permanent identity. Where a candidate role's work can plausibly be absorbed by
an existing generalist with confirmation rather than a new identity, this document
says so and stops there.

---

## 1. Phase-by-phase pass

Walking all 14 phases (plus Phase 0) against the four generalists' functions
(requirements/domain analysis, implementation, verification, decisions/documentation),
most phases show no gap: Fizz can supply the authoritative-PRD-sections framing (as
already demonstrated in `Domain-Phase-Mapping.md`), Honey can implement against a
Work Package Rule YAML, Pollen can verify against its `acceptance_criteria`, and the
Memory & Knowledge Manager can record the outcome and any decisions made. This is true
without further scrutiny for Phases 2, 3, 5, 6, 9, 10, 11, 12, and 13 — none of them
introduce a function the four don't already have a plausible claim to.

Three points in the sequence warranted closer scrutiny because they involve a kind of
judgment or permission that doesn't obviously belong to any of the four's core
function:

1. **Ratifying the 8 Architecture Freeze Points** (produced in Phase 1, gating
   Phases 2 through 13 per `Domain-Phase-Mapping.md`'s Freeze Point table).
2. **Phase 0** (repo/CI/branch-protection/licence/coordinated-release-metadata setup)
   and **Phase 14** (coordinated multi-repo release manifest, compatibility matrix,
   reproducibility instructions) — the two phases that are explicitly about
   cross-repository infrastructure and release process rather than implementing a
   single repository's contracts.
3. **Phase 4's** cryosphere/GLOF domain schema work, where the PRD itself warns about
   "domain-specific redefinition of a core type instead of extension" as the named
   risk.

Each is evaluated on its merits below. Two are rejected as permanent roles and
reframed as existing-role checkpoints or escalation paths. One is accepted, but scoped
as a temporary/rotating responsibility rather than a fifth standing identity.

---

## 2. Candidate: Solution-Architect-style role for ratifying the 8 Architecture Freeze Points

**Verdict: Reject as a new role. Reframe as a joint checkpoint of existing roles.**

The 8 Freeze Points (ID format, base OKF frontmatter, temporal model, provenance
model, relationship representation, knowledge-state vocabulary, review decision
schema, agent manifest schema) are all produced in Phase 1 and, per the Repository
Dependency doc, "remain possible [to change] but require explicit migration after the
freeze." That makes ratifying them a genuinely high-stakes, cross-cutting decision —
but decomposing what "ratify" actually requires shows it is composed entirely of
functions the four generalists already own:

- Assembling the candidate freeze-point specification with correct citations to its
  authoritative PRD sections, and checking it doesn't contradict a higher-precedence
  document (`CRIC-Schema-and-Vocabulary-Registry.md` outranks specialised docs per
  `CRIC-PRD-MASTER.md`) — this is Fizz's existing function, exercised at one
  particularly consequential moment rather than a new function.
- Independently verifying the candidate against downstream impact — `Domain-Phase-Mapping.md`'s
  Freeze Point table already shows exactly which phases (e.g. Freeze Point 3, the
  temporal model, gates Phases 4, 5, 6, 9, 10) would be affected by getting this
  wrong — this is a blast-radius verification, which is Pollen's existing function.
- Final human sign-off given the "explicit migration" cost of reversing a bad freeze —
  this is Ashley's role, not any agent's.

No new capability is missing; what's missing (if anything) is a defined *moment* —
a named checkpoint at Phase 1's exit (and again, rarely, whenever a migration to an
already-locked Freeze Point is proposed) where Fizz and Pollen are explicitly
dispatched together against the freeze-point candidate before Ashley signs off. That
checkpoint should be written into the Phase 1 exit-criterion review (see
`00-Overview-and-Superpowers-Codex-Pathway.md` §2's row on `requesting-code-review` /
`receiving-code-review`), not staffed by a new identity.

---

## 3. Candidate: DevOps/Release Engineer for Phase 0 and Phase 14

**Verdict: Accept — as a temporary/rotating responsibility, not a permanent fifth
identity.**

Phase 0 ("Create repositories, branch protection, licences, contribution templates,
CI skeletons and coordinated release metadata... Exit criterion: repositories exist
and `cric-core` can publish a versioned Python package") and Phase 14 ("Required
evidence: tests; release manifest; compatibility matrix; reference Event Cube;
reference benchmark; baseline model; agent/HITL demonstration; workbench;
reproducibility instructions") are qualitatively different from every other phase in
the sequence: every other phase implements a repository's contracts against a spec.
These two phases coordinate *infrastructure and process across all of the
repositories at once* — branch protection and CI conventions that every later repo
must inherit consistently, and a release manifest/compatibility matrix that has to be
true of ten-plus independently-buildable repositories simultaneously.

This could plausibly already sit inside Honey's "Implementation Engineer" mandate —
setting up CI and branch protection is still "build to spec," just applied to
repository infrastructure instead of product code, and a release manifest is still a
deliverable with acceptance criteria Pollen can verify. The reason this document
accepts it as a genuine (if narrow) gap rather than folding it silently into Honey's
existing mandate: the confirmed cross-project identity finding means Honey's mandate
was tuned against EnergyMatrix, which — as far as this study can determine — is a
single-repo project. Coordinating CI conventions, branch protection, and a
compatibility matrix *consistently across ten-plus independently-versioned
repositories at once* is a different surface area than implementing features inside
one repository, even though both are recognizably "engineering." That is enough of a
plausible skill-surface mismatch to name explicitly rather than assume away — but not
enough to justify a standing fifth identity that exists for all 14 phases, when it is
only load-bearing at two of them.

### Spec: Build & Release Engineer (temporary/rotating responsibility)

- **Not a permanent identity.** This is a responsibility that activates at named
  phases, most plausibly carried by Honey under an explicitly widened brief for just
  those phases — confirm with Ashley whether Honey should simply carry this brief
  directly, before standing up any separate instruction set. The spec below is
  written so it can be handed to Honey-scoped-for-this-purpose or to a distinct
  identity, whichever Ashley prefers.
- **Activation window:** Phase 0 (full activation), a light standing custodial tail
  through Phases 1–13 (apply Phase 0's CI/branch-protection template consistently as
  each new repository comes online — no new judgment calls, just consistent
  application and drift detection), and full reactivation at Phase 14.
- **Day-to-day mandate:**
  - At Phase 0: stand up every repository's scaffolding — licence, contribution
    templates, CODEOWNERS/branch protection, a CI skeleton (lint/test/build), and a
    coordinated version/release metadata scheme — to the point `cric-core` can
    publish a versioned Python package (Phase 0's exit criterion, verbatim).
  - Through Phases 1–13: apply the same CI/branch-protection template to each newly
    created repository as it comes online; flag any repo whose CI has drifted from
    the shared template rather than silently letting conventions diverge.
  - At Phase 14: assemble the coordinated v0.1 release manifest and compatibility
    matrix across all repositories, verify each of the nine items in the Repository
    Dependency doc's "Required evidence" list, and produce reproducibility
    instructions an external researcher can follow end-to-end.
- **Inputs:** Phase 0 and Phase 14 sections of
  `CRIC-Repository-Dependency-and-Implementation-Sequence.md`; each repository's own
  CI status; each work package's `acceptance_criteria` and `tests_required` fields
  (to know what "passing" means per repository); `engineering/Testing-and-Quality-Assurance.md`'s
  quality gates; `engineering/Deployment-Versioning-and-Releases.md`.
- **Outputs:** repository scaffolding and CI configuration (Phase 0); a release
  manifest and compatibility matrix document plus reproducibility instructions
  (Phase 14).
- **Permissions:** repository admin/settings access (branch protection rules,
  CODEOWNERS) across all CRIC repositories — a permission level none of the other
  four roles need by default — plus write access to CI configuration files and
  read-only access to every repository's test results for the Phase 14 compatibility
  matrix. Should **not** have merge rights into product-code branches; that stays
  with Honey and the normal review gates.
- **Handoff points:** receives the repository list and dependency order from Fizz's
  domain-mapping function (already produced in `Domain-Phase-Mapping.md`); Honey owns
  all product-code implementation once Phase 0 scaffolding exists, with no overlap;
  Pollen verifies each repository's CI actually enforces the Coding-Agent Work
  Package Rule's `tests_required`/`acceptance_criteria` fields before the Phase 14
  manifest is finalized; the Memory & Knowledge Manager records the release manifest
  and compatibility matrix as the permanent record once Phase 14 closes.
- **Restraint note, restated:** confirm with Ashley whether Honey's existing mandate
  already covers this before treating it as a separate instruction set at all — the
  case for a distinct brief rests on an unverified assumption (that Honey's tuning is
  single-repo-shaped), not a confirmed one.

---

## 4. Candidate: Domain/Ontology Specialist for Phase 4's cryosphere/GLOF science

**Verdict: Reject as a standing role for the v0.1 build. Reframe as an escalation
path, not a role.**

Phase 4 requires schema and controlled-vocabulary work for Glacier, GlacialLake,
Moraine/MoraineDam, cryosphere observations, GLOFEvent, trigger/failure mechanisms,
StateSnapshot extensions, and Event Cube manifests — and `Domain-Phase-Mapping.md`
flags this phase's specific risk as "domain-specific redefinition of a core type
instead of extension," testable directly against
`knowledge/Core-Ontology-Specification.md`'s own design rule. This sounds, on its
face, like it needs cryosphere/glaciology domain expertise distinct from software
requirements analysis.

The reason this document rejects a standing role rather than accepting the gap: the
domain science for v0.1 already appears to be captured as written specification —
`domains/Cryosphere-Ontology.md` and `domains/GLOF-Ontology.md` exist as the
authoritative PRD sections for this phase per `Domain-Phase-Mapping.md`'s citation of
them. If those documents already fully specify the schema (which this study did not
verify by reading them directly — see caveat below), then Phase 4's build-time job is
schema *implementation* against a written spec plus the explicit
extend-don't-redefine constraint, which sits inside Fizz's requirements-interpretation
function and Honey's implementation function without requiring new scientific
judgment.

**Caveat on this conclusion:** this study did not deep-read
`domains/Cryosphere-Ontology.md` or `domains/GLOF-Ontology.md` — that was out of scope
for this pass, which focused on the Repository Dependency doc and the two
product-vs-build-time documents. If whoever owns those two domain files confirms open
scientific judgment calls remain unresolved in the written text (for example, an
ambiguous trigger-mechanism taxonomy that the PRD doesn't settle), the correct
response is a **one-off named subject-matter reviewer** consulted for that specific
open question — not a standing identity carrying cryosphere science expertise across
every future phase. This keeps the same restraint logic as the other two candidates:
the gap, if it exists at all, is narrow and occasional, not a permanent function.

---

## 5. Summary

| Candidate | Verdict | Disposition |
|---|---|---|
| Freeze Point ratification | Reject as new role | Joint Fizz (assemble + cite) + Pollen (blast-radius verify) + Ashley (sign-off) checkpoint at Phase 1 exit and any later migration proposal |
| DevOps/Release Engineer (Phase 0 + Phase 14) | **Accept**, narrowly | Temporary/rotating "Build & Release Engineer" brief, most plausibly carried by Honey under a widened scope for just these two phases — confirm with Ashley before treating as a separate instruction set |
| Domain/Ontology Specialist (Phase 4) | Reject as standing role | Escalation-only: a named one-off subject-matter reviewer if and only if Phase 4 work surfaces an open scientific judgment call the written domain PRD docs don't resolve |

One genuine gap surfaces from this pass, and it is scoped as narrowly as the evidence
supports: two bookend phases needing a release-engineering brief that may or may not
already live inside Honey's mandate. Everything else in the 14-phase sequence is
covered by Fizz, Honey, Pollen, and the Memory & Knowledge Manager, either directly or
via the checkpoint/escalation patterns above.
