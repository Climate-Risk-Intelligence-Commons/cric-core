# Requirements

Extracted from the 7 PRD-classified documents in the ingest set:
`CRIC-PRD-MASTER.md` (precedence 1), `CRIC-Requirements-Traceability-Matrix.md`,
`product/Product-Vision-and-Principles.md`, `product/Product-Scope-and-Domain-Architecture.md`,
`community/Open-Source-Governance.md`, `community/Contribution-and-Review-Process.md`,
`implementation/CRIC-v0.2-Implementation-Specification.md`.

Requirement IDs R-001..R-041 are the corpus's own numbering and are preserved verbatim inside
the derived slug, because cross-document traceability in this corpus depends on them.
`acceptance:` for those entries is the matrix's own "v0.1 Verification" column.

---

## REQ-R-001-climate-risk-wide
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: CRIC is climate-risk-wide, with Cryosphere/GLOF first. Primary specification: Product Vision. Supporting: Core Ontology; Cryosphere Ontology; GLOF Ontology.
- acceptance: Core contains no unnecessary GLOF assumptions
- scope: product scope, core invariance, domain architecture

## REQ-R-002-immutable-evidence-lineage
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Immutable evidence lineage. Primary: Evidence, Provenance and Trust. Supporting: Data Commons; Model Commons; Testing.
- acceptance: End-to-end provenance test
- scope: provenance, lineage immutability

## REQ-R-003-derived-value-traceability
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Every significant derived value can answer "where did this come from?". Primary: Evidence, Provenance and Trust. Supporting: Search/Graph; UI; API.
- acceptance: Provenance traversal succeeds
- scope: provenance traversal, API, UI

## REQ-R-004-okf-first-class
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: OKF Markdown is a first-class product. Primary: OKF Knowledge Graph. Supporting: Human UI; Repository Architecture.
- acceptance: Vault opens and navigates independently
- scope: knowledge commons, Obsidian compatibility

## REQ-R-005-atomic-scientific-knowledge
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Atomic scientific knowledge. Primary: OKF Knowledge Graph. Supporting: Claims Lifecycle; Event Cube.
- acceptance: Atomicity fixtures validate
- scope: node atomicity rule, OKF

## REQ-R-006-multi-temporal-truth
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Multi-temporal truth. Primary: Temporal and Epistemic Ontology. Supporting: Event Cube; Search/Graph.
- acceptance: Historical-knowledge query test
- scope: temporal model, bitemporal query

## REQ-R-007-contradictions-preserved
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Contradictions are preserved. Primary: Claims/Contradictions. Supporting: Search/Graph; UI.
- acceptance: Contradictory claims retrieved together
- scope: claims, contradiction retrieval, UI

## REQ-R-008-pydantic-schema-authority
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Pydantic is schema authority. Primary: Software Architecture. Supporting: Core Ontology; Agent Commons; API.
- acceptance: Pydantic/JSON Schema tests
- scope: schema authority, validation, JSON Schema export

## REQ-R-009-agents-first-class-reusable
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Agents are first-class reusable components. Primary: Agent Commons. Supporting: Agent Teams; API; Software Architecture.
- acceptance: Agent reused with alternate dependencies
- scope: Agent Commons, reuse

## REQ-R-010-separable-agent-injection
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Tools, datasets, workspaces and dependencies are separately injectable. Primary: Agent Commons. Supporting: Software Architecture.
- acceptance: Composition contract test
- scope: dependency injection, agent composition contract

## REQ-R-011-deterministic-preferred
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Deterministic computation is preferred where suitable. Primary: Agent Commons. Supporting: Software Architecture; Ingestion.
- acceptance: Deterministic workflow fixtures
- scope: deterministic workflow layer, ingestion

## REQ-R-012-continuous-ontology-detection
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Ontology evolution is continuously detected. Primary: Ontology Governance. Supporting: Agent Teams.
- acceptance: Ontology Watch evaluation
- scope: ontology gap detection, Ontology Watch Agent

## REQ-R-013-governed-ontology-prs
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Stable ontology changes use governed PRs. Primary: Ontology Governance. Supporting: Contribution Process; Open Source Governance.
- acceptance: PR gate fixture
- scope: ontology governance, pull request workflow

## REQ-R-014-statesnapshot-first-class
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: StateSnapshot is first-class. Primary: Event Cube. Supporting: Core Ontology; GLOF Ontology.
- acceptance: Snapshot schema and immutability test
- scope: StateSnapshot, immutability

## REQ-R-015-event-cube-pre-post-reconstruction
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: GLOF Event Cube supports pre/post reconstruction. Primary: Event Cube. Supporting: GLOF Ontology; Training Data.
- acceptance: Reference cube reproduced
- scope: Event Cube, event reconstruction

## REQ-R-016-negative-cases-explicit
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Negative cases are epistemically explicit. Primary: Training Data. Supporting: Temporal/Epistemic; Registry.
- acceptance: Unknown-to-negative prohibition test
- scope: negative-case vocabulary, training labels

## REQ-R-017-training-lineage-reconstructable
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Training lineage is reconstructable. Primary: Training Data. Supporting: Model Commons; Provenance.
- acceptance: Model-to-source traversal
- scope: training data provenance, model lineage

## REQ-R-018-no-future-leakage
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Future information leakage is prohibited. Primary: Training Data. Supporting: Testing.
- acceptance: Cutoff/leakage tests
- scope: prediction cutoff, temporal leakage

## REQ-R-019-large-assets-not-in-git
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Large assets are not required in Git. Primary: Data Commons. Supporting: Repository Architecture; Ingestion.
- acceptance: Asset manifest test
- scope: storage tiers, DataAsset references

## REQ-R-020-licence-first-class
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Copyright and licence constraints are first-class. Primary: Ingestion/Licensing. Supporting: Security; Contribution.
- acceptance: Protected-paper workflow test
- scope: licensing, copyright, ingestion

## REQ-R-021-hitl-risk-based
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: HITL is risk based, not universal. Primary: Responsible Autonomy. Supporting: Volunteer HITL; Agent Teams.
- acceptance: Autonomy policy tests
- scope: autonomy levels, review routing

## REQ-R-022-durable-pause-resume
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Agents can pause and resume durably. Primary: Responsible Autonomy. Supporting: Software Architecture; Volunteer HITL.
- acceptance: Pause/resume E2E test
- scope: durable workflow state, review bundles

## REQ-R-023-level4-requires-human-review
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Level 4 safety-significant outputs require human review. Primary: Responsible Autonomy. Supporting: Security.
- acceptance: Bypass test must fail
- scope: autonomy Level 4, safety-significant interpretation

## REQ-R-024-no-government-warning-authority
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: CRIC never assumes government warning authority. Primary: Responsible Autonomy. Supporting: Security; Product Vision.
- acceptance: Prohibited-action tests
- scope: safety, prohibited autonomous actions

## REQ-R-025-deterministic-bounded-retrieval
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Graph retrieval is deterministic and bounded. Primary: Search/Graph. Supporting: Deterministic Retrieval Engine; API; Software Architecture.
- acceptance: Bounded traversal tests; ranking-reproducibility test (Testing/QA)
- scope: retrieval engine, traversal profiles, bounded traversal

## REQ-R-026-inspectable-context-packages
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: LLMs receive inspectable context packages. Primary: Search/Graph. Supporting: Deterministic Retrieval Engine; Agent Commons.
- acceptance: Retrieval reproducibility test; Context Package completeness/exclusions fields present
- scope: ContextPack, LLM read boundary

## REQ-R-027-completeness-separate-from-risk
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Evidence completeness is separate from hazard/risk. Primary: Data Quality. Supporting: UI; GLOF Ontology.
- acceptance: UI/schema distinction test
- scope: data quality, UI display

## REQ-R-028-materialised-databases-rebuildable
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Materialised databases are rebuildable. Primary: Software Architecture. Supporting: Search/Graph; Data Commons.
- acceptance: Rebuild integration test
- scope: graph materialisation, indexes

## REQ-R-029-offline-sovereign-deployment
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Local/offline/sovereign deployment is supported. Primary: Software Architecture. Supporting: Deployment; Data Commons.
- acceptance: Offline bundle test
- scope: deployment profiles, offline bundle

## REQ-R-030-multi-repository-from-v01
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Multi-repository architecture exists from v0.1. Primary: Repository Architecture. Supporting: Deployment; v0.1 Implementation.
- acceptance: Coordinated release manifest
- scope: repository family, releases

## REQ-R-031-repository-native-volunteer-review
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Volunteer review is repository native. Primary: Volunteer HITL. Supporting: Responsible Autonomy.
- acceptance: Git review workflow test
- scope: cric-review, Git-based review

## REQ-R-032-review-decisions-in-provenance
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Review decisions enter provenance. Primary: Responsible Autonomy. Supporting: Evidence/Provenance.
- acceptance: Decision-to-output traversal
- scope: review provenance

## REQ-R-033-scientific-vs-software-validation
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Scientific validation is distinct from software validation. Primary: Testing/QA. Supporting: Data Quality; Model Commons.
- acceptance: Separate QA artefacts
- scope: testing, scientific validation

## REQ-R-034-no-uncalibrated-probability-claims
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Model scores are not called probabilities without calibration support. Primary: Model Commons. Supporting: Training/Benchmark.
- acceptance: Calibration reporting test
- scope: model outputs, calibration

## REQ-R-035-replaceable-model-providers
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Model providers are replaceable. Primary: Agent Commons. Supporting: Software Architecture.
- acceptance: Alternate-provider test
- scope: model provider abstraction

## REQ-R-036-private-overlays-coexist
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Sensitive/private overlays can coexist with public schemas. Primary: Data Commons. Supporting: Security; Deployment.
- acceptance: Institutional profile design test
- scope: sovereign deployment, sensitive data

## REQ-R-037-core-extensible-to-other-hazards
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: CRIC Core remains extensible to other climate hazards. Primary: Core Ontology. Supporting: Product Vision; v0.2.
- acceptance: Second-domain extension test
- scope: core ontology extensibility

## REQ-R-038-releases-identify-versions
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Releases identify exact component versions. Primary: Deployment/Releases. Supporting: Repository Architecture.
- acceptance: Coordinated manifest
- scope: release manifest, versioning

## REQ-R-039-candidate-knowledge-visibly-distinct
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: Candidate agent knowledge is visibly distinct. Primary: Human UI. Supporting: Knowledge Lifecycle.
- acceptance: UI acceptance test
- scope: UI, candidate knowledge marking

## REQ-R-040-external-reproducibility
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: External researchers can reproduce the v0.1 evidence-to-model chain. Primary: v0.1 Implementation. Supporting: Testing; all core specifications.
- acceptance: v0.1 Definition of Done
- scope: v0.1 reproducibility

## REQ-R-041-llm-write-boundary
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: LLMs may write to the knowledge store only via structured mutation → validation → human/policy check → atomic write. Primary: Agent Commons. Supporting: Deterministic Retrieval Engine; Responsible Autonomy.
- acceptance: Write-boundary bypass test must fail
- scope: LLM write boundary, agent permissions
- NOTE: this requirement's ratification status is contested across three documents in the ingest set. See competing variants REQ-R-041-status-variant-a and REQ-R-041-status-variant-b below and the WARNING in `.planning/INGEST-CONFLICTS.md`. The substantive rule (the four-step write pipeline) is asserted identically by all three sources; only the ratification status differs.

## REQ-R-041-status-variant-a
- source: docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md
- description: R-041 is recorded as ratified — "ACCEPTED — Engineering Coordinator, `docs/OPEN_QUESTIONS.md` U5, channel event `7c037f772b9bb01b6b388ca4dea1ddc980b26738b08d721f35e7b0ac539041e1`, 2026-09-03T10:04:53Z".
- acceptance: Write-boundary bypass test must fail
- scope: R-041 ratification status

## REQ-R-041-status-variant-b
- source: docs/CRIC-PRD-v0.1/CRIC-Integration-Audit.md; docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- description: R-041 is recorded as not ratified. `CRIC-Integration-Audit.md` (batch 08): "A candidate requirement R-041 ... is pending Ashley's decision. It has been added to `CRIC-Requirements-Traceability-Matrix.md`, explicitly marked *PROPOSED — pending Ashley's decision, not yet ratified*, so its existence is visible for review without it being treated as an active requirement before that decision is made." `ai/Agent-Commons-Architecture.md`: "This write-side boundary is intentionally as strict as the read-side boundary above, even though it is not yet backed by its own numbered requirement. A dedicated traceability-matrix requirement for the write-side boundary specifically (candidate identifier \"R-041\") is under separate consideration; this document does not assume or cite that identifier."
- acceptance: (not stated as an active requirement by these sources)
- scope: R-041 ratification status

## REQ-v01-definition-of-done
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- description: v0.1 Definition of Done — an external technically competent researcher can (1) clone the relevant CRIC repositories; (2) inspect the Obsidian-compatible knowledge commons; (3) validate canonical OKF nodes; (4) reproduce a reference GLOF Event Cube; (5) create a provenance-linked TrainingSample; (6) run a baseline model; (7) trace its output back to original evidence; (8) inspect contradiction and uncertainty; (9) observe or complete a HITL review; (10) reproduce the component versions used.
- acceptance: all ten numbered capabilities are exercisable by an external researcher
- scope: v0.1 release gate

## REQ-v01-first-implementation-goal
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- description: CRIC v0.1 must make the chain source observation → provenance → normalised knowledge → state reconstruction → risk-relevant feature → model or rule → downstream consequence → human-reviewed interpretation visible, inspectable and reproducible.
- acceptance: the full chain is visible, inspectable and reproducible
- scope: v0.1 product question

## REQ-safety-statement
- source: docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md
- description: "CRIC v0.1 and v0.2 are research and reference implementations unless separately validated and authorised for operational use. Model scores, risk states and agent outputs must not be represented as official warnings merely because they are generated by CRIC."
- acceptance: (not separately enumerated in this document; enforced via R-024 prohibited-action tests)
- scope: safety, operational status, public communication

## REQ-product-mission
- source: docs/CRIC-PRD-v0.1/product/Product-Vision-and-Principles.md
- description: CRIC shall provide reusable infrastructure for climate-risk evidence integration; knowledge graph construction; temporal knowledge preservation; scientific provenance; data quality; contradiction management; reusable agent creation; model training and evaluation; cascading hazard reasoning; exposure and consequence analysis; open scientific collaboration.
- acceptance: (see REQ-success-criteria)
- scope: product mission

## REQ-success-criteria
- source: docs/CRIC-PRD-v0.1/product/Product-Vision-and-Principles.md
- description: CRIC succeeds when a knowledge repository can be cloned and opened in Obsidian; all important nodes validate against published schemas; a deterministic parser can reconstruct the graph; an agent can traverse relevant nodes without ad hoc file parsing assumptions; every derived output exposes provenance; historic knowledge states remain reconstructable; contradictory claims are preserved; reusable agents can be composed with different tools and datasets; model runs are reproducible; human review can resume paused workflows through repository artefacts; ontology changes can be proposed, reviewed and merged through standard pull requests.
- acceptance: all eleven success conditions hold
- scope: product success criteria

## REQ-design-invariants
- source: docs/CRIC-PRD-v0.1/product/Product-Vision-and-Principles.md
- description: The following must remain true across all CRIC releases — no significant evidence is destroyed by correction; no missing value is silently interpreted as low risk; no inferred claim is silently promoted to observed fact; no model output is confused with scientific consensus; no copyrighted source is redistributed without permission; no agent depends on globally mutable runtime state; no stable ontology change occurs without versioning; no safety-critical decision is delegated merely because an agent can technically execute it.
- acceptance: all eight invariants hold across every release
- scope: cross-release invariants

## REQ-product-values
- source: docs/CRIC-PRD-v0.1/product/Product-Vision-and-Principles.md
- description: Evidence Before Interpretation; Provenance Before Convenience; Open by Default; Uncertainty is Data; Contradiction is Valuable; Temporal Context is Mandatory; Human and Machine Readability; Modularity; Replaceability ("No single model provider, database engine, orchestration framework or cloud vendor should be structurally required"); Scientific Modesty.
- acceptance: (not separately enumerated)
- scope: product values, design philosophy

## REQ-product-non-goals
- source: docs/CRIC-PRD-v0.1/product/Product-Vision-and-Principles.md; docs/CRIC-PRD-v0.1/product/Product-Scope-and-Domain-Architecture.md
- description: CRIC Core is not required to make emergency declarations; replace government warning systems; guarantee model predictions; provide autonomous evacuation instructions; ingest every possible dataset into Git; impose one graph database; impose one LLM provider; impose one agent orchestration system; eliminate scientific disagreement. CRIC is not a single hazard dashboard; a single AI model; a single agent; a proprietary data warehouse; an autonomous government warning authority.
- acceptance: (negative scope; enforced by absence)
- scope: product non-goals

## REQ-domain-architecture
- source: docs/CRIC-PRD-v0.1/product/Product-Scope-and-Domain-Architecture.md
- description: The domain layering is CRIC Core → Climate Risk Ontology → Domain Ontology → Hazard/Application Package (worked example: CRIC Core → Climate Risk → Cryosphere → GLOF). Core Invariance Rule: nothing in `cric-core` should unnecessarily assume glacier, glacial lake, GLOF, Himalayan geography, satellite-only observation, one risk equation or one model family. Each domain publishes a versioned manifest (domain_id, name, version, parent_ontology, schema_dependencies, types, predicates, controlled_vocabularies, validators, migrations). A user should be able to install `cric-core + cric-knowledge + another future domain` without installing cryosphere/GLOF packages.
- acceptance: domain-neutral core schemas exist; Cryosphere extends rather than modifies core semantics; GLOF extends Cryosphere and Climate Risk; cross-domain predicates are possible; domain manifests are versioned; a second domain can be prototyped without redesigning core
- scope: domain architecture, core invariance, domain packages

## REQ-governance-model
- source: docs/CRIC-PRD-v0.1/community/Open-Source-Governance.md
- description: Separate governance for software, ontology, knowledge, datasets, models, agents and safety-relevant interpretation — "One approval rule should not govern everything." Roles: User, Contributor, Reviewer, Domain Reviewer, Ontology Reviewer, Maintainer, Core Maintainer. Maintainers may merge eligible PRs, manage releases, enforce policy, revert harmful changes and approve role assignments, but "must not silently rewrite historical scientific evidence." Scientific disagreement is represented in the graph rather than resolved through repository politics; a repository may accept two contradictory claims if both are validly sourced. Stable core ontology changes require proposal, evidence, impact analysis, tests, review and version change. Security vulnerabilities need a private reporting route. Operational warning authority remains with competent institutions.
- acceptance: governance roles documented; maintainer responsibilities defined; ontology governance linked to PR process; scientific contradiction policy exists; security reporting route defined; contribution and conduct documents exist
- scope: open-source governance, roles, safety governance

## REQ-contribution-process
- source: docs/CRIC-PRD-v0.1/community/Contribution-and-Review-Process.md
- description: Contribution types span software, documentation, OKF knowledge node, source/evidence addition, dataset manifest, training label, ontology proposal, model, agent, evaluation and review decision. A PR should state purpose, affected components, evidence where scientific, schema/ontology impact, licence impact, testing, migration impact and safety impact. New OKF knowledge must pass schema, ontology, provenance, licence and graph-link validation. Data contributions must include source, licence, acquisition method, version, hash/manifests and quality information. Ontology contributions must use OntologyProposal. Agent contributions must include manifest, Pydantic dependencies, output schema, toolsets, permission profile, evaluation suite and documentation. Model contributions must include model card, training provenance, evaluation, licence, artifact hash and limitations. Ground-truth-like training labels require evidence, and disputed labels must remain representable rather than forced into binary consensus. Reviewers separate code correctness, schema correctness, scientific validity, licensing, security, safety and documentation.
- acceptance: CONTRIBUTING document exists; PR templates exist; CODEOWNERS exists; knowledge/data/ontology/agent contribution paths are documented; automated checks block invalid merges; scientific disagreements can be represented without destructive resolution
- scope: contribution flow, PR requirements, review dimensions, CODEOWNERS

## REQ-v02-objectives
- source: docs/CRIC-PRD-v0.1/implementation/CRIC-v0.2-Implementation-Specification.md
- description: v0.2 objectives — scale the GLOF knowledge commons; automate more observation generation; expand agent teams; improve multimodal modelling; strengthen benchmark quality; support institutional deployments; prove extensibility toward additional climate-risk domains. Includes an Observation Factory expansion list, historical reconstruction across the Landsat/Sentinel archives, a candidate GLOF-SM model series (Vision, LakeChange, Susceptibility, Trigger, Fusion — "working identifiers"), an optional 50M-300M-parameter self-supervised cryosphere foundation encoder research track, fifteen additional reusable agents, typed and versioned agent workflow authoring, hybrid semantic search, institutional deployment hardening, benchmark expansion, structured scientific validation, one cross-domain pilot (landslide / extreme precipitation-flood / heat / wildfire) and community expansion. "Evaluation must test modality ablation and missing-data behaviour."
- acceptance: v0.2 Definition of Done — CRIC demonstrates that the same core contracts can support substantially larger cryosphere knowledge, richer agentic workflows, multimodal model research, institutional/private deployment and at least one second climate-risk domain without sacrificing provenance, temporal truth or inspectability
- scope: v0.2 scope, model expansion, agent expansion, cross-domain pilot

## REQ-v02-non-goals
- source: docs/CRIC-PRD-v0.1/implementation/CRIC-v0.2-Implementation-Specification.md
- description: Unless separately validated, v0.2 does not include autonomous official warning; replacement of government early-warning systems; exact-date GLOF prediction claims; universal climate-risk ontology completion. "v0.2 remains research infrastructure unless separate validation establishes operational suitability."
- acceptance: (negative scope; enforced by absence)
- scope: v0.2 non-goals, safety boundary
