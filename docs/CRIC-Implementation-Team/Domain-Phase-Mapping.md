# CRIC Build-Time Domain-to-Phase Mapping

## Purpose and scope

This document answers one question: **for each of the 14 implementation phases in
`CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md`, which PRD
sections are authoritative, which Architecture Freeze Points gate it, and what does a
build-time agent working that phase need to have read before touching code?**

It is written for whoever is assembling the CRIC build-time agent team (Claude Code /
Codex agents using the superpowers skill framework), not for the CRIC product itself.

**This is not a duplicate of `ai/Agent-Team-Specifications.md`.** That document specs
CRIC's *product* agents — the 23 Pydantic AI agents (Evidence Extraction, Ontology
Watch/Synthesis/Critic, etc.) that run **inside the deployed platform** doing science
and knowledge work. This document is about the **build-time** team that writes the
code those product agents will eventually run in. Phase 8 below (`cric-agents`) is
where the two systems meet: a build-time specialist *implements* the product-agent
infrastructure; it is not itself one of the 23 product agents.

This is the domain-mapping half of a two-part study. The companion half — whether
CRIC's existing generalist identities (Fizz/Honey/Pollen/Memory & Knowledge Manager)
already cover this build, the superpowers/Codex mechanics, and final assembly — is
owned by the Engineering Coordinator.

---

## How to use this with the Coding-Agent Work Package Rule

`CRIC-Repository-Dependency-and-Implementation-Sequence.md` already defines the
required shape of every task handed to a coding agent:

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

The phase table below exists to populate `authoritative_prd_sections` and
`upstream_contracts` correctly for every phase, without each build-time agent having
to re-derive it by reading all 34 PRD files itself.

---

## Cross-cutting reading — every specialist, every phase, before phase-specific reading

These apply regardless of which phase/repo an agent is assigned:

1. `CRIC-PRD-MASTER.md` — product thesis, 12 Constitutional Product Rules, Implementation Authority precedence.
2. `CRIC-Schema-and-Vocabulary-Registry.md` — canonical naming, identifier form, predicates, vocabularies. **Authority precedence rank 2**, above every specialised PRD document (`CRIC-PRD-MASTER.md` §Implementation Authority) — when a specialised doc and the registry disagree, the registry wins.
3. `engineering/Software-Architecture.md` — architectural layers, language choices, dependency direction, repository architecture.
4. `engineering/Security-and-Responsible-AI.md` — threat categories, tool permissions, prompt-injection handling; applies to every repo, not just `cric-agents`.
5. `engineering/Testing-and-Quality-Assurance.md` — test classes and quality gates that apply to whatever the agent produces.

A build-time agent that has not read these five has not read enough to be handed a
work package, regardless of phase.

---

## Architecture Freeze Points — what gates what

`CRIC-Repository-Dependency-and-Implementation-Sequence.md` names 8 freeze points that
must stabilise before v0.1 coding accelerates. All 8 are produced in **Phase 1**
(`cric-core`); every later phase consumes some subset. Sequencing build-time agents in
parallel is only safe once the freeze points that phase depends on are locked.

| # | Freeze point | Produced in | Primary spec | Phases that cannot safely start before this locks |
|---|---|---|---|---|
| 1 | ID format | Phase 1 | `CRIC-Schema-and-Vocabulary-Registry.md` §2 (identifier form) + the machine-readable Ontology Registry (`knowledge/Core-Ontology-Specification.md` — governs the `<type>` segment's legal values via its per-type `id_segment`; ratified in ADR-0004 Decisions 5–6). Registry §3 (Root Object Types) lists the same type names in prose but is not what ADR-0004 ratifies for `<type>` — whether the two are meant to stay in lockstep is open, see `docs/OPEN_QUESTIONS.md` D32. | All (every node/edge/predicate reference depends on it) |
| 2 | Base OKF frontmatter | Phase 1 | `knowledge/OKF-Knowledge-Graph-Specification.md` (Universal Frontmatter, Node Categories) + registry §1 (Naming — defines OKF Markdown itself and Pydantic as runtime schema authority) + registry §3 (Root Object Types — governs the frontmatter's `type:`/`subtype:` field values, confirmed against the doc's own worked examples) | 2, 4, 5, 6, 9 |
| 3 | Temporal model | Phase 1 | `knowledge/Temporal-and-Epistemic-Ontology.md` + registry §7 (Multi-Temporal Model — the doc's Temporal Structure block is a verbatim superset of §7's schema) + registry §5 (Epistemic Status — the doc's own Epistemic Model section duplicates it) + registry §6 (Negative-Case Vocabulary — the doc's Unknown Versus Negative section overlaps it, at coarser granularity) | 4, 5, 6, 9, 10 |
| 4 | Provenance model | Phase 1 | `knowledge/Evidence-Provenance-and-Trust.md` + registry §9 (Evidence and Provenance Levels — the doc's Source→Acquired Asset→…→Decision-Support Output chain is the same lineage as §9's L0–L6; note §9 states backward traversal as MUST, the doc as "should" — registry's stronger modal wins) | 3, 5, 6, 9, 10 |
| 5 | Relationship representation | Phase 1 | `knowledge/OKF-Knowledge-Graph-Specification.md` §Relationship Grammar + registry §8 — unchanged; the doc itself states "`CRIC-Schema-and-Vocabulary-Registry.md` section 8 is the sole authority for the canonical predicate list," the strongest possible confirmation of this row | 2, 4, 6, 9 |
| 6 | Knowledge-state vocabulary | Phase 1 | `CRIC-Schema-and-Vocabulary-Registry.md` §4, `knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md` — unchanged; checked whether §5/§6 belong here too (both are Epistemic content, not Knowledge-state) and confirmed they don't, since `Claims-Contradictions-and-Knowledge-Lifecycle.md` carries no epistemic-status or negative-case content — that content lives in `Temporal-and-Epistemic-Ontology.md` instead, which is why it was added to row 3, not this row | 4, 6, 7, 9, 13 |
| 7 | Review decision schema | Phase 1 | `ai/Responsible-Autonomy-and-HITL.md` + registry §10 (Canonical Review States — the doc's Review as Repository State folder list and its ReviewDecision.decision values are both verbatim matches of §10) | 7, 8, 13 |
| 8 | Agent manifest schema | Phase 1 | `ai/Agent-Commons-Architecture.md` §Agent Manifest + registry §13 (Agent Composition Contract — the doc's Architectural Principle ten-part list is a verbatim match of §13's list) | 8 |

**Provenance of the "Primary spec" column above:** every registry section cited was read in full, not matched by heading title alone (`CRIC-Implementation-Team/00-Overview-and-Superpowers-Codex-Pathway.md`'s own precedence framing and the Engineering Coordinator's audit of this table, 2026-08-29, both required this). Where a row's citation is unchanged from an earlier version of this table, that means it was checked and confirmed sufficient, not that it was skipped — rows 5 and 6 both carry an explicit note saying what was checked and why nothing else governs. `CRIC-Schema-and-Vocabulary-Registry.md` is authority rank 2, above every specialised document cited alongside it in this table; where a registry section and a specialised document's own wording differ in modal strength (e.g. row 4's MUST vs "should"), the registry's wording is authoritative.

**Two things this pass surfaced that are findings, not table fixes, and are out of this table's scope to correct:**
- `knowledge/OKF-Knowledge-Graph-Specification.md`'s own Node Categories list (row 2) still uses `Asset`, not `DataAsset` — the same drift ADR-0004 already named in `Core-Ontology-Specification.md`, now confirmed in a second file. Registry §3's Asset Resolution governs both.
- Rows 3 and 6 were previously ambiguous about whether registry §5/§6 belonged to Temporal or Knowledge-state; this pass resolves it by reading both specialised documents directly rather than by title correspondence, per the acceptance criterion this work package was scoped against.

**Practical consequence for scheduling build-time agents:** nothing outside Phase 0/1
should be dispatched to a build-time agent until Phase 1's exit criterion ("canonical
example OKF nodes validate") is met. This is a hard gate, not a soft preference — the
Repository Dependency doc's own Critical Path confirms it (`Core schemas → OKF parser
→ domain schemas → ...`).

---

## Phase-by-phase specialisation table

| Phase | Repo(s) | Authoritative PRD section(s) | Supporting sections | Freeze-point dependencies | Can run parallel with | Where mistakes happen |
|---|---|---|---|---|---|---|
| **0** — Organisation and Contracts | (all, scaffolding) | `CRIC-Repository-Dependency-and-Implementation-Sequence.md` §Phase 0 | `community/Open-Source-Governance.md`, `engineering/Security-and-Responsible-AI.md` §Git Security | none | n/a — must complete first | Skipping CODEOWNERS/branch protection setup because it "can be added later" — it gates Phase 7's review-integrity requirements |
| **1** — `cric-core` | `cric-core` | `knowledge/Core-Ontology-Specification.md`, `knowledge/OKF-Knowledge-Graph-Specification.md`, `knowledge/Temporal-and-Epistemic-Ontology.md`, `knowledge/Evidence-Provenance-and-Trust.md`, `CRIC-Schema-and-Vocabulary-Registry.md` | `knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md`, `ai/Responsible-Autonomy-and-HITL.md` (review contracts), `ai/Agent-Commons-Architecture.md` (agent manifest schema) | produces all 8, blocked on none | nothing meaningful — everything else depends on this | Producing all 8 freeze points from one document only; the freeze points are spread across 5 files and disagreements between them must resolve through the registry, not through whichever file the agent read first |
| **2** — `cric-knowledge` | `cric-knowledge` | `knowledge/OKF-Knowledge-Graph-Specification.md` | `product/Repository-and-System-Architecture.md` §`cric-knowledge` | 2, 5 | 3, 4 (once Phase 1 exits) | Building a parser that stores both directions of a relationship explicitly in frontmatter — **ruled** (retrieval-architecture thread): the compiler derives both directions from a single declared predicate; paired predicate names (`feeds`/`fed_by`) stay for authoring ergonomics only, not as two facts an author must keep in sync |
| **3** — `cric-data` | `cric-data` | `data/Data-Commons-Architecture.md` | `data/Ingestion-and-Licensing.md` (licence vocabulary only, not pipelines yet) | 4 | 2, 4 | Treating `Asset` as the schema type instead of the registry's canonical `DataAsset` (registry §3, Asset Resolution) |
| **4** — `cric-cryosphere` + `cric-glof` | `cric-cryosphere`, `cric-glof` | `domains/Cryosphere-Ontology.md`, `domains/GLOF-Ontology.md`, `domains/StateSnapshot-and-Event-Cube-Specification.md` | `knowledge/Core-Ontology-Specification.md` §Climate Risk Extension Types (Hazard/Trigger/Cascade must not be redefined, only extended) | 2, 3, 5, 6 | 2, 3 | Domain-specific redefinition of a core type instead of extension — `knowledge/Core-Ontology-Specification.md`'s own design rule ("domain repositories may extend the core ontology but must not redefine the semantic meaning of stable core types") is the direct test |
| **5** — `cric-ingest` | `cric-ingest` | `data/Ingestion-and-Licensing.md` | `data/Data-Quality-and-Validation.md`, `ai/Agent-Team-Specifications.md` (agents 1–7, Scout through Contradiction — this is the *first* phase where product-agent specs and build-time work meet directly) | 2, 3, 4 | none (needs Phase 3+4 output) | Building non-idempotent ingestion — `data/Ingestion-and-Licensing.md` §Idempotency is a named requirement, easy to treat as optional in a first pass |
| **6** — Graph Materialisation and Retrieval | `cric-core`/`cric-api` (initially) | `interfaces/Search-and-Graph-Interfaces.md` | *(pending)* new `engineering/Deterministic-Retrieval-Engine-Specification.md` | 2, 5, 6 | 7, 8 (once Phase 1 exits) | **Already has a full work-package breakdown from earlier today** — see the retrieval-architecture thread (root `9502c6df77...`) for the WP1–WP7 table, the predicate-conflict finding, and the two open governance calls. Do not re-derive this phase's scope from scratch; that thread's output is this phase's authoritative_prd_sections list once merged |
| **7** — `cric-review` | `cric-review` | `ai/Responsible-Autonomy-and-HITL.md` | `community/Volunteer-HITL-Workflow.md` | 6, 7 | 6, 8 | Building review state as ephemeral/in-memory instead of "review as repository state" — `ai/Responsible-Autonomy-and-HITL.md` §Review as Repository State is the explicit constraint, and Phase 14's pause/resume E2E test (R-022) will fail silently if this is wrong |
| **8** — `cric-agents` | `cric-agents` | `ai/Agent-Commons-Architecture.md` | `ai/Agent-Team-Specifications.md` (build only the v0.1 minimum set: Evidence Extraction, Entity Resolution, Ontology Watch, Provenance Auditor, Human Review Router) | 8 | 6, 7 | Conflating this build-time work with the product agents it produces — see Purpose section above. Also: giving early agents merge permission, which `ai/Agent-Commons-Architecture.md` §Agent Permissions explicitly withholds from most research agents |
| **9** — Event Cube Pipeline | (integration, no new repo) | `domains/StateSnapshot-and-Event-Cube-Specification.md` | everything from Phases 4, 5, 6, 8 | 2, 3, 5, 6 | none — integration phase, sequential by nature | Building positive Event Cubes only; the exit criterion explicitly requires "first positive Event Cube **and** first negative cube" — negative-case construction is easy to defer and then forget |
| **10** — `cric-models` | `cric-models` | `ai/Model-Commons-and-ML-Specification.md`, `data/Training-Data-and-Benchmark-Specification.md` | `knowledge/Temporal-and-Epistemic-Ontology.md` §Unknown Versus Negative (training-label semantics) | 3, 4 | none (needs Phase 9 output) | Auto-converting `unknown`/`unobserved`/`no_known_event` into negative training labels — explicitly prohibited by the registry §6 and restated in Training-Data spec |
| **11** — `cric-api` | `cric-api` | `interfaces/API-and-SDK-Specification.md` | `engineering/Software-Architecture.md` §Backend API (FastAPI) | none new (consumes Phases 1, 6) | 12 | Letting the API become a second source of truth — `product/Repository-and-System-Architecture.md` states `cric-api` "must not become the source of truth" |
| **12** — `cric-ui` | `cric-ui` | `interfaces/Human-Applications-and-UI.md` | `engineering/Software-Architecture.md` §Frontend (React/Vite/TS/MapLibre) | none new (consumes Phase 11) | 11 | Rendering candidate/agent-generated knowledge without visual distinction from accepted knowledge — R-039 in the traceability matrix exists specifically because this is easy to miss |
| **13** — Reference Dataset Expansion | `cric-data`, `cric-cryosphere`/`cric-glof` (content, not new code) | `data/Data-Quality-and-Validation.md` | `knowledge/Ontology-Evolution-and-Governance.md` (continuous gap detection must run *during* expansion, not after) | 6, 7 | n/a — depends on Phases 4–10 being functional | Scaling data volume before quality-gate automation exists, producing a backlog no human review queue can clear |
| **14** — Coordinated v0.1 Release | (all) | `engineering/Deployment-Versioning-and-Releases.md`, `CRIC-PRD-MASTER.md` §v0.1 Definition of Done | `engineering/Testing-and-Quality-Assurance.md` §Quality Gates | all | n/a — final gate | Treating the 10-point Definition of Done as a checklist to satisfy individually rather than one reproducible chain an external researcher can walk end-to-end |

---

## Parallel workstream summary

Directly from `CRIC-Repository-Dependency-and-Implementation-Sequence.md` §Parallel
Workstreams, confirmed against the phase table above: after Phase 1 exits, Knowledge
Commons (2), Data Commons (3), Cryosphere ontology (4), Agent runtime (8) and review
protocol (7) can all be staffed with build-time agents simultaneously — five
non-colliding specialists is the natural first wave, not one agent working
sequentially through fourteen phases.

Phases 9, 13 and 14 are integration/gate phases by construction and should not be
staffed with a dedicated build-time specialist in the same sense as 1–8, 10–12 — they
need a coordinator role that pulls from multiple upstream specialists' output, which
is squarely the Engineering Coordinator's half of this study.

---

## Resolved items from the retrieval-architecture thread

Both calls that gated Phase 2 and Phase 6 have landed and are no longer caveats:

- **Predicate conflict** — `connected_to` and `associated_with` are deprecated;
  `exposes`, `supported_by`, `threatens`, `depends_on` and `has_snapshot` are accepted
  as new canonical predicates; `caused_by` is rejected as redundant with `triggered_by`.
- **Reverse-adjacency** — the compiler derives both traversal directions from a single
  declared predicate (reflected in the Phase 2 row above); paired predicate names
  remain for authoring ergonomics only.
- Ashley has separately confirmed the candidate 13th Constitutional Product Rule: the
  LLM must not perform graph traversal; deterministic software assembles context first.

Phase 2 and Phase 6 build-time agents are unblocked.
