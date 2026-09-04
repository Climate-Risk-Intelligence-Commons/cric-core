# cric-core

### Climate Risk Intelligence Commons — the contract root

> Climate Risk Intelligence Commons (CRIC) is an open-source, provenance-preserving,
> temporally aware knowledge, modelling and agentic infrastructure for climate-risk
> evidence. It is designed for human researchers, deterministic software and
> autonomous agents to operate on the same inspectable evidence base.
>
> — [`CRIC-PRD-MASTER.md`](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md), Product Thesis

In plain terms: most climate-risk tools give you an answer. CRIC is built to also give
you the evidence behind the answer — what source produced it, what the system believed
at an earlier point in time, which scientific sources disagree, and which
transformation produced the number in front of you. That reconstructability, not any
single model or dashboard, is what CRIC is.

Cryosphere risk — starting with Himalayan Glacial Lake Outburst Floods (GLOF) — is the
first domain it's being built against. The architecture underneath is deliberately
hazard-agnostic: flood, drought, landslide, wildfire, heat, coastal and compound
hazards are the intended next domains, not a future rewrite.

`cric-core` is the contract root of the CRIC repository family: every other CRIC
repository depends on this one, and this one may not depend on any domain-specific
repository.

---

## What CRIC is built from

CRIC is layered infrastructure, not a single tool. Each layer has its own PRD chapter:

| Layer | What it does | Specification |
|---|---|---|
| CRIC Core | Identifiers, base contracts, versioning rules every other layer builds on | *this repository* |
| Climate Risk Ontology | Hazard-agnostic concepts shared across every domain (Hazard, Exposure, Consequence, Cascade…) | [`product/Product-Scope-and-Domain-Architecture.md`](docs/CRIC-PRD-v0.1/product/Product-Scope-and-Domain-Architecture.md) |
| Domain Ontologies | Domain-specific extensions — cryosphere and GLOF first | [`domains/`](docs/CRIC-PRD-v0.1/domains/) |
| Evidence and Data Commons | Data cataloguing, licensing, quality and ingestion | [`data/`](docs/CRIC-PRD-v0.1/data/) |
| Knowledge Commons | The OKF knowledge graph — provenance, temporal truth, contradiction kept as data, not noise | [`knowledge/`](docs/CRIC-PRD-v0.1/knowledge/) |
| Agent Commons | Reusable, typed, permissioned AI agents — not prompt wrappers | [`ai/Agent-Commons-Architecture.md`](docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md) |
| Model Commons | Reproducible model training and evaluation | [`ai/Model-Commons-and-ML-Specification.md`](docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md) |
| Computational Commons | Deterministic retrieval and computation, ahead of any LLM step | [`engineering/Deterministic-Retrieval-Engine-Specification.md`](docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md) |
| Interfaces | APIs, search, and human-facing applications | [`interfaces/`](docs/CRIC-PRD-v0.1/interfaces/) |
| Human Review and Governance | Where human judgement sits, and where it's mandatory | [`ai/Responsible-Autonomy-and-HITL.md`](docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md) |

Full layer definition: [`CRIC-PRD-MASTER.md` — Product
Layers](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md).

The near-term priority deliverable across these layers is the **OKF Knowledge
Graph** — the property-graph-style knowledge representation the Knowledge Commons
layer is built around, and the layer everything downstream (retrieval, agents,
models) reads from. Specification:
[`knowledge/OKF-Knowledge-Graph-Specification.md`](docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md).

---

## How it's built

Thirteen constitutional rules govern every layer above — among them: evidence lineage
is immutable, scientific contradiction is represented rather than erased, unknown is
not treated as negative, and agents operate through typed contracts rather than
open-ended autonomy. Full list: [`CRIC-PRD-MASTER.md` — Constitutional Product
Rules](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md).

CRIC is equally explicit about what it is *not* building:

- not a single hazard dashboard, a single AI model, or a single agent;
- not a proprietary data warehouse;
- not an autonomous government warning authority, and it does not replace one — CRIC
  never silently assumes institutional warning authority.

Full list: [`product/Product-Scope-and-Domain-Architecture.md` — Product
Non-Goals](docs/CRIC-PRD-v0.1/product/Product-Scope-and-Domain-Architecture.md) and
[`product/Product-Vision-and-Principles.md` —
Non-Goals](docs/CRIC-PRD-v0.1/product/Product-Vision-and-Principles.md).

---

## Where the build actually is

*(Deliberately short — see [`docs/PROJECT_FACTS.md`](docs/PROJECT_FACTS.md) for the
maintained detail behind every figure below.)*

As of 2026-09-03: the v0.1 specification — 39 PRD documents spanning product,
knowledge, domain, data, AI, interfaces, engineering, community and implementation —
is complete and under active, ratified revision. Of 8 Architecture Freeze Points, 3
are ratified (identifier format; knowledge-state vocabulary; review-decision schema)
and 1 is implemented as tested code
([`src/cric_core/identifiers/`](src/cric_core/identifiers/), 32 passing test cases
across 21 test functions, one parametrized). This is a spec-complete, early-build
project: most of what's described above is design-complete rather than code-complete
today, and this paragraph is written to keep saying so for as long as that's true.

<details>
<summary>This paragraph is a snapshot, not a promise — the mechanism keeping it honest</summary>

Every commit changes what's built. This paragraph is hand-maintained today. The
stronger fix — a CI-generated status, so a stale number becomes a build failure
instead of a silent drift — is a named, tracked work item that has not started yet,
not work already in motion. Until it ships, treat the date above as this paragraph's
real expiry, not a formality.

</details>

---

## Roadmap

No delivery dates — CRIC is sequenced by dependency, not by calendar, and we'd rather
say that plainly than invent a date. Full detail, including the dependency graph and
per-phase acceptance criteria:
[`CRIC-Repository-Dependency-and-Implementation-Sequence.md`](docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md).

<details>
<summary>15 phases, dependency-ordered</summary>

0. **Organisation and Contracts** — repositories, branch protection, licences, CI
   skeletons.
1. **`cric-core`** *(in progress)* — implemented first; every other repository
   consumes its contracts.
2. **`cric-knowledge`** — the knowledge commons implementation.
3. **`cric-data`** — the evidence and data commons implementation.
4. **`cric-cryosphere` and `cric-glof`** — domain schemas and controlled
   vocabularies.
5. **`cric-ingest`** — deterministic acquisition and normalisation.
6. **Graph Materialisation and Retrieval**.
7. **`cric-review`** — human review and governance workflows.
8. **`cric-agents`** — reusable agent infrastructure.
9. **Event Cube Pipeline** — integrating domain, ingestion, retrieval and agents.
10. **`cric-models`** — model training and evaluation.
11. **`cric-api`**.
12. **`cric-ui`**.
13. **Reference Dataset Expansion**.
14. **Coordinated v0.1 Release** — the point an external researcher can clone,
    reproduce and audit the whole chain.

</details>

---

## Everything here is open

The specification, the decision records, the architecture — all of it, not just the
code. [`docs/CRIC-PRD-v0.1/`](docs/CRIC-PRD-v0.1/) is the authoritative,
continuously-updated PRD; [`decisions/`](decisions/) holds every ratified
architecture decision with its approver and evidence; `docs/OPEN_QUESTIONS.md` tracks
what's still unresolved, in the open, rather than off-repo. Nothing that shapes this
project happens somewhere a contributor can't read it.

## Get involved

- **Clone:**

  ```sh
  git clone https://github.com/Climate-Risk-Intelligence-Commons/cric-core.git
  ```

- **Specification:** starts at
  [`docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md`](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md).
- **Contributing:** [`docs/CRIC-PRD-v0.1/community/Contribution-and-Review-Process.md`](docs/CRIC-PRD-v0.1/community/Contribution-and-Review-Process.md).
  Machine-facing operating rules for this repository: [`CLAUDE.md`](CLAUDE.md) (how
  work is done) and [`AGENTS.md`](AGENTS.md) (who does what).

## Talk to us

For research collaboration, institutional partnership, or funding discussions:

**Eyekyam Risk Resolutions**
507, 5th Floor, Nirvana Courtyard, Sector 50, Gurgaon, Haryana – 122018

- [ashley@eyekyam.com](mailto:ashley@eyekyam.com) (CTO)
- [vidya@eyekyam.com](mailto:vidya@eyekyam.com) (CEO)

## Licence

AGPL-3.0. See [`LICENSE`](LICENSE).
