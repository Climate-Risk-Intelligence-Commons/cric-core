# Climate Risk Intelligence Commons

### Climate-risk intelligence we can build together.

[![CI](https://github.com/Climate-Risk-Intelligence-Commons/cric-core/actions/workflows/ci.yml/badge.svg)](https://github.com/Climate-Risk-Intelligence-Commons/cric-core/actions/workflows/ci.yml)
[![Licence: AGPL-3.0](https://img.shields.io/badge/Licence-AGPL--3.0-blue)](LICENSE)

**People, software and AI agents. Shared evidence. Traceable knowledge.**

Climate Risk Intelligence Commons (CRIC) is building open-source infrastructure for
representing, connecting and analysing climate-risk evidence—and turning that
evidence into knowledge and intelligence others can inspect and reuse.

It brings together **knowledge, data, modelling and autonomous AI agents** on a
shared foundation. Human researchers, deterministic software that performs defined
calculations and checks, and agentic systems can collaborate on the same inspectable
evidence base: investigating questions, contributing findings and proposing improvements.

That foundation preserves where information came from, how it was transformed,
when it applied, and when the system learned it. Our ambition is a **durable
scientific memory for climate risk**, where evidence, uncertainty and history remain
traceable as understanding grows.

Whether you care about climate change and disasters, contribute scientific expertise,
build software or operate research agents, there is a place to begin here.

<details>
<summary><strong>Full product thesis</strong></summary>

Climate Risk Intelligence Commons (CRIC) is an open-source, provenance-preserving, temporally aware knowledge, data, modelling and agentic infrastructure for representing, integrating, analysing and deriving intelligence from climate-risk evidence. It is designed for human researchers, deterministic software and autonomous agents to operate on the same inspectable evidence base.

Source: [Master PRD — Product Thesis](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md#product-thesis).

</details>

> **Project stage: early development.** This README describes the CRIC ecosystem
> we are building. This repository, cric-core, contains its shared foundations
> and product specifications. [Build status](#build-status) distinguishes
> implemented capabilities from planned infrastructure.

[Why CRIC](#why-a-climate-risk-commons) ·
[First application](#starting-with-glacial-lake-outburst-floods) ·
[Traceability](#trace-every-contribution) ·
[Architecture](#how-the-pieces-fit) ·
[Agent participation](#agents-can-contribute) ·
[Get involved](#help-build-the-commons)

---

## Why a climate-risk commons?

Understanding climate risk means connecting observations, scientific studies and
models with the places and people exposed to harm. CRIC aims to make those
connections reusable across research groups, software pipelines and agent runs.

A researcher might frame a question. Software might calculate a feature from
observations. An agent might extract a candidate claim or identify conflicting
evidence. Another contributor should be able to inspect that work and continue it
without depending on the original conversation or a single tool provider.

The shared evidence base should let people and systems ask:

- **What supports this assessment?** Recover the observations, sources and calculations.
- **Who or what produced this insight?** Identify the contributor, software or agent run.
- **Which actions changed it?** Inspect transformations, proposed mutations, checks and decisions.
- **What did we know at the time?** Reconstruct earlier knowledge without silently adding later discoveries.
- **Where do sources disagree, and what is missing?** Examine uncertainty and competing claims explicitly.
- **Can the work be reproduced?** Recover its inputs, methods, parameters and versions.

**Commons** means a shared resource that humans and machines can inspect, challenge,
extend and reuse. The specifications, software and repository contribution process
are open. Source datasets retain their own licensing and access conditions.

Read the [vision and principles](docs/CRIC-PRD-v0.1/product/Product-Vision-and-Principles.md).

## Starting with glacial lake outburst floods

Our first application is **cryosphere risk**: risk involving Earth's snow, ice and
frozen ground. We begin with Himalayan **glacial lake outburst floods (GLOFs)**,
floods caused by a sudden release of water from a glacial lake.

Changing landscapes, observations across time, possible cascading triggers and
downstream exposure give us a concrete setting in which to develop and test
collaboration between scientific expertise, computation and AI.

### Follow one question through the evidence

*Illustrative research workflow, planned for CRIC:*

> How did a glacial lake change before an outburst, what evidence supports the
> proposed trigger, and which settlements and infrastructure lay downstream?

~~~mermaid
flowchart TD
    A[Research question from a person or agent] --> B[Sources and observations with identities and dates]
    B --> C[Software calculates lake-change measurements]
    C --> D[Agents propose claims and identify conflicting evidence]
    D --> E[Validation and applicable policy or human review]
    E --> F[Versioned knowledge, linked to evidence and run records]
    F --> G[Further research, models and consequence analysis]
    G --> A
~~~

An agent could discover relevant studies and prepare structured evidence
extractions. Software could derive a lake-area measurement from a satellite asset.
A second agent could propose a relationship between an observation and a trigger
claim, while preserving alternative explanations. Domain experts can contribute
interpretations and review work that needs their judgement.

Each contribution should retain its supporting evidence, producing method and
workflow status. A proposed inference remains distinguishable from an observation;
passing a structural check does not establish scientific correctness.

The planned **Event Cube** connects records from before, during and after an event
with sources, claims and consequences. It supports historical reconstruction and
model experiments, with controls to keep post-event information out of predictive
training inputs. Missing observations and conflicting interpretations remain visible.

Explore the [Event Cube specification](docs/CRIC-PRD-v0.1/domains/StateSnapshot-and-Event-Cube-Specification.md).

### Built to extend across hazards

The foundation is designed for future work on floods, droughts, landslides,
wildfire, heat, coastal hazards and their interactions. These are intended extensions.

Shared identities, provenance and contribution rules are intended to let domain
specialists and agent systems add knowledge while preserving connections across
hazards. A future domain package should be able to use CRIC without installing
cryosphere or GLOF packages.

## What makes CRIC distinctive?

These are commitments across the planned ecosystem:

| Commitment | What it enables |
|---|---|
| **Humans, software and agents collaborate** | Each can contribute through defined interfaces and permissions, using the same inspectable evidence base. |
| **Evidence travels with knowledge** | Insights and scientific relationships retain links to their sources and producing transformations. |
| **Actions are observable** | Run and change records show what was attempted, by which actor, with which tools, and with what outcome. |
| **History remains inspectable** | Event time, observation time, the period an assertion applies to, and the time CRIC learned it remain distinguishable. |
| **Uncertainty and disagreement remain visible** | Missing evidence is not low risk; conflicting claims can coexist; an accepted claim can still be uncertain. |
| **Autonomy follows the significance of the work** | Routine computation and candidate generation can proceed autonomously; oversight increases with uncertainty, consequence and authority. |
| **Components remain replaceable** | Knowledge, data, agents and models can be reused without requiring one database, model provider, cloud or agent framework. |

The [Master PRD](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md) sets out the constitutional rules.

## Trace every contribution

**Every scientific insight represented as a note, node or relationship should retain
a traceable connection to its evidence and the process that created or changed it.**

The planned traceability infrastructure connects three kinds of record:

| Record | What should be inspectable |
|---|---|
| **Provenance — where did it come from?** | Source identities and versions, acquisition dates, parent records, transformations, parameters, licences and content hashes where available. |
| **Explainability — what supports it?** | Methods, assumptions, supporting and conflicting evidence, uncertainty, and the recorded rationale for an interpretation or review decision. |
| **Observability — what happened?** | Actor and run identity; software, model, instruction and tool versions; actions, targets, timestamps, validation failures, retries and outcomes. |

Git commits and pull requests record repository changes. Scientific provenance
records the evidence and derivations behind them. Run records capture execution.
**These histories must connect:** from a changed scientific record to the producing
run, its inputs and transformations, and the applicable validation and review decisions.

For agent-generated knowledge, the specifications call for agent identity and version,
model/provider, instruction and tool versions, dataset versions, input/output nodes,
run identity and validation results. Reviews should bind to the exact artefact version
reviewed, and their effects should remain linked to downstream outputs.

### Relationships need evidence too

An edge such as “supports,” “contradicts” or “refines” carries scientific
meaning. Its basis, status and relevant time should be inspectable alongside those
of the nodes it connects. An inferred relationship must remain identifiable as such.

In CRIC's planned **Open Knowledge Format (OKF)**, a node combines a readable
Markdown note, structured metadata and typed relationships. This gives people and
software complementary views of the same record.

Provenance is recorded at the smallest level that materially affects reproducibility.
A meaningful calculation, filtering decision or scientific inference needs a traceable
record; a trivial formatting edit need not become a separate scientific node.
Repository edits still have their Git change history.

Corrections should preserve earlier accepted records through explicit supersession.
Audit records exclude secrets and avoid unnecessary personal or restricted data.
Hashes help establish integrity; they do not prove scientific truth.

Read the [provenance specification](docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md),
[knowledge format](docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md)
and [agent run and observability design](docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md#agent-run-provenance).

## How the pieces fit

**This is the target architecture; implementation starts with the core.**
Provenance, temporal context, validation and applicable review span every layer.

| Part | Purpose | Explore |
|---|---|---|
| **Core and shared vocabulary** | Shared identifiers, schemas and climate-risk concepts through which independent systems exchange knowledge | [Domain architecture](docs/CRIC-PRD-v0.1/product/Product-Scope-and-Domain-Architecture.md) |
| **Evidence and Data Commons** | Source catalogues, acquisition, licensing, versions and quality | [Data architecture](docs/CRIC-PRD-v0.1/data/Data-Commons-Architecture.md) |
| **Knowledge Commons** | Connected observations, claims, relationships, uncertainty and historical knowledge | [Knowledge specification](docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md) |
| **Domain packages** | Specialised concepts and rules, beginning with cryosphere and GLOF | [Cryosphere](docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md) |
| **Computation** | Deterministic retrieval, calculations and validation with reproducible inputs and outputs | [Retrieval](docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md) |
| **Agent Commons** | Reusable agents with configurable tools, datasets, models, permissions and observable runs | [Agents](docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md) |
| **Model Commons** | Traceable training samples, reproducible model runs and evaluation | [Models](docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md) |
| **Interfaces and review** | APIs and human workbenches, plus durable review decisions that workflows can act on | [Applications](docs/CRIC-PRD-v0.1/interfaces/Human-Applications-and-UI.md) · [Review](docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md) |

A **knowledge graph** records information and its relationships: which observation
supports a claim, which lake it describes, or which calculation produced a model
input. The Knowledge Commons is a product in its own right, designed to support
human research, deterministic software and agent workflows.

### The role of this repository

cric-core establishes the shared identifiers, schemas and versioning rules that
independently developed systems will use to exchange, validate and propose knowledge.
Every other repository in the CRIC architecture depends on it; **the core may not
depend on a domain-specific repository**.

The [Master PRD](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md) maps the specifications.
The [implementation sequence](docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md)
maps the repository family and its dependencies.

## Build status

As of 2026-09-05: cric-core ships an installable [Python package](pyproject.toml),
with CI enforcing lint, type, test and build checks on every commit. Specifications,
[architecture decisions](docs/DECISION_REGISTER.md) and an
[open-questions register](docs/OPEN_QUESTIONS.md) are published. Humans and
appropriately authorised agentic systems can already contribute through GitHub;
that route is distinct from the **planned CRIC agent runtime, knowledge-mutation
pipeline and connected observability infrastructure**, which — together with the
complete evidence-to-analysis workflow, reference Event Cubes, model pipelines and
public research interfaces — remain planned work.

<!-- BUILD-STATUS:START -->
(regenerated by `scripts/generate_build_status.py` on every CI run -- see decisions/0008)
<!-- BUILD-STATUS:END -->

See [Project Facts](docs/PROJECT_FACTS.md) for dated implementation records and
[GitHub Actions](https://github.com/Climate-Risk-Intelligence-Commons/cric-core/actions/workflows/ci.yml)
for build results.

### Where we are going

1. **Establish shared foundations** — identifiers, schemas, time, provenance and validation.
2. **Connect knowledge and data** — source catalogues, domain records, graph relationships and reproducible ingestion.
3. **Enable traceable collaborative workflows** — deterministic retrieval, durable review, observable agent runs and reference Event Cubes.
4. **Build and evaluate models** — training samples and model outputs linked to evidence, transformations and versions.
5. **Open up exploration** — APIs, research interfaces and a coordinated reference release.

The v0.1 milestone is a reproducible chain: an external researcher can reconstruct
a reference GLOF Event Cube, run a baseline model, trace its output to original
evidence, inspect uncertainty and observe or complete human review. Agent runs and
review decisions form part of that inspectable history.

[Read the full sequence and acceptance criteria](docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md).
Milestones follow dependencies rather than promised delivery dates.

> **Research scope:** CRIC v0.1 and v0.2 are research and reference implementations
> unless separately validated and authorised for operational use. Model and agent
> outputs are not official warnings.

## Help build the commons

**Contribute expertise, evidence, software or agent capabilities.** People can take
part directly, and agentic systems are welcome to initiate and carry forward work
within their permissions and the contribution process.

| Your interest | A useful place to start |
|---|---|
| **Climate change and disasters** | Read the vision, follow development and flag questions or confusing explanations. |
| **Education and communication** | Make terminology, evidence and research workflows accessible to wider audiences. |
| **Science and disaster-risk practice** | Propose sources, review scientific concepts or describe a research question. |
| **Data and mapping** | Suggest datasets with source/licence information, or identify gaps in quality and coverage. |
| **Software and modelling** | Develop shared contracts, reproducible calculations, validation or model evaluation. |
| **Agent systems and their builders** | Propose evidence-backed improvements through forks and PRs; help develop reusable agents, run records and interoperability. |
| **Research institutions and resourcing partners** | Discuss domain expertise, reference studies or support for open infrastructure. |

[Browse the issues](https://github.com/Climate-Risk-Intelligence-Commons/cric-core/issues)
or [open a proposal](https://github.com/Climate-Risk-Intelligence-Commons/cric-core/issues/new).
Describe the purpose, why it matters and the supporting sources. Some contribution
types depend on infrastructure still being built; a proposal helps scope that work.

### Agents can contribute

An appropriately authorised agentic system can fork the repository, work in its
own branch and submit a pull request. Existing contributors with write access can
use a branch in the shared repository. Both routes use the same contribution rules.

The intended contribution path is:

**Fork or branch → investigate and compute → prepare candidate changes → attach
evidence and run records → validate → open a PR → applicable review → merge and
preserve history.**

Scientific proposals should explain their sources, methods, producing actor/run,
changed records and relationships, uncertainty and validation results. Where
structured contribution tooling is still pending, make this information inspectable
in the PR and supporting artefacts using the applicable published specifications.

In the planned runtime, agents can discover sources, propose knowledge, detect
contradictions, audit provenance and prepare review bundles. They can pause and
resume from durable repository records without relying on a live chat session.

For access to CRIC knowledge, deterministic software assembles a bounded evidence
context for the model. Agents propose structured mutations through validation and
policy checks; they do not write directly into the canonical knowledge store.

### Autonomy and human participation

People can explore, contribute and review throughout the workflow. Routine
deterministic computation and provisional knowledge generation do not require
manual intervention at every step. The design permits promotion through defined
source rules, corroboration rules, human review or maintainer-approved workflows.

Stable core changes require maintainer approval; scientific agents do not
autonomously merge them. Safety-significant interpretations require human review,
and authoritative emergency action remains with competent institutions.

Read [Contributing](CONTRIBUTING.md), [Governance](GOVERNANCE.md),
the [Code of Conduct](CODE_OF_CONDUCT.md) and the
[responsible-autonomy specification](docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md).
Report vulnerabilities through the [security process](SECURITY.md).

You can **star the repository** to help others discover it or **watch it** to
follow development.

## For developers and agent builders

Requires **Python 3.12 or later**. Install the foundational package from source:

~~~sh
git clone https://github.com/Climate-Risk-Intelligence-Commons/cric-core.git
cd cric-core
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m pytest
~~~

The activation command is for bash/zsh. On Windows PowerShell, use
.venv\\Scripts\\Activate.ps1.

Start with the [Master PRD](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md) and
[Contributing](CONTRIBUTING.md). For agent integration, read the
[Agent Commons specification](docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md)
for context access, structured outputs, permissions, run provenance and evaluation.

Coding-agent sessions working on the repository should also read
[CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md). Those documents govern the
build-time team; the Agent Commons specification describes CRIC's product agents.

> **Research scope:** CRIC v0.1 and v0.2 are research and reference implementations
> unless separately validated and authorised for operational use. Model and agent
> outputs are not official warnings.

## Talk to us

For research collaboration, agent interoperability, provenance tooling,
reproducible scientific workflows, institutional partnership or funding discussions:

**Eyekyam Risk Resolutions**  
507, 5th Floor, Nirvana Courtyard, Sector 50, Gurgaon, Haryana – 122018

- [ashley@eyekyam.com](mailto:ashley@eyekyam.com) — CTO
- [vidya@eyekyam.com](mailto:vidya@eyekyam.com) — CEO

## Licence

cric-core is licensed under **AGPL-3.0**. See [LICENSE](LICENSE).

---

**Bring your questions, expertise, evidence, software or agents.
Help build climate-risk intelligence whose evidence and history remain open to inspection.**
