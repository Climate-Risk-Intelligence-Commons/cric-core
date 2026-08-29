# Decision Register

Index of all Architecture Decision Records for this repository. ADRs live in
`decisions/NNNN-slug.md` (see `decisions/0001-adr-location.md` for why, not
`docs/adr/`). One row per decision; status uses the project's standard ladder where
applicable, otherwise `Proposed` / `Accepted` / `Superseded`.

| ID | Title | Status | Approver | Date | Freeze Point? |
|---|---|---|---|---|---|
| [0001](../decisions/0001-adr-location.md) | ADRs live in `decisions/`, not `docs/adr/` | Accepted | Engineering Coordinator | 2026-08-29 | No |
| [0002](../decisions/0002-defer-github-organisation.md) | Defer creating the `climate-risk-intelligence-commons` GitHub organisation | Accepted | Ashley | 2026-08-29 | No |

No Architecture Freeze Point has been ratified yet — Phase 1 (`cric-core`) has not
started. When one is, its ADR's **Freeze Point?** column entry links to the specific
freeze point (of the 8 listed in `docs/PROJECT_FACTS.md`), names Ashley as approver
(not the Engineering Coordinator), and its consequences section states explicitly that
reversal requires a formal migration, not routine amendment — per the ratification
checkpoint in `docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` §2.
