# CLAUDE.md — `cric-core`

Machine-facing operating rules for any Claude Code / coding-agent session in this
repository. Read `AGENTS.md` for **who** does what; this file is **how** work is done.

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

## 2. Authority precedence — non-negotiable

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

## 3. Before you touch code

Read these five, every phase, regardless of assignment
(`docs/CRIC-Implementation-Team/Domain-Phase-Mapping.md` §Cross-cutting reading):

1. `CRIC-PRD-MASTER.md` — thesis, 13 Constitutional Product Rules, authority precedence
2. `CRIC-Schema-and-Vocabulary-Registry.md` — canonical naming, IDs, predicates, vocabularies
3. `engineering/Software-Architecture.md` — layers, languages, dependency direction
4. `engineering/Security-and-Responsible-AI.md` — threats, tool permissions, prompt injection
5. `engineering/Testing-and-Quality-Assurance.md` — test classes and quality gates

Then read the phase-specific rows in `docs/CRIC-Implementation-Team/Domain-Phase-Mapping.md`.

## 4. Every task arrives as a work package

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

## 5. Architecture Freeze Points

Eight contracts are produced in Phase 1 and consumed by every later phase: ID format,
base OKF frontmatter, temporal model, provenance model, relationship representation,
knowledge-state vocabulary, review decision schema, agent manifest schema.

Once locked, changing one **requires explicit migration and Ashley's sign-off**. A
work package may not silently alter a locked freeze point — that is an escalation, not
an implementation detail.

## 6. Constitutional rules that bite in code

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

## 7. Stack and conventions

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
  as folklore if this stops being true, check the config first.
- **On this development host specifically:** prefix `python3`, `pip`, `pytest` and
  `build` invocations with `env -u PYTHONHOME -u PYTHONPATH`. The local harness's
  AppImage leaks those two variables into child processes, including venvs, and an
  unset `python3` fails with `ModuleNotFoundError: No module named 'encodings'`. This
  is an artefact of this machine, not a project requirement — it does not apply to
  the GitHub Actions CI workflow, which runs on a clean image.

## 8. Test discipline

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

## 9. Branch, review and merge policy

- **Never commit directly to `main`.** One branch per work package, off `origin/main`.
  `main` is branch-protected (`enforce_admins` on): a direct push to `main` is
  rejected by GitHub itself ("protected branch hook declined"), for every token
  including the Coordinator's. A push to any other branch succeeds — protection
  only guards `main`, not the repository generally.
- Use a git worktree (`/home/ash/Eyekyam/.worktrees/cric-core/<branch>`) — multiple
  agents work this repository concurrently and a shared checkout will collide.
- **Agents prepare branches and pull requests; agents do not autonomously merge stable
  core changes** (`community/Contribution-and-Review-Process.md` §Merge Rules).
- Merge requires independent verification against the work package's
  `acceptance_criteria` by someone who did not implement it.
- Verify a merge by running the **merged tree's** tests. "No conflicts" and "the merged
  result passes" are different properties.
- **Open two PRs — they do different jobs, neither substitutes for the other.**
  `buzz pr open --channel 17bd72a0-4d90-4e0b-b102-f9163f0cfd4b` creates a NIP-34
  Nostr PR that links the channel to the work; it is **not** a GitHub PR and cannot
  satisfy branch protection. Merging requires an actual GitHub PR (`gh pr create`)
  against `main` — open that too, and merge there.
- New org members default to `read` access (`default_repository_permission: read`)
  and cannot push a branch until granted `write` explicitly — confirm you have
  write access to the repository before starting a work package if you're unsure.

## 10. Escalate to Ashley, do not decide alone

Stop and escalate when a **stable** change:

- alters semantic meaning of an existing type;
- affects multiple repositories;
- changes safety-relevant concepts;
- creates a breaking schema change;
- deprecates a widely used type;
- touches a locked Architecture Freeze Point;
- is irreversible, destructive, credential-related, or changes scope or cost.

(First five: `knowledge/Ontology-Evolution-and-Governance.md` §Human Review triggers.)

## 11. Safety

CRIC v0.1 is a research and reference implementation. Model scores, risk states and
agent outputs **must not** be presented as official warnings. CRIC never silently
assumes institutional warning authority (Rule 11). Operational warning authority stays
with competent external institutions.

## 12. Fan-out and decomposition

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
  of the 8 Architecture Freeze Points (§5), they are not two packages, they are one:
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
the integrator, alongside the work-package shape in §4 (adapt freely — this is
illustrative):

```yaml
decomposition:
  integrator: <name>
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
result of the entire fan-out, not per child — the same shape as §9's existing "verify
the merged tree's tests, not each branch's" rule, one level up.

**The redundant-fan-out anti-pattern.** Stated because it looks like diligence rather
than a mistake: fanning out N subagents on the *same* question is not N independent
checks — it's one answer restated N times, which reads as corroboration but isn't.
Parallelism is for disjoint work, never for redundant opinions. A genuine second opinion
comes from a different **method** (e.g. an independent verification pass by a different
role, or a different tool/engine in challenge mode), never from a second instance of the
same prompt run again. A child too small to carry its own meaningful test/acceptance
criteria is not a child package, it's a step, and shouldn't have been split out.
