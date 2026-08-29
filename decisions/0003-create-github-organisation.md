# ADR-0003: Create the `Climate-Risk-Intelligence-Commons` GitHub organisation and transfer `cric-core` into it

- **Status:** Accepted — **supersedes ADR-0002**
- **Approver:** Ashley
- **Date:** 2026-08-29
- **Evidence:** Ashley, channel CRIC-Dev (`17bd72a0-4d90-4e0b-b102-f9163f0cfd4b`), event
  `f427cf9b057f5d014e481fd41a1ddfb61ab67cf1e808988ecdf9c754f85a4953`, 2026-08-29T14:01:12Z
  — "I have changed my mind on creating the organization on GitHub. I have already
  created the organization <https://github.com/Climate-Risk-Intelligence-Commons>. I
  am about to transfer the ownership to the organization." Engineering Coordinator
  independently verified the org's existence and the token's access to it before this
  ADR was written: event `18d9b9acdc38cc180996ebe869e354a06e80c2bea04363b1fbaa122db4f4c22b`,
  2026-08-29T14:03:12Z (`GET /orgs/Climate-Risk-Intelligence-Commons` → exists, free
  plan; `GET /user/orgs` → lists it; `GET /user/memberships/orgs/…` → `role: admin`).

## Context

This is the third state D1 (GitHub organisation placement) has held in roughly 30
minutes: agree to create (13:31:46Z) → defer, stay put (13:43:22Z, ADR-0002) → create
after all, transfer in progress (14:01:12Z, this ADR). Per the Engineering
Coordinator's request, this is recorded as a superseding ADR rather than an edit to
ADR-0002, and `docs/OPEN_QUESTIONS.md`'s D1 row is kept as a dated sequence of all
three states rather than overwritten to only the latest — the reversals are
informative in their own right (see Consequences).

## Decision

Create `github.com/Climate-Risk-Intelligence-Commons` (done — verified by the
Engineering Coordinator, not merely asserted by Ashley) and transfer `cric-core` into
it (in progress as of this ADR's date — see Status below). This supersedes ADR-0002's
"stay at `ashley-eyekyam/cric-core`" decision.

## Alternatives considered

Both prior states are alternatives actually held, not hypotheticals:

1. **Create the org immediately** (Ashley's original 13:31:46Z position). Superseded by
   (2) 12 minutes later.
2. **Defer indefinitely, stay at `ashley-eyekyam/`** (ADR-0002, 13:43:22Z — "too
   complicated," revisit later). Superseded by (3) 18 minutes later, once Ashley
   created the org directly rather than through the Coordinator's proposed mechanics.
3. **Create the org, transfer `cric-core` into it** (this ADR, 14:01:12Z). Current.

## Execution status (update this section in place as it progresses, do not re-ADR each step)

- ✅ Organisation created and verified reachable by the Coordinator's token
  (`role: admin`), 2026-08-29T14:03:12Z.
- ✅ Repository transfer of `cric-core` — **confirmed complete.** Engineering
  Coordinator, event `1ba66212dee5a30c7b56f1ce58c1dd0de48931201c42a9924deae0b096da469f`,
  2026-08-29T14:08:50Z: `GET /repos/Climate-Risk-Intelligence-Commons/cric-core` →
  `full_name Climate-Risk-Intelligence-Commons/cric-core, owner_type Organization`.
  Independently re-verified by the Memory & Knowledge Manager against the live GitHub
  API before writing this line, not accepted from the pasted output alone:
  `gh repo view Climate-Risk-Intelligence-Commons/cric-core` returns
  `nameWithOwner: Climate-Risk-Intelligence-Commons/cric-core`, `defaultBranchRef: main`;
  `gh pr view 7 --repo Climate-Risk-Intelligence-Commons/cric-core` resolves and returns
  `state: OPEN, mergeable: MERGEABLE` — the org-owned remote is live and this PR is
  reachable through it. `docs/PROJECT_FACTS.md`'s remote field updated accordingly.
- ✅ Branch protection surviving the move — confirmed by the Coordinator: settings read
  back identical post-transfer (`enforce_admins` on, PR required, force-push/deletions
  off, conversation-resolution on), and enforcement re-verified against the org URL
  (direct push to `main` rejected, a branch push accepted). Not independently re-run by
  this role — accepted on the Coordinator's evidence, which included the actual
  before/after config and a live enforcement test, not narration.
- ⏳ Repo creation working *inside* the org from the Coordinator's token — still
  unproven by design (no throwaway repo left behind to test it); proven by the first
  real Phase 0 repository instead.

## Consequences

- `product/Repository-and-System-Architecture.md`'s `github.com/climate-risk-intelligence-commons/`
  layout (case differs slightly from the actual org name,
  `Climate-Risk-Intelligence-Commons` — GitHub org slugs are case-insensitive for
  routing but the canonical display name should be cited consistently; using the
  actual created org's casing going forward) moves from **aspirational to
  descriptive**, reversing ADR-0002's consequence once the transfer completes.
- ADR-0002 is **not deleted** — it remains the accurate record of what was decided and
  why between 13:43:22Z and 14:01:12Z. Marked Superseded in `docs/DECISION_REGISTER.md`,
  not removed.
- `docs/OPEN_QUESTIONS.md`'s D1 row becomes a timeline of all three states rather than
  a single current value — see that file for the format.
- Old clone URL `github.com/ashley-eyekyam/cric-core.git` redirects post-transfer (per
  the Coordinator's verification); update references opportunistically, not urgently.
- **Process note, stated plainly because it's true:** three D-item reversals inside 30
  minutes on the same question is a real cost of moving fast on a governance-adjacent
  decision before the mechanics were understood, not a process failure on this role's
  part or Ashley's — recording it accurately, including the churn, is what makes the
  record trustworthy the *next* time D1-shaped uncertainty comes up on a different
  question.
