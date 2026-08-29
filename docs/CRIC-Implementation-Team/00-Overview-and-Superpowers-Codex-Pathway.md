# CRIC Build-Time Implementation Team: Overview and the Superpowers/Codex Pathway

## 0. What this document is not

`docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md` and
`docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md` already fully specify a set of
**23 "product" agents** (Research Scout, Source Qualification, Licence, Acquisition,
Metadata, Evidence Extraction, Entity Resolution, Temporal/Spatial Reconciliation,
Contradiction, Data Quality, Ontology Watch/Synthesis/Critic, Provenance Auditor,
StateSnapshot Builder, Event Reconstruction, Training Curator, Scientific Critic, Model
Evaluation, Human Review Router, Review Resumption, Repository Maintenance). Per
`Agent-Team-Specifications.md`'s own Purpose section, these are "the initial reusable
agent catalogue" — Pydantic AI agents that **run inside the deployed CRIC platform**
doing science and knowledge work at runtime (evidence extraction, ontology evolution,
scientific review, model curation). `Agent-Commons-Architecture.md` frames the
infrastructure those 23 agents share ("Agent Definition + Instructions + Dependency
Schema + Toolsets + Datasets + Workspace + Model Configuration + Structured Output
Schema + Permissions + Evaluation Suite") — again, runtime infrastructure for the
product.

This document is about a completely different team: the **build-time engineering
team** that writes the twelve repositories those 23 product agents (and everything
else in CRIC) will eventually run in. It answers "who codes CRIC, using what process,"
not "what does CRIC do once built." The only point where the two systems touch is
Phase 8 (`cric-agents`): a build-time specialist *implements* the product-agent
infrastructure described in `Agent-Commons-Architecture.md`; that specialist is not
itself one of the 23 product agents, and finishing Phase 8 does not mean the product
agents "exist" in any running sense — it means their scaffolding does.

If a reader arrives at this folder having already read the two files above, the
distinction to hold onto is: **product agents do science; build-time agents do
software engineering on the repositories the product agents live in.**

---

## 1. Source documents this study is built from

- `docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md` — 14
  phases, the dependency graph, the Critical Path, the Parallel Workstreams list, the 8
  Architecture Freeze Points, and the Coding-Agent Work Package Rule (§5 below adopts
  this rule directly).
- `docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md` and
  `.../ai/Agent-Commons-Architecture.md` — read for the product-vs-build-time
  distinction above; not otherwise used in this study.
- The companion document `Domain-Phase-Mapping.md` (produced by Fizz, currently on
  branch `fizz/cric-implementation-team-domain-mapping`, to be merged into this folder
  — see §6) — maps each of the 14 phases to its authoritative PRD sections, which
  Freeze Points gate it, and where it can run in parallel. This document assumes that
  mapping exists and does not re-derive it; where the phase table is needed below, it
  is cited rather than reproduced.

---

## 2. Mapping the superpowers skill lifecycle onto the 14-phase sequence

The Claude Code "superpowers" plugin ships a lifecycle of skills
(`superpowers:brainstorming`, `superpowers:writing-plans`,
`superpowers:executing-plans`, `superpowers:subagent-driven-development`,
`superpowers:test-driven-development`, `superpowers:systematic-debugging`,
`superpowers:requesting-code-review`, `superpowers:receiving-code-review`,
`superpowers:finishing-a-development-branch`, `superpowers:using-git-worktrees`,
`superpowers:dispatching-parallel-agents`, `superpowers:verification-before-completion`).
These are confirmed present in this environment's skill listing (verified by name,
2026-08-29). The table below maps each skill onto the Repository Dependency doc's own
structure — it does not invent a new process, it names which existing skill discipline
applies at which point the PRD document already defines.

| Repository-Dependency doc concept | Superpowers skill(s) | Why |
|---|---|---|
| Start of any phase (0–13) or any individual work package inside a phase | `brainstorming` → `writing-plans` | The PRD phase descriptions (e.g. Phase 1's 11-item build order, Phase 4's schema list) state *what* to build, not *how* to sequence or design it. `brainstorming` forces the design questions to surface before code exists; `writing-plans` turns the agreed design into a checked-in plan. This is mandatory before Phase 1 doubly so, because Phase 1 produces all 8 Architecture Freeze Points — undoing a bad design after freeze requires the "explicit migration" the PRD warns about. |
| Ratifying one of the 8 Architecture Freeze Points specifically | `brainstorming` (design alternatives) → `writing-plans` (record the chosen one) → `requesting-code-review`/`receiving-code-review` (see below) | Freeze Points are the highest-cost-to-reverse decisions in the whole sequence; they deserve the heaviest-weight version of this pairing, not the lightest. |
| Actual implementation of a phase's build-order items | `executing-plans` (sequential, single-agent phases — e.g. Phase 1's 11 build-order items have a stated order and shared freeze-point stakes, so they likely stay sequential) or `subagent-driven-development` (phases with genuinely independent sub-tasks — e.g. Phase 8's five first agents: Evidence Extraction, Entity Resolution, Ontology Watch, Provenance Auditor, Human Review Router, which the PRD lists without an implied build order) | The PRD text itself signals which shape applies: Phase 1's list is numbered 1–11 (sequential contract-building); Phase 8's list of five agents is enumerated but not sequenced, and Phase 3/Phase 7 read the same way. |
| Default implementation discipline for every work package | `test-driven-development` | This is the default, not a special case, because the Coding-Agent Work Package Rule (§5) has a mandatory `tests_required` field on every task — TDD is the natural discipline that produces that field's contents as a byproduct of writing the code, rather than as an afterthought. |
| Something breaks (test failure, integration mismatch, unexpected regression) | `systematic-debugging` | Most likely to trigger at Phase 9 (Event Cube Pipeline), which the Repository Dependency doc itself calls out as integrating "domain, ingestion, retrieval and agents" — the highest-surface-area integration point before Phase 14. Also relevant any time a downstream phase discovers its Freeze Point assumption was wrong. |
| Before declaring any phase's exit criterion met | `requesting-code-review` → `receiving-code-review` → `verification-before-completion` | Every phase in the Repository Dependency doc ends with an explicit "Exit criterion:" sentence (e.g. Phase 1: "canonical example OKF nodes validate"; Phase 7: "a synthetic workflow pauses and resumes through Git/local review"). These read as acceptance tests, not vibes — they should each be the literal object of a code-review request and a `verification-before-completion` pass, not something the implementing agent self-certifies. |
| Closing out a work package or phase once merged | `finishing-a-development-branch` | Standard branch hygiene; matters more here than usual because of the multi-repo, multi-agent parallelism below — stale branches across ten-plus repositories are harder to track than in a single-repo project. |
| The "Parallel Workstreams" the Repository Dependency doc says can run after Phase 1 (Knowledge Commons, Data Commons, Cryosphere ontology, Agent runtime, review protocol, documentation) | `using-git-worktrees` + `dispatching-parallel-agents` | This is the literal mechanism for staffing what the PRD calls out by name as parallelisable. Each workstream gets its own worktree/branch and its own dispatched agent, working from the same frozen Phase 1 contracts. This pattern is not hypothetical — it is the same mechanism used to produce this very document (this study itself was dispatched into an isolated worktree so as not to collide with sibling agents also working the same repo), and sibling work-package agents for the Phase 6 retrieval-engine breakdown mentioned in `Domain-Phase-Mapping.md` are running the same way in this session as this document is being written. |

One caution the Repository Dependency doc itself supports: **Parallel Workstreams
only start "after Phase 1,"** and `Domain-Phase-Mapping.md`'s Freeze Point table shows
each of the six named workstreams consumes at least one of the 8 Freeze Points. Dispatching
`dispatching-parallel-agents` before Phase 1's exit criterion is met is not a process
violation the skills themselves will catch — it has to be enforced by whoever is
sequencing the work.

---

## 3. Where Codex fits

A `codex` skill is present in this environment's skill listing, described only as an
"OpenAI Codex CLI wrapper — three modes." I could not verify what those three modes
are from this environment (no skill documentation was opened as part of this study,
and the task instructions were explicit not to invent specifics I'm not sure of) —
**verify the exact modes before relying on this** in any staffing plan.

Structurally, the right way to place Codex in this pathway is as **an alternative or
parallel execution engine for a given work package**, not as a replacement for the
skill lifecycle above. Concretely: once a work package is scoped using the
Coding-Agent Work Package Rule (§5) — with `files_allowed_to_change`,
`tests_required`, and `acceptance_criteria` all pinned down — the *implementation* step
(`executing-plans` / `subagent-driven-development`) could be carried out either by a
Claude Code agent or dispatched to Codex, since the work package's acceptance
criteria are engine-agnostic by construction. This is most plausible for:

- Parallel Workstream phases (Phase 2, 3, 4, 7, 8) where independent, well-scoped work
  packages exist and a second execution engine adds throughput without adding
  coordination cost;
- as an independent second implementation of a security- or correctness-sensitive
  work package, used as an informal cross-check against the Claude-Code-produced
  version before either is merged (this is a stronger form of `requesting-code-review`,
  not a replacement for it).

This placement is a reasonable default, not a confirmed methodology — Ashley's brief
names Codex as "methodology" alongside superpowers without further detail, and the
exact operational contract (does Codex receive the same YAML work package? does it
run inside the same worktree?) should be confirmed before this is relied on for real
scheduling.

---

## 4. Note on the git-worktree pattern already visible in this session

This study's own dispatch instructions required setting up an isolated worktree before
touching the repo, specifically to avoid collision with other agents editing the same
repository in parallel. That is `using-git-worktrees` in practice, and the fact that
seven other work-package agents were addressable in this same session (for Phase 6
retrieval/graph/interface work, per `Domain-Phase-Mapping.md`'s note about "the
retrieval-architecture thread") is `dispatching-parallel-agents` in practice. Section 2's
mapping is not aspirational; the mechanism it describes is the one already running.

---

## 5. The Coding-Agent Work Package Rule as the mandatory task shape

`CRIC-Repository-Dependency-and-Implementation-Sequence.md` already defines this
schema and states its purpose plainly: "This prevents coding agents from
opportunistically redesigning CRIC architecture while implementing a narrow task."
This study adopts it, unmodified, as the **mandatory shape for every task handed to
any build-time agent** — Claude Code, Codex, or otherwise — regardless of which of the
four existing generalists (see `01-Existing-Agent-Fit-Assessment.md`) or which new role
(see `02-New-Role-Gap-Analysis.md`) is doing the work.

```yaml
work_package:
  repository:
  objective:
  authoritative_prd_sections: []
  upstream_contracts: []
  files_allowed_to_change: []
  tests_required: []
  acceptance_criteria: []
  prohibited_changes: []
  review_required:
```

### Worked example: Phase 1, `cric-core`, identifier types

Phase 1's build order lists "identifier types" as item 1 of 11, and Freeze Point 1
("ID format") is produced here. This is the highest-leverage, lowest-margin-for-error
work package in the entire 14-phase sequence — everything downstream references it.

```yaml
work_package:
  repository: cric-core
  objective: >
    Implement the canonical CRIC identifier type(s) — parsing, validation, and
    stable serialization — establishing Architecture Freeze Point 1 (ID format).
    This is build-order item 1 of 11 for cric-core and has no upstream
    dependency inside this repository; every later phase depends on it.
  authoritative_prd_sections:
    - docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md (ID format section)
    - docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md (identifier usage
      in the base object hierarchy, build-order item 6)
  upstream_contracts: []
  files_allowed_to_change:
    - src/cric_core/identifiers/**
    - tests/identifiers/**
  tests_required:
    - Unit tests covering valid and invalid ID strings against the registry's
      declared grammar
    - Round-trip serialization test (ID object -> string -> ID object, equality
      preserved)
    - A rejection test proving IDs outside the declared grammar fail validation
      rather than silently coercing
  acceptance_criteria:
    - Canonical example OKF node IDs validate against this implementation (this
      is Phase 1's own stated exit criterion, applied narrowly to this work
      package's slice of it)
    - No other Phase 1 build-order item (knowledge-state, temporal, spatial,
      provenance, base object hierarchy, relationship model, ontology registry,
      review contracts, validation framework, JSON Schema export) is touched by
      this change
  prohibited_changes:
    - Do not edit CRIC-Schema-and-Vocabulary-Registry.md itself — this work
      package implements the registry, it does not amend it
    - Do not introduce a second identifier type or an alternate ID format "for
      flexibility" — Freeze Point 1 is singular by design
  review_required: >
    Independent verification against the acceptance criteria above before
    merge (see 01-Existing-Agent-Fit-Assessment.md for who). Because this work
    package establishes a Freeze Point, it additionally requires the
    freeze-point ratification checkpoint described in
    02-New-Role-Gap-Analysis.md before any phase depending on Freeze Point 1 is
    allowed to start.
```

The same shape applies unchanged to every other work package in every other phase;
only the content of each field changes.

---

## 6. Companion document — the domain-phase mapping

`Domain-Phase-Mapping.md`, in this same folder, is the domain-mapping half of this
study, produced independently by Fizz and merged in alongside this document and the
two that follow it — for each of the 14 phases, which PRD sections are authoritative,
which of the 8 Architecture Freeze Points gate it, and where parallelism is safe. It
is deliberately not duplicated or re-derived here; read it as this document's
companion, not a subset.
