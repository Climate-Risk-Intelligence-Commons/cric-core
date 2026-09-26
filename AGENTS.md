# AGENTS.md — `cric-core` operating contract

The complete, harness-agnostic operating contract for any coding agent or human
contributor working in this repository. It is the **single** source: `CLAUDE.md`
imports this file rather than restating any part of it, and no rule lives in two
places.

Nothing here is specific to one agent harness. Roles are defined by **mandate**, not
by identity — whichever harness, model or person picks a role up inherits that
mandate and is held to it.

## 1. What this repository is

`cric-core` is the contract root of the Climate Risk Intelligence Commons (CRIC): an
open-source, provenance-preserving, temporally aware knowledge/data/model/agent
infrastructure for climate-risk evidence. First domain: Himalayan cryosphere / GLOF.

The repository is owned by the `Climate-Risk-Intelligence-Commons` GitHub
organisation: `github.com/Climate-Risk-Intelligence-Commons/cric-core`. The prior
location, `github.com/ashley-eyekyam/cric-core`, redirects — existing clones and
remotes keep working unchanged, though new clones should use the org URL.

It currently holds the **authoritative PRD family** (`docs/CRIC-PRD-v0.1/`, 39
documents) and the **build-time team charter** (`docs/CRIC-Implementation-Team/`).
Python package code lands here from Phase 1 onward.

Every other CRIC repository depends on this one. `cric-core` may not depend on any
domain-specific repository.

## 2. Two different agent systems — do not conflate them

`ai/Agent-Team-Specifications.md` and `ai/Agent-Commons-Architecture.md` specify **23
product agents** (Evidence Extraction, Ontology Watch, Provenance Auditor, …) that run
*inside the deployed CRIC platform* doing science and knowledge work at runtime.

**This document is not about those.** It is about the **build-time engineering roles**
that write the twelve repositories those product agents will eventually run in.

> Product agents do science. Build-time roles do software engineering on the
> repositories the product agents live in.

Phase 8 (`cric-agents`) is the only place the two touch: a build-time role
*implements* the product-agent infrastructure. Finishing Phase 8 does not mean the 23
product agents exist in any running sense — it means their scaffolding does.

## 3. Authority precedence — non-negotiable

When two documents disagree, resolve in this order (`CRIC-PRD-MASTER.md`
§Implementation Authority, verbatim):

1. executable contracts in a released `cric-core`;
2. `docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md`;
3. `docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md`;
4. specialised PRD documents;
5. examples and older illustrative snippets.

**The registry outranks every specialised PRD document.** Never resolve a conflict by
"whichever file I read first" or "whichever was edited most recently". If the conflict
is unresolvable at this precedence, stop and escalate — do not pick one and proceed.

**Why this table is written out in full rather than referenced.** Every session starts
with no CRIC-specific content in memory, whatever harness it runs on. What a capable
agent carries across projects is a *process* reflex — "check the primary document's
clause, don't run on a prose gloss" — not CRIC's *content*. Re-deriving the right
answer once is not the same guarantee as a written rule every implementer and reviewer
can be checked against. Nothing else in this repository carries this content for a
fresh session, so it lives here.

## 4. Human approval authority

Two roles hold human approval authority. Both are defined in
`docs/CRIC-PRD-v0.1/community/Open-Source-Governance.md`:

- **Core Maintainer** (§Roles — *"Approves stable changes to CRIC Core contracts"*):
  architecture changes, Architecture Freeze Point ratification and any post-lock
  migration, breaking schema changes, semantic redefinition of a stable type,
  safety-relevant concepts, deprecation of a widely used type.
- **Project Steward** (§Project Stewardship — *"The founding organisation may
  initially act as steward and appoint maintainers"*): production deployment,
  credentials, destructive or irreversible actions, security-sensitive changes,
  licensing, significant cost, and any change of scope or business intent.

**No agent holds either role.** Current holders are listed in `MAINTAINERS.md`, which
is the only place a person is named as an authority — the rules themselves cite roles.

Agents prepare branches and pull requests. **Agents do not autonomously merge stable
core changes** (`community/Contribution-and-Review-Process.md` §Merge Rules).

Repositories live in the `Climate-Risk-Intelligence-Commons` GitHub organisation,
which defaults new members to `read` access (`default_repository_permission: read`):
clone and open a pull request, yes; push a branch, no, until granted `write`
explicitly. Don't assume push access follows from org membership alone.

## 5. Before you touch code

Read these five, every phase, regardless of assignment
(`docs/CRIC-Implementation-Team/Domain-Phase-Mapping.md` §Cross-cutting reading):

1. `CRIC-PRD-MASTER.md` — thesis, 13 Constitutional Product Rules, authority precedence
2. `CRIC-Schema-and-Vocabulary-Registry.md` — canonical naming, IDs, predicates, vocabularies
3. `engineering/Software-Architecture.md` — layers, languages, dependency direction
4. `engineering/Security-and-Responsible-AI.md` — threats, tool permissions, prompt injection
5. `engineering/Testing-and-Quality-Assurance.md` — test classes and quality gates

Then read the phase-specific rows in `docs/CRIC-Implementation-Team/Domain-Phase-Mapping.md`.

## 6. Every task arrives as a work package

The Coding-Agent Work Package Rule
(`CRIC-Repository-Dependency-and-Implementation-Sequence.md`) is the **mandatory task
shape**. No implementation starts without one:

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

- `files_allowed_to_change` is a **hard boundary**, not a hint. Touching a file outside
  it invalidates the work package — raise it, do not widen it yourself.
- `prohibited_changes` is a **hard boundary**. Its purpose, stated in the PRD, is to stop
  agents "opportunistically redesigning CRIC architecture while implementing a narrow task."
- Spotted an unrelated defect? File it. Do not fix it in this branch.
- `acceptance_criteria` is the pass/fail bar the independent verifier will use. If a
  criterion cannot be violated by any test you can write, say so before implementing.

## 7. Architecture Freeze Points

Eight contracts are produced in Phase 1 and consumed by every later phase: ID format,
base OKF frontmatter, temporal model, provenance model, relationship representation,
knowledge-state vocabulary, review decision schema, agent manifest schema.

Once locked, changing one **requires explicit migration and Core Maintainer sign-off**.
A work package may not silently alter a locked freeze point — that is an escalation,
not an implementation detail.

**A candidate is not ratifiable on accuracy alone.** Every closed set it proposes — an
enum, a transition graph, a schema — needs a stated negative test: a concrete scenario
the PRD itself documents, shown representable under the proposed closure. A closure
nobody attempted to break with a real counter-example is not ready for sign-off. The
candidate also states explicitly which object classes the closure applies to — a
field's scope is part of its contract, not something left for the attacker or the
sign-off to infer.

### Ratification checkpoint

Ratification is a **three-way checkpoint, not a role**:

1. **The Requirements Analyst** assembles the candidate with citations, and states its
   blast radius — which downstream phases it gates, per `Domain-Phase-Mapping.md`'s
   Freeze Point table — not just its value. Every closed set the candidate proposes
   carries a **negative test**, and states explicitly which **object classes** the
   closure applies to. A field's scope is part of its contract; it does not get left
   for someone downstream to infer.
2. **The Independent Verifier** blast-radius-verifies independently, and tries to break
   the candidate rather than co-signing the Requirements Analyst's reasoning — checking
   two separable things, not one: whether the artefact is **accurate** (citations
   correct, transcription faithful) and whether its **shape is sufficient** (the closure
   actually covers what the PRD documents, the stated scope is right). Passing the first
   has been mistaken for passing both more than once; they are checked separately, every
   time.
3. **The Core Maintainer** signs off.

**Fast agreement between two agents restating the same reasoning is not independent
confirmation.** Convergence on this *policy* is fine; convergence on a specific
*finding* with no independent method behind it is not.

## 8. Constitutional rules that bite in code

All 13 are in `CRIC-PRD-MASTER.md`. These four are the ones most often broken by
well-intentioned implementations:

- **Unknown is not negative** (Rule 6). Never auto-convert `unknown` / `unobserved` /
  `no_known_event` into a negative label or a false value. Explicitly prohibited by the
  registry §6 and the Training-Data spec.
- **Evidence lineage is immutable** (Rule 1) and every derived value traces to source
  evidence (Rule 2). No value without provenance.
- **Contradiction is represented, not erased** (Rule 3). Two validly sourced conflicting
  claims both live in the graph. Do not "resolve" them in code.
- **The LLM must not perform graph traversal** (Rule 13). Deterministic software
  assembles context first; the model consumes an assembled context package.

Domain repositories may **extend** core types but must never **redefine** the semantic
meaning of a stable core type.

## 9. The build-time engineering roles

Five roles. Each is defined by the **mandate** below and nothing else — no role is tied
to a particular agent harness, model, vendor or persistent identity. Any harness may
hold any role; holding it means being bound by its mandate and its stated limits.

One role, one holder, per work package. The limits below ("does not implement", "never
the final reviewer of own work") are the point of the split — a single agent holding
two adjacent roles on the same package collapses the separation that makes review
meaningful.

### Requirements Analyst

- Reads and reconciles the 39 PRD documents; resolves doc-vs-doc conflicts through the
  precedence in §3.
- **Owns `authoritative_prd_sections` and `upstream_contracts` on every work package.**
  No implementer re-derives these from 39 files. `Domain-Phase-Mapping.md`'s phase
  table is the base layer; the Requirements Analyst refines it to work-package
  granularity as each package is scoped inside a phase.
- Assembles and cites candidate Architecture Freeze Points for ratification.
- **Assembles and cites; does not self-verify.** The Independent Verifier checks the
  section picks before a package is handed to the Implementation Engineer.
- Stays out of implementation and out of verification sign-off.

### Implementation Engineer

- Implements against a work package. Test-driven development is the **default**, not a
  special case.
- **`files_allowed_to_change` and `prohibited_changes` are hard boundaries.** An
  out-of-scope defect spotted mid-package becomes a note back to the Requirements
  Analyst or the Coordinator for a new work package — never a silent addition to the
  diff already shipping. This is also what keeps an unratified Freeze Point change from
  sneaking in undetected.
- Strict typed models and validated construction over duck-typing shortcuts. Pydantic
  is the runtime schema authority (`engineering/Software-Architecture.md`).
- **Also carries the Build & Release Engineer brief** (see §10).

### Independent Verifier

- Verifies against the work package's `acceptance_criteria` as the **primary** pass/fail
  bar — but not the only one. Also checks, independent of what the package page happens
  to spell out:
  - scope: `files_allowed_to_change` / `prohibited_changes`;
  - the seven Review Dimensions from `community/Contribution-and-Review-Process.md` —
    code correctness, schema correctness, scientific validity, licensing, security,
    safety, documentation.
- Holds the distinction `engineering/Testing-and-Quality-Assurance.md` states directly:
  **"Passing software tests does not establish scientific validity. Scientific
  validation is an additional activity."** Acceptance criteria passing says the narrow
  slice works as specified; it says nothing on its own about blast radius, licensing or
  scientific validity.
- **Stops and escalates rather than self-approving** on any §16 trigger or Freeze Point
  touch. Applies the gate asymmetrically, as the PRD intends: tight on the five
  triggers, deliberately light elsewhere ("low-risk additions may use lighter review
  rules", `knowledge/Ontology-Evolution-and-Governance.md`).
- Never the final reviewer of code this role implemented. Never co-signs the
  Requirements Analyst's citations — verifies them independently.

### Memory & Knowledge Manager

- One ADR per decision: alternatives, rationale, approver, date, consequences.
- **Freeze Point rule, adopted as hard:** any ADR recording one of the 8 Architecture
  Freeze Points names the **Core Maintainer who approved it, by name and date** — an ADR
  is the historical record, so it records the person, not only the role — and its
  consequences section states explicitly that reversal requires a formal migration, not
  routine amendment.
- Owns an open-questions register with owner / blocks / raised / resolved — **chased,
  not merely logged** — plus project facts, lessons, and the durable record of each
  phase's exit evidence.
- Scope: `docs/` only, on a task branch. Defers merge to the Coordinator and review to
  someone who did not write the document.

### Engineering Coordinator

- Decomposes phases into work packages, sequences them, sets acceptance criteria and
  evidence standards, activates roles, issues rulings as ADRs, merges specialist inputs.
- **Does not implement, and never reviews own work.**
- Merges PRs after independent verification. Escalates §16 items to the Core Maintainer
  or Project Steward, per the split in §4.

## 10. Build & Release Engineer — a brief, not a sixth role

Carried by the **Implementation Engineer** under a widened scope, activation-windowed:

- **Phase 0 (full):** repository scaffolding, licences, CODEOWNERS and branch
  protection, CI skeleton, coordinated release/version metadata — to the point
  `cric-core` can publish a versioned Python package. Every Phase 0 repository is
  created directly in the `Climate-Risk-Intelligence-Commons` org, never under a
  personal account.
- **Phases 1–13 (light custodial tail):** apply the Phase 0 template to each repository
  as it comes online; flag drift. No new judgment calls.
- **Phase 14 (full):** coordinated release manifest, compatibility matrix, and
  reproducibility instructions an external researcher can follow end-to-end, against
  the nine required-evidence items in
  `CRIC-Repository-Dependency-and-Implementation-Sequence.md` §Phase 14.

**Two hats, kept separate.** Under this brief the Implementation Engineer holds
repository-admin, branch-protection and CI-configuration access across CRIC
repositories. That does **not** confer merge rights into product-code branches — those
stay behind the normal verify-then-Coordinator-merges gate.

## 11. Roles deliberately not created

Recorded so they are not re-litigated (`02-New-Role-Gap-Analysis.md`; the governing
restraint principle is that a role earns creation only when a named phase needs it and
the existing generalist roles provably do not cover it):

| Candidate | Verdict | Instead |
|---|---|---|
| Solution Architect for Freeze Point ratification | Rejected | The three-way checkpoint in §7 |
| DevOps / Release Engineer | **Accepted, narrowly** | The Build & Release brief, §10 |
| Domain / Ontology Specialist for Phase 4 cryosphere science | Rejected as standing role | Escalation only — a named one-off subject-matter reviewer, if and only if Phase 4 surfaces a scientific judgment call the written domain PRD documents do not resolve |

## 12. Stack and conventions

- **Python 3.12+** is the primary backend/scientific language. **TypeScript** for the web frontend.
- **Pydantic is the runtime schema authority** — OKF validation, API contracts, agent
  dependencies and outputs, review artefacts, manifests, model metadata. Generated JSON
  Schema is published. Prefer strict typed contracts over duck-typing everywhere.
- No mandatory orchestration framework (no LangGraph requirement) for agents.
- Identifier form (registry §2): `CRIC:<namespace>:<type>:<ulid>` — one ID format,
  singular by design. Human-facing short IDs such as `CRIC-LAKE-001` may appear in
  examples and fixtures but **must not** be treated as the canonical production
  identifier. Do not add a second ID format "for flexibility".
- Run tests with `python -m pytest` or bare `pytest` — both work. `pyproject.toml`
  sets `pythonpath = ["src"]` under `[tool.pytest.ini_options]`, so the `src` layout
  resolves regardless of invocation or cwd; don't reinstate a `python -m` requirement
  as folklore — if this stops being true, check the config first.
- **`ruff` and `mypy` are pinned in `pyproject.toml`** (`[project.optional-dependencies]
  dev`) to the exact versions CI last passed with. Both are unversioned upstream and
  PyPI releases land without warning — `ruff` moved 0.16.5 → 0.16.6 between two CI
  runs eighteen hours apart during this project's first week, with `test` a required,
  `strict` status check. An unpinned linter release can turn `main` red with zero
  change to our code. Bump the pin deliberately, in its own commit, after confirming
  the new version is clean against this codebase — not as a side effect of some other
  PR happening to reinstall `dev` extras.

## 13. Local development

Nothing in this section is a project requirement. It is the shortest path to a working
checkout, plus two environment failures that cost real time to diagnose.

- **Virtual environment, for CI parity.** `.venv/` at the repo root, populated from the
  same declaration CI installs from:

  ```sh
  python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"
  ```

  This gives a working `ruff`/`mypy`/`pytest`/`build` inside the venv without depending
  on whatever a given host happens to have installed globally. `.venv/` is gitignored;
  never commit it.

- **A `uv`-created venv with nothing installed into it is a trap, not a dev
  environment.** It has a working `python3` and passes a casual glance (`git status`
  stays clean — a bare `uv venv` self-ignores via its own `.venv/.gitignore`), but
  carries no `pip`, `ruff` or `mypy`. If you find a `.venv/` that doesn't run
  `ruff --version`, don't assume it's broken — assume it was never populated, and
  populate it. `uv venv` works fine provided you then `uv pip install`.

- **Symptom: `ModuleNotFoundError: No module named 'encodings'` from an otherwise
  healthy `python3`.** Your agent harness or launcher — an AppImage wrapper is the
  usual culprit — is leaking `PYTHONHOME` and `PYTHONPATH` into child processes,
  including into venvs. Fix by unsetting them for the call:

  ```sh
  env -u PYTHONHOME -u PYTHONPATH python3 -m venv .venv
  env -u PYTHONHOME -u PYTHONPATH .venv/bin/pip install -e ".[dev]"
  ```

  This is an artefact of how the process was launched, not of this project, and it does
  not apply to the GitHub Actions CI workflow, which runs on a clean image.

- **Work in a git worktree, outside the repository checkout.** Multiple agents work
  this repository concurrently and a shared checkout will collide. One worktree per
  work package, and one per child in a fan-out (§18). Any location outside the checkout
  works; a sibling `.worktrees/cric-core/<branch>` directory keeps them together.

## 14. Test discipline

Test-driven development is the **default**, not a special case — `tests_required` is a
mandatory work-package field, and TDD produces its contents as a byproduct rather than
an afterthought.

Test classes required by `engineering/Testing-and-Quality-Assurance.md`: unit, schema
(valid + invalid + boundary + backwards-compat fixtures for **every** Pydantic model),
ontology, OKF, graph, deterministic-ranking, geospatial, provenance, agent, prompt
injection, HITL, training-data, model.

**Retrieval-path failures must be classified** into exactly one of: knowledge,
retrieval, context-construction, reasoning, generation. An unclassified retrieval-path
failure is itself a test-infrastructure defect. "Hallucination" is not a classification.

A green test on the wrong assertion is worse than no test — it retires the question.
Assert that the check actually reached the thing it claims to check.

## 15. Branch, review and merge policy

- **Never commit directly to `main`.** One branch per work package, off `origin/main`.
  `main` is branch-protected (`enforce_admins` on): a direct push to `main` is
  rejected by GitHub itself ("protected branch hook declined"), for every token
  including the Coordinator's. A push to any other branch succeeds — protection
  only guards `main`, not the repository generally.
- Use a git worktree (§13) — a shared checkout will collide.
- **Agents prepare branches and pull requests; agents do not autonomously merge stable
  core changes** (`community/Contribution-and-Review-Process.md` §Merge Rules).
- Merge requires independent verification against the work package's
  `acceptance_criteria` by someone who did not implement it.
- Verify a merge by running the **merged tree's** tests. "No conflicts" and "the merged
  result passes" are different properties.
- **Merging requires a GitHub pull request against `main`** (`gh pr create`). If your
  team also runs an out-of-band coordination or review system, a record opened there is
  **not** a substitute and cannot satisfy branch protection — branch protection
  recognises the GitHub PR and nothing else. Open both if both are in use; they do
  different jobs.
- New org members default to `read` access (`default_repository_permission: read`)
  and cannot push a branch until granted `write` explicitly — confirm you have
  write access to the repository before starting a work package if you're unsure.

## 16. Escalate to a human approver — do not self-approve

Route by the split in §4.

**To the Core Maintainer** — a **stable** change that:

- alters semantic meaning of an existing type;
- affects multiple repositories;
- changes safety-relevant concepts;
- creates a breaking schema change;
- deprecates a widely used type;
- touches a locked Architecture Freeze Point.

(First five: `knowledge/Ontology-Evolution-and-Governance.md` §Human Review triggers.)

**To the Project Steward** — anything irreversible, destructive, credential-related,
security-sensitive, or that changes licensing, scope, business intent or cost.

## 17. Safety

CRIC v0.1 is a research and reference implementation. Model scores, risk states and
agent outputs **must not** be presented as official warnings. CRIC never silently
assumes institutional warning authority (Rule 11). Operational warning authority stays
with competent external institutions.

## 18. Fan-out and decomposition

An agent holding a work package must split it into **two or more child packages**
dispatched to subagents unless it can state, in one line, why not. Two or more children
may run in **parallel** only if all four of the following hold:

- **(a) Disjoint files** — the children's `files_allowed_to_change` globs have a
  pairwise-empty intersection, checked over **every pair** in the fan-out, not just the
  first two. Pairwise-disjoint is globally sufficient: if no two children share a
  declared glob, no file has two writers.
- **(b) No producer/consumer edge** — for every pair, neither child's
  `upstream_contracts` names something the other child produces. This pairwise check is
  sufficient even for chains and cycles without needing a full graph traversal: any
  directed edge A→B means the pair `{A, B}` already fails on its own, so a cycle
  A→B→C→A is caught at its first edge.
- **(c) No shared Freeze Point** — for every pair, if two children would both touch one
  of the 8 Architecture Freeze Points (§7), they are not two packages, they are one:
  a Freeze Point produced by two agents in parallel is two candidate definitions of it.
- **(d) A named integrator, before dispatch** — unlike (a)–(c), this is checked **once**
  for the whole fan-out, not pairwise: who merges the children and runs the merged tree.

**(a)–(c) apply pairwise, over every pair in the fan-out; (d) applies once, for the
fan-out as a whole.** Fail any one of the four → the work proceeds sequentially instead,
and the agent says which one failed.

**The vacuous-disjointness fix.** A child that changes no files at all (a research,
analysis or review child) has an empty `files_allowed_to_change` set, and the empty set
trivially doesn't intersect any other empty set — so naively, two such children would
pass test (a) automatically. This is wrong: it is exactly how the redundant-fan-out
anti-pattern below would sneak through the admission test. Fix: **for a child that
changes no files, disjointness is judged on its stated deliverable, not its file set —
every child must name a deliverable no sibling also names.** Two children pointed at the
same question are not a valid split; they are the anti-pattern.

A parent work package that fans out gains a `decomposition:` block naming each child and
the integrator, alongside the work-package shape in §6 (adapt freely — this is
illustrative):

```yaml
decomposition:
  integrator: <role>
  children:
    - id: <child-id>
      deliverable: <one-line, must be unique across siblings>
      files_allowed_to_change: [...]
```

**One worktree per child.**

**Verify the merged result, never the slices.** Two subagents can each stay perfectly
inside their own `files_allowed_to_change` and still jointly violate an invariant
neither touches alone — a child changing file A and a sibling changing file B can still
produce two files that contradict each other. Verification runs against the merged
result of the entire fan-out, not per child — the same shape as §15's existing "verify
the merged tree's tests, not each branch's" rule, one level up.

**The redundant-fan-out anti-pattern.** Stated because it looks like diligence rather
than a mistake: fanning out N subagents on the *same* question is not N independent
checks — it's one answer restated N times, which reads as corroboration but isn't.
Parallelism is for disjoint work, never for redundant opinions. A genuine second opinion
comes from a different **method** (e.g. an independent verification pass by a different
role, or a different tool/engine in challenge mode), never from a second instance of the
same prompt run again. A child too small to carry its own meaningful test/acceptance
criteria is not a child package, it's a step, and shouldn't have been split out.

### The parent's three obligations

This is what stops fan-out from becoming invisible:

1. **Declare the split before dispatching.** The `decomposition:` block names each child
   and its disjoint file set (or, per the vacuous-disjointness fix, its unique
   deliverable) — reviewable *before* any subagent runs. A fan-out that appears with no
   prior audit trail is the failure mode this obligation exists to prevent.
2. **Whoever splits it, lands it.** The agent that fans a work package out is the
   integrator — a fan-out with no integrator produces N branches nobody merges.
3. **Verify the merged result, never the slices** — stated here as the accountable
   holder's obligation rather than as the mechanism.

### Per-role decomposition shape

- The **Requirements Analyst** decomposes along document/contract boundaries, and must
  populate each child's `authoritative_prd_sections` individually.
- The **Implementation Engineer** decomposes along file boundaries and integrates that
  fan-out — the same role both splits work-package-shaped implementation tasks and lands
  them.
- The **Independent Verifier** verifies the merged result and explicitly does **not**
  split verification into per-slice verifiers — one verification pass covers the whole
  merged fan-out, never N independent partial passes.
- The **Memory & Knowledge Manager**'s document work parallelises naturally, one
  document per child.

## 19. Second opinions

An **independent second engine in adversarial mode** — a different tool or model from
the one that produced the work, not a second run of the same prompt — is the only kind
of second opinion that carries information. The OpenAI Codex CLI is verified present on
this project's hosts and offers three usable modes: **review** (independent diff review
with a pass/fail gate), **challenge** (adversarial), **consult** (session-continuity
Q&A). Any comparable independent engine satisfies this section.

Ruling for v0.1: a second engine is an **adversarial second opinion** on Freeze Point
and security-sensitive work packages. It is **not** a primary implementer, and **not** a
substitute for the Independent Verifier's pass — those packages get both, not one
instead of the other. Revisit at the first parallel wave (Phases 2/3/4).

## 20. Document conventions

| Artefact | Location | Owner |
|---|---|---|
| Architecture Decision Records | `decisions/NNNN-slug.md` | Memory & Knowledge Manager |
| Decision register | `docs/DECISION_REGISTER.md` | Memory & Knowledge Manager |
| Open questions (owner / blocks / raised / resolved) | `docs/OPEN_QUESTIONS.md` | Memory & Knowledge Manager |
| Project facts | `docs/PROJECT_FACTS.md` | Memory & Knowledge Manager |
| Lessons | `docs/LESSONS.md` | Memory & Knowledge Manager |
| Role→holder roster | `MAINTAINERS.md` | Core Maintainer |
| Authoritative PRD | `docs/CRIC-PRD-v0.1/` | Requirements Analyst interprets; nobody amends while implementing it |
| Build-time team charter | `docs/CRIC-Implementation-Team/` | Engineering Coordinator |
| Plan state | `.planning/` | Written by planning tooling only — never hand-written |

**`decisions/`, not `docs/adr/`** — settled in ADR-0001, and checked against the
mechanism rather than assumed. ADR discovery tooling matches a numbered-filename
convention (`NNNN-*.md`) wherever it lives, so the folder name is not load-bearing. This
keeps `docs/` for narrative and reference material and gives the ratified-decision log
its own append-only top-level folder, consistent with the sibling EnergyMatrix project.
Do not re-open this on the assumption that `docs/adr/` is required for tooling; it is
not.
