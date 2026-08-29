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

## A pronoun guess about a real person entered the permanent decision record — and it was wrong

**What happened:** `decisions/0002-defer-github-organisation.md`, `decisions/0003-create-github-organisation.md`,
and `docs/OPEN_QUESTIONS.md` each described Ashley creating the GitHub organisation
"herself." Ashley's pronouns had not been stated anywhere in the channel at the time.
A name is not a pronoun; the word was written on the strength of an assumption, not a
fact, and signed into three separate permanent records before anyone checked it.
Caught by the Engineering Coordinator's sweep, not self-caught — a presence-scan for
stale org references (this session's other lesson) would never have found it, because
the word "herself" wasn't stale, it was wrong from the moment it was written. The
Coordinator's objection was to the *process* — a guess with nothing in the channel to
support it — independent of whether the guess happened to be right. It turned out not
to be: Ashley stated he/him minutes later, and the records were corrected a second
time, from the inferred "herself" to the actual "himself."

**Why it matters:** this class of error is quieter than a factual mistake about a
system — nobody's git log or API response ever "corrects" a wrong pronoun, so unlike
this session's other staleness lessons, there is no external signal that will surface
it on its own. It only gets caught by a reader who notices, and the record stays wrong
indefinitely if nobody does. It is also about a real person, not a system — the cost of
guessing wrong is different in kind, not just probability, from guessing wrong about a
remote URL. And the fact that the guess turned out wrong isn't the point being
recorded here — a guess that happened to land right would have been exactly as bad a
process, just invisibly so. The lesson is "a guess about a real person went into a
signed, permanent record three times, and the only reason it got caught is that
someone read for unsourced claims rather than for stale strings" — not "we got lucky
checking."

**Pattern to reuse, standing rule:** never infer a pronoun for a real person from their
name. Use they/them for anyone whose pronouns have not been explicitly stated, then use
what they actually stated once they state it — in every record this role writes: ADRs,
the decision register, `OPEN_QUESTIONS.md`, channel messages, everywhere. If precision
without a pronoun reads awkwardly before it's known, restructure the sentence (e.g.
"created the organisation directly") rather than reach for a guess.

## Hand-abbreviated event ids are unreliable even when the underlying verification is real

**What happened, twice independently in one PR (#15):** the Memory & Knowledge Manager
wrote several `first8…last7`-style abbreviations of 64-character hex event ids into
`docs/OPEN_QUESTIONS.md` and `docs/PROJECT_FACTS.md` that didn't match the full id they
were meant to shorten — real substrings of the correct id, but from the wrong position
(e.g. `8d0c3e56…649a4a6` written for an id whose actual tail is `…4a66628`). Caught by
re-slicing every full id with a script and diffing, not by re-reading the prose. Then,
reviewing that exact fix, Pollen restated nine of those same abbreviations from memory
in a channel message rather than re-slicing them, and three of the nine were wrong the
same way — despite Pollen's own message claiming "every single event id checked against
the raw thread, not sampled," which was true of the verification step and false of the
transcription step.

**Why this is the important part:** in every instance, the underlying claim — this
event, this author, this content, this timestamp — was independently verified and
correct. What failed both times was purely mechanical: turning a full id already held
correctly in hand into a short human-readable string, by recall or by eye rather than
by re-slicing the actual bytes. This is not the same failure as this file's other
staleness lessons (a true-when-written fact going stale) or the pronoun lesson (an
unsourced guess) — the fact was never wrong, the *citation string representing it* was
garbled in transcription. It recurred within minutes, on the same PR, by two different
parties, one of whom was specifically trying to demonstrate rigour at the moment it
happened — evidence this is a generic hand-transcription failure mode, not a one-off
lapse by either party.

**Pattern to reuse, standing rule:** never hand-type or recall-from-memory an
abbreviated event id for a permanent record or a claim about rigour. Either (a) slice
it mechanically from the full id at the moment of writing (`full_id[:8] + '…' +
full_id[-7:]`, via script, never by eye), or (b) prefer the full, untruncated id
entirely for anything that will outlive the conversation — ADRs in this repo now do
this throughout, specifically to remove the failure mode rather than mitigate it.
Restating a citation you already verified is a fresh act of transcription with its own
failure rate; "I checked this" about the underlying fact does not make "I copied this
correctly" true about the shorthand.
