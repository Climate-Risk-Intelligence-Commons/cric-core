# Decision Register

Index of all Architecture Decision Records for this repository. ADRs live in
`decisions/NNNN-slug.md` (see `decisions/0001-adr-location.md` for why, not
`docs/adr/`). One row per decision; status uses the project's standard ladder where
applicable, otherwise `Proposed` / `Accepted` / `Superseded`.

| ID | Title | Status | Approver | Date | Freeze Point? |
|---|---|---|---|---|---|
| [0001](../decisions/0001-adr-location.md) | ADRs live in `decisions/`, not `docs/adr/` | Accepted | Engineering Coordinator | 2026-08-29 | No |
| [0002](../decisions/0002-defer-github-organisation.md) | Defer creating the `climate-risk-intelligence-commons` GitHub organisation | **Superseded** by 0003 | Ashley | 2026-08-29 | No |
| [0003](../decisions/0003-create-github-organisation.md) | Create the `Climate-Risk-Intelligence-Commons` GitHub organisation and transfer `cric-core` into it | Accepted, transfer confirmed complete | Ashley | 2026-08-29 | No |
| [0004](../decisions/0004-freeze-point-1-identifier-format.md) | Freeze Point 1 — object identifier format, `CRIC:<namespace>:<type>:<ulid>` | **Accepted — locked** | Ashley | 2026-08-29 | **Yes — Freeze Point 1 of 8** |
| [0005](../decisions/0005-fanout-default-with-stated-reason.md) | Parallelisation is the default; declining it needs a stated reason | Accepted | Ashley | 2026-08-29 | No |

**Freeze Point 1 (ID format) is ratified — the first of 8 to lock.** Phase 1
(`cric-core`) has started: packaging and CI are merged (WP-4 waves 1-2, see
`docs/PROJECT_FACTS.md`), and WP-6 (build-order item 1, identifier types) is dispatched
against ADR-0004. The remaining 7 Freeze Points are not yet ratified. Each of their
ADRs, when written, links its **Freeze Point?** column entry to the specific freeze
point (of the 8 listed in `docs/PROJECT_FACTS.md`), names Ashley as approver (not the
Engineering Coordinator or Fizz), and its consequences section states explicitly that
reversal requires a formal migration, not routine amendment — per the ratification
checkpoint in `docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` §2, exercised
for the first time in ADR-0004.
