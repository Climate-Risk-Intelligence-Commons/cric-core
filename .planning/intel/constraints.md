# Constraints

Extracted from the 30 SPEC-classified documents in the ingest set. Entry `type` is one of
`api-contract | schema | nfr | protocol`.

`CRIC-Schema-and-Vocabulary-Registry.md` carries per-doc precedence 0 (highest in this ingest)
and its constraints override any contradicting constraint from another document. Where another
document's content diverges from the registry, the divergence is recorded in
`.planning/INGEST-CONFLICTS.md` rather than silently rewritten here; both the registry's form
and the divergent document's form are preserved below under their own sources.

---

# CRIC-Schema-and-Vocabulary-Registry.md (precedence 0)

## Canonical naming rules
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 1 — project name "Climate Risk Intelligence Commons (CRIC)"; first domain Cryosphere with GLOF the first hazard workflow; canonical knowledge format OKF Markdown (Markdown + YAML frontmatter); runtime schema authority Pydantic; canonical knowledge is version-controlled OKF, with databases and indexes as materialisations; significant historical knowledge is preserved and supersession does not delete prior assertions.

## Canonical identifier form
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 2 — `CRIC:<namespace>:<type>:<ulid>`. Examples `CRIC:core:claim:01J...`, `CRIC:cryosphere:glacial_lake:01J...`, `CRIC:glof:event:01J...`. Human-facing short IDs (`CRIC-LAKE-001`) permitted in examples and fixtures only; MUST NOT be the canonical production identifier format.

## Canonical root object types and core type list
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 3 — root hierarchy `CRICObject` → {KnowledgeObject, ResourceObject, ComputationalObject, GovernanceObject, QualityObject}. Canonical core types: Entity, Event, Observation, StateSnapshot, Claim, Evidence, Assessment, Source, Dataset, DatasetVersion, DataAsset, Licence, Workflow, TraversalProfile, Agent, AgentRun, Toolset, Model, ModelRun, TrainingRun, EvaluationRun, TrainingSample, Label, FeatureSet, Prediction, ContextSubgraph, ContextPack, ReviewRequest, ReviewDecision, OntologyProposal, MigrationRecord, ProvenanceRecord, QualityAssessment, UncertaintyAssessment.

## Knowledge state vocabulary
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 4 — closed workflow status vocabulary: candidate, accepted, disputed, superseded, rejected, withdrawn, archived. Recommended structure `knowledge_state: {status, origin, verification: {method, verified_by, verified_at}}`. "`scientific_confidence` or epistemic confidence MUST remain separate from workflow status."

## Epistemic status vocabulary
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 5 — closed epistemic vocabulary: observed, reported, derived, inferred, simulated, hypothesised, disputed, unknown.

## Negative-case vocabulary
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 6 — closed training/evidence vocabulary: confirmed_negative, probable_negative, no_known_event, unknown, unobserved, not_applicable. "`unknown`, `unobserved`, and `no_known_event` MUST NOT be automatically converted to negative training labels."

## Multi-temporal model block
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 7 — canonical temporal block `temporal: {event_time: {start, end, precision}, observation_time: {start, end, acquisition_time}, valid_time: {from, to}, system_time: {created_at, updated_at, superseded_at}}`. "CRIC describes this as multi-temporal, with tri-temporal truth at its core: event/world time, valid time, and system/knowledge time, while observation/acquisition time remains explicitly represented."

## Canonical relationship predicates
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 8 — core scientific/evidential predicates: supports, supported_by, contradicts, refines, supersedes, superseded_by, corroborates, disputes, derived_from, consistent_with, inconsistent_with. Spatial/domain predicates: located_in, part_of, contains, depends_on, feeds, fed_by, drains_to, upstream_of, downstream_of, adjacent_to, intersects, overlaps, within, terminates_at, terminates_in, dammed_by, exposed_to, exposes, experienced, impacted, threatens, triggered_by, observed_by. Structural: has_snapshot. Deprecated and removed: `connected_to`, `associated_with`. Rejected: `caused_by` (redundant with `triggered_by`). "Predicates MUST be registered and versioned."

## Evidence and provenance levels
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 9 — canonical conceptual lineage L0 Source Evidence → L1 Normalised Data → L2 Knowledge → L3 Derived Features → L4 Model Output → L5 Interpretation → L6 Decision Intelligence. "Every significant derived object MUST support backward traversal."

## Canonical review states and decision values
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 10 — repository queue/state vocabulary: inbox, assigned, in-review, approved, rejected, needs-more-evidence, disputed, escalated, archived. Canonical `ReviewDecision.decision` values: approve, reject, modify, needs_more_evidence, disputed, escalate. "The queue folder name and decision value are deliberately different grammatical forms."

## Autonomy levels
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: protocol
- content: Section 11 — Level 0 unrestricted deterministic computation; Level 1 autonomous analytical generation; Level 2 autonomous provisional knowledge; Level 3 trusted scientific graph promotion; Level 4 safety-significant interpretation; Level 5 authoritative action by competent external institution.

## Canonical repository names
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 12 — cric-core, cric-knowledge, cric-data, cric-ingest, cric-cryosphere, cric-glof, cric-models, cric-agents, cric-api, cric-ui, cric-docs, cric-review. `cric-review` is canonical because HITL is a first-class workflow layer.

## Canonical GLOF analytical decomposition
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 14 — Lake Evolution → Susceptibility → Trigger Conditions → Failure State/Mechanism → Flood Propagation → Exposure → Vulnerability → Consequence → Decision-Support Interpretation.

## Canonical data formats
- source: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md
- type: schema
- content: Section 15 — Markdown + YAML for OKF knowledge; JSON / JSON Schema for machine contracts; GeoJSON for small interoperable geometry; GeoParquet for analytical vector data; COG for large rasters; STAC for EO cataloguing and asset references.

---

# CRIC-Repository-Dependency-and-Implementation-Sequence.md

## Repository dependency spine
- source: docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md
- type: schema
- content: `cric-core` is the root; cric-knowledge, cric-data, cric-cryosphere (→ cric-glof), cric-ingest, cric-agents, cric-models, cric-review, cric-api, cric-ui depend on it. "Operationally, several repositories depend on more than one upstream package. The diagram expresses the architectural spine rather than every package-manager dependency."

## Phase exit criteria
- source: docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md
- type: protocol
- content: Phase 0 exit — repositories exist and `cric-core` can publish a versioned Python package. Phase 1 exit — canonical example OKF nodes validate. Phase 2 exit — knowledge-only deployment works without API/database. Phase 3 exit — small and large assets can be represented without ambiguity. Phase 4 exit — one manually curated historical event validates. Phase 5 exit — one source-to-observation workflow is reproducible. Phase 6 exit — multi-hop retrieval requires no manual LLM file crawling. Phase 7 exit — a synthetic workflow pauses and resumes through Git/local review. Phase 8 exit — the same agent can run with different injected dataset/workspace/model configurations. Phase 9 exit — first positive Event Cube and first negative cube are reproducible. Phase 10 exit — model output traces to original source evidence.

## Phase 1 cric-core build order
- source: docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md
- type: protocol
- content: 1. identifier types; 2. knowledge-state models; 3. temporal models; 4. spatial models; 5. provenance; 6. base object hierarchy; 7. relationship model; 8. ontology registry; 9. review contracts; 10. validation framework; 11. JSON Schema export.

## Phase 14 coordinated release evidence
- source: docs/CRIC-PRD-v0.1/CRIC-Repository-Dependency-and-Implementation-Sequence.md
- type: protocol
- content: Required evidence for the coordinated v0.1 release — tests; release manifest; compatibility matrix; reference Event Cube; reference benchmark; baseline model; agent/HITL demonstration; workbench; reproducibility instructions.

---

# knowledge/OKF-Knowledge-Graph-Specification.md

## Universal OKF frontmatter contract
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: schema
- content: Reference base frontmatter carries okf_version, cric_schema_version, ontology_version, id, type, subtype, title, aliases; `knowledge_state` {status, origin, accepted_at, rejected_at, superseded_at}; `temporal` {event_time, observation_time, valid_time, system_time}; `spatial` {geometry, geometry_ref, centroid, bbox, crs, elevation_m, administrative_units, basin_ids}; `epistemic` {status, confidence, confidence_method, uncertainty, completeness}; `provenance` {source_nodes, source_uris, parent_nodes, transformations, software, software_version, agent_run_id, human_review_ids, content_sha256}; `licensing` {licence, licence_uri, attribution, redistribution, derivative_use, notes}; `relationships`; `tags`.

## Canonical node model
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: schema
- content: Every knowledge node is YAML frontmatter + human-readable Markdown body + typed links to other CRIC nodes. The Markdown repository is a first-class scientific artefact and must remain human-readable, machine-parseable, Git-diffable, Obsidian-compatible, programmatically traversable, agent-friendly, versionable and provenance-preserving.

## Time precision vocabulary
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: schema
- content: Allowed values should include exact, second, minute, hour, day, month, year, approximate, estimated, inferred, bounded, unknown.

## Relationship grammar and adjacency derivation
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: protocol
- content: Every relationship supports `{predicate, target, confidence, status, source_nodes, valid_time: {from, to}}`. Adjacency Derivation: a relationship is declared on only one of its two participating nodes; the runtime graph compiler derives both `out_edges` on the source and `in_edges` on the target automatically. Paired predicate names (`feeds`/`fed_by`, `supports`/`supported_by`) exist purely as an authoring convenience. "If both directions of what is semantically the same relationship are ever declared independently, the compiler must treat this as a duplicate edge and resolve it through canonical-direction deduplication, not materialise it as two live edges." The document states `CRIC-Schema-and-Vocabulary-Registry.md` section 8 is the sole authority for the canonical predicate list and its own list is illustrative.

## Atomicity rule
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: protocol
- content: A separate node should be created when the information has independent provenance, temporal validity, scientific significance, uncertainty, contradiction potential, graph connectivity, training relevance or review status. "A scalar field should not automatically become a node."

## Persistent identity versus state
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: protocol
- content: Persistent entities must not accumulate changing state directly when that state has independent scientific meaning. The entity node represents identity; Observation nodes represent measured state; StateSnapshot nodes represent coherent temporal context; Claim nodes represent scientific assertions; Event nodes represent real-world occurrences.

## Data asset node required fields
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: schema
- content: Large files remain outside Git but must have OKF nodes with canonical URI, original source URI, SHA-256, byte size, media type, provider, licence, acquisition time, spatial coverage, temporal coverage and availability status.

## Copyrighted publication handling
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: nfr
- content: Papers may be represented as source nodes even when not redistributable. Allowed: title, authors, DOI, bibliographic metadata, licence, source URI, CRIC-generated summary, structured claims, relationships, provenance. "Protected content must not be copied beyond lawful limits."

## Reference parser requirements
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: api-contract
- content: A reference parser must parse YAML safely; validate against Pydantic schemas; resolve node IDs; build adjacency indexes; detect broken edges; detect duplicate IDs; validate temporal structures; expose relationship traversal; preserve source line/file locations for diagnostics.

## Validation levels
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: protocol
- content: Syntax validation (YAML parses, required fields exist); Schema validation (Pydantic passes); Ontology validation (types and predicates allowed); Graph validation (targets resolve); Temporal validation (times internally consistent); Provenance validation (required lineage exists); Scientific review (separate from structural validation).

## File naming and identity
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: schema
- content: Recommended pattern `<type>--<short-human-name>--<id-fragment>.md`. "Node IDs, not filenames, are the authoritative identifiers." Each node carries OKF version, CRIC schema version and ontology version. "Schema migrations must not silently rewrite semantic meaning."

## Graph materialisation is non-canonical
- source: docs/CRIC-PRD-v0.1/knowledge/OKF-Knowledge-Graph-Specification.md
- type: nfr
- content: Optional materialisations include DuckDB, PostgreSQL/PostGIS, NetworkX, graph databases, full-text indexes and vector stores. "None are canonical. All should be rebuildable from CRIC source artefacts."

---

# knowledge/Core-Ontology-Specification.md

## Ontology design rules
- source: docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md
- type: protocol
- content: CRIC Core remains deliberately small; domain-specific meaning belongs in domain repositories. "Domain repositories may extend the core ontology but must not redefine the semantic meaning of stable core types." Every type has canonical identifier, canonical name, definition, parent type, ontology version introduced, status, aliases and constraints. Inheritance must be semantically meaningful, not a file-organisation device. Important relationships must use controlled predicates rather than being hidden in prose. A value remains an embedded field when it has no independent scientific lifecycle; it becomes a node when it has independent provenance, uncertainty, temporal validity, contradiction potential, review state, graph relationships or training value.

## Root type hierarchy
- source: docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md
- type: schema
- content: `CRICObject` → KnowledgeObject {Entity, Event, Observation, StateSnapshot, Claim, Evidence, Assessment}; ResourceObject {Source, Dataset, DatasetVersion, Asset, Licence}; ComputationalObject {Workflow, Agent, AgentRun, Toolset, Model, ModelRun, TrainingSample, Label, Prediction}; GovernanceObject {ReviewRequest, ReviewDecision, OntologyProposal, MigrationRecord}; QualityObject {ProvenanceRecord, QualityAssessment, UncertaintyAssessment}. NOTE: this list diverges from the registry's canonical core-type list (uses `Asset` not `DataAsset`; omits TrainingRun, EvaluationRun, FeatureSet, TraversalProfile, ContextSubgraph, ContextPack). Registry §3 governs — see `.planning/INGEST-CONFLICTS.md`.

## CRICObject inherited fields
- source: docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md
- type: schema
- content: Every canonical CRIC object inherits id, type, subtype, title, aliases, schema_version, ontology_version, knowledge_state, temporal, provenance, licensing, relationships, tags.

## Core type semantics
- source: docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md
- type: schema
- content: `Entity` — persistent identifiable thing whose identity continues while state changes; must not be overwritten with historical measurements. `Event` — occurrence situated in time; requires temporal extent or uncertainty, participating entities where known, evidence, and location where relevant. `Observation` — {subject_id, variable, value, unit, method, observation_time, source, quality, uncertainty}; "Observation values must not be silently changed. Corrections create a superseding observation." `StateSnapshot` — {subject_id, snapshot_time, included_observations, derived_features, context_nodes, completeness, conflicts}; references observations rather than duplicating provenance. `Claim` — {subject, predicate, object/value, claim_text, claimant, evidence_nodes, confidence, status, spatial_scope, temporal_scope}. `Evidence` — "Evidence does not automatically imply truth." `Assessment` — must identify subject, method, evidence, assumptions, uncertainty, assessor, assessment time, operational status. `Dataset`/`DatasetVersion` — "Every training or modelling workflow must depend on DatasetVersion rather than mutable Dataset identity."

## Climate risk extension types
- source: docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md
- type: schema
- content: Hazard, HazardProcess, Trigger, Exposure, Vulnerability, Consequence, Risk, Scenario, Indicator, Threshold, Alert, Intervention, Control, Cascade, CompoundEvent. "Hazard must be separated from exposure, vulnerability and consequence." A trigger may itself be another hazard event. Cascade represents causal or contributory propagation across multiple events, and "each edge must retain evidence and confidence where appropriate."

## Controlled vocabulary governance
- source: docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md
- type: protocol
- content: Controlled vocabularies must have stable IDs, definitions, aliases, status, source, version introduced and deprecation metadata. "Free-text values should not be used where a stable controlled vocabulary is necessary for programmatic comparison."

## Pydantic representation and ontology registry
- source: docs/CRIC-PRD-v0.1/knowledge/Core-Ontology-Specification.md
- type: api-contract
- content: Every stable core type should have a Pydantic model, generated JSON Schema, OKF mapping, example fixture and validation tests. "Schema generation must be deterministic." `cric-core` publishes a machine-readable ontology registry with `ontology_id`, `version`, `types: [{id, name, parent, status}]`, `predicates: [{id, name, status}]`.

---

# knowledge/Temporal-and-Epistemic-Ontology.md

## Four temporal dimensions
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: schema
- content: Event time (when the real-world phenomenon occurred); observation time (when acquired or made); valid time (period for which a state, claim or interpretation applies); system time (when CRIC knew or stored it — created_at, updated_at, superseded_at, review time, ingestion time). Reference schema adds `precision` and `uncertainty` to event_time, `precision` to observation_time and `open_ended` to valid_time. "CRIC must preserve all four."

## Partial and uncertain dates
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: nfr
- content: CRIC must support exact timestamp, date only, month only, year only, bounded interval, before, after, approximately, inferred interval and unknown. "Do not invent a precise timestamp to satisfy a schema." Temporal precision vocabulary: second, minute, hour, day, month, year, interval, approximate, estimated, inferred, unknown.

## Temporal conflict preservation
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: protocol
- content: "Conflicting dates must be preserved." CRIC should create separate claim or event-time assertion nodes where the disagreement is scientifically relevant; a reconciliation assessment may later state a preferred date while retaining both sources.

## Bitemporal query requirement
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: api-contract
- content: At minimum CRIC must answer "What was considered valid on date X?" and "What did CRIC know on date Y?" — "This is the basis of historical knowledge reconstruction."

## Snapshot immutability rule
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: protocol
- content: "A `StateSnapshot` is immutable once accepted." If additional evidence changes the reconstructed state: create a new snapshot, link it with `supersedes`, preserve the earlier snapshot.

## Confidence representation
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: schema
- content: "Confidence should not be treated as a universal probability. Every confidence value should identify its meaning or method." Reference form `confidence: {value, scale, method}`; methods may include model probability, inter-rater agreement, source reliability rubric, measurement uncertainty, deterministic certainty.

## Unknown versus negative
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: protocol
- content: CRIC must distinguish false, absent, not detected, no known evidence, unknown, unobserved, not applicable. "This distinction is mandatory for training-data construction."

## Three-way reconciliation
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: protocol
- content: Conflicting or updated information is analysed from three simultaneous perspectives — world-time, evidence-time and knowledge-system. "This prevents retrospective knowledge from being incorrectly projected backwards."

## Temporal agent prohibitions
- source: docs/CRIC-PRD-v0.1/knowledge/Temporal-and-Epistemic-Ontology.md
- type: protocol
- content: Temporal reconciliation agents must never overwrite an earlier assertion merely because a later source exists; invent precision; collapse `unknown` into `false`; or convert inference into observation. They may create candidate reconciliations, identify temporal conflicts, propose supersession and request human review.

---

# knowledge/Evidence-Provenance-and-Trust.md

## Provenance record schema
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: schema
- content: `ProvenanceRecord` reference structure — id, type, object_id; `source` {node_ids, uris, provider, version}; `acquisition` {retrieved_at, method, actor}; `parents`; `transformation` {workflow_id, step_id, software, software_version, parameters, deterministic}; `agent` {agent_id, agent_version, run_id, model}; `human_reviews`; `integrity` {content_sha256, parent_hashes}; `licensing` {licence, redistribution, derivative_use}.

## Reference evidence chain
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: protocol
- content: Source → Acquired Asset → Normalised Asset → Observation → Feature → Claim → Assessment → Prediction/Decision-Support Output. "Not every workflow uses every stage, but missing stages must not be invented."

## Immutable lineage
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: protocol
- content: "Lineage records must not be rewritten to make a later workflow appear cleaner." If provenance metadata was incorrect: create a corrected record, link with `supersedes`, preserve the original.

## Hashing
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: nfr
- content: "SHA-256 is the minimum reference algorithm for v0.1." Hashes generated for canonical files, externally acquired assets where bytes are available, dataset manifests, model artefacts and release manifests. For externally changing URLs, URI identity is insufficient — store acquisition time and content hash where legally and technically possible.

## Provenance granularity
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: protocol
- content: A provenance record should exist at the smallest level that materially affects scientific reproducibility. Not for trivial formatting; required for scientific transformations, feature extraction, aggregation, filtering that changes sample composition, label creation, model training, simulation and agent-generated scientific interpretation.

## Evidence classes vocabulary
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: schema
- content: instrument_observation, satellite_observation, field_observation, government_dataset, peer_reviewed_publication, preprint, technical_report, institutional_record, news_report, eyewitness_report, community_report, model_output, simulation_output, agent_inference, human_expert_assessment.

## Licence status vocabulary
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: schema
- content: open_redistribution, attribution_required, share_alike, noncommercial, reference_only, restricted, unknown, permission_required. "Unknown licence status should default to conservative handling."

## Trust decomposition and source authority
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: nfr
- content: "Trust should be decomposed rather than collapsed into one opaque score" across source authority, provenance completeness, measurement quality, temporal relevance, spatial relevance, reproducibility, corroboration, uncertainty and review status. "CRIC may store source-authority assessments, but authority must not be confused with truth. A high-authority source can still be wrong."

## Evidence completeness separation
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: nfr
- content: "Evidence completeness must remain separate from hazard or risk. Missing evidence does not imply low hazard."

## Integrity versus scientific validity
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: nfr
- content: Cryptographic integrity proves bytes/manifests unchanged; it does not prove scientific correctness, sensor calibration, causal validity or absence of bias. "CRIC documentation and UI must preserve this distinction."

## Agent and model provenance required fields
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: schema
- content: Agent-generated knowledge records agent ID, agent version, model, model provider, prompt/instructions version, toolsets, datasets, run ID, output validation and human review where applicable. Every model output identifies model ID, model version, training dataset version, inference code version, feature version, threshold/configuration, input nodes and execution time.

## Release manifest fields
- source: docs/CRIC-PRD-v0.1/knowledge/Evidence-Provenance-and-Trust.md
- type: schema
- content: Each major knowledge or dataset release provides a manifest with release identifier, Git commit, included artefacts, hashes, ontology version, schema version and generated time.

---

# knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md

## Claim node schema
- source: docs/CRIC-PRD-v0.1/knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md
- type: schema
- content: `Claim` — id, type, subject, predicate, object, value, unit, claim_text, claimant, source_nodes, evidence_nodes, temporal_scope, spatial_scope, `epistemic` {status, confidence}, `knowledge_state` {status}.

## Claim relationship predicates
- source: docs/CRIC-PRD-v0.1/knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md
- type: schema
- content: supports, contradicts, disputes, corroborates, refines, supersedes, consistent_with, inconsistent_with, derived_from.

## Contradiction is first-class
- source: docs/CRIC-PRD-v0.1/knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md
- type: protocol
- content: "CRIC must not automatically choose a winner merely to simplify retrieval." Contradiction records carry claims compared, contradiction type, degree, evidence, possible reconciliation, reviewer and status. Contradiction types: direct, partial, temporal, spatial, definitional, methodological, measurement, causal, classification, apparent, unresolved. Reconciliation outcomes: claim A preferred, claim B preferred, both valid in different contexts, both partially valid, terminology mismatch, insufficient evidence, unresolved. "Reconciliation does not mean deletion."

## Knowledge lifecycle transitions
- source: docs/CRIC-PRD-v0.1/knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md
- type: protocol
- content: Main path candidate → accepted → disputed → superseded → archived; alternative branches candidate → rejected and accepted → withdrawn. "Candidate nodes must be visibly distinguishable from accepted knowledge." Promotion mechanisms may be deterministic validation, authoritative source, multi-source corroboration, qualified human review or maintainer approval, and "the promotion mechanism must be recorded."

## Retraction and dependency impact
- source: docs/CRIC-PRD-v0.1/knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md
- type: protocol
- content: On retraction or withdrawal: preserve the original source node, update source status, create relevant relationships, flag dependent claims for re-evaluation, "do not silently erase historical use." When a claim is superseded, disputed or withdrawn, CRIC identifies downstream dependencies (assessments, training labels, features, model runs, reports, other claims) and an impact-analysis workflow produces candidate review tasks.

## Agent prohibitions on claims
- source: docs/CRIC-PRD-v0.1/knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md
- type: protocol
- content: Agents must not erase competing claims; silently convert uncertainty into consensus; or promote a high-impact disputed claim without applicable review. "A minority interpretation supported by defensible evidence should not be removed merely because another interpretation is dominant."

## Required retrieval queries
- source: docs/CRIC-PRD-v0.1/knowledge/Claims-Contradictions-and-Knowledge-Lifecycle.md
- type: api-contract
- content: Users and agents can query all claims about a subject; accepted claims; disputed claims; superseded claims; evidence supporting a claim; evidence contradicting a claim; claim history; downstream objects dependent on a claim.

---

# knowledge/Ontology-Evolution-and-Governance.md

## OntologyGapResult schema
- source: docs/CRIC-PRD-v0.1/knowledge/Ontology-Evolution-and-Governance.md
- type: schema
- content: gap_id, encountered_term, context_nodes, current_best_match, `gap_type` ∈ {missing_type, missing_predicate, ambiguous_definition, synonym_collision, overly_broad, overly_narrow, cross_domain_gap}, proposed_action, confidence, evidence_nodes.

## OntologyProposal required fields
- source: docs/CRIC-PRD-v0.1/knowledge/Ontology-Evolution-and-Governance.md
- type: schema
- content: proposal ID, proposer, proposed identifier, proposed name, definition, parent, rationale, evidence, affected types, affected predicates, backwards-compatibility impact, migration impact, example nodes, test cases, status.

## Ontology lifecycle and experimental namespace
- source: docs/CRIC-PRD-v0.1/knowledge/Ontology-Evolution-and-Governance.md
- type: protocol
- content: Lifecycle experimental → candidate → review → stable → deprecated → removed. Experimental terms must be clearly namespaced (e.g. `CRIC-EXP:glof:possible-new-trigger`) and "must not masquerade as stable core types." Deprecated types remain resolvable with `{status: deprecated, deprecated_at, replacement, migration_guidance}`. Removal only after deprecation period, migration tooling, documentation and release notes; "historical nodes must remain interpretable."

## Ontology PR workflow
- source: docs/CRIC-PRD-v0.1/knowledge/Ontology-Evolution-and-Governance.md
- type: protocol
- content: gap → OntologyGapResult → OntologyProposal → prototype schema → validation against example nodes → impact analysis → human review where required → pull request to cric-core → automated tests → maintainer review → merge → ontology version increment → migration artefacts → dependent repositories update. Required automated checks: schema generation, Pydantic tests, duplicate identifier checks, predicate validation, inheritance validation, example validation, migration tests, documentation generation.

## Ontology versioning and migration
- source: docs/CRIC-PRD-v0.1/knowledge/Ontology-Evolution-and-Governance.md
- type: protocol
- content: Semantic versioning — major for breaking semantic changes, minor for backward-compatible additions, patch for clarifications that do not change machine semantics. Every breaking or structurally meaningful change provides a migration script where feasible, a migration record, before/after examples, affected node count and a validation report.

## Ontology agent separation of duties
- source: docs/CRIC-PRD-v0.1/knowledge/Ontology-Evolution-and-Governance.md
- type: protocol
- content: Ontology Watch Agent emits gap results; Ontology Synthesis Agent drafts proposals and "cannot merge its own proposal"; a separate Ontology Critic Agent challenges proposals for duplication, excessive/insufficient specificity, domain leakage into core, unclear definitions, incompatible inheritance and unnecessary new predicates. Ontology states indicate governance maturity, not universal scientific truth — "CRIC should avoid using 'certified'."

---

# domains/Cryosphere-Ontology.md

## Cryosphere type hierarchy
- source: docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md
- type: schema
- content: `CryosphereEntity` → Glacier, GlacierComplex, GlacierTerminus, IceBody, IceCliff, Snowpack, Snowfield, GlacialLake, Moraine, MoraineDam, IceDam, PermafrostBody, FrozenGroundFeature, AvalanchePath, MassMovementSourceArea, CryosphereCatchmentFeature. `CryosphereEvent` → GlacierAdvance, GlacierRetreatEpisode, GlacierSurge, CalvingEvent, IceAvalanche, SnowAvalanche, RockIceAvalanche, LakeFormationEvent, LakeExpansionEpisode, LakeDrainageEvent, CryosphereMassMovement. `CryosphereObservation` → GlacierArea/Terminus/Velocity/Elevation, SnowCover, SnowWaterEquivalent, LakeArea/Level/Volume/Depth/Temperature, MoraineGeometry, SurfaceDeformation, Permafrost observations.

## Domain boundary rule
- source: docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md
- type: protocol
- content: "The Cryosphere ontology extends CRIC Core. It must not redefine core concepts such as Entity, Event, Observation, StateSnapshot, Claim, Evidence, Dataset, Asset, Hazard, Trigger, Exposure, Assessment. Instead it creates domain-specific child types."

## Lake classification vocabulary
- source: docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md
- type: schema
- content: proglacial, supraglacial, moraine_dammed, ice_dammed, bedrock_dammed, landslide_dammed, composite, unclassified, unknown. "Classification must permit multiple claims if sources disagree."

## Observation methods vocabulary
- source: docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md
- type: schema
- content: optical_remote_sensing, SAR, LiDAR, photogrammetry, DEM_analysis, field_survey, GNSS, gauge, bathymetry, thermal_remote_sensing, literature_extraction, manual_digitisation, model_estimate. "Every observation must state method and uncertainty where available."

## Measured versus estimated distinction
- source: docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md
- type: protocol
- content: "Bathymetric measurements, empirical estimates and modelled estimates are epistemically different." CRIC must represent measured bathymetry, estimated depth, empirical volume estimate and modelled volume as separate methods/statuses. "Observed and estimated values must remain distinguishable."

## Cryosphere spatial predicates (divergent)
- source: docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md
- type: schema
- content: The document lists upstream_of, downstream_of, adjacent_to, intersects, overlaps, within, connected_to, drains_to, feeds, terminates_in, exposed_to as important spatial predicates, and lists `associated_with` among Glacier and GlacialLake relationships. NOTE: `connected_to` and `associated_with` are deprecated by registry §8. Registry governs — see `.planning/INGEST-CONFLICTS.md`. "Each inferred spatial relationship should record its derivation."

## Cryosphere uncertainty dimensions
- source: docs/CRIC-PRD-v0.1/domains/Cryosphere-Ontology.md
- type: nfr
- content: Observations should support positional uncertainty, area uncertainty, classification confidence, temporal uncertainty, sensor limitations, cloud/snow confusion, shadow, SAR interpretation limitations and DEM error.

---

# domains/GLOF-Ontology.md

## GLOF type hierarchy
- source: docs/CRIC-PRD-v0.1/domains/GLOF-Ontology.md
- type: schema
- content: `GLOFEvent` → MoraineDamFailureGLOF, IceDamFailureGLOF, OvertoppingGLOF, DisplacementWaveGLOF, CascadingLakeFailureGLOF, CompoundMechanismGLOF, UnknownMechanismGLOF. `GLOFTrigger` → ExtremePrecipitation, Snowmelt, IceAvalanche, SnowAvalanche, RockAvalanche, Landslide, GlacierCalving, Seismic, Piping, DamDegradation, UpstreamLakeFailure, Unknown. `GLOFFailureProcess` → Overtopping, BreachErosion, Piping, InternalErosion, StructuralCollapse, IceDamDrainage, UnknownFailureProcess. "Multiple triggers and processes may apply to one event."

## GLOFEvent required/recommended fields
- source: docs/CRIC-PRD-v0.1/domains/GLOF-Ontology.md
- type: schema
- content: Identity (event ID, name, aliases, source event IDs, lake ID, glacier ID, basin, country, administrative region); Temporal (event start/end, temporal precision, earliest/latest possible time, CRIC knowledge time); Mechanism (failure mode claims, trigger claims, trigger confidence, breach mechanism, compound/cascading status); Hydraulic properties where available (released volume, peak discharge, breach dimensions, flood depth, velocity, travel time, runout distance) — "Each value must be independently sourced or derived"; Consequences (fatalities, injuries, missing, displaced, settlement/road/bridge/hydropower/communication/agricultural/geomorphic impacts) — "Reported consequence values may conflict and must be represented as claims/observations rather than overwritten."

## Failure mechanism vocabulary
- source: docs/CRIC-PRD-v0.1/domains/GLOF-Ontology.md
- type: schema
- content: moraine_breach, overtopping, ice_dam_failure, landslide_displacement_wave, avalanche_displacement_wave, glacier_calving, piping, internal_erosion, seismic_destabilisation, cascading_lake_failure, compound, unknown.

## Trigger representation rules
- source: docs/CRIC-PRD-v0.1/domains/GLOF-Ontology.md
- type: protocol
- content: "A trigger is not automatically a proven cause." CRIC distinguishes observed precursor, candidate trigger, inferred trigger, reported trigger, preferred interpretation, disputed trigger and unknown trigger. Multi-trigger events must be represented "as a graph rather than force one categorical trigger." "Compound mechanisms must not be collapsed into a single trigger merely for classifier convenience."

## Lake stability states
- source: docs/CRIC-PRD-v0.1/domains/GLOF-Ontology.md
- type: schema
- content: Research states normal, elevated, high, critical, indeterminate. "Every state must expose reasons, evidence, uncertainty, completeness, model/rule version, operational disclaimer." "CRIC should favour interpretable states over unsupported exact-date failure claims."

## GLOF training labels and task separation
- source: docs/CRIC-PRD-v0.1/domains/GLOF-Ontology.md
- type: schema
- content: Event labels distinguish confirmed_glof, probable_glof, disputed_glof, non_glof, unknown. "Failure-mode labels and trigger labels should be separate." Susceptibility must be distinct from trigger likelihood. "Exposure is not consequence. Consequence depends additionally on hazard intensity and vulnerability."

---

# domains/StateSnapshot-and-Event-Cube-Specification.md

## StateSnapshot identity fields
- source: docs/CRIC-PRD-v0.1/domains/StateSnapshot-and-Event-Cube-Specification.md
- type: schema
- content: id, type, subject_id, snapshot_time, snapshot_window, snapshot_purpose, schema_version, ontology_version. "A snapshot is not a copy of all source data. It is a structured index into observations, features, claims and evidence." Components: subject state, upstream context, downstream context, environmental context, derived features, evidence completeness, conflicts.

## Snapshot temporal semantics and immutability
- source: docs/CRIC-PRD-v0.1/domains/StateSnapshot-and-Event-Cube-Specification.md
- type: protocol
- content: A snapshot must identify whether it represents exact acquisition time, nearest available observation, reconstructed state, aggregated interval or event-relative window. "Accepted snapshots must not be edited to reflect later knowledge" — improvements produce Snapshot v1 → superseded_by → Snapshot v2, both retrievable.

## Nearest-observation semantics
- source: docs/CRIC-PRD-v0.1/domains/StateSnapshot-and-Event-Cube-Specification.md
- type: schema
- content: When the requested window is unavailable, record `requested_relative_time`, `actual_relative_time`, `temporal_offset_days`, `selection_method` (e.g. `nearest_usable_observation`). "This prevents false temporal precision."

## Event Cube manifest
- source: docs/CRIC-PRD-v0.1/domains/StateSnapshot-and-Event-Cube-Specification.md
- type: schema
- content: event_cube_id, event_id, subject_id, snapshot_ids, source_assets, derived_features, claims, conflicts, dataset_version, created_at, content_manifest_sha256. Recommended temporal windows T-10y, T-5y, T-2y, T-1y, T-6m, T-1m, T-7d, T-24h, T-event, T+24h, T+7d, T+1m, T+6m — "target analysis windows", with the actual snapshot recording the distance between requested and available observation time.

## Negative event cubes
- source: docs/CRIC-PRD-v0.1/domains/StateSnapshot-and-Event-Cube-Specification.md
- type: schema
- content: Types hard negative, routine negative, confirmed negative, no-known-event, unknown. "Negative cubes must define the observation interval over which absence is asserted."

## Leakage prevention
- source: docs/CRIC-PRD-v0.1/domains/StateSnapshot-and-Event-Cube-Specification.md
- type: protocol
- content: "For predictive experiments, post-event information must never leak into pre-event training features." The TrainingSample manifest must define prediction cutoff, allowed source times and prohibited future information. Training sample generation must record cube version, included snapshots, excluded data, label source, leakage controls and feature generation code.

---

# data/Data-Commons-Architecture.md

## Data object hierarchy and storage tiers
- source: docs/CRIC-PRD-v0.1/data/Data-Commons-Architecture.md
- type: schema
- content: Dataset → DatasetVersion → {DataAsset..., Manifest}. "A Dataset is persistent identity. A DatasetVersion is immutable." Tier 1 Git for metadata, manifests, schemas, small examples, test fixtures, small GeoJSON, controlled vocabularies; Tier 2 local/object storage for imagery, DEMs, COGs, large GeoParquet, hydrodynamic outputs, training tensors, model weights; Tier 3 external provider retaining only source URI, provider identifier, retrieval recipe, checksum if acquired and metadata.

## Data registry and DatasetVersion required fields
- source: docs/CRIC-PRD-v0.1/data/Data-Commons-Architecture.md
- type: schema
- content: Registry entry — dataset_id, name, provider, description, domain, spatial_coverage, temporal_coverage, update_frequency, licence, access_method, versions. DatasetVersion required — version ID, parent dataset, release/acquisition time, manifest, schema, licence, source version, spatial extent, temporal extent, asset list, quality status.

## Immutability and derivation rules
- source: docs/CRIC-PRD-v0.1/data/Data-Commons-Architecture.md
- type: protocol
- content: "Acquired raw assets should be treated as immutable. Reprocessing creates new derived assets." Every scientifically material normalisation must retain lineage. Derived datasets must record source versions, code version, parameters and execution environment. "Partitioning must not alter canonical identity." Agents must know whether a resource is canonical, derived, cached or temporary; "caches are disposable."

## Format contracts
- source: docs/CRIC-PRD-v0.1/data/Data-Commons-Architecture.md
- type: schema
- content: EO assets should use STAC where practical, referencing STAC Items/Collections/Assets while adding CRIC-specific provenance, scientific relationships and knowledge lifecycle; COG preferred for large raster access; GeoParquet preferred for portable analytical vector/tabular geospatial data.

## Data access abstraction and sovereign deployment
- source: docs/CRIC-PRD-v0.1/data/Data-Commons-Architecture.md
- type: nfr
- content: "Applications should request data through logical dataset identifiers rather than hard-coded local paths." Runtime dependency injection resolves a logical asset to local disk, object store, remote provider or institutional service. Offline deployment must be able to materialise a selected geographic/data package (OKF nodes, manifests, selected assets, indexes, required models). Organisations must be able to host private data, controlled infrastructure layers, local model weights and local agent runtimes "without modifying public CRIC schemas."

---

# data/Ingestion-and-Licensing.md

## Ingestion pipeline
- source: docs/CRIC-PRD-v0.1/data/Ingestion-and-Licensing.md
- type: protocol
- content: Discover → Qualify Source → Assess Licence → Acquire or Reference → Hash → Extract Metadata → Normalise → Validate → Create OKF Nodes → Create Provenance → Publish Candidate Knowledge. "Ingestion is a controlled evidence pipeline, not merely a download operation." Normalisation is separate from acquisition; the raw acquired object remains immutable and normalised outputs become derived assets with parent links.

## Licence assessment and acquisition modes
- source: docs/CRIC-PRD-v0.1/data/Ingestion-and-Licensing.md
- type: protocol
- content: Before redistribution CRIC must determine licence, attribution requirements, redistribution permission, derivative-use permission, commercial-use restrictions, share-alike obligations, API terms and storage restrictions. Licence status vocabulary: open_redistribution, attribution_required, share_alike, noncommercial, reference_only, restricted, permission_required, unknown — "Unknown should default to conservative handling." Acquisition modes: Copy Permitted, Cache Permitted, Reference Only, Permission Required. "Agents must not bypass explicit licence restrictions."

## Ingestion manifest schema
- source: docs/CRIC-PRD-v0.1/data/Ingestion-and-Licensing.md
- type: schema
- content: ingestion_run_id, workflow_version, started_at, completed_at, sources, assets_acquired, assets_referenced, licence_decisions, created_nodes, failed_items, warnings.

## Idempotency and change detection
- source: docs/CRIC-PRD-v0.1/data/Ingestion-and-Licensing.md
- type: protocol
- content: "Repeated ingestion of the same immutable source should not create uncontrolled duplicates" — use source IDs, provider IDs, hashes, canonical URIs and temporal/version metadata. For mutable sources detect changed bytes, changed metadata, new version, removed source and licence change; "a changed source should create a new version rather than silently replacing previous provenance."

## Ingestion security and quarantine
- source: docs/CRIC-PRD-v0.1/data/Ingestion-and-Licensing.md
- type: nfr
- content: Ingestion must defend against malicious files, prompt injection in documents, oversized payloads, path traversal, embedded executable content, poisoned metadata and untrusted archives. "Agent instructions embedded in source material must be treated as data, not system instructions." Quarantine reference states: discovered, licence_pending, quarantined, acquired, validated, rejected, archived. "Do not silently skip sources when the missing source materially affects completeness."

## Human review triggers for ingestion
- source: docs/CRIC-PRD-v0.1/data/Ingestion-and-Licensing.md
- type: protocol
- content: Review may be required for unclear licence, ambiguous source identity, high-impact scientific claim, unresolved entity collision, safety-significant interpretation or ontology change affecting stable core. "Routine open-data ingestion should not require human approval for every item."

---

# data/Data-Quality-and-Validation.md

## Quality dimensions
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: nfr
- content: "CRIC must never collapse structural validity, provenance completeness, scientific quality, evidence completeness and operational suitability into one score." Independent dimensions: schema validity, ontology validity, graph integrity, temporal integrity, spatial integrity, provenance completeness, licence clarity, source quality, measurement quality, scientific plausibility, reproducibility, evidence completeness, contradiction status, human-review status, fitness for intended use.

## Validation layers V0-V8
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: protocol
- content: V0 file integrity; V1 schema (Pydantic: required fields, types, enums, units, identifier format, nested structures); V2 ontology (registered type, valid parent, allowed predicate, controlled vocabulary, ontology version compatibility); V3 graph (targets resolve, duplicate IDs absent, reciprocal relationships where required, orphans identified, circularity rules); V4 temporal (valid syntax, no invented precision, temporal order, observation vs event time, supersession chronology, training cutoff rules); V5 spatial (CRS, geometry validity, coordinate ranges, topology, basin consistency, impossible spatial relationships); V6 provenance (source nodes, parentage, hashes, transformation records, software/agent run, licence state); V7 scientific quality assessment (may require expert review); V8 fitness-for-use.

## QualityAssessment node schema
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: schema
- content: id, type, subject_id, assessment_type, `dimensions` {schema_validity, provenance_completeness, measurement_quality, temporal_quality, spatial_quality, scientific_plausibility, reproducibility, evidence_completeness}, fitness_for_use, assessor, method, evidence_nodes, created_at.

## Quality flags vocabulary
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: schema
- content: missing_provenance, uncertain_licence, temporal_ambiguity, spatial_ambiguity, low_resolution, cloud_contamination, shadow_contamination, sensor_artifact, estimated_not_measured, unresolved_contradiction, insufficient_negative_evidence, possible_label_leakage, stale_source, unverifiable_source, manual_digitisation, low_inter_rater_agreement.

## Evidence completeness representation
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: schema
- content: `evidence_completeness: {expected_categories, available_categories, score, missing: [...]}`. "A low completeness score must never automatically lower hazard classification."

## Promotion gates
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: protocol
- content: Candidate knowledge must pass V0-V3; accepted deterministic knowledge must pass V0-V6 plus applicable deterministic scientific checks; training-eligible must additionally pass training-specific provenance, label and leakage rules; benchmark-eligible requires stronger review, frozen version and documented inclusion criteria; safety-relevant interpretation requires a defined human-review policy.

## Automated repair boundary
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: protocol
- content: Validators may automatically repair only semantically safe issues (formatting, canonical ordering, harmless whitespace, generated index refresh). "Scientific values, temporal precision, ontology meaning or provenance must not be silently repaired." The Data Quality Agent "must not convert low-quality data into high-quality data by assertion."

## Contradiction-aware validation
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: protocol
- content: The validator must distinguish structural conflict, scientific contradiction, temporal mismatch and expected methodological difference. "Scientific contradiction should normally generate a review or contradiction artefact, not a schema failure."

## Validation report schema and quality regression
- source: docs/CRIC-PRD-v0.1/data/Data-Quality-and-Validation.md
- type: schema
- content: validation_run_id, target_ids, validator_version, started_at, completed_at, passed, errors, warnings, quality_flags, review_requests. Every release compares broken links, validation failures, missing provenance, unresolved licences, benchmark composition and unresolved contradictions; "quality degradation should fail CI where thresholds are exceeded."

---

# data/Training-Data-and-Benchmark-Specification.md

## TrainingSample and Label schemas
- source: docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md
- type: schema
- content: `TrainingSample` — id, type, task_id, subject_id, event_cube_id, snapshot_ids, prediction_cutoff, feature_set_id, label_ids, source_nodes, exclusion_notes, quality_flags, created_by. "A TrainingSample is an immutable manifest referencing source knowledge" and "should reference data rather than duplicate canonical scientific facts." `Label` — id, type, sample_id, label_type, value, class, temporal_window, epistemic_status, confidence, source_nodes, created_by, review_status.

## Negative label semantics
- source: docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md
- type: schema
- content: `confirmed_negative` (sufficient evidence supports absence during a defined observation interval); `probable_negative` (evidence strongly suggests absence but is incomplete); `no_known_event` (no qualifying event found in the evidence searched as of a stated CRIC system time); `unknown` (evidence insufficient); `unobserved` (interval not adequately observed); `not_applicable`. "`unknown`, `unobserved` and `no_known_event` must never silently become confirmed negatives." Hard-negative status must itself have evidence.

## Temporal leakage contract
- source: docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md
- type: schema
- content: "Every predictive sample must define a prediction cutoff. No feature may use information acquired after that cutoff unless the experiment explicitly studies retrospective reconstruction." Required fields: prediction_cutoff, allowed_observation_end, allowed_system_knowledge_end, future_information_policy.

## Split definitions
- source: docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md
- type: protocol
- content: "Random row splitting is often inappropriate for geospatial climate-risk data." Supported splits: lake-disjoint, basin-disjoint, geography-disjoint, temporal holdout, event-disjoint, source-disjoint. "SplitDefinition is versioned and immutable." Benchmarks should document whether connected upstream/downstream or adjacent systems may appear across train/test splits.

## DatasetVersion freeze and benchmark definition
- source: docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md
- type: schema
- content: A DatasetVersion freezes sample list, labels, feature versions, splits, inclusion criteria, exclusion criteria, ontology version, code version and hashes. A Benchmark defines task, dataset version, split, metrics, baseline models, evaluation protocol, uncertainty reporting, prohibited information and reporting template. "A benchmark release should be immutable. Corrections create a new benchmark version."

## Metrics and calibration
- source: docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md
- type: nfr
- content: Classification metrics may include precision, recall, F1, PR-AUC, ROC-AUC, Brier score, calibration error — "For rare high-consequence events, accuracy alone is inadequate." Segmentation: IoU, Dice, boundary error. Regression: MAE, RMSE, interval coverage. "A model score must not be described as probability unless calibration supports that interpretation." "Evaluation must preserve realistic prevalence where operational interpretation is claimed."

## Reconstructability chain
- source: docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md
- type: api-contract
- content: A user must be able to answer "Exactly which evidence trained this model?" through Model → TrainingRun → DatasetVersion → TrainingSample → Snapshot → Observation → Asset → Source.

## v0.1 reference dataset target
- source: docs/CRIC-PRD-v0.1/data/Training-Data-and-Benchmark-Specification.md
- type: nfr
- content: First benchmark may target approximately 10 confirmed GLOF/event cases, 10 hard negatives and 20 routine negatives, "subject to evidence quality rather than fixed quotas. The architecture must scale far beyond this initial set."

---

# ai/Agent-Commons-Architecture.md

## Agent composition and factory contract
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: api-contract
- content: A reusable agent is Agent Definition + Instructions + Dependency Schema + Toolsets + Datasets + Workspace + Model Configuration + Structured Output Schema + Permissions + Evaluation Suite. "The agent definition should remain as stateless as practical. Runtime state is injected." Agents are instantiated through factory functions, not globally mutable singletons: `create_agent(model, instructions, toolsets, output_type, dependency_type, permissions, workspace_policy)`. "Dependencies must not be hidden in global state." The reference implementation uses Pydantic AI.

## Agent manifest (agent.yaml) schema
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: schema
- content: agent_id, name, version, purpose, domain, risk_class, factory, dependency_schema, output_schema, default_model, supported_models, required_toolsets, optional_toolsets, required_datasets, optional_datasets, workspace_policy, permissions, human_review_policy, evaluation_suite.

## LLM knowledge boundary — reads
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: protocol
- content: "An LLM or agent may access CRIC knowledge only through the Context Pack API produced by deterministic retrieval. Direct filesystem access and direct vault access by the model are prohibited, regardless of agent risk class."

## LLM knowledge boundary — writes
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: protocol
- content: "An LLM or agent may never write directly to the knowledge store." Fixed pipeline: LLM write request → structured proposed mutation → Pydantic validation → human/policy check → atomic Markdown write. The human/policy check is the existing Responsible Autonomy review framework: a Level 2 mutation is created as a candidate, and promotion toward Level 3 resolves through deterministic corroboration rules or a ReviewRequest/ReviewDecision cycle before the atomic write. "No agent, regardless of risk class, may bypass this pipeline to write canonical knowledge directly."

## LLM prompt contract
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: protocol
- content: Every LLM invocation carries standard framing independent of provider: the model is told it is given a deterministically assembled knowledge subgraph, must not assume information outside that context, must distinguish observed facts / derived facts / claims / hypotheses / missing evidence / contradictory evidence, and must reference node IDs when making material claims. The context pack is supplied as delimited input (`<context-pack>...</context-pack>`) rather than free-form instructions. "Any output that asserts a fact must be traceable to a node ID inside the context pack; an assertion with no corresponding node ID cannot be treated as an observed or derived fact."

## Agent permissions and risk classes
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: protocol
- content: Capabilities: read canonical graph; search data registry; read external sources; write scratch files; create candidate nodes; create review bundles; propose ontology changes; open pull requests; modify canonical knowledge; publish risk assessment; invoke external actions. "Most research agents should not receive the final two permissions." Risk classes A (deterministic support), B (low-risk analytical), C (provisional knowledge — may create candidate knowledge), D (safety-relevant interpretation — requires human review before trusted publication or operational use), E (authoritative action — "CRIC agents must not autonomously claim authoritative emergency powers").

## Agent workspace isolation
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: protocol
- content: Every agent run receives an isolated workspace `run/{input, scratch, output, logs, proposed-changes, review-bundles}`. "Agents should not write directly into stable knowledge repositories unless the permission policy explicitly allows it."

## Structured outputs and self-correction
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: api-contract
- content: All consequential agent outputs use typed Pydantic schemas (examples: EvidenceExtractionResult, OntologyGapResult, EntityResolutionResult, ContradictionAssessment, ReviewRoutingDecision, TrainingCandidateResult). "Unstructured prose may accompany typed output but must not replace it." Invalid structured output may be returned to the model for correction, with validation failures logged as part of the agent run; "repeated failures must not result in silently malformed canonical knowledge."

## Agent run provenance
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: schema
- content: Every run records agent ID, agent version, model provider, model identifier, instructions version, toolset versions, dependency configuration excluding secrets, dataset versions, input nodes, output nodes, started at, completed at, token/cost metadata where available, errors, human reviews and Git commit hashes.

## Agent versioning
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: protocol
- content: Semantic versioning — major for breaking output schema, dependency schema, permission semantics or removed tools; minor for added toolsets, optional dependency fields, expanded capabilities, new compatible models; patch for prompt refinements, bug fixes, documentation, internal corrections.

## Model independence and MCP optionality
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: nfr
- content: "Agents should support runtime model selection. The agent contract must not require one vendor." MCP integration is available but "MCP must remain optional" and "agent definitions should not assume the presence of a specific MCP server."

## Human review integration and durable resume
- source: docs/CRIC-PRD-v0.1/ai/Agent-Commons-Architecture.md
- type: protocol
- content: Agents pause by creating a review bundle. A paused workflow persists run ID, agent state, unresolved question, evidence, proposed change and required reviewer expertise. The agent later detects an approved `decision.yaml` and resumes. "No ephemeral conversational memory should be required to resume."

---

# ai/Agent-Team-Specifications.md

## Agent construction contract
- source: docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md
- type: api-contract
- content: Each agent must define agent ID, version, purpose, typed dependencies, typed output, required toolsets, optional toolsets, required datasets, workspace policy, permissions, risk class, HITL policy and evaluation suite.

## Team design principles
- source: docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md
- type: protocol
- content: Prefer specialised agents; parallelise independent work; keep deterministic operations outside LLM reasoning; persist intermediate outputs; make handoffs typed; make every agent replaceable; preserve run provenance; avoid hidden shared memory. Parallelism preferred for independent source reviews, competing scientific interpretations, ontology critics, geographic partitions and quality checks; "sequential execution is required where a later task depends on validated output from an earlier stage."

## Agent catalogue (23 agents)
- source: docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md
- type: schema
- content: 1 Research Scout; 2 Source Qualification; 3 Licence; 4 Acquisition; 5 Metadata; 6 Evidence Extraction; 7 Entity Resolution; 8 Temporal Reconciliation; 9 Spatial Reconciliation; 10 Contradiction; 11 Data Quality; 12 Ontology Watch; 13 Ontology Synthesis; 14 Ontology Critic; 15 Provenance Auditor; 16 StateSnapshot Builder; 17 Event Reconstruction; 18 Training Curator; 19 Scientific Critic; 20 Model Evaluation; 21 Human Review Router; 22 Review Resumption; 23 Repository Maintenance.

## Named agent teams
- source: docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md
- type: protocol
- content: Literature-to-Knowledge (Scout → Source Qualification / Licence / Ontology Watch → Acquisition → Metadata → Evidence Extraction → Entity Resolution / Temporal Reconciliation / Contradiction / Ontology Watch → Provenance Audit → Promotion or HITL); Event Reconstruction; Training Dataset; Ontology Evolution.

## CRICAgentDeps dependency bundle
- source: docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md
- type: schema
- content: `class CRICAgentDeps(BaseModel): workspace: WorkspaceHandle; graph: KnowledgeGraphHandle; dataset_registry: DatasetRegistryHandle; review_repo: ReviewRepositoryHandle; identity: RuntimeIdentity`. "Secrets should be injected through runtime providers, not serialised into manifests."

## Per-agent evaluation requirement
- source: docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md
- type: protocol
- content: Each agent must have unit-tested tools, structured-output tests, mock-model tests, adversarial cases, regression fixtures and permission tests.

## v0.1 minimum agent set
- source: docs/CRIC-PRD-v0.1/ai/Agent-Team-Specifications.md
- type: nfr
- content: The first functioning release implements at least Evidence Extraction, Entity Resolution, Ontology Watch, Provenance Auditor and Human Review Router. "Additional agents may initially exist as specifications and test stubs."

---

# ai/Responsible-Autonomy-and-HITL.md

## Six autonomy levels
- source: docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md
- type: protocol
- content: Level 0 unrestricted deterministic computation (no routine HITL); Level 1 autonomous analytical generation (outputs remain analytical/candidate); Level 2 autonomous provisional knowledge (agents may create candidate nodes, claims, event reconstructions, provisional labels, ontology proposals — "They may not automatically represent these as reviewed scientific consensus"); Level 3 trusted scientific graph promotion (deterministic authoritative-source rules, corroboration rules, human review or maintainer-approved workflows — "Not every node requires manual review"); Level 4 safety-significant interpretation (human review required for outputs intended to influence operational warning, evacuation, critical infrastructure action, official risk certification or safety-critical public communication); Level 5 authoritative action (external competent institutions retain authority).

## ReviewRequest schema
- source: docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md
- type: schema
- content: review_id, type, status, created_at, created_by, workflow_run_id, subject_ids, review_type, risk_level, required_expertise, question, options, evidence_nodes, proposed_action, blocking.

## ReviewDecision schema
- source: docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md
- type: schema
- content: review_id, `decision` ∈ {approve, reject, modify, needs_more_evidence, disputed, escalate}, reviewer, reviewer_role, decided_at, rationale, conditions, modified_values, signature_method.

## Review as repository state
- source: docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md
- type: protocol
- content: `cric-review` directory queue: inbox/, assigned/, in-review/, approved/, rejected/, needs-more-evidence/, disputed/, escalated/, archived/. "The filesystem/Git state is part of the workflow protocol." Review bundle `review-<id>/` contains request.yaml, README.md, evidence/references.yaml, proposed/changes.yaml, agent/analysis.yaml, decision.yaml. "Large evidence remains referenced rather than copied unnecessarily."

## Agent pause and resume protocol
- source: docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md
- type: protocol
- content: Pause — (1) agent persists run state; (2) agent creates review bundle; (3) workflow status becomes `waiting_for_review`; (4) execution exits cleanly. "No long-running process must remain alive." Resume — a later invocation (1) scans review status; (2) validates decision; (3) verifies reviewer authority; (4) loads persisted run state; (5) applies decision; (6) continues workflow; (7) records review in provenance.

## Local and offline review
- source: docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md
- type: nfr
- content: A local user may interact with review folders through Obsidian, a text editor, a Git client, the CLI or the CRIC UI. "The review protocol must not require a hosted service."

## Review provenance and reversibility
- source: docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md
- type: protocol
- content: "Every decision must be linked to downstream outputs affected by it" (ReviewDecision → accepted Claim → StateSnapshot → Training Label → DatasetVersion). "A human approval is not immutable scientific truth" — later evidence may dispute, supersede, withdraw or trigger re-review, and "the original decision remains historically visible."

## HITL failure modes to defend against
- source: docs/CRIC-PRD-v0.1/ai/Responsible-Autonomy-and-HITL.md
- type: nfr
- content: Rubber-stamp approval; reviewer impersonation; unqualified approval; stale evidence; approval of a different node version; post-approval mutation; ambiguous decision records. Review decisions may leverage Git commit identity, signed commits, release signatures and artefact hashes — "This proves review-object integrity, not scientific correctness."

---

# ai/Model-Commons-and-ML-Specification.md

## Model Commons principles
- source: docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md
- type: nfr
- content: Provenance before leaderboard performance; small and medium models are first-class; local and sovereign deployment must remain possible; model architecture is replaceable; multimodal fusion preserves modality provenance; uncertainty and calibration must be visible; reproducibility is mandatory for published benchmarks.

## First-class model entities and required fields
- source: docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md
- type: schema
- content: Model, ModelCard, TrainingRun, EvaluationRun, Prediction, FeatureSet, DatasetVersion, ModelArtifact. `Model` — model ID, name, task, architecture family, input modalities, output schema, licence, intended use, prohibited use. Model version/artifact — parent model, architecture, weight URI, hash, training run, framework version, quantisation, licence, hardware notes. `ModelCard` must document purpose, training data, evaluation data, metrics, limitations, known failure modes, geography, temporal coverage, sensor dependencies, calibration, uncertainty and safety disclaimer.

## ModelRun record schema
- source: docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md
- type: schema
- content: model_id, code_commit, environment, dataset_version, split_definition, feature_set, hyperparameters, random_seeds, hardware, started_at, completed_at, artifacts, metrics.

## Model status lifecycle
- source: docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md
- type: schema
- content: experimental, candidate, benchmarked, research_validated, deprecated. "Operationally validated status must require a separate governance process and should not be inferred from benchmark performance."

## Reproducibility and local compute
- source: docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md
- type: nfr
- content: Published runs preserve code commit, environment lock, dataset version, seeds, parameters and weight hash. "Deterministic reproducibility may not always be achievable on all hardware, but deviations must be documented." CRIC should support CPU and commodity GPU experimentation; model size and inference requirements should be reported; quantised variants are encouraged when scientifically acceptable.

## Explainability and uncertainty display
- source: docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md
- type: nfr
- content: Model output should expose influential features, source observations, modality contributions, uncertainty and missing inputs. "Explanations must not be presented as causal proof unless methodologically justified." Uncertainty sources include data, measurement, model, distribution shift, missing modalities and label uncertainty — "The interface should avoid presenting one confidence number as if it captured all uncertainty."

## Prediction node required fields
- source: docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md
- type: schema
- content: model artifact, input sample/snapshot, execution time, output, confidence, calibration context, threshold, code version.

## v0.1 baselines
- source: docs/CRIC-PRD-v0.1/ai/Model-Commons-and-ML-Specification.md
- type: nfr
- content: Prioritise interpretable baselines — deterministic lake-change features, tree-based susceptibility classifier, simple segmentation baseline where data permits. "The objective is to validate the evidence-to-model pipeline before optimising model complexity."

---

# interfaces/Search-and-Graph-Interfaces.md

## Retrieval principle pipeline
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: protocol
- content: User/Agent question → Query planning → Deterministic candidate retrieval → Graph expansion → Temporal/spatial filtering → Evidence/provenance expansion → Ranking → Context package → LLM reasoning. "The LLM is not the primary graph crawler."

## Traversal request shape
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: api-contract
- content: A traversal request specifies seed nodes, allowed predicates, allowed node types, maximum depth, direction, temporal filters, knowledge-state filters, maximum nodes and evidence-expansion policy. "Arbitrary unbounded graph traversal should be restricted."

## Traversal Profile schema
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: schema
- content: A traversal profile declares profile name, profile version, start_types, allowed_paths (permitted sequences of predicate and node type), max_depth and max_nodes. "`max_nodes` ... is a declared field of the profile, not a per-request option, specifically so it cannot silently change between two calls that cite the same profile." Changing allowed_paths, max_depth or max_nodes requires a new profile version, "so that a context package can always be reproduced from the `(query, vault state, traversal profile, engine version)` tuple recorded in its retrieval metadata." A production traversal request reduces to seeds + profile + profile_version. "The traversal engine, not the LLM, decides which of the profile's paths are legal for a given request."

## Edge index schema
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: schema
- content: Every canonical relationship materialises into an edge table with source_id, predicate, target_id, edge_metadata, source_file, ontology_version, knowledge_state — "allows deterministic traversal without parsing every YAML frontmatter block during each request."

## Context Package (ContextPack) schema
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: schema
- content: query_id, question, seed_nodes, selected_nodes, selected_edges, claims, evidence, sources, contradictions, provenance_roots, temporal_scope, spatial_scope, retrieval_policy, traversal_profile, engine_version, truncation, uncertainty, missing_expected_information, exclusions. This document states the YAML schema is "its single canonical definition" of the artefact registered as `ContextPack` in registry §3. Each `claims` and `evidence` entry carries the `epistemic_status` tag from `Temporal-and-Epistemic-Ontology.md`. "This package itself should be inspectable."

## Query Template schema
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: schema
- content: A query template declares allowed seed node types, allowed edge types, edge direction, maximum depth, mandatory node types, optional node types, temporal constraints, trust constraints, provenance requirements, maximum nodes, maximum edges, token budget and completeness criteria. Three named versioned templates are specified: `scientific_claim_review` v1, `lake_state_review` v1, `model_audit` v1.

## Search result object
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: api-contract
- content: Every result exposes node ID, title, type, score, match reason, knowledge state, relevant time, provenance status and graph path where applicable.

## Retrieval completeness reporting
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: protocol
- content: Each traversal profile or query template may declare a `required_context` checklist; for every retrieval the engine reports a completeness table against that checklist, carried in the context package alongside `missing_expected_information`. "Retrieval completeness is a property of the retrieval engine and its declared checklist; it does not certify that the underlying evidence itself is complete."

## Hybrid retrieval and vector index
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: protocol
- content: Semantic embeddings may improve recall but "must not replace exact graph constraints." Recommended sequence: metadata/ontology filter → lexical/vector candidate retrieval → graph expansion → provenance/evidence enrichment → bounded ranking. Each embedding identifies source node, text representation version, embedding model, model version and generated time; "vector indexes must be rebuildable."

## Contradiction- and provenance-aware retrieval
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: protocol
- content: "When a selected claim has known contradictions, retrieval policy should normally include them. The system should not present only the highest-ranked claim and conceal known disagreement." High-impact retrieval may require a minimum provenance completeness (`minimum_provenance`, `include_unverified`, `mark_unverified`).

## Retrieval reproducibility fields
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: schema
- content: A context package records index version, graph release, query, traversal policy, ranking version and embedding version where used.

## Temporal and spatial search
- source: docs/CRIC-PRD-v0.1/interfaces/Search-and-Graph-Interfaces.md
- type: api-contract
- content: Queries must distinguish event-time, observation-time, valid-time and system-time intervals. Spatial capabilities: bounding box, radius, polygon, basin, upstream/downstream network, intersection, nearest feature — "Spatial predicates should use deterministic GIS."

---

# engineering/Deterministic-Retrieval-Engine-Specification.md

## Engine module responsibilities
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: api-contract
- content: parser (Markdown/YAML → unvalidated documents; runs during indexing, "never during a live query"); compiler (Pydantic + ontology validation → canonical Node/Edge objects → persistent graph index); graph (runtime representation and indexes); traversal (traversal profiles and deterministic multi-hop expansion); context (ContextSubgraph assembly, Context Pack rendering, token budgeting, structure-preserving rendering); ranking (versioned scoring function); completeness (required-context checklist evaluation). "Each responsibility should be independently testable and independently versioned."

## Compiled graph indexes
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: schema
- content: out_edges (forward traversal by source node ID); in_edges (reverse traversal by target node ID, "with equal efficiency to the forward direction"); by_type (type-scoped seed resolution and profile validation); by_time (temporal filtering against created_at/valid_from/valid_to for point-in-time reconstruction); by_trust (trust-tier filtering without re-evaluating a full provenance chain). "An index exists because a defined query pattern needs it, not speculatively."

## Deterministic ordering requirement
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: nfr
- content: "At every step where the algorithm iterates over a frontier or a set of edges, that iteration must proceed in a fixed, deterministic order (for example, lexicographic ordering of node and edge identifiers) rather than relying on incidental data-structure iteration order." Rationale: reproducibility (byte-identical selected nodes, edges and ordering on every run and machine); deterministic truncation at max_nodes/max_depth boundaries; auditability of replayed queries; stable input to ranking and token budgeting.

## Traversal algorithm
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: protocol
- content: At each hop the engine (1) filters the current frontier to nodes not yet visited; (2) applies temporal validity against the query time; (3) accepts the node into the result set; (4) resolves the allowed outgoing or incoming edges via out_edges/in_edges; (5) adds unvisited targets to the next frontier — repeating until max_depth is reached or the frontier is exhausted.

## Compiled artefact and incremental recompilation
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: protocol
- content: "The vault (Markdown + YAML frontmatter) remains the canonical, human-readable source of truth. The engine never traverses it directly at query time." Incremental recompilation: file changed → hash changed → reparse only the changed file → remove edges sourced from that file → insert newly parsed edges → revalidate (schema + ontology) → update indexes. A per-file content hash (e.g. SHA-256) is the change-detection mechanism. "The compiled artefact and its persistence backend are separable concerns" — in-process structures initially, with SQLite, DuckDB or a graph engine as later options.

## Engine phase pipeline
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: protocol
- content: Seed resolution → Traversal profile selection → Graph expansion → Temporal filtering → Trust filtering → Provenance expansion → Deduplication → Context prioritisation → Completeness check → Token budgeting → Context package. "Each phase ... should emit logs and machine-readable diagnostics, so that a failure can be attributed to a specific phase rather than to 'retrieval' as an undifferentiated whole."

## Deterministic ranking function
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: protocol
- content: `score = path_proximity_weight + node_type_weight + evidence_weight + trust_weight + temporal_weight + directness_weight + contradiction_weight`. Contradiction weight "ensures contradictory evidence is not suppressed simply because it scores lower on other dimensions." Coefficients are deliberately not fixed by the document but must be documented (recorded, not implicit), versioned (as `ranking_version`) and testable (regression tests against reference queries). "No specific numeric weights are prescribed here; any concrete values elsewhere in draft material are illustrative only."

## Five-way retrieval failure classification
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: protocol
- content: Knowledge failure (evidence does not exist in the vault); retrieval failure (exists in the compiled graph but the pipeline did not select it); context-construction failure (selected but mis-rendered, mis-prioritised or dropped during token-budget pruning); reasoning failure (correct context, incorrect reasoning); generation failure (correct reasoning, output misrepresents it). "Each layer maps to a distinct owner ... a distinct remediation, and a distinct test suite."

## Open gap: trust / review-status vocabulary
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: schema
- content: "No controlled vocabulary for trust or review-status enum values (for example, distinguishing `machine-confirmed` from `human-reviewed`) currently exists anywhere in the PRD." `Evidence-Provenance-and-Trust.md` and `Claims-Contradictions-and-Knowledge-Lifecycle.md` each list "review status" as a dimension but neither enumerates permitted values. The `by_trust` index and the ranking trust weight both assume such values exist and are comparable/orderable. The document declines to invent the enumeration and flags it as an open gap for the knowledge-tier documents that own the dimension. NOTE: this is a self-declared gap in the corpus, not a contradiction between documents.

## Context Pack responsibility mapping
- source: docs/CRIC-PRD-v0.1/engineering/Deterministic-Retrieval-Engine-Specification.md
- type: api-contract
- content: The document maps engine responsibilities onto the canonical Context Package field names owned by `interfaces/Search-and-Graph-Interfaces.md` ("Context Pack" and "Context Package" name the same object; "ContextPack" is its canonical type identifier). "A Pydantic `ContextPack` model must be built against these canonical field names; this table exists so that model and the schema in `Search-and-Graph-Interfaces.md` cannot drift apart. The context pack must be independently inspectable before it reaches the LLM."

---

# interfaces/API-and-SDK-Specification.md

## Interface principles
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: nfr
- content: Schema first (public contracts generated from or validated against Pydantic models); stable identity (clients use CRIC IDs, not storage paths); explicit knowledge state ("Responses must not silently mix candidate, accepted, disputed, superseded, rejected knowledge"); temporal explicitness (time-sensitive queries must state which temporal dimension is filtered); provenance traversability; storage independence. "The API is not the canonical knowledge store."

## REST resource surface
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: api-contract
- content: Base `/api/v1/`. Core resource endpoints: /entities, /events, /observations, /snapshots, /claims, /evidence, /datasets, /assets, /models, /agents, /reviews, /ontology, /provenance, /search, /graph. Resource responses include canonical ID, type, title, knowledge state, temporal metadata, relevant relationships, schema/ontology version and provenance reference.

## SDK module surface
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: api-contract
- content: Package `cric-sdk`; namespaces cric.entities, .events, .observations, .snapshots, .claims, .evidence, .datasets, .assets, .models, .agents, .reviews, .ontology, .provenance, .search, .graph, .geo, .temporal.

## Graph API operations
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: api-contract
- content: neighbours; bounded traversal; shortest semantic path; predicate-constrained traversal; traversal-profile-selected retrieval (`cric.graph.traverse(seed=..., traversal_profile=...)`); temporal graph slice; provenance traversal; dependency impact traversal. "Arbitrary unbounded graph traversal should be restricted."

## Provenance and historical-knowledge APIs
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: api-contract
- content: `GET /api/v1/provenance/{object_id}/trace` with options ancestors, descendants, depth, include transformations, include review decisions, include model runs. "CRIC must support queries equivalent to: What did CRIC know about lake X on 2026-01-01? This should use system time rather than silently returning today's graph."

## Agent API
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: api-contract
- content: `GET /agents`, `GET /agents/{agent_id}`, `POST /agent-runs`, `GET /agent-runs/{run_id}`, `POST /agent-runs/{run_id}/resume`. Execution requests must specify or resolve agent version, dependency profile, toolset, dataset context, workspace, model provider and permission profile.

## Pagination, errors and auth
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: api-contract
- content: "All list endpoints must support bounded pagination. Cursor-based pagination is preferred for large mutable indexes." Machine-readable error structure `error: {code, message, details, trace_id}`. "Scientific uncertainty is not an API error." Permissions must be capability based where practical.

## OpenAPI, compatibility and MCP
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: api-contract
- content: FastAPI generates OpenAPI from typed routes; "Generated documentation must not replace semantic PRD documentation." API versions and ontology versions are separate — a client must be able to determine API version, schema version, ontology version and knowledge release version. A future MCP server should reuse the same Pydantic contracts, permission system, provenance and deterministic retrieval layer: "MCP must remain an adapter, not the canonical CRIC architecture."

## CLI surface
- source: docs/CRIC-PRD-v0.1/interfaces/API-and-SDK-Specification.md
- type: api-contract
- content: `cric validate`, `search`, `graph`, `provenance`, `dataset`, `agent`, `review`, `ontology`, `snapshot`, `materialise`.

---

# interfaces/Human-Applications-and-UI.md

## Application modules
- source: docs/CRIC-PRD-v0.1/interfaces/Human-Applications-and-UI.md
- type: api-contract
- content: Twelve modules — Knowledge Explorer, Climate Risk Map, Entity Explorer, Timeline Explorer, Evidence Explorer, Contradiction Explorer, Provenance Explorer, Dataset Explorer, Model Explorer, Agent Commons Console, HITL Review Console, Ontology Explorer. "The UI is a lens over CRIC, not a separate source of truth."

## Mapping technology
- source: docs/CRIC-PRD-v0.1/interfaces/Human-Applications-and-UI.md
- type: nfr
- content: "MapLibre GL JS is the preferred open-source mapping layer for the web application." Map capabilities: lake/glacier layers, event locations, exposure, catchments, temporal filtering, dataset overlays, selectable StateSnapshots, provenance-aware layer metadata.

## Timeline multi-temporal display
- source: docs/CRIC-PRD-v0.1/interfaces/Human-Applications-and-UI.md
- type: nfr
- content: The Timeline Explorer displays separate tracks for real-world events, observations, publications, CRIC ingestion, claim changes, review decisions and model predictions — "This visually communicates CRIC's multi-temporal architecture."

## Contradiction and candidate display rules
- source: docs/CRIC-PRD-v0.1/interfaces/Human-Applications-and-UI.md
- type: nfr
- content: "The UI must avoid visually treating one claim as settled unless its status supports that interpretation." "Candidate/agent-generated knowledge must be visually distinguishable from accepted knowledge." "Evidence completeness must be visually distinct from risk state. A user should not infer: low evidence = low risk." Confidence display must avoid deceptive precision — qualitative where qualitative, and with value, method and meaning where numerical.

## Secrets and accessibility
- source: docs/CRIC-PRD-v0.1/interfaces/Human-Applications-and-UI.md
- type: nfr
- content: In the Agent Run View, "Sensitive secrets must never be displayed." Accessibility targets: keyboard navigation, sufficient contrast, screen-reader semantics, non-colour-only status indicators, scalable typography. Desktop-first workbench, with review and inspection interfaces remaining responsive.

## Obsidian as a supported interface and export formats
- source: docs/CRIC-PRD-v0.1/interfaces/Human-Applications-and-UI.md
- type: nfr
- content: "The downloadable `cric-knowledge` repository itself is a supported human interface" with Obsidian-compatible links, generated indexes, graph-friendly naming and templates; "The knowledge base must remain useful without CRIC's web UI." Exports: Markdown, JSON, GeoJSON, CSV, GeoParquet references, provenance bundle.

---

# engineering/Software-Architecture.md

## Architectural layers and cross-cutting concerns
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: schema
- content: Human Applications / API-SDK-CLI / Agent Commons / Scientific Workflows / Model Commons / Retrieval-Graph-Search / Materialised Data Services / OKF Knowledge Commons + Data Commons / Storage. Cross-cutting: Pydantic schemas, provenance, temporal semantics, permissions, validation, HITL, ontology.

## Language and schema authority
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: nfr
- content: "Python 3.12+ is the primary backend/scientific language. TypeScript is preferred for the web frontend." "Pydantic is the runtime schema authority" for OKF validation, API contracts, agent dependencies, agent outputs, review artefacts, dataset manifests, ontology proposals and model metadata. "Generated JSON Schema should be published."

## Stack choices
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: nfr
- content: Backend API FastAPI. Geospatial: GeoPandas, Shapely, Rasterio, Xarray, PyProj, PySTAC/pystac-client. Analytical storage: DuckDB (with DuckDB spatial) locally, PostgreSQL/PostGIS for larger deployments — "The application layer should minimise backend-specific coupling." Knowledge storage canonical: Markdown + YAML frontmatter. Large asset adapters: local filesystem, S3-compatible object storage, remote HTTP/STAC reference. Frontend: React, Vite, TypeScript, MapLibre GL JS.

## Dependency direction
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: protocol
- content: cric-core ← domain packages ← ingest/models/agents ← api/ui. "Higher-level repositories must not redefine core schemas."

## Deterministic workflow layer
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: protocol
- content: Use ordinary Python for ingestion, hashing, validation, geospatial computation, feature generation, indexing, graph materialisation and dataset construction. "LLM agents should not replace deterministic code where deterministic code is suitable."

## Workspace isolation and configuration precedence
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: protocol
- content: Agent runs receive isolated workspaces `workspaces/<run-id>/{input, working, output, logs, state}`; "Agents should not receive unrestricted repository write access by default." Configuration precedence: (1) defaults; (2) repository profile; (3) deployment profile; (4) environment; (5) explicit runtime overrides. "Secrets must not enter committed configuration."

## Durable state and background processing
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: nfr
- content: "Long-running workflows should persist state. Especially when waiting for HITL, the process should terminate cleanly and resume later." "CRIC should not require a distributed task queue in v0.1"; interfaces should permit later adapters to Celery, Dramatiq, cloud queues or Kubernetes jobs. Docker supports reproducible development and deployment but must not be mandatory for simple local knowledge-base use.

## CI categories
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: protocol
- content: GitHub Actions should initially run formatting/linting, unit tests, schema tests, ontology validation, OKF validation, provenance checks, licence checks, security scanning and build tests.

## Deployment profiles
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: nfr
- content: Knowledge-Only (Obsidian + Markdown); Local Research Workstation (Markdown + DuckDB + Python SDK + agents + local assets); Web Workbench (API + UI + materialised graph); Institutional (PostGIS/object storage/auth/private datasets).

## Performance posture
- source: docs/CRIC-PRD-v0.1/engineering/Software-Architecture.md
- type: nfr
- content: "Optimise first for correctness; reproducibility; bounded retrieval; batch efficiency. Do not prematurely introduce distributed complexity."

---

# engineering/Testing-and-Quality-Assurance.md

## Mandatory test classes
- source: docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md
- type: protocol
- content: Unit; Schema ("Every Pydantic model requires: valid fixture; invalid fixture; boundary cases; backwards-compatibility cases"); Ontology; OKF; Graph; Deterministic Ranking; Geospatial; Provenance; Agent; Prompt Injection; HITL; Training Data; Model. "Passing software tests does not establish scientific validity. Scientific validation is an additional activity."

## Retrieval failure classification requirement
- source: docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md
- type: protocol
- content: "Every retrieval-path test failure must be assigned to exactly one of five classes": knowledge, retrieval, context-construction, reasoning, generation. "A wrong answer labelled only as 'hallucination' hides which layer needs the fix." "Test harnesses for graph, provenance and agent tests must record which of these five classes a failing case belongs to; an unclassified retrieval-path failure is itself a test-infrastructure defect."

## Deterministic ranking tests
- source: docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md
- type: protocol
- content: Named test id `retrieval-ranking-reproducibility` — "the same query, vault state, traversal profile and retrieval-engine version must always produce an identical context package — the same node selection, the same edge selection and the same ordering — across repeated runs and across repeated deployments. Any divergence is a retrieval failure or a context-construction failure, never a knowledge or reasoning failure, and must be filed as such." Also weight-coefficient regression (scoring weights change only through a reviewed, versioned update) and tie-break determinism (equal scores resolve to a stable, documented order).

## Golden scientific fixtures
- source: docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md
- type: protocol
- content: A golden fixture contains canonical nodes, expected relationships, source references, expected derived values, known contradictions and expected validation outcome. "Golden fixtures provide regression protection without pretending to represent the full scientific domain."

## Agent testing and evaluation dimensions
- source: docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md
- type: protocol
- content: Each agent requires tool unit tests, dependency-contract tests, structured-output validation, mock-model tests, adversarial prompts, permission tests and regression cases; "Live-model evaluation should supplement, not replace, deterministic tests." Evaluation dimensions: factual grounding, provenance completeness, schema compliance, contradiction awareness, temporal correctness, ontology compliance, unnecessary escalation, missed escalation, tool-selection correctness, unsupported certainty.

## Prompt injection, HITL and training-data tests
- source: docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md
- type: protocol
- content: Prompt-injection fixtures embed malicious text inside papers, Markdown, metadata, web content and dataset descriptions — "Agents must treat these as data." HITL tests cover review bundle creation, blocking state, clean process termination, valid approval, invalid approval, unauthorised reviewer, modified artefact after review, rejected decision, needs-more-evidence, workflow resumption and provenance of decision. Training-data tests cover unknown-is-not-negative, event-relative cutoffs, no future leakage, split integrity, duplicate contamination, label provenance and hard-negative eligibility.

## End-to-end reference test
- source: docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md
- type: protocol
- content: At least one v0.1 workflow runs acquire/reference source → create provenance → create observation → create StateSnapshot → build Event Cube → create TrainingSample → train/evaluate baseline → generate prediction → trace prediction back to source.

## Quality gates and regression budgets
- source: docs/CRIC-PRD-v0.1/engineering/Testing-and-Quality-Assurance.md
- type: protocol
- content: Pull Request Gate (fast deterministic suite); Main Branch Gate (full integration suite); Release Candidate Gate (end-to-end reference workflows plus benchmark checks); Stable Release Gate (release manifest, signatures, documentation, migrations, reproducibility checks). Example regression budgets: zero new broken graph links; zero unlicensed redistributed assets; zero Level 4 HITL bypasses; zero provenance breaks in benchmark samples; bounded model metric regression.

---

# engineering/Security-and-Responsible-AI.md

## Security principles and threat categories
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: nfr
- content: Least privilege; untrusted input by default; immutable provenance; explicit permissions; separation of code, data and instructions; reproducible builds; auditable agent actions; human authority for safety-significant action. Threats: malicious source files, prompt injection, poisoned datasets, compromised dependencies, malicious contributors, credential leakage, unauthorised repository writes, model supply-chain attacks, tampered review decisions, sensitive-location disclosure, denial of service, provenance manipulation.

## Prompt injection handling
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: protocol
- content: "Scientific documents, web pages, Markdown, metadata and datasets are untrusted data." The document gives an illustrative injection string inside a fenced code block and states such text "inside a source document must be treated as source content, never agent instruction."

## Tool permission classes
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: protocol
- content: read graph; search external sources; acquire data; create candidate nodes; create review request; write workspace; create Git branch; create pull request; merge. "Merge permission should normally remain outside autonomous scientific agents." Workspace controls: bounded paths, no arbitrary secret access, controlled network, file-size limits, content validation.

## Secrets handling
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: nfr
- content: "Secrets must be provided through secure runtime mechanisms. Never store API keys, passwords, tokens in OKF, prompts, committed manifests or agent-run artefacts."

## External URL and file handling
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: nfr
- content: Acquisition tools validate schemes, domains where policy requires, redirects, size and content type; "Defend against SSRF in hosted deployments." Quarantine and inspect untrusted archives, executables, office documents, PDFs and model weights; "Model artefacts should use safer formats where possible."

## Git and review integrity
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: protocol
- content: Protected branches; mandatory review for core; signed releases; least-privilege automation tokens; CODEOWNERS for critical schemas; branch protection. "A ReviewDecision must bind to the exact artefact version reviewed" recording subject hashes, Git commit, reviewer and decision time; "A later mutation must invalidate the approval for the modified object where applicable."

## Responsible AI principles
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: protocol
- content: Evidence grounding ("Agent-generated scientific statements must link to evidence or be marked unverified"); epistemic honesty (distinguish observation, report, derivation, inference, hypothesis, simulation); uncertainty visibility; contradiction preservation ("Agents must not erase scientific disagreement for conversational neatness"); human authority ("CRIC does not autonomously issue authoritative government warnings or evacuation orders"). Hallucination controls: structured outputs, bounded retrieval, controlled vocabularies, provenance requirements, validators, evidence citations, adversarial scientific critic agents, HITL escalation. "Every agent output should pass Pydantic validation before entering workflow state. Validation does not guarantee scientific correctness."

## Prohibited autonomous actions
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: protocol
- content: Unless a future competent authority explicitly establishes a governed deployment, CRIC agents must not autonomously order evacuation; declare official emergency; issue official public warning; certify infrastructure safe/unsafe; suppress contradictory safety evidence; or alter authoritative external records. Before Level 4 communication, require evidence package, model/rule version, uncertainty, alternative interpretations, evidence completeness and authorised human review.

## Data poisoning and model supply chain
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: nfr
- content: Training ingestion detects duplicate contamination, suspicious labels, impossible values, distribution anomalies, source concentration and future leakage — "Detection does not prove malicious intent." Model records include source, licence, hash, framework, training provenance where known and trust status; "Unknown external weights should not automatically enter trusted workflows."

## Audit logs, incident response and red teaming
- source: docs/CRIC-PRD-v0.1/engineering/Security-and-Responsible-AI.md
- type: protocol
- content: Audit records agent, run, tool, action, target, time, outcome — "Avoid logging secrets." Incident response supports affected artefact identification, token revocation, provenance impact analysis, compromised-node quarantine, release withdrawal and downstream dependency identification. Agent evaluations include prompt injection, malicious source instructions, fabricated citation, contradictory evidence, poisoned metadata, permission escalation attempts, false reviewer approval and unsafe certainty.

---

# engineering/Deployment-Versioning-and-Releases.md

## Independent version dimensions
- source: docs/CRIC-PRD-v0.1/engineering/Deployment-Versioning-and-Releases.md
- type: schema
- content: Software package version; API version; schema version; ontology version; knowledge release; dataset version; model version; agent version. "These must not be conflated." Semantic versioning applies to software, schemas, ontology packages and agents.

## Knowledge, dataset, model and agent version rules
- source: docs/CRIC-PRD-v0.1/engineering/Deployment-Versioning-and-Releases.md
- type: protocol
- content: `cric-knowledge` releases have immutable identifiers (e.g. `CRIC-KNOWLEDGE-2026.09.0`) recording Git commit, schema version, ontology version, included nodes, hashes and validation report. "Datasets must use immutable versions independent of repository tags. A new sample, corrected label or changed split requires a new DatasetVersion." Model artifacts require semantic/release version, weight hash, training run, dataset version and code version. Agent breaking changes: output schema, dependency-contract, tool-signature and permission-semantic changes.

## Multi-repository release manifest
- source: docs/CRIC-PRD-v0.1/engineering/Deployment-Versioning-and-Releases.md
- type: schema
- content: release_id, released_at, `components` {cric-core: {version, commit}, cric-knowledge: {...}, cric-agents: {...}, cric-glof: {...}}, schemas, ontology, datasets, models. A published compatibility matrix covers core schema, ontology, domain packages, agents and API.

## Offline bundle layout
- source: docs/CRIC-PRD-v0.1/engineering/Deployment-Versioning-and-Releases.md
- type: schema
- content: `cric-offline-bundle/{knowledge, indexes, datasets, models, schemas, manifests, README.md}`. "Every included artefact must retain provenance and licence metadata."

## Migrations and rollback
- source: docs/CRIC-PRD-v0.1/engineering/Deployment-Versioning-and-Releases.md
- type: protocol
- content: "Materialised databases are rebuildable ... Canonical knowledge remains outside the database." Breaking schema changes require migration documentation, migration tooling where feasible, before/after fixtures and a MigrationRecord. "A deployment should be able to roll back software independently of canonical knowledge. Knowledge rollback must not erase historical records."

## Release channels, checklist and signing
- source: docs/CRIC-PRD-v0.1/engineering/Deployment-Versioning-and-Releases.md
- type: protocol
- content: Channels experimental, alpha, beta, stable — "Scientific dataset/model maturity should use its own status rather than being inferred from software channel." Release checklist: tests pass; ontology validates; OKF validates; provenance validates; licences checked; security scan; migration notes; compatibility matrix; release manifest; documentation; model cards; dataset cards; known limitations. Stable releases should support cryptographic signing of tags, manifests and selected artifacts. Container images should be version pinned, reproducibly built where feasible, scanned, signed where practical and linked to source commit.

---

# product/Repository-and-System-Architecture.md

## Repository boundaries and dependency rules
- source: docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md
- type: protocol
- content: `cric-core` "may not depend on any domain-specific repository" and contains base Pydantic models, OKF schema models, identifiers, base node types, temporal/epistemic/provenance/licensing structures, controlled vocabularies, climate-risk core ontology, validators and migration helpers. `cric-knowledge` "must be useful without running CRIC software". `cric-glof` depends on cric-core and cric-cryosphere. `cric-api` "must not become the source of truth". "Repository internals should not be imported across boundaries when a public interface exists."

## DataAsset record schema
- source: docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md
- type: schema
- content: id, type (`DataAsset`), uri, source_uri, sha256, size_bytes, media_type, provider, licence, redistribution, temporal_coverage, spatial_coverage, retrieved_at, availability_status. Git is not the default storage for raw satellite products, DEM rasters, hydrodynamic rasters, large training tensors, model weights or large time-series archives.

## Canonical versus materialised artefacts
- source: docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md
- type: protocol
- content: Canonical — OKF Markdown, schema definitions, immutable manifests, provenance records, source metadata, training dataset manifests, model cards, review decisions. Materialised — DuckDB, PostgreSQL/PostGIS, search indexes, vector stores, graph databases, parquet caches, API caches. "Materialised representations must be regenerable."

## Interface contracts across repositories
- source: docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md
- type: api-contract
- content: Cross-repository communication occurs through published Pydantic models, JSON Schema, OKF Markdown, GeoJSON, GeoParquet, STAC, typed Python packages, REST/OpenAPI and optional MCP interfaces.

## Release artefacts per repository
- source: docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md
- type: protocol
- content: Each release generates where applicable a Git tag, release notes, schema version, ontology version, migration notes, content manifest, checksums and `CITATION.cff`. Core ontology changes require proposal, compatibility analysis, tests, migration impact and maintainer approval.

## Review repository and agent workspace layouts
- source: docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md
- type: schema
- content: `review/{inbox, assigned, in-review, approved, rejected, needs-more-evidence, disputed, escalated, archived}` — "Each bundle must be machine-readable enough for an agent to detect its status and resume automatically." `.workspaces/<run-id>/{input, scratch, output, logs, proposed-changes}` — "Agents must not write arbitrary intermediate files into canonical repositories. Only approved outputs are promoted into canonical locations."

## v0.1 architectural requirement
- source: docs/CRIC-PRD-v0.1/product/Repository-and-System-Architecture.md
- type: nfr
- content: "v0.1 must demonstrate that the multi-repository architecture is real, even if only a subset of repositories contains substantial functionality." At minimum cric-core, cric-knowledge, cric-agents, cric-cryosphere, cric-glof, cric-review and cric-docs should exist with functioning interfaces and documentation.

---

# community/Volunteer-HITL-Workflow.md

## Review repository and bundle layout
- source: docs/CRIC-PRD-v0.1/community/Volunteer-HITL-Workflow.md
- type: schema
- content: `cric-review/{inbox, assigned, in-review, approved, rejected, needs-more-evidence, disputed, escalated, archived}`. Bundle e.g. `HITL-00000421/{request.md, request.yaml, evidence/references.yaml, candidate-changes/changes.yaml, agent-analysis.md, instructions.md, decision.yaml}`.

## Reviewer registry schema
- source: docs/CRIC-PRD-v0.1/community/Volunteer-HITL-Workflow.md
- type: schema
- content: reviewer_id, public_name, expertise, review_permissions, affiliations, conflicts_declared, status, review_history. "Avoid unnecessary personal data." Expertise tags: cryosphere, glaciology, hydrology, remote_sensing, GIS, geotechnical, meteorology, seismicity, ML, ontology, data_quality, software_security.

## Review outcome vocabulary
- source: docs/CRIC-PRD-v0.1/community/Volunteer-HITL-Workflow.md
- type: schema
- content: approved, rejected, modified, needs_more_evidence, disputed, escalated.

## Review instruction requirements
- source: docs/CRIC-PRD-v0.1/community/Volunteer-HITL-Workflow.md
- type: protocol
- content: "Every bundle must clearly state what is being reviewed; why; exact decision requested; evidence; uncertainties; alternatives; consequences of approval; required expertise."

## GitHub review workflow
- source: docs/CRIC-PRD-v0.1/community/Volunteer-HITL-Workflow.md
- type: protocol
- content: (1) agent creates bundle; (2) bundle committed to branch; (3) pull request opened; (4) reviewer comments or commits decision; (5) automated validation checks decision; (6) workflow resumes; (7) review is archived with provenance. Signature: Git identity, commit hash and reviewer ID initially, with signed commits or institutional identity for higher-assurance deployments.

## Double review and reputation
- source: docs/CRIC-PRD-v0.1/community/Volunteer-HITL-Workflow.md
- type: protocol
- content: Multiple reviewers may be required for benchmark ground-truth labels, a new GLOF failure mechanism, safety-significant classification and stable core ontology change. "Reputation should not become an opaque automated truth score." A reviewer can be suspended from particular approval classes "without deleting their historical contributions."

## Volunteer safety boundary
- source: docs/CRIC-PRD-v0.1/community/Volunteer-HITL-Workflow.md
- type: nfr
- content: "Volunteer reviewers must not be presented as official emergency authorities merely because they participate in CRIC."

---

# implementation/CRIC-v0.1-Implementation-Specification.md

## v0.1 scope and repositories
- source: docs/CRIC-PRD-v0.1/implementation/CRIC-v0.1-Implementation-Specification.md
- type: nfr
- content: "v0.1 is an experimental proof of concept, not a validated operational early-warning system." Geographic scope: Indian Himalayan Region plus connected transboundary Indus, Ganga and Brahmaputra cryosphere systems where relevant; the reference dataset may use cases outside India where scientifically useful. Required repositories: cric-core, cric-knowledge, cric-data, cric-ingest, cric-cryosphere, cric-glof, cric-agents, cric-models, cric-api, cric-ui, cric-docs; `cric-review` listed as Recommended. NOTE: registry §12 makes `cric-review` canonical — see `.planning/INGEST-CONFLICTS.md`.

## Twelve workstreams
- source: docs/CRIC-PRD-v0.1/implementation/CRIC-v0.1-Implementation-Specification.md
- type: protocol
- content: 1 CRIC Core (Pydantic core schemas, JSON Schemas, ontology registry, temporal/provenance/knowledge-state schemas, validators, ID conventions); 2 Knowledge Commons (Obsidian-compatible OKF vault); 3 GLOF Reference Dataset (~10 confirmed GLOFs, 10 hard negatives, 20 routine negatives, "Do not force quotas if reliable evidence is unavailable"); 4 Observation Factory; 5 StateSnapshot and Event Cube; 6 Training Dataset; 7 Baseline Models ("Model performance is secondary to pipeline reproducibility"); 8 Agent Commons (five minimum agents); 9 HITL; 10 Search and Graph; 11 API; 12 UI.

## Milestones A-G
- source: docs/CRIC-PRD-v0.1/implementation/CRIC-v0.1-Implementation-Specification.md
- type: protocol
- content: A Schema Spine (core schemas, ontology, example OKF nodes, validators); B First Lake Digital Record (one lake, glacier, observations, provenance, snapshot, graph traversal); C First Event Cube (historical GLOF, pre/post snapshots, claims, contradictions, event manifest); D Dataset Slice (positive, hard negative, routine negative, reproducible sample generation); E Baseline Model (versioned dataset, training run, evaluation, model card, source-to-model provenance); F Agent/HITL Loop (agent candidate knowledge, ontology watch, review bundle, human approval/rejection, durable resume); G Reference Workbench (API, map, entity explorer, timeline, evidence lineage).

## v0.1 non-goals
- source: docs/CRIC-PRD-v0.1/implementation/CRIC-v0.1-Implementation-Specification.md
- type: nfr
- content: v0.1 does not require operational warning; national-scale production ingestion; real-time sensor network; calibrated failure probability; exhaustive ontology for all climate hazards; distributed microservices; large foundation-model training.

## Initial source families
- source: docs/CRIC-PRD-v0.1/implementation/CRIC-v0.1-Implementation-Specification.md
- type: nfr
- content: Candidate sources — NRSC/ISRO glacial lake inventories, Landsat, Sentinel-1, Sentinel-2, GPM IMERG, Copernicus DEM, HydroSHEDS, WorldPop, OpenStreetMap, peer-reviewed and institutional GLOF inventories. "Actual use depends on access and licensing."
