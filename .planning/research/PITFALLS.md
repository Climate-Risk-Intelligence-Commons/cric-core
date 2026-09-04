# Pitfalls Research

**Domain:** Provenance-preserving, temporally aware knowledge/data/model/agent infrastructure for climate-risk evidence (open-source, multi-repo, multi-agent)
**Researched:** 2026-09-04
**Confidence:** HIGH — derived directly from the 39-document PRD family, ratified ADRs, CLAUDE.md operating rules, and known blocking issue D6; not speculative.

---

## Critical Pitfalls

### Pitfall 1: Auto-Converting `unknown` to a Negative Label

**What goes wrong:**
A downstream consumer reads a knowledge-state of `unknown`, `unobserved`, or `no_known_event` and silently coerces it to `false`, `0`, or a negative class label. Risk estimates, training datasets, and retrieval filters all exhibit this failure mode. The most dangerous form is in ML training pipelines: an unlabelled or `unknown` glacier hazard record gets treated as "no hazard," producing a model that confidently under-predicts risk in data-sparse regions.

**Why it happens:**
Boolean logic, Python truthiness, and standard ML labelling workflows all default to treating absence-of-evidence as evidence-of-absence. Developers reach for `if not record.hazard_state:` and it "works" — until an `unknown` passes through and becomes `False`.

**How to avoid:**
- The 7-value knowledge-state vocabulary (ADR-0007) is a Pydantic `Literal` or `Enum` — never coerce it to bool.
- Every code path that branches on knowledge-state must exhaustively handle all 7 values. Use `match`/`case` with an explicit `case _: raise ValueError(f"Unhandled state: {state}")` rather than `if/elif` chains that fall through.
- Training-data export pipelines must have a dedicated test that asserts `unknown` records are excluded from the negative class, not included.

**Warning signs:**
- A `bool(knowledge_state)` call anywhere in the codebase.
- A pandas/numpy label encoder that receives a `KnowledgeState` column.
- Test coverage for the happy path (confirmed state) but no test for `unknown` input.
- Risk score distributions that have implausibly low variance in data-sparse regions.

**Phase to address:**
Phase 1 (FP6 code, WP-18) — the Pydantic model must make coercion impossible at the type level, and the schema test suite must include explicit `unknown`-as-negative rejection tests.

---

### Pitfall 2: Silently Resolving Contradictions

**What goes wrong:**
Two validly sourced, conflicting claims about the same entity (e.g., two field surveys disagree on a glacier's drainage area) enter the graph, and code "helpfully" picks one — the more recent, the higher-confidence, the one from the more authoritative source. The other record is discarded or overwritten. The contradiction, which is itself a signal about measurement uncertainty, disappears from the evidence chain.

**Why it happens:**
Deduplication and upsert patterns from standard data engineering assume that two records for the same entity are duplicates to merge. CRIC's model is the opposite: two records for the same entity with different values and different provenance are both data, not noise.

**How to avoid:**
- The graph schema must make it structurally impossible to have a single "current value" field that overwrites earlier values. Each claim node carries its own provenance edge; there is no canonical "latest value" field on the entity node itself.
- Ingest pipelines must be tested for the case where a second ingest of a conflicting observation produces two graph nodes, not one updated node.
- "Deduplication" in CRIC means deduplicating identical provenance paths (same source document, same extraction), not deduplicating identical claim values.

**Warning signs:**
- `UPDATE` or `upsert` patterns in graph write code with no provenance check.
- A "latest" or "canonical" field on entity nodes.
- Test suites that only assert the final state after two conflicting ingest runs, not the intermediate graph structure containing both claims.

**Phase to address:**
Phase 1 (FP4 provenance model) and Phase 5 (cric-ingest) — the provenance schema must make it structurally clear that claims are immutable append-only nodes, not mutable state.

---

### Pitfall 3: Identifier Proliferation — the Second ID Format

**What goes wrong:**
A domain repository introduces human-readable short IDs (e.g., `CRIC-LAKE-001`, `GLOF-BASIN-42`) as production identifiers because the `CRIC:<ns>:<type>:<ulid>` format is hard to type, hard to read in logs, or hard to use in filenames. These IDs start in fixtures, graduate to API responses, and eventually get stored in external systems. Now there are two ID systems that must be kept in sync across 12 repositories forever.

**Why it happens:**
ULIDs are opaque. Developers and domain scientists want stable, human-memorable identifiers. The pressure to add a "friendly" alias is constant and each individual case seems reasonable.

**How to avoid:**
- Freeze Point 1 is already ratified and prohibits a second ID format at the architecture level. The test suite for `src/cric_core/identifiers/` must include a test asserting that no other identifier pattern parses successfully through the canonical parser.
- Short IDs (`CRIC-LAKE-001`) are permitted in fixture files and documentation only. Any code path that accepts an ID must reject anything that doesn't parse as `CRIC:<ns>:<type>:<ulid>`.
- Logging and display: derive a short display string from the ULID (e.g., last 8 chars) rather than adding a second production field.

**Warning signs:**
- A field named `short_id`, `human_id`, `display_id`, or `slug` on any schema.
- Fixture data leaking into production code paths via `if settings.debug: use_short_id = True`.
- A domain repo that adds `id_alias` as an optional field "just for convenience."

**Phase to address:**
Phase 1 (all Freeze Points) — the base OKF frontmatter (FP2) must not include a short-ID field, even optional. Optional fields on a base type become required fields in implementations.

---

### Pitfall 4: Freeze Point Ratification Without a Negative Test

**What goes wrong:**
A Freeze Point candidate is presented as accurate, well-reasoned, and internally consistent — and ratified. Nobody tested whether the proposed closure (an enum, a transition graph, a schema) can represent all the scenarios the PRD documents. Later, a legitimate scenario appears that the closure cannot represent, requiring a migration of a locked contract.

**Why it happens:**
Positive validation ("does this schema represent the cases I designed it for?") is natural. Adversarial validation ("find a PRD-documented scenario this schema cannot represent") requires deliberate effort and willingness to invalidate one's own work.

**How to avoid:**
- The ratification bar is explicit: every proposed closure must include a stated negative test — a concrete PRD-documented scenario demonstrated to be representable under the closure, attempted as a break. "Attempted as a break" means the author tried to find a case where the schema fails, not just a case where it succeeds.
- Freeze Point sign-off checklist: (1) positive examples, (2) negative test with documented attempt to break, (3) explicit statement of what object classes the closure applies to.
- Independent review: the person who wrote the candidate should not be the only one attempting to break it.

**Warning signs:**
- A Freeze Point PR with only positive fixture examples.
- A ratification comment that says "looks complete" without naming a scenario that was attempted and survived.
- An enum that covers exactly the cases the author thought of, with no documented exploration of edge cases.

**Phase to address:**
Phase 1 (all remaining Freeze Points: FP2–FP5, FP8) — establish the break-attempt discipline before ratifying any of them.

---

### Pitfall 5: cric-core Importing from Domain Repositories

**What goes wrong:**
A convenience function, a shared utility, or a type defined in `cric-cryosphere` gets imported into `cric-core` "just for this one case." The dependency graph now has a cycle: `cric-core` → `cric-cryosphere` → `cric-core`. Installation of `cric-core` alone fails because `cric-cryosphere` is not installed. Every downstream repository that depends only on `cric-core` must now also pull the entire domain repo.

**Why it happens:**
Domain types are richer and more specific than base types. When writing base infrastructure it is tempting to reference a domain concept rather than generalising it properly.

**How to avoid:**
- CI must include an import test that installs `cric-core` in a clean environment with no domain packages present and asserts that all `cric_core.*` imports succeed.
- Code review gate: any `import cric_` line in `src/cric_core/` is an automatic block unless it imports from within `cric_core` itself.
- The correct direction: domain repos extend cric-core base types; cric-core defines extension points (abstract base classes, protocol interfaces) that domain repos implement.

**Warning signs:**
- Any `from cric_cryosphere` or `from cric_glof` line anywhere in `src/cric_core/`.
- A type hint that references a domain-specific concept by name rather than a base protocol.
- A `pyproject.toml` that lists a domain repo as a dependency.

**Phase to address:**
Phase 0 (already — the package scaffolding must never acquire domain imports); verify at every phase boundary.

---

### Pitfall 6: LLM Performing Graph Traversal

**What goes wrong:**
An agent is asked a question about climate risk, and instead of receiving a pre-assembled context package from deterministic software, it is given access to a graph query tool and told to "explore as needed." The LLM decides which nodes to traverse, which provenance edges to follow, and which contradictions to surface. The result is non-deterministic: the same question asked twice may surface different evidence, reach different conclusions, and attribute claims to different sources — none of which is auditable.

**Why it happens:**
LLM-native "tool use" patterns make it natural to give models direct database access. It feels like flexibility. It is actually an abdication of the deterministic context-assembly requirement.

**How to avoid:**
- Constitutional Rule 13: deterministic software assembles the context package; the model consumes it. The model receives a structured bundle, not a live query interface.
- Agent schemas (FP8) must define `input_context_schema` — the shape of what the agent receives — separately from `output_schema`. The context bundle is assembled by code, not by the agent.
- Retrieval tests must be classifiable into exactly one of: knowledge, retrieval, context-construction, reasoning, generation. A retrieval failure caused by the model choosing the wrong traversal is a context-construction failure, not a reasoning failure.

**Warning signs:**
- An agent that receives a graph connection object or a query function as a tool.
- Agent output that varies for identical inputs without a documented source of legitimate variance.
- A test that asserts "the agent got the right answer" without asserting "the agent received the right context bundle."

**Phase to address:**
Phase 8 (first agent work) — the agent manifest schema (FP8) must make context-assembly vs. model-consumption boundary explicit before any agent is implemented.

---

### Pitfall 7: `mode: yolo` / `auto_advance: true` Removing Freeze Point Gates

**What goes wrong:**
`.planning/config.json` currently sets `mode: yolo` and `auto_advance: true`. If any agent or orchestrator reads these settings and skips Freeze Point ratification steps, a work package can silently advance past a gate that was never properly closed. The schema gets implemented without ratification; the implementation becomes the de facto standard; and the ratification step is retroactively treated as a formality.

**Why it happens:**
Automation pressure: gates slow down pipelines. `auto_advance: true` was presumably set to speed up iteration. But Freeze Points are not performance bottlenecks — they are the mechanism by which the 12-repo ecosystem achieves coordination.

**How to avoid:**
- Ashley must explicitly review and approve these config settings before any work package reads them.
- Freeze Point ratification is a human-in-the-loop step regardless of what `config.json` says. No automated agent may declare a Freeze Point ratified.
- Consider renaming the config key to `allow_auto_advance_of_non_freeze_point_steps` to make the scope explicit.

**Warning signs:**
- A work package completion report that says "Freeze Point X ratified" without a corresponding human sign-off in the PR or ADR.
- A CI step named "auto-ratify" or similar.
- Agents completing work packages in sequence faster than a human could have reviewed each Freeze Point.

**Phase to address:**
Immediately — before Phase 1 work packages begin. This is a governance risk, not a Phase 1 deliverable.

---

### Pitfall 8: Sharing a Git Worktree Between Concurrent Agents

**What goes wrong:**
Two agents run in the same checkout directory. Agent A modifies `src/cric_core/temporal/model.py`; Agent B reads it to understand the base type it needs to extend. Agent B reads an intermediate state — partial edits, uncommitted changes — and builds on it. When A's branch is reviewed, B's output is already committed to a different branch, based on a transient state that was never merged.

**Why it happens:**
The worktree requirement adds operational complexity. When running work packages quickly, the temptation is to skip the `git worktree add` step and just use the main checkout with careful branching.

**How to avoid:**
- Each work package gets its own worktree at `/home/ash/Eyekyam/.worktrees/cric-core/<branch>`. No exceptions.
- The fan-out admission test (CLAUDE.md §12) checks pairwise-disjoint `files_allowed_to_change` — if two children pass that test, they are safe to run in parallel each in their own worktree.
- Worktrees must be cleaned up with `docker compose down -v` (if any compose project was started inside) before `git worktree remove`.

**Warning signs:**
- Two open PRs that both modify the same file with no merge dependency between them.
- A work package that was completed "in main checkout" rather than a named worktree.
- Merge conflicts that would not have existed if the work had been sequential.

**Phase to address:**
All phases — this is an operational discipline, not a code problem. Enforce at the point of work package dispatch.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Duck-typed dicts instead of Pydantic models for OKF nodes | Faster to write, no schema ceremony | Errors at query time, not import time; schema validation silently absent; downstream code cannot trust field presence | Never — Pydantic is the explicit architectural choice |
| Optional fields on base OKF schema | Flexibility for domains that don't need them | Optional fields become de facto required in implementations; missing-field bugs are invisible at import time | Never for identity/provenance fields; only for genuinely optional metadata |
| Storing `unknown` as `None` / `null` | Simpler DB schema | `null` is ambiguous — does it mean unknown, not-yet-fetched, or not-applicable? The 7-value vocabulary exists to replace this ambiguity | Never — use the vocabulary |
| Implementing a Freeze Point before ratification | Unblocks downstream work | The implementation becomes the de facto standard; ratification becomes a rubber stamp; the negative-test requirement is skipped | Never for Architecture Freeze Points; acceptable for non-locked design decisions |
| Running tests only in the happy path | Faster CI | Schema failures on invalid inputs are never caught; the `unknown ≠ false` invariant is never tested | Never for Pydantic schema tests, which explicitly require valid + invalid + boundary + backwards-compat fixtures |
| Resolving doc conflicts by "whichever PRD I read first" | Unblocks implementation immediately | Inconsistent implementations across agents; later agents contradict earlier ones | Never — blocked on D6 resolution (`gsd-ingest-docs --manifest` re-run) |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Pydantic model → JSON Schema export | Generating schema at test time and comparing to a committed fixture with `==` | Use `model_json_schema()` and compare structurally, not as raw strings; pin the Pydantic version in CI since schema output changed between v1 and v2 |
| ULID generation in tests | Using a fixed ULID string literal in test fixtures | Use `ulid.new()` in fixtures and assert structure, not exact value; fixed ULIDs in fixtures become ordering assumptions in sort-dependent tests |
| 39-document PRD as specification | Reading one PRD document to understand a concept | Follow authority precedence: Registry → PRD-MASTER → specialised PRD → examples; concepts defined differently across documents resolve in this order, not by recency |
| GitHub branch protection with `enforce_admins` | Expecting the Coordinator token to push directly to `main` | Every change needs a GitHub PR; direct pushes are rejected at the server, not just warned about |
| Multi-agent fan-out | Assuming two children with non-overlapping file lists are safe to run in parallel | Also check: no producer/consumer edge between them, no shared Freeze Point, and a named integrator exists before dispatch |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Eager provenance chain materialisation at query time | Query latency spikes as evidence depth grows; O(n) provenance hops per claim | Provenance chains are stored as edges in the graph, not reconstructed at read time; retrieval assembles a bounded context window, not the full chain | ~1,000 evidence nodes; irrelevant at current scale but design choice must be made in FP4 |
| Full-graph traversal for context assembly | Agent response time grows with corpus size | Context assembly is bounded: a deterministic windowing function, not an unbounded search | Phase 8 (first agent) — design this window before implementing any agent |
| Pydantic model validation on every graph read | CPU-bound validation becomes bottleneck for bulk retrieval | Validate at write time (ingest), not at read time (retrieval); use `model_validate` with `from_attributes=True` only at the ingest boundary | >10,000 nodes/second retrieval; not a current concern but schema design locks the validation boundary |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Agent output presented as official warning | A downstream UI or API consumer displays CRIC risk scores as institutional GLOF warnings; a community acts on them; a real warning is delayed because the community thinks it was already covered | Every agent output schema must include a `disclaimer` field; API responses must carry a machine-readable `is_official_warning: false` flag; Constitutional Rule 11 is non-negotiable |
| Prompt injection via ingested document content | A malicious actor submits a scientific paper whose abstract contains instructions to the LLM; the ingest agent exfiltrates credentials or modifies provenance records | `engineering/Security-and-Responsible-AI.md` defines prompt-injection test class; every agent that processes external document text must have a prompt-injection test in its suite |
| Provenance edges pointing to mutable sources | A source document URL is included in a provenance chain; the document at that URL changes or disappears; the evidence chain is silently invalidated | Provenance must reference a content-addressed snapshot (hash + access timestamp), not a mutable URL; this is an FP4 (provenance model) decision |
| Agent tool permissions wider than the work package | An agent with write access to the graph uses it to modify provenance edges it was not authorised to touch | Agent manifest (FP8) must declare `tool_permissions` scoped to its task; the harness enforces these, not agent self-restraint |

---

## "Looks Done But Isn't" Checklist

- [ ] **Freeze Point implementation:** Pydantic model exists and imports — verify the schema test suite covers valid, invalid, boundary, and backwards-compat fixtures, not just the happy path.
- [ ] **Knowledge-state field:** field is present on the model — verify that `unknown` cannot be coerced to `bool`, and that every branch on the field handles all 7 values exhaustively.
- [ ] **Provenance on a claim:** a `source_id` field exists — verify the field is a validated `CRICIdentifier`, not a bare string, and that no claim node can be created without it.
- [ ] **Freeze Point ratification:** ADR is written and merged — verify it includes a documented negative test (a PRD-documented scenario the author attempted to break the closure with) and explicit sign-off from Ashley.
- [ ] **CI is green on a branch:** tests pass locally — verify CI ran on the merged tree after PR merge, not just on the branch tip.
- [ ] **Conflict resolution complete:** doc conflicts were noted — verify `gsd-ingest-docs --manifest gsd-ingest-manifest.yaml` was re-run and `.planning/INGEST-CONFLICTS.md` exists before dispatching Phase 1 work packages.
- [ ] **Agent context assembly:** agent returns correct answers — verify it receives a deterministic context bundle, not live graph access; that the same input produces the same context bundle; and that a retrieval failure is classified by failure mode.
- [ ] **Worktree cleanup:** branch merged and PR closed — verify `git worktree remove` was run and (if applicable) `docker compose down -v` was run inside the worktree before removal.

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| `unknown` coerced to negative in training data | HIGH | Audit all label-encoding paths; re-label affected training examples; retrain affected models; document the correction as a provenance event on the training dataset node |
| Contradiction silently resolved (data lost) | HIGH | Restore from the ingest source (if the original source document is still available); re-ingest as a new claim node with full provenance; the "resolved" node is never deleted — it is marked as `superseded` with a provenance edge to the correction event |
| Second ID format in production | HIGH | Migrate all external systems to canonical ULID-format IDs; the short-ID field cannot be simply removed if it was in a published API; requires a versioned deprecation with migration guide |
| Freeze Point implemented before ratification | MEDIUM | Freeze the implementation branch; complete ratification (including negative test) before merging; if the implementation is already merged, open a migration work package with Ashley's sign-off |
| cric-core importing a domain repo | MEDIUM | Identify the shared concept, extract it to a base type in cric-core, implement it there, have the domain repo extend it; remove the reverse import and update CI |
| Worktree collision (two agents, one checkout) | LOW | Stash or discard the conflicted agent's work; re-dispatch it in a fresh worktree; the correct work (from the agent that had the proper worktree) is unaffected |
| D6 (ingest run without --manifest) | LOW | Re-run `gsd-ingest-docs docs/CRIC-PRD-v0.1 --mode new --manifest gsd-ingest-manifest.yaml`; verify `.planning/INGEST-CONFLICTS.md` is created; do not dispatch Phase 1 work packages until this file exists |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| `unknown` → `false` coercion | Phase 1, FP6 code (WP-18) | Schema test suite includes explicit `unknown`-as-negative rejection test; CI blocks merge if absent |
| Silent contradiction resolution | Phase 1, FP4 (provenance model) + Phase 5 (cric-ingest) | Ingest test: two conflicting observations of the same entity produce two claim nodes, not one |
| Second ID format | Phase 1, FP2 (base OKF frontmatter) | OKF schema has no short-ID field; identifier parser test rejects non-ULID formats |
| Ratification without negative test | Phase 1, all remaining FPs | Ratification checklist is a PR template requirement; PRs missing negative-test documentation are blocked |
| Dependency inversion | Phase 0 (ongoing) | CI installs cric-core in isolation (no domain packages) and asserts all imports succeed |
| LLM graph traversal | Phase 8 (first agent) | Agent receives a typed context bundle, not a query interface; test asserts identical input → identical context bundle |
| `mode: yolo` governance gap | Pre-Phase 1 (immediate) | Ashley reviews and updates `config.json` before work packages read it; no automated Freeze Point ratification |
| Worktree collision | All phases | Work package dispatch requires a named worktree path; orchestrator confirms path exists before dispatch |
| Provenance on mutable URL | Phase 1, FP4 | Provenance model requires content-addressed snapshot; test: creating a claim with a bare mutable URL fails validation |
| Agent output as official warning | Phase 8 (first agent) | Every agent output schema includes `is_official_warning: false`; prompt-injection test class present in agent test suite |

---

## Sources

- `docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md` — 13 Constitutional Product Rules (Rules 1, 2, 3, 6, 11, 13 are directly cited above)
- `docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md` — §2 (ID format), §6 (`unknown` handling)
- `CLAUDE.md` §5 (Freeze Point ratification bar), §6 (Constitutional rules), §8 (test discipline), §12 (fan-out admission tests)
- `.planning/PROJECT.md` — D6 blocking issue, `config.json` governance flag, Key Decisions table
- `ADR-0004` (Freeze Point 1, identifier format) — ratified 2026-08-29
- `ADR-0007` (Freeze Points 6+7, knowledge-state vocabulary) — ratified 2026-09-03

---
*Pitfalls research for: cric-core — provenance-preserving climate-risk knowledge infrastructure*
*Researched: 2026-09-04*
