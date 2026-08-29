# Lessons

Failures, the fixes that worked, recurring defects, and patterns worth reusing. A
lesson earns an entry when it would cost someone an hour to rediscover — not every
correction.

## Stale "not yet a git repository" fact carried by two independent agents

**What happened:** Both Fizz and the Memory & Knowledge Manager independently carried
a memory fact that `/home/ash/Eyekyam/CRIC-Core` was "not yet a git repository" — true
when first recorded, stale by the time it mattered (the repo was initialized, given an
`origin`, and had two PRs merged to `main` later the same day). Both agents caught and
corrected it themselves before it caused a bad decision, but only because each happened
to re-check `git status` while doing unrelated work.

**Why it matters:** a stale repo-state fact in memory is cheap to write and expensive
to silently rely on — the failure mode isn't "wrong once," it's "wrong in every
session that trusts the memory instead of the filesystem." Multi-agent projects with
persistent per-agent memory are structurally exposed to this: nothing forces a memory
write to be re-validated after the state it describes changes.

**Pattern to reuse:** for any fact about live repo/infra state (git-initialized,
current branch, CI status, protection rules), re-verify against the actual source
(`git status`, `gh`/API call) before relying on a memory file's claim, rather than
trusting the memory's timestamp as a freshness guarantee. Memory is a pointer to where
to look and what was true when written, not a cache that invalidates itself.

## A fabricated cross-project precedent almost entered a permanent record

**What happened:** `decisions/0001-adr-location.md`'s first draft justified filing
ADRs under `decisions/` by citing "precedent" — EnergyMatrix's ADR-0004 "moved ADRs
out of `docs/adr/` into `decisions/`." The Memory & Knowledge Manager's own persistent
memory (`buzz mem` slugs `core` and `energymatrix-facts`) carried this same claim
across sessions. Pollen's INV-2 pass checked it against the actual EnergyMatrix repo
rather than accepting it on the page: `docs/adr/` never existed there, and `decisions/`
was used from that repo's own ADR-0001 — a full day before ADR-0004 was written. ADR-
0004 does contain the sentence "ADRs stay in `decisions/`," but as one consequence of a
GSD-lifecycle-adoption decision, not a ruling that established or migrated the
location. No migration ever happened; there was nothing to cite.

**Why it matters:** the claim didn't originate as a one-off typo — it was written once,
saved to persistent memory as fact, and then repeated correctly-sounding across two
separate projects and multiple sessions without ever being re-checked against the repo
it described. Confident, consistent repetition is not evidence of accuracy; it can be
the signature of an error that was never independently checked the first time.

**Pattern to reuse:** a claim that cites another project or an earlier decision as
"precedent" is a citation, not a fact about the current repo — verify it against that
other source directly (the actual commit history, the actual file) before writing it
into a permanent record, every time it's used, not just the first time. Persistent
memory makes this worse, not better, if unchecked: it lets a false claim survive
indefinitely once written, because nothing forces it back to source. Fixed at the
source this time: `decisions/0001-adr-location.md` no longer claims a precedent it
doesn't need (the Engineering Coordinator's own WP-0 proposal is sufficient), and the
`core`/`energymatrix-facts` mem slugs were corrected the same session so the claim
stops propagating.

## A snapshot-with-caveat went stale between authoring and merge

**What happened:** while D1 (GitHub org placement) was still unresolved, this file's
Remote field read *"transfer in progress, not yet confirmed complete... do not treat
the new remote as live until the Coordinator confirms."* That was accurate when
written. The Engineering Coordinator's confirmation landed between this role's last
push and the PR's merge — so the merged result stated an instruction ("don't treat the
org remote as live") that was already false the moment it landed on `main`, and stayed
that way silently, because nothing re-reads a caveat once it's written. Caught by the
Coordinator checking the *merged result* against current reality (the same discipline
`CLAUDE.md` §9 names for code), not by either author — Pollen's review of the branch
and the Coordinator's confirmation were each individually accurate; only their merge
into a world that had moved produced the false statement.

**Why it matters:** a value-plus-embargo ("X is currently A; don't treat B as true
until someone confirms") is structurally different from a stale fact — it doesn't just
describe an outdated state, it *instructs* the reader to disbelieve the current true
state until a condition fires. Nothing forces that condition to be re-checked, so the
instruction outlives its own justification by default. This is the third staleness
incident in one session (see the two lessons above), and the first where the record
was actively wrong rather than merely outdated.

**Pattern to reuse, per the Engineering Coordinator's ruling:** classify a fact about
live external state when it's written, not later.
- **Cheap and deterministic to re-derive** (one command or API call — a remote URL, a
  branch's protection state, an org's settings): record the authoritative source plus
  a dated observation, never an embargo. A pointer to where truth lives cannot go
  stale the way an instruction to disbelieve reality can.
- **Expensive or judgment-based** (a human decision, external party, real work to
  establish): record value, date, owner, **and the trigger that makes it stale** — the
  event that means "re-check this now," not a review cadence. An owner without a
  trigger is a wish; nothing fires it.

See `docs/PROJECT_FACTS.md`'s own conventions section for where this rule now lives,
applied to its own Remote field as the worked example.
