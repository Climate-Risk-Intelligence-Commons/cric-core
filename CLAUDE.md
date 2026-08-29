# CLAUDE.md — `cric-core`

Machine-facing operating rules for any Claude Code / coding-agent session in this
repository. Read `AGENTS.md` for **who** does what; this file is **how** work is done.

## 1. What this repository is

`cric-core` is the contract root of the Climate Risk Intelligence Commons (CRIC): an
open-source, provenance-preserving, temporally aware knowledge/data/model/agent
infrastructure for climate-risk evidence. First domain: Himalayan cryosphere / GLOF.

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
- Run tests as `python -m pytest` (the `-m` matters: it puts the repo root on `sys.path`;
  a bare `pytest` from a cold shell can fail to import the package).

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
- Use a git worktree (`/home/ash/Eyekyam/.worktrees/cric-core/<branch>`) — multiple
  agents work this repository concurrently and a shared checkout will collide.
- **Agents prepare branches and pull requests; agents do not autonomously merge stable
  core changes** (`community/Contribution-and-Review-Process.md` §Merge Rules).
- Merge requires independent verification against the work package's
  `acceptance_criteria` by someone who did not implement it.
- Verify a merge by running the **merged tree's** tests. "No conflicts" and "the merged
  result passes" are different properties.
- Open PRs with `buzz pr open --channel 17bd72a0-4d90-4e0b-b102-f9163f0cfd4b` so the
  PR links back to the conversation that authorised it.

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
