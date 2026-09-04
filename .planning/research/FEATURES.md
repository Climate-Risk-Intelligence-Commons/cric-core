# Feature Research

**Domain:** Open-source provenance-preserving climate-risk knowledge infrastructure (Python package / contract root)
**Researched:** 2026-09-04
**Confidence:** HIGH — derived directly from the 39-document PRD family, ratified ADRs, and CLAUDE.md operating rules

---

## Feature Landscape

### Table Stakes (Users Expect These)

These are the minimum capabilities every downstream repository (`cric-cryosphere`, `cric-glof`, `cric-api`, etc.) will assume exist in `cric-core`. Missing any of these causes dependent repos to either stall or paper over the gap with ad-hoc local definitions — exactly the proliferation problem the single-root architecture was designed to prevent.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Canonical identifier system** | Every cross-repo entity reference requires a stable, parseable, sortable ID | LOW | ✓ Done — FP1, ADR-0004. `CRIC:<ns>:<type>:<ulid>`, 12 namespaces, 32 tests green |
| **OKF base frontmatter schema** | All knowledge fragments must share a common header; without it every repo invents its own | MEDIUM | FP2 — active, not yet ratified |
| **Temporal + epistemic model** | Observation windows and belief timestamps are fundamental to time-series climate data; without them you cannot distinguish "not yet observed" from "false" | HIGH | FP3 — active; the `unknown ≠ false` invariant is a Constitutional Rule (Rule 6) |
| **Evidence-provenance chain schema** | Core value proposition of CRIC; "no value without provenance" is the product thesis, not a nice-to-have | HIGH | FP4 — active; every derived value must trace to source |
| **OKF relationship grammar** | Fragments relate to each other (supports, contradicts, refines, supersedes); without a canonical grammar each repo picks its own predicates | MEDIUM | FP5 — active |
| **Knowledge-state vocabulary (7-value)** | Downstream risk models cannot distinguish `unknown`, `unobserved`, `contradicted`, `confirmed` etc. without a shared enum | MEDIUM | FP6 — ratified (ADR-0007); code not yet written (WP-18) |
| **Review-decision schema** | HITL review produces structured artefacts that feed back into the graph; must be canonical | MEDIUM | FP7 — ratified (ADR-0007); code not yet written (WP-18) |
| **Agent manifest schema** | Every agent declares its input contracts and output types; without this no agent can be safely composed | MEDIUM | FP8 — active |
| **Pydantic models for every schema** | Runtime contract enforcement at import time; duck-typed contracts do not fail fast enough in multi-repo pipelines | MEDIUM | Applies to all 8 Freeze Points; generated JSON Schema published as artefact |
| **Published JSON Schema artefacts** | Non-Python consumers (TypeScript frontend, external validators) need machine-readable schemas | LOW | Generated from Pydantic; CI should publish on each release |
| **CI quality gates (ruff, mypy, pytest)** | Every PR to a downstream repo that imports cric-core must be able to trust the upstream is type-clean | LOW | ✓ Done — Phase 0; stays required for all subsequent phases |
| **Schema test suite per model** | Valid, invalid, boundary, and backwards-compat fixtures are required by the TQA spec for every Pydantic model | MEDIUM | Mandatory per `Testing-and-Quality-Assurance.md` |

### Differentiators (What Makes CRIC-Core Different)

These are the properties that justify building cric-core instead of using an existing knowledge-graph or provenance library. They map directly to the PRD's Constitutional Product Rules.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Contradiction-preserving graph** | Two validly sourced conflicting claims both live in the graph; contradiction is data, not an error to resolve (Rule 3) | HIGH | Most provenance systems merge or pick-winner; CRIC explicitly forbids silent resolution |
| **7-value epistemic vocabulary** | `unknown` ≠ `false` ≠ `unobserved` ≠ `no_known_event`; downstream risk scores cannot silently produce false negatives (Rule 6) | MEDIUM | Binary true/false is the default in every competitor system; 7 values is a hard differentiator |
| **Immutable evidence lineage** | Once a derivation chain is written, it cannot be altered — only superseded with a new chain (Rule 1) | HIGH | Requires append-only provenance semantics in the schema design |
| **Negative-test ratification bar** | Every Freeze Point closure must be stress-tested with a concrete counter-example from the PRD before sign-off | LOW | Governance feature, not code; prevents premature lock-in of under-specified schemas |
| **No orchestration framework lock-in** | Agents own their own loops; 23 product agents across 12 repos are not coupled to any single framework's upgrade cycle | MEDIUM | Explicit PRD decision; the manifest schema (FP8) enables composition without shared runtime |
| **Worktree-based multi-agent parallelism** | Multiple agents can work the same repo concurrently without checkout collision | LOW | Infrastructure already in place; pairwise-disjoint file sets enforced by CLAUDE.md |
| **Single canonical namespace registry** | 12 named namespaces, no aliases, no second ID format; prevents identifier proliferation across repos | LOW | ✓ Shipped as FP1; the registry is the governing artefact |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| **Domain ontologies in cric-core** | Convenient to have everything in one repo | Violates dependency direction — cric-core is the root; domain repos extend it, never the reverse; a domain ontology in core creates a coupling that blocks all 12 downstream repos from evolving independently | Put cryosphere/GLOF ontologies in `cric-cryosphere` / `cric-glof` (Phase 4) |
| **Graph query execution in cric-core** | Reduces the number of repos to set up | cric-core ships schemas, not a query engine; embedding retrieval here couples schema evolution to query performance and makes the package non-embeddable in lightweight contexts | Retrieval engine lives in `cric-api` (Phase 6) |
| **A second "human-friendly" ID format** | `CRIC-LAKE-001` is easier to read in docs | Two ID formats → two parsers → divergence bugs; ULID already provides sortability and uniqueness without coordination | Use the canonical `CRIC:<ns>:<type>:<ulid>` for production; short IDs appear only in fixtures and examples |
| **Auto-resolving contradictions** | Simplifies downstream consumers | Silently drops valid evidence; violates Rule 3 and produces false certainty in risk estimates | Represent both claims; let the review/HITL layer produce an explicit resolution artefact |
| **Binary knowledge states (true/false)** | Simplest possible model | Cannot express `unknown`, `unobserved`, `contradicted`; Rule 6 explicitly prohibits auto-converting these to false | Use the 7-value vocabulary (FP6) |
| **`unknown` auto-coerced to negative** | Feels safe to treat "no data" as "no event" | Is exactly how false negatives enter risk models; prohibited by Constitutional Rule 6 and registry §6 | `unknown` and `unobserved` must propagate explicitly; downstream models decide how to handle them |
| **LangGraph or similar as cric-core dependency** | Attractive tooling for agent orchestration | Couples all 23 agents across 12 repos to a single framework's upgrade cycle; any breaking change in LangGraph becomes a cric-core breaking change | Agents implement their own loops; FP8 manifest schema enables safe composition without shared runtime |

---

## Feature Dependencies

```
[FP1: Identifier system]
    └──required by──> [FP2: OKF frontmatter]  (frontmatter references IDs)
    └──required by──> [FP4: Provenance chain]  (chain nodes are identified entities)
    └──required by──> [FP8: Agent manifest]    (agents and their I/O are identified entities)

[FP2: OKF frontmatter]
    └──required by──> [FP5: Relationship grammar]  (relationships link identified OKF nodes)
    └──required by──> [FP3: Temporal model]         (temporal model annotates OKF nodes)
    └──required by──> [FP4: Provenance chain]       (provenance chains are OKF node metadata)

[FP3: Temporal model]
    └──required by──> [FP6: Knowledge-state vocabulary]  (states are time-stamped assertions)

[FP6: Knowledge-state vocab]
    └──required by──> [FP7: Review-decision schema]  (review produces state transitions)

[FP4: Provenance chain]
    └──enhances──> [FP6: Knowledge-state vocab]  (state transitions must be provenance-traced)

[FP7: Review-decision schema]
    └──required by──> [FP8: Agent manifest]  (agents declare review-decision output types)

[Schema test suite]
    └──required by──> ALL Freeze Points  (no FP ships without valid/invalid/boundary fixtures)
```

### Dependency Notes

- **FP1 must ship before everything else:** every other schema references IDs; this is why FP1 was Phase 0 and is already done.
- **FP2 (OKF frontmatter) gates FP3, FP4, FP5:** the frontmatter is the envelope; temporal, provenance, and relationship data all annotate or link OKF nodes.
- **FP6 and FP7 are ratified but unimplemented (WP-18):** the vocabulary design is locked; the Pydantic code is the immediate next deliverable, blocking anything that needs to express knowledge states.
- **FP8 (agent manifest) is last:** it depends on knowing what types agents produce (FP6/FP7) and what entities they reference (FP1).
- **Schema test suites are not a separate phase:** they are a mandatory deliverable concurrent with each FP's Pydantic implementation — the TQA spec requires them at the same commit.

---

## MVP Definition

### Phase 1 Exit (All 8 Freeze Points ratified + Pydantic-implemented, CI green)

This is the non-negotiable minimum before any downstream repo can safely build on cric-core. A partial set of Freeze Points is worse than none — dependent repos that start building against partial contracts will need retroactive migration.

- [x] FP1: Identifier system — **done**
- [ ] FP2: OKF base frontmatter — Pydantic model + schema tests + negative-test ratification
- [ ] FP3: Temporal + epistemic model — Pydantic model + schema tests + negative-test ratification (including `unknown ≠ false` counter-example)
- [ ] FP4: Provenance chain schema — Pydantic model + schema tests + immutable-lineage invariant demonstrated
- [ ] FP5: Relationship grammar — Pydantic model + schema tests + predicate vocabulary locked
- [ ] FP6: Knowledge-state vocabulary — Pydantic model + schema tests (ratified ADR-0007; WP-18 is the immediate next step)
- [ ] FP7: Review-decision schema — Pydantic model + schema tests (ratified ADR-0007; WP-18)
- [ ] FP8: Agent manifest schema — Pydantic model + schema tests + negative-test ratification
- [ ] Phase 1 exit gate: canonical example OKF nodes validate against all 8 FPs; CI green

### Add After Phase 1 Exits (Phase 2–3)

- [ ] Published JSON Schema artefacts from CI — downstream TypeScript consumers need this before Phase 12 frontend work begins
- [ ] Backwards-compatibility fixtures for every schema — required before Phase 4 domain repos start extending core types
- [ ] Semantic versioning and changelog discipline — multiple downstream repos will pin cric-core; they need clear migration signals

### Future Consideration (Phase 4+)

- [ ] Schema migration tooling — as FPs evolve post-v1, automated migration aids adoption by 12 downstream repos
- [ ] OKF validation CLI — `cric validate my-fragment.yaml` for human contributors; low priority until domain repos produce real OKF content
- [ ] Cross-repo integration test harness — verifies cric-core against a pinned snapshot of each domain repo; needed before any stable FP changes

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| FP6 + FP7 Pydantic code (WP-18) | HIGH | LOW (schema already ratified; code is mechanical) | **P1** |
| FP2: OKF frontmatter | HIGH | MEDIUM | **P1** |
| FP3: Temporal model | HIGH | HIGH (epistemic nuance; `unknown ≠ false` invariant) | **P1** |
| FP4: Provenance chain | HIGH | HIGH (immutability semantics, chain structure) | **P1** |
| FP5: Relationship grammar | HIGH | MEDIUM | **P1** |
| FP8: Agent manifest | HIGH | MEDIUM (depends on FP6/FP7 types being settled) | **P1** |
| Published JSON Schema artefacts | MEDIUM | LOW (CI step on top of Pydantic) | **P2** |
| Backwards-compat fixtures | MEDIUM | MEDIUM | **P2** |
| OKF validation CLI | LOW | MEDIUM | **P3** |
| Schema migration tooling | MEDIUM | HIGH | **P3** |

**Priority key:**
- P1: Must have for Phase 1 exit — blocks all downstream repos
- P2: Should have before Phase 4 domain work begins
- P3: Valuable, but can wait for product-market validation at domain level

---

## Competitor / Analogous System Analysis

cric-core is a research infrastructure package, not a user-facing product, so "competitors" are the systems it supersedes or draws from.

| Feature | W3C PROV-O | CIDOC-CRM | Nanopublications | CRIC approach |
|---------|------------|-----------|------------------|---------------|
| Provenance chain | Yes (Activity/Entity/Agent) | Yes (complex) | Yes (assertion + provenance + pubinfo) | FP4 — domain-specific, Pydantic-enforced, traceable to source evidence |
| Contradiction handling | No (merge expected) | No | No (each nanopub is atomic) | Explicit contradiction-preserving graph (Rule 3 — differentiator) |
| Epistemic states | No (binary assertion) | No | No | 7-value vocabulary (FP6 — differentiator) |
| Temporal model | Partial (timestamps) | Yes (complex) | Minimal | FP3 with `unknown ≠ false` invariant — climate-specific |
| Schema enforcement | RDF/OWL (runtime permissive) | RDF/OWL | RDF | Pydantic (strict, Python-native, fail-fast at import time) |
| Multi-repo contract root | No | No | No | Single canonical root; 12 downstream repos depend on it |

**Our approach beats alternatives here:** strict Pydantic enforcement, contradiction preservation, and the 7-value epistemic vocabulary are all absent from existing provenance standards. The trade-off is Python-centricity — non-Python consumers get JSON Schema artefacts, not native bindings.

---

## Sources

- `docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md` — 13 Constitutional Product Rules, authority precedence
- `docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md` — canonical vocabulary, registry §6
- `docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md` — dependency direction, layer boundaries
- `docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md` — test class requirements
- `CLAUDE.md` — Freeze Point ratification bar (negative-test requirement), Constitutional Rules 1, 2, 3, 6, 11, 13
- `.planning/PROJECT.md` — validated requirements, active work packages, out-of-scope inventory
- ADR-0004 (2026-08-29) — Identifier format ratification record
- ADR-0007 (2026-09-03) — Knowledge-state vocabulary + review-decision schema ratification record

---
*Feature research for: cric-core (Climate Risk Intelligence Commons — contract root package)*
*Researched: 2026-09-04*
