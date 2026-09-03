# CRIC Cross-Document Requirements Traceability Matrix

## Purpose

This matrix connects CRIC's constitutional requirements to the PRD documents that define and implement them.

| ID | Requirement | Primary Specification | Supporting Specifications | v0.1 Verification |
|---|---|---|---|---|
| R-001 | CRIC is climate-risk-wide, with Cryosphere/GLOF first | Product Vision | Core Ontology; Cryosphere Ontology; GLOF Ontology | Core contains no unnecessary GLOF assumptions |
| R-002 | Immutable evidence lineage | Evidence, Provenance and Trust | Data Commons; Model Commons; Testing | End-to-end provenance test |
| R-003 | Every significant derived value can answer “where did this come from?” | Evidence, Provenance and Trust | Search/Graph; UI; API | Provenance traversal succeeds |
| R-004 | OKF Markdown is a first-class product | OKF Knowledge Graph | Human UI; Repository Architecture | Vault opens and navigates independently |
| R-005 | Atomic scientific knowledge | OKF Knowledge Graph | Claims Lifecycle; Event Cube | Atomicity fixtures validate |
| R-006 | Multi-temporal truth | Temporal and Epistemic Ontology | Event Cube; Search/Graph | Historical-knowledge query test |
| R-007 | Contradictions are preserved | Claims/Contradictions | Search/Graph; UI | Contradictory claims retrieved together |
| R-008 | Pydantic is schema authority | Software Architecture | Core Ontology; Agent Commons; API | Pydantic/JSON Schema tests |
| R-009 | Agents are first-class reusable components | Agent Commons | Agent Teams; API; Software Architecture | Agent reused with alternate dependencies |
| R-010 | Tools, datasets, workspaces and dependencies are separately injectable | Agent Commons | Software Architecture | Composition contract test |
| R-011 | Deterministic computation is preferred where suitable | Agent Commons | Software Architecture; Ingestion | Deterministic workflow fixtures |
| R-012 | Ontology evolution is continuously detected | Ontology Governance | Agent Teams | Ontology Watch evaluation |
| R-013 | Stable ontology changes use governed PRs | Ontology Governance | Contribution Process; Open Source Governance | PR gate fixture |
| R-014 | StateSnapshot is first-class | Event Cube | Core Ontology; GLOF Ontology | Snapshot schema and immutability test |
| R-015 | GLOF Event Cube supports pre/post reconstruction | Event Cube | GLOF Ontology; Training Data | Reference cube reproduced |
| R-016 | Negative cases are epistemically explicit | Training Data | Temporal/Epistemic; Registry | Unknown-to-negative prohibition test |
| R-017 | Training lineage is reconstructable | Training Data | Model Commons; Provenance | Model-to-source traversal |
| R-018 | Future information leakage is prohibited | Training Data | Testing | Cutoff/leakage tests |
| R-019 | Large assets are not required in Git | Data Commons | Repository Architecture; Ingestion | Asset manifest test |
| R-020 | Copyright and licence constraints are first-class | Ingestion/Licensing | Security; Contribution | Protected-paper workflow test |
| R-021 | HITL is risk based, not universal | Responsible Autonomy | Volunteer HITL; Agent Teams | Autonomy policy tests |
| R-022 | Agents can pause and resume durably | Responsible Autonomy | Software Architecture; Volunteer HITL | Pause/resume E2E test |
| R-023 | Level 4 safety-significant outputs require human review | Responsible Autonomy | Security | Bypass test must fail |
| R-024 | CRIC never assumes government warning authority | Responsible Autonomy | Security; Product Vision | Prohibited-action tests |
| R-025 | Graph retrieval is deterministic and bounded | Search/Graph | Deterministic Retrieval Engine; API; Software Architecture | Bounded traversal tests; ranking-reproducibility test (Testing/QA) |
| R-026 | LLMs receive inspectable context packages | Search/Graph | Deterministic Retrieval Engine; Agent Commons | Retrieval reproducibility test; Context Package completeness/exclusions fields present |
| R-027 | Evidence completeness is separate from hazard/risk | Data Quality | UI; GLOF Ontology | UI/schema distinction test |
| R-028 | Materialised databases are rebuildable | Software Architecture | Search/Graph; Data Commons | Rebuild integration test |
| R-029 | Local/offline/sovereign deployment is supported | Software Architecture | Deployment; Data Commons | Offline bundle test |
| R-030 | Multi-repository architecture exists from v0.1 | Repository Architecture | Deployment; v0.1 Implementation | Coordinated release manifest |
| R-031 | Volunteer review is repository native | Volunteer HITL | Responsible Autonomy | Git review workflow test |
| R-032 | Review decisions enter provenance | Responsible Autonomy | Evidence/Provenance | Decision-to-output traversal |
| R-033 | Scientific validation is distinct from software validation | Testing/QA | Data Quality; Model Commons | Separate QA artefacts |
| R-034 | Model scores are not called probabilities without calibration support | Model Commons | Training/Benchmark | Calibration reporting test |
| R-035 | Model providers are replaceable | Agent Commons | Software Architecture | Alternate-provider test |
| R-036 | Sensitive/private overlays can coexist with public schemas | Data Commons | Security; Deployment | Institutional profile design test |
| R-037 | CRIC Core remains extensible to other climate hazards | Core Ontology | Product Vision; v0.2 | Second-domain extension test |
| R-038 | Releases identify exact component versions | Deployment/Releases | Repository Architecture | Coordinated manifest |
| R-039 | Candidate agent knowledge is visibly distinct | Human UI | Knowledge Lifecycle | UI acceptance test |
| R-040 | External researchers can reproduce the v0.1 evidence-to-model chain | v0.1 Implementation | Testing; all core specifications | v0.1 Definition of Done |
| R-041 *(ACCEPTED — Engineering Coordinator, `docs/OPEN_QUESTIONS.md` U5, channel event `7c037f772b9bb01b6b388ca4dea1ddc980b26738b08d721f35e7b0ac539041e1`, 2026-09-03T10:04:53Z)* | LLMs may write to the knowledge store only via structured mutation → validation → human/policy check → atomic write | Agent Commons | Deterministic Retrieval Engine; Responsible Autonomy | Write-boundary bypass test must fail |
