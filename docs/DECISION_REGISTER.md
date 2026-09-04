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
| [0006](../decisions/0006-dataasset-canonical-type.md) | `DataAsset` is the canonical ontology type; `Asset` is prose only | Accepted — propagation, not amendment | Engineering Coordinator | 2026-08-29 | No (mandatory input to Freeze Point 2) |
| [0007](../decisions/0007-freeze-points-6-7-knowledge-state-review-decision.md) | Freeze Points 6 + 7 — knowledge-state vocabulary and review decision schema, ratified as one unit | **Accepted — locked** | Ashley | 2026-09-03 | **Yes — Freeze Points 6 and 7 of 8** |
| [0008](../decisions/0008-ci-generated-build-status.md) | Build status is CI-generated, never hand-typed; no CI job without a subject | Accepted | Engineering Coordinator | 2026-09-03 | No |

**Consolidation note, 2026-09-03:** Ashley asked for "proper decisions" on licence,
README, contributing, code of conduct, security, governance, CI, branch protection and
decision records in one message (event `5e4d410b5988dbf69139e7b162262ef6bd4e38a4ce3a01a9c8d43949fd104b6b`).
Most of that set restates decisions already on this register — licence (D2, below),
branch protection (D3, below), the `decisions/` location convention (0001), and
today's community-health-file work (WP-19/WP-19a: `CODE_OF_CONDUCT.md`, `SECURITY.md`,
root `CONTRIBUTING.md`/`GOVERNANCE.md` pointers) — those are not re-recorded as new
ADRs. **ADR-0008 is the one genuinely new ruling from that pass**; see its own Context
for why the rest don't get their own entries here.

**Freeze Points 1, 6 and 7 are ratified — three of 8 locked.** Phase 1
(`cric-core`) has started: packaging and CI are merged (WP-4 waves 1-2, see
`docs/PROJECT_FACTS.md`), and WP-6 (build-order item 1, identifier types), against
ADR-0004, is merged (PR #17, `main` at `fda79b1`) — Freeze Point 1 is now executable
code. Freeze Points 6 and 7 (ADR-0007) are ratified but not yet implemented — Honey's
WP-18 (build-order item 2, knowledge-state models) is the first code against them.
Freeze Point 4 (provenance model) briefly looked coupled into ADR-0007's unit and was
found not to be — it remains unratified, on its own evidence, along with Freeze
Points 2, 3, 5 and 8. Each remaining ADR, when written, links its **Freeze Point?**
column entry to the specific freeze point (of the 8 listed in `docs/PROJECT_FACTS.md`),
names Ashley as approver (not the Engineering Coordinator or Fizz), and its
consequences section states explicitly that reversal requires a formal migration, not
routine amendment — per the ratification checkpoint in
`docs/CRIC-Implementation-Team/02-New-Role-Gap-Analysis.md` §2, exercised first in
ADR-0004 and, for the first time under real adversarial pressure across five rounds,
in ADR-0007.
