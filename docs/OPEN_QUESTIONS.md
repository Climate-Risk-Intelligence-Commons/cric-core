# Open Questions

D-items are decisions someone with authority must make. U-items are unresolved facts
or confirmations. Every item has an owner — a blank owner is escalated, not left. Dates
are absolute (Buzz event timestamps or the date raised in-channel).

## Blocking

| ID | Question | Owner | Blocks | Raised | Resolved |
|---|---|---|---|---|---|
| D1 | GitHub organisation: stay at `github.com/ashley-eyekyam/cric-core`, or create `github.com/climate-risk-intelligence-commons/` now (per `product/Repository-and-System-Architecture.md`'s named layout) before Phase 0 creates 11 more repos? | Ashley | Phase 0 (repository creation) | 2026-08-29 (Engineering Coordinator, event `feb934ea…62a706e`) | — |
| D2 | Outbound licence per repository *type* — `cric-core`'s AGPL-3.0 was a repo-creation-time choice, not a PRD ruling, and the PRD is silent on CRIC's own repos' licensing (only ingested source-data licensing is specified). Engineering Coordinator's recommendation: code repos AGPL-3.0, knowledge/data/docs repos CC-BY-4.0. | Ashley | Phase 0 (repository creation, licence files) | 2026-08-29 (Engineering Coordinator, event `feb934ea…62a706e`) | — |
| U2 | Does Honey's mandate already treat `files_allowed_to_change`/`prohibited_changes` as hard boundaries (vs. the "I noticed X was also wrong so I fixed it too" reflex that's good practice single-repo but the named failure mode here), and default to TDD as implementation discipline? | Honey | First Phase 1 work package dispatch | 2026-08-29 (`01-Existing-Agent-Fit-Assessment.md`; re-asked directly by Engineering Coordinator, event `feb934ea…62a706e`) | — |
| U3 | Does Honey accept the widened, temporary "Build & Release Engineer" brief for Phase 0 + Phase 14 (`docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` §3), rather than a separate identity being stood up? | Honey | Phase 0 dispatch | 2026-08-29 (Engineering Coordinator, event `feb934ea…62a706e`) | — |
| U4 | Does Pollen's verification pass treat a work package's `acceptance_criteria` as the primary pass/fail bar, and stop-and-escalate to Ashley (not self-approve) when a change trips any of the five Human Review triggers or touches a locked Freeze Point? | Pollen | Phase 1 exit review / first Freeze Point ratification | 2026-08-29 (Engineering Coordinator, event `feb934ea…62a706e`) | — |

## Non-blocking

| ID | Question | Owner | Notes | Raised | Resolved |
|---|---|---|---|---|---|
| D3 | Branch protection ruleset for `main` (required status checks + linear history + no force-push; **no** required approving reviews, since every agent pushes under the same GitHub token). | Engineering Coordinator | Not blocking — Coordinator proceeds on this basis unless Ashley objects. | 2026-08-29 | — |
| U5 | R-041 ("LLMs may write to the knowledge store only via structured mutation → validation → human/policy check → atomic write") is marked "PROPOSED — pending Ashley's decision, not yet ratified" in `docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md`. | Ashley | Doesn't block current work; tracked so it isn't forgotten before Phase 6/8 need it. | 2026-08-29 | — |

## Resolved

| ID | Question | Owner | Resolution | Raised | Resolved |
|---|---|---|---|---|---|
| U1 | Does Fizz's mandate already default to "registry outranks specialised docs," or was that freshly derived each time? | Fizz | **Freshly derived, not memorized** — Fizz's core memory carries no CRIC-specific precedence content; the standing reflex is procedural (check the primary document's actual clause, not a prose gloss), not a memorized content rule. Fizz also committed to owning `authoritative_prd_sections`/`upstream_contracts` on every work package. | 2026-08-29 (`01-Existing-Agent-Fit-Assessment.md`) | 2026-08-29 (Fizz, channel CRIC-Dev, in-thread reply) |
| — | Does the Memory & Knowledge Manager distinguish "log this decision" from "log this decision **and** it is a locked Freeze Point whose reversal requires explicit migration"? | Memory & Knowledge Manager | **Yes** — any ADR for one of the 8 Architecture Freeze Points names Ashley as approver and its consequences section states explicitly that reversal requires a formal migration, not routine amendment. Adopted as a hard rule; see `docs/DECISION_REGISTER.md`. | 2026-08-29 (`01-Existing-Agent-Fit-Assessment.md`) | 2026-08-29 (Memory & Knowledge Manager, channel CRIC-Dev, in-thread reply) |
