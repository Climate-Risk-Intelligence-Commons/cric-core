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

## A bundled open-question item let a partial answer read as a full resolution

**What happened:** D6 in `docs/OPEN_QUESTIONS.md` carried two decisions in one row —
running `/gsd-ingest-docs` with the precedence manifest, and separately, whether
`.planning/config.json`'s `"mode": "yolo"` / `"auto_advance": true` posture (which
removes GSD's human-gated phase-advance step, the same discipline this project's
Freeze Point ratification runs on) should stand as-is. Both were raised in the same
channel message and recorded as one item because they were *discovered* together, not
because they were the same decision. The Engineering Coordinator's 2026-09-04 digest
carried the bundle forward into a single blocking item, and flagged it himself before
anyone acted on it: if Ashley had simply run the `/gsd-ingest-docs` command, the row
would read as resolved — closed by the mechanical action — while the `yolo`/
`auto_advance` governance question, never actually addressed, silently rode along to
"resolved" with it.

**Why it matters:** a register or digest item's job is to make one decision visible
and trackable to closure. Bundling two independently-answerable questions into one row
breaks that at the structural level, not the prose level — no amount of careful digest
wording fixes it, because the underlying record itself conflates "this row is closed"
with "every question raised alongside this row is closed." The failure is invisible
until someone answers only the easier half, which is exactly the shape a human
skimming a blocking-items list is likely to do.

**Pattern to reuse:** one D/U item, one decision. When two questions are discovered in
the same finding or the same channel message, that's a reason they were raised
together — not a reason to record them together. Split at the source (the register
row itself), not just in how a digest phrases it downstream; a digest built from an
already-bundled item will re-bundle it every time, no matter how careful that day's
phrasing is. Applied here: D6 (the ingest-docs re-run) and the new D9 (the
`yolo`/`auto_advance` posture) were split into separate rows the same day this was
caught, both still pointing at their shared origin event so the history isn't lost.

## A citation resolved, was correctly authored and timestamped, and still labelled the wrong content

**What happened:** `docs/OPEN_QUESTIONS.md` D10 cited an event as "the Coordinator's
ruling and FP2-routing withdrawal." The event was real, the author was right, the
timestamp was right, and the quoted words genuinely appeared in it — but they appeared
as a passing backward reference ("having already withdrawn one routing ruling today"),
not as the ruling itself. The actual ruling lived in a different message, five and a
half minutes earlier. Pollen's review had checked the citation and reported it clean —
correctly, by the check he ran: the ID resolved, to the right author, at the right
time, containing the quoted substring. That check answers "does this citation point at
something real." It does not answer "does the citing sentence's description match what
the event actually contains" — a different claim, about content rather than existence,
and nobody had run it until the Coordinator re-read his own citation before amplifying
it further and caught the mismatch himself.

**Why it matters:** a citation that carries a label — "ruling," "withdrawal,"
"finding," "the severe one" — is making two claims at once: that the pointer resolves,
and that the described content lives there. A review that verifies only the first
claim looks identical to one that verified both, right up until someone reads the
cited passage for what it actually says. This is the third citation-integrity failure
recorded in this file (hand-abbreviated event ids; a fabricated cross-project
precedent), and it's the first where the pointer itself was flawless — the defect was
entirely in the description wrapped around it.

**Pattern to reuse:** when a citation carries a label describing what the cited event
*is* or *contains* (not merely *where a fact appears*), verify the label against the
body of the cited passage directly — read it for whether it is the labelled thing —
rather than stopping once the ID resolves to the right author and timestamp. "Existence
verified" and "content verified" are different claims; a review checklist that only
runs the first will pass a citation that is wrong in exactly the way that matters.

## A generator can be internally coherent and still be wrong — and coherence is what stops review

**What happened:** a `/gsd-ingest-docs` bootstrap run produced `.planning/REQUIREMENTS.md`
with `KS-01` defining a `KnowledgeState` enum (`confirmed, supported, contested,
contradicted, unknown, unobserved, no_known_event`) with zero overlap against both the
ratified Registry vocabulary and the `KnowledgeStateStatus` enum that had already
shipped as tested code. The first check of the run's output (`ROADMAP.md` only) found
two real but comparatively minor defects and stopped — not from carelessness, but
because `ROADMAP.md` genuinely was clean past those two, and `REQUIREMENTS.md`, the
file an implementer actually builds from, was never opened. Testing a proposed
verification rule against the same artefact then surfaced a third, distinct failure
mode in a different Freeze Point's block: a real field (`content_sha256`, doubly
attested in the corpus) renamed and relocated as a differently-named top-level field
(`content_hash`) — a defect that survives a concept-level grep, unlike an outright
invention like `source_type`, which fails one immediately.

**Why it matters:** the generator got the hard, genuinely constitutional part of KS-01
right (`unknown ≠ false`) and built five mutually-consistent requirements around that
correct principle before attaching the whole structure to the wrong field. Internal
coherence is exactly what makes a reviewer stop checking — nothing about a
self-consistent, plausible-sounding requirement block signals that it needs a check
against source. Three distinct generator failure modes are now documented from one
session's output: invent a value from nothing (fails a grep immediately); rename and
relocate a real field (survives a concept-level grep — the most dangerous of the
three, because it reads as familiar); lift real values from the wrong section onto the
wrong field (internally coherent, which is what stops review). All three are checkable
only by reading the artefact against its source, never by trusting internal
consistency as a proxy for correctness.

**Pattern to reuse:** a generated artefact's internal consistency is not evidence of
its correctness — it is, if anything, weak evidence *against* someone having checked
it, since coherence is exactly what makes a defect easy to miss. When checking
generated content against a source of truth, read every file the downstream builder
would actually read (not just the most prominent one), and check for all three failure
shapes explicitly — invented values, renamed/relocated real values, and misattributed
real values — rather than stopping at the first clean-looking pass. `decisions/0009-fp-requirement-verification.md`
encodes the resulting standing check for this project's own generated planning
artefacts.

## A "missing rows" finding was reported without checking the actual file, and was wrong

**What happened:** WP-34's finding #3 stated `docs/DECISION_REGISTER.md` was "missing
rows for ADR-0008 and ADR-0009, both already on `main`." The Engineering Coordinator
routed it for a future fix without checking it himself. Verified directly against
`main` while preparing this records package: both rows have existed since the commit
that introduced each ADR (`f94694b` for 0008, `2547ffe` for 0009) — there was never a
point where either ADR existed on `main` without its register row. The finding was
simply wrong, relayed from a subagent's report rather than checked against the file.

**Why it matters:** a "missing X" claim is a negative claim about a specific,
cheaply-checkable file — exactly the kind this project's own EVIDENCE requirements
name as needing the exact scope searched, stated with the claim. This one didn't get
even that: nobody grepped the file before reporting or before routing the fix.
Unlike a citation that resolves to the wrong content, this defect had a one-command
falsification available the whole time and nobody ran it.

**Pattern to reuse:** before reporting or routing a "missing X" / "no row for Y" /
"file doesn't contain Z" finding, grep or read the actual current file yourself. A
completeness claim about a small, named file is cheaper to verify directly than to
carry forward on trust — cheaper, in fact, than writing the finding down.

## A test count taken from a stale local checkout looked exactly like a regression

**What happened:** verifying the README's documented install-and-test instructions,
the Engineering Coordinator's first attempt cloned the local checkout at
`/home/ash/Eyekyam/CRIC-Core` instead of the public GitHub repository, and got
`32 passed` — a number that would have read as a severe regression from the `139`/
`166` already on record, on a repository nobody had actually broken. He caught it
himself before publishing the number, re-ran against a genuine fresh clone of the
public repo, and got `166` — reported plainly as his own error rather than silently
corrected.

**Why it matters:** the shared local checkout at that path is explicitly documented
(this project's own worktree convention, `docs/PROJECT_FACTS.md`) as liable to be
sitting on someone else's branch at any given moment — it is not a stable stand-in
for "the public repo." A test count taken from it can be internally consistent
(pytest ran, produced a real number, nothing crashed) and still describe the wrong
tree entirely, with no error message to flag the mismatch. This is the same family as
"32 vs 21" (right number, wrong unit) but one layer further back: wrong *source*, not
wrong *unit* — and unlike a unit mismatch, a wrong-source test count is
indistinguishable from a real regression until someone checks where it actually ran.

**Pattern to reuse:** when a claim will be published as "verified against the real
repo" — an install guide, a README instruction, a release check — clone fresh from
the actual remote rather than reusing a local checkout, even one that looks current.
If a number would read as alarming (a big drop, a red check), that is itself a signal
to check the source before the number, not after.

## A rebase moved the tree without moving the prose that describes it

**What happened:** PR #39's `docs/PHASE-1-COMPLETION-PLAN.md` and
`docs/PROJECT_FACTS.md` were drafted against `fa22597`, then the branch was rebased
onto `origin/main` (`72f3fb7`, which includes PR #38/WP-32's
`src/cric_core/review/`) to avoid conflicts. The rebase did exactly what a rebase
does — the tree ended up in sync with `main`, no conflicts, nothing lost. It cannot,
and did not, update the prose describing that tree: three separate spots kept saying
build-order item 9 ("review contracts") hadn't shipped, on a commit where it plainly
had (confirmed directly: `git merge-base HEAD origin/main` was exactly `72f3fb7`,
`ls src/cric_core/` showed `review/` present). Found by Honey's non-author review,
independently reconfirmed by the Engineering Coordinator before either routed it as
fixed.

**Why it matters:** this is the same family as "a measurement taken at one commit and
reported at another" (see this file's other entries on stale snapshots and stale test
counts) but a new variant within it — the earlier ones involved a number disagreeing
with itself (166 vs 32, 3 vs 2 defects); this one had no number to disagree with. A
document that names its own basis commit in its header reads as more trustworthy for
doing so, which is exactly what let the mismatch survive a citation-level check: every
individual citation in the document was still accurate against `fa22597`, and the
document's own header still named `fa22597` as its pin. The defect was only visible by
reading the prose against the tree the branch actually ships in, not against the tree
it was drafted against.

**Pattern to reuse:** if a document declares its own basis commit and its branch gets
rebased afterward — for any reason, including pure conflict avoidance — treat every
claim in that document about what code exists as needing re-derivation, not just
re-verification of citations. The rebase changes the tree the document ships in even
when it changes none of the document's own lines.

## "Nothing forbids it" is not evidence for it — the same inference failed three times in one round

**What happened:** in one Wave 1 ruling round, the same reasoning shape produced a
wrong inference three separate times, each caught by someone other than its author.
FP4's original field-count claim borrowed a nine-field embedded-`provenance` shape
from the OKF Universal Frontmatter — the field existed and nothing said it didn't
apply to FP4 — when the actual source was one side of an unrelated, unresolved
disagreement (D10) about a different Freeze Point's subject. FP3's original
`Observation.value` placement reasoned that `false`/`absent`/`not detected` belonged
there because nothing said they belonged anywhere else — an untyped field, not a
closed one. And earlier the same day, carve-out #4 was closed on the inference that
FP4 implied a `derived_from` predicate, when the text never mentioned one at all in
either direction.

**Why it matters:** all three have the identical shape — treating the absence of a
contrary statement as if it were a statement of support — and all three were
initially presented with the same confidence as the claims that turned out to be
well-supported. Nothing about the sentence *"nothing says otherwise"* distinguishes a
genuinely settled question from an unexamined one; the tell is always external (a
whole-corpus grep, a check against the actual disputed source), never in the
confidence of the sentence itself.

**Pattern to reuse:** when a candidate's supporting argument is "the corpus doesn't
say otherwise" or "nothing rules this out," treat that as a flag requiring a
positive citation, not as a citation in its own right. A Freeze Point (or any
decision meant to be relied on later) may not rest on absence of prohibition —
state the gap as open rather than closing it by inference, the same discipline
`decisions/0011` and `decisions/0012` apply explicitly in their own Decision
sections, not only in Alternatives.

## A wording fix and a parser fix are not two guards — the wording one is the disease

**What happened:** an unreleased build-status generator (WP-33a) would have read any
`decisions/` Status line containing the phrase "Architecture Freeze Point" as
ratified — a substring match with no check for the Status value actually being
`Accepted`. Three ADRs' Proposed-status lines all contained that phrase verbatim
(`decisions/0010`/`0011`/`0012`), which would have produced "6 of 8 Freeze Points
ratified" on a public README while Ashley had signed none of them. The Engineering
Coordinator initially asked for both a wording fix (reword the three Status lines to
avoid the phrase) and a parser fix (require the Status value to be literally
`Accepted`), then withdrew the wording half before it was committed: "one real guard
beats one guard plus a standing obligation on people who have not been told it
exists."

**Why it matters:** the wording fix looks like defence in depth — belt and braces —
but it isn't a second guard, it's an unenforced convention. It depends on every
future ADR author remembering to write around a parser defect they were never told
about, with no mechanism to catch the day someone doesn't. The parser fix (require
`Accepted` *and* a named Freeze Point, not a substring anywhere in the line) removes
the hazard structurally — "Proposed — Architecture Freeze Point candidate" becomes
an accurate, un-gamed sentence again, because nothing downstream mis-reads it.
Requiring the wording fix *in addition* would have reinstated the exact defect being
ruled against, one ADR later, the moment someone wrote a natural sentence containing
the phrase.

**Pattern to reuse:** when a defect is "a program reads meaning into text that wasn't
meant to carry it," fix the program, not the text. A text-side workaround is not a
second independent guard — it's an obligation with no mechanism enforcing it, and it
buys nothing once the real fix exists. Full chain: `decisions/0010`/`0011`/`0012`
drafted with the phrase, Coordinator finding + both-fixes instruction (channel event
`3da70cd9d4aae0fd1541306e0927380b256f5c40eeb3fc860678a22cdbef7e20`, 2026-09-05T10:46:46Z),
Honey's parser fix verified against the real PR #40 files — old check `{1,3,4,5,6,7}`,
new check `{1,6,7}` (event `f4773c6a606f1763b3ab906c17c01437e4927b835e7466b3eeb6936b50a1ec93`,
10:49:39Z), Coordinator's withdrawal of the wording instruction (event
`2744522a452ffe271e7caee423188686dc0c52b4d8775a28b12281a92f8f9996`, 10:50:20Z).

## "Someone's attention slipped" is a placeholder for a cause, not a cause

**What happened:** two people found the same defect (a wrong event timestamp cited
in `decisions/0011`/`0012` and `docs/OPEN_QUESTIONS.md`) and produced three counts
between them — the Engineering Coordinator reported four occurrences, then seven;
Pollen reported five in between. (Independently, and before either later message
landed, the Memory & Knowledge Manager caught the third file — `docs/OPEN_QUESTIONS.md`'s
D23 — by reading the file directly rather than trusting either number in flight;
that catch is its own point, not a fourth count folded into theirs.) The Coordinator
then explained *Pollen's* undercount with an attention-based theory: that "a
semantic frame re-entered at the narration," excluding a row about a decline from a
report framed around rows about signing. Pollen, separately, explained his own
undercount the same way: that he had described the finding by hand-checking with a
plain grep and "read only the first two lines" it returned. **Both explanations were
wrong.** Pollen then read his own script rather than reasoning about it, and found
the actual cause: the sweep's dedup key was `(file, event_id, cited_timestamp)` —
since three rows (D21, D22, D23) cited the identical triple, the key collapsed all
three into one reported instance per file. That key is structurally incapable of
expressing a count; the sweep could not have reported seven regardless of how
carefully anyone read its output.

**Why it matters:** an attention-based explanation ("I misread it," "a frame
narrowed my report," "I stopped trusting the tool") is always available, fits any
miss, costs nothing to produce, and implies no fix beyond "look harder next time" —
which is not a control. It is the easiest wrong answer to reach for precisely
because it requires no evidence and is never falsified by looking closer. The
structural explanation here was expensive to find (reading the actual script) and,
once found, pointed at a concrete fix that generalises: a dedup key built for
readability had silently turned a count into a boolean, the same failure shape as a
check that can assert reach but not quantity.

**A second failure, one level up, worth recording alongside the first:** this
entry's own first draft compressed the chain above — misattributing the
Coordinator's semantic-framing theory and Pollen's script-read to the wrong events,
and counting two people as three — despite the chain having been spelled out in six
numbered steps in-channel, and despite being transcribed by this team's most careful
record-keeper. The Coordinator's own first explanation for *that* mistake — "it
compressed in the direction that flatters whoever wrote the last message" — was
itself a motive story with no mechanism, the exact kind of placeholder this entry is
about, reached for one message after ruling the pattern out. The real mechanism,
found by Pollen: each event in the chain contained two things — often a real finding
paired with a wrong first guess — and the summary gave each event only one label,
displacing the second content onto the next event. A one-slot lag, not a bias toward
anyone.

**Pattern to reuse:** when explaining a miss, "someone's attention slipped" is a
placeholder, not a cause — treat it as unfinished until the actual mechanism is
identified (a key, a check, a scope, a race), or state plainly that no structural
cause was found. Anything that dedupes on content for a count you intend to trust
later must keep a location or position in its key, or it must not be the thing that
count is read from. And: an event is not a step — when transcribing who-found-what-
when, label each event with everything it contains, including the wrong halves, or
the summary silently re-times whatever it drops. A chain has to be re-derived from
the source events at write time, not paraphrased from the message that already
summarised it once — otherwise the summary becomes the source and its author
becomes the finder.

Full chain, channel CRIC-Dev. **`a18f5cf9`, 11:16:43Z (Pollen)** — the sweep, 91
citation instances across 37 unique event ids: exactly one wrong timestamp exists
corpus-wide and every cited id resolves; named D21 and D22. **`20c5cabe`, 11:17:49Z
(Coordinator)** — the seventh occurrence, D23, by grep; replaced his own fix
instruction with grep-and-prove-zero; and offered a semantic-framing theory of
Pollen's undercount, which was wrong and inferred from the symptom. **`e1f677c5`,
11:18:29Z (Pollen)** — read his own sweep script and named the dedup key `(file,
event_id, cited_timestamp)`, the one structural fact in the exchange; and attached
an attention story to it ("read only the first two lines"), which was wrong.
**`bf3c8f23`, 11:19:23Z (Coordinator)** — withdrew the semantic-framing theory; and
drew the structural implication, that such a key can express presence but never
count, so the sweep could not have reported seven regardless of who read its output
— a second step on Pollen's first, not the first step. **`603fc428`, 11:20:04Z
(Pollen)** — re-checked against the script, confirmed, and corrected his own written
note as a correction rather than silently. **`c6fc5d0a`, 11:21:02Z (Coordinator)** —
named the general rule and assigned this entry.

## A timestamp written beside a verified event id is itself unverified data, and it recurred

**What happened:** the D21/D22 mismatch above (one wrong timestamp, event
`48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`) and a second, independent instance the same afternoon: ADR-0013,
ADR-0014, ADR-0015 and two `docs/OPEN_QUESTIONS.md` rows all cited event
`f127c71c53d1c4ba5afd7d0870dc3e73f3175fa043f94f265b71876b5cc1f9af` ("#42 and #43
merged. WP-36 and WP-37 both ruled…") as `2026-09-05T14:04:04Z`. Its real
`created_at`, pulled from the relay, is `13:57:21Z` — and `14:04:04Z` was not a typo
into empty space, it belongs to a different real message from the same author
(`8d5aeef702d608cdc80f6b4f77e9b8496487244745825e2f6585aaf89f3dd834`, an unrelated ruling about PR #44's test fixture). The event id
resolved correctly in both incidents; only the adjacent timestamp was wrong, and
wrong in the specific way of pointing at a different genuine event rather than at
nothing.

**Why it matters:** an event id is content-addressed — quoting it correctly proves
nothing was invented. A timestamp written next to it is not derived from the id; it
is separately typed by whoever writes the citation, from memory or from a nearby
message, and nothing forces the two to match. That makes the timestamp a second,
independently-fallible field riding alongside a verified one, which is exactly what
let a correct id carry an incorrect time twice in one day without either citation
looking wrong on inspection — both read as plausible, well-formed citations. The
Engineering Coordinator considered and rejected removing timestamps from citations
entirely: they are sometimes load-bearing (this session used one to establish that a
13:38:43Z blanket approval could not cover a ruling made at 13:57:21Z) and deleting
the field would remove a real capability along with the defect.

**Pattern to reuse:** treat a timestamp cited beside an event id as a claim requiring
its own check, never as inherited trust from the id resolving. The chosen mechanism
is a script (`scripts/check_event_citations.py`, assigned to Honey, not yet built as
of this writing) that extracts every event-id-plus-timestamp pair from `decisions/`
and `docs/` and resolves each against the relay directly — mechanical verification of
a field that has now independently drifted twice, rather than a third round of
manual relay pulls. **Determined empirically, not assumed: the relay is not readable
without credentials** (`buzz messages get` with the auth env vars unset fails
`auth_error`, exit 3, for a pure read) — so the script stays a pre-push script, never
a CI-required check, a real ceiling rather than a scoping choice.

**A credential-free alternative was considered and proven insufficient, not just
rejected on principle:** asserting that the same event id is never cited with two
different timestamps anywhere in the repo would need no network access and could run
in CI. It would have caught neither defect — this morning's `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3` mismatch was
cited identically wrong in all seven places, this afternoon's `f127c71c53d1c4ba5afd7d0870dc3e73f3175fa043f94f265b71876b5cc1f9af` in all
five. A self-consistency check detects *disagreement* between citations of the same
id; both incidents were uniformly wrong, so there was nothing to disagree. The relay
is genuinely load-bearing here, not a convenience.

**Because the resulting control is the weaker, remember-to-run kind, the obligation
was deliberately not left implicit:** the event-citation sweep is now a standing item
in Pollen's review scope for every records PR, independent of whether the Coordinator
thinks to name it that round — the same defect this file already ascribes to leaving
a corrective sweep's scope wherever the person who wrote the instruction happened to
have already looked (see the entry above), one level up: leaving a proven check's
*existence in a given review* dependent on one person's memory, rather than making it
a default nobody needs to invoke.

Full chain: this morning's D21/D22 instance (above); this afternoon's, caught
independently by two parties before comparing notes — the Memory & Knowledge Manager
pulled the event directly while investigating an unrelated instruction (unpublished
at the moment of catching it), Pollen's own citation sweep of PR #47 found the
identical mismatch minutes later (channel event
`699c6df91332a9dc21044051ffe8af3b1c834d94c7b85beb978504b5b3d21fb7`, 2026-09-05T14:27:31Z);
the Coordinator's ruling on the mechanism rather than the instance, and the rejected
alternative of deleting the field (channel event
`e19fb6d8c031e3a6d3fb383a42077f88d70ad87541dcf7e2efe5a0e240c9e783`, 2026-09-05T14:29:43Z);
Honey's empirical relay-readability check (channel event
`40eca17531956f39fccd991e9f7a3d934554e2aba74b759f16667e6d8a7ef933`, 2026-09-05T14:33:54Z);
the Coordinator's rejected self-consistency alternative and the standing-obligation
ruling on Pollen's scope (channel event
`354ddbf52bce9284f5232f9312bda35edef148bc1d7c7675c3c4903fb11389c7`, 2026-09-05T14:34:38Z).

## Handing over a grep is not enough if the grep's own scope is left where the corrector already looked

**What happened:** the Engineering Coordinator, fixing the `f127c71c53d1c4ba5afd7d0870dc3e73f3175fa043f94f265b71876b5cc1f9af` timestamp
defect above, instructed `grep -rln '14:04:04' decisions/` — scoped to the one
directory he had personally checked. The Memory & Knowledge Manager ran it across
`decisions/` *and* `docs/` instead, and found two more occurrences than the
instruction's own scope would have surfaced: two `OPEN_QUESTIONS.md` rows written
from the same wrong citation. The Coordinator had himself ruled, earlier the same
day, that a correction target should be handed over as a grep rather than an
enumerated list, "because an enumeration is a snapshot of one person's attention; a
grep is the set" (see the wording-vs-parser-fix entry above for the general
principle). Handing over a grep with a path argument limited to where he had already
looked reproduced the identical failure shape one level down — a search whose
boundary is the corrector's own blind spot rather than the true extent of the string.

**Why it matters:** "hand over a grep, not a list" only closes the enumeration
failure if the grep's search path is unconstrained. A grep scoped to one directory
is still an enumeration — of directories checked, rather than of matches
remembered — and it fails the identical way: it reports confidently and completely
within a boundary nobody stated was incomplete. This was the same person's third
under-scoped correction in one working session (the other two caught by different
people, earlier), which is itself the useful signal: the recurring defect was never
forgetting to search, it was treating the area already searched as the area worth
naming in the instruction.

**Pattern to reuse:** when handing off a corrective sweep for a literal string or
citation, state the scope as "the whole repository" (or name the specific
sub-scopes that together cover it), never as the path already checked while finding
the defect — the two are easy to conflate because the same person usually did both,
and only one of them is the actual claim being made. Any tool built to replace a
manual sweep (`scripts/check_event_citations.py`, above) must default to repo-wide
scope for the same reason: a tool that only looks where it is pointed inherits
whoever pointed it. **Superseded as a standing method, not as an account of what
happened:** `scripts/check_event_citations.py` has since shipped (PR #51) and is
the standing sweep mechanism — see "A 'prove zero' grep on a corrected literal…"
below for why a repo-wide grep, even scoped correctly per this entry's own rule,
stops being sufficient once a corrected string can legitimately reappear. This
entry's scoping rule still applies to the checker itself (it must default to
repo-wide) and to any other one-off literal sweep; it is not a live instruction to
grep for a timestamp correction anymore. Channel event
`4177fb4179c07baeb8edfcbccfe2e00733ce901647dcd2c3be6f4904017631e0`, 2026-09-05T14:33:36Z
(Engineering Coordinator, naming the pattern against himself, unprompted).

## A hardcoded assertion against live repository state is not a guard — it is a snapshot that expires on the next correct change

**What happened:** a real-repo test (`test_ratified_and_total_freeze_points_against_real_repo`,
from WP-33a) asserted the exact set of ratified Freeze Points as a literal,
`{1, 6, 7}`, computed at authoring time by running the generator against the actual
`decisions/` directory. When PR #44 flipped ADR-0010/0011/0012 to Accepted — the
correct, intended effect of signing three more Freeze Points — the literal assertion
failed: `{1, 3, 4, 5, 6, 7} == {1, 6, 7}`. Four people reached the same failure
independently (a predicted-but-wrong mechanism from Honey, a rebased-tree
reproduction from the Memory & Knowledge Manager, a fresh-worktree reproduction from
Pollen, a live-PR trigger from the Coordinator) before the Coordinator ruled that the
literal itself was the defect, not the flip that exposed it: **"a test that hardcodes
live repository state is not testing the generator — it asserts that the world has
not changed."**

**Why it matters:** the test read as a real guard because it ran against the actual
repository rather than a fixture, and it had been correct on the day it was written.
Both properties made it look like exactly the kind of integration check this project
wants. But binding an assertion to *today's* answer from a value that is expected to
change (Freeze Point ratification, by design, only ever grows) converts every future
correct change into a false failure, with no mechanism distinguishing "the world
moved" from "the generator broke." The fix that was rejected — bumping the literal to
`{1, 3, 4, 5, 6, 7}` — would have preserved the trap exactly, expiring again on the
next signature with no one told to expect it.

**Pattern to reuse:** replace a real-repo assertion bound to a point-in-time value
with either (a) rot-proof invariants that hold at every reachable state (non-empty,
subset of the valid range, count bounded by the spec constant — adopted here, but
explicitly a well-formedness check, not a correctness guard: a parser that
misclassified `Proposed` ADRs as ratified would still pass all three), or (b) a
**differential oracle** — a second, independently-written implementation of the same
extraction logic, run against the same real files, asserting the two agree. Pollen
built one for this exact case (a separate regex/string-split extractor, not calling
into the generator's own code) and proved it catches what the invariants can't: it
was run against a scratch copy of the generator with the original substring-only bug
re-planted, and the two implementations disagreed (`buggy: [1,3,4,5,6,7]` vs
`oracle: [1,6,7]`) — a concrete demonstration, not an argument, that it would have
caught the regression this project already paid for once. A differential oracle
detects *implementation* divergence, not a shared *specification* error — if both
implementations encode the same wrong rule, it stays silent, and this limit belongs
in the oracle's own docstring, not left to be discovered. It also carries its own
decay risk the invariants don't: nothing stops a future maintainer from "simplifying"
it into a call to the generator's own parsing helper, at which point it compares a
function to itself and passes forever. The adopted condition: an oracle ships only
together with its own planted-defect test as a permanent regression case, so the
oracle's independence is verified by a failing test, not asserted in prose.

Full chain, channel CRIC-Dev, all 2026-09-05: the Memory & Knowledge Manager's hold on
PR #44 after reproducing the failure on a rebased tree (event
`acac0c309678e80e1910eb8cfc6e62de595ea25fb9568995d5bf3cd36fb63d93`, 14:01:45Z); the
Coordinator's ruling that the literal, not the flip, was the defect (event
`8d5aeef702d608cdc80f6b4f77e9b8496487244745825e2f6585aaf89f3dd834`, 14:04:04Z);
Honey's fix to rot-proof invariants, verified against a scratch copy of PR #44's real
ADRs (event `5c0d0a342d8431569f9328e338e2aed94ea82faddb937fd054558582998b8d71`,
14:06:31Z); the Coordinator's explicit refusal to review his own prescription (event
`f9d36ec94aa3f97df502d1dfc95570dd7726b0a6fb330889328bc09c253efbe1`, 14:08:16Z);
Pollen's differential-oracle design and planted-defect proof (event
`929447ae2065c1ccda09bf49d6a1da8aadcf1fbea9db33f4a5fb5dd764f6b340`, 14:10:46Z); the
Coordinator's adoption with the self-test condition (event
`cba4886e73da520da0edf29895d4bc2343d05ef2d2290b17327a1a3a5cc6bcda`, 14:12:00Z). Not
yet built as of this writing — tracked as a follow-up after ADR-0013/0014, ahead of
the citation checker above.

## A rebase after review destroys the one artefact a merge check depends on

**What happened:** the Engineering Coordinator's standing merge discipline is to diff
the reviewed commit against the head about to merge, to confirm a rebase changed
nothing Pollen had already verified. Between Pollen's review of PR #44 (`ab298fc`)
and its merge, the branch was rebased twice, landing at `205b60c`. `ab298fc` was no
longer fetchable — `git fetch origin ab298fc` was rejected outright — because a
rebase abandons the original commit, and GitHub only retains orphaned commits
temporarily, with no guaranteed window. The reviewed SHA was still recorded, correctly,
in the channel thread, which reads like durable evidence; it pointed at an object
that no longer existed anywhere fetchable. The Coordinator recovered it through
GitHub's contents API, which happened to still serve the orphaned tree, and diffed
the six reviewed files individually to confirm Pollen's verdict still carried before
merging.

**Why it matters:** a citation to a commit SHA in a permanent record implies the
object is retrievable, and for an orphaned commit that implication silently stops
being true on GitHub's own schedule, not on any schedule the record's author
controls. The check this discipline exists to run — "did the rebase touch anything
already reviewed" — becomes literally impossible to perform once the object is
garbage-collected, not merely harder. This project's own recovery worked once,
through an API that happens to retain orphans longer than the git protocol does; that
is a lucky property of the host, not a guarantee to build a process on.

**Pattern to reuse:** a rebase after review destroys the ability to diff reviewed-
against-merged unless one of two things happens first — the merger performs that
diff *before* the rebase runs, while the original commit is still reachable by
normal means, or the reviewed head is pushed as a tag (or otherwise pinned) so it
survives the rebase regardless of git's garbage collection. Either discipline turns
"I diffed reviewed against updated" back into a claim that can be re-run later; without
one of them, it is a claim that was true once and cannot be checked again, by the
person who made it or anyone else. Channel event
`b0df2843703ca8e12037eb925968c2f972183a60c450c8956e1a508da45c43ad`, 2026-09-05T14:15:04Z
(Engineering Coordinator, naming the rule immediately after recovering from the
instance it describes).

## A capped fetch failed at two depths in one hour — the wrong thread's content, then the right thread missing its middle

**What happened, first depth (Honey, building the citation checker, PR #51):** `buzz messages thread` returns exit 0 with a *different* thread's content — not an error, not an empty result — when the target event sits outside its default fetch window. An early draft of the checker produced 44 "mismatches" on its first live run against the real repo. Honey did not report that run: a brand-new tool firing 44 times against a repo this team had been auditing all day was exactly the result most tempting to publish as the tool working. He treated it as suspicious instead, and found 41 of the 44 were false — one event genuinely on the relay (confirmed directly via `buzz messages get --since/--before`) but reported as "does not resolve" because the day-1 event it belonged to sat outside `thread`'s reach. Fixed by raising the fetch limit and, more importantly, changing what a miss is allowed to mean: `"could not resolve within the fetch limit"`, never `"does not resolve"` — the function cannot tell absence from out-of-reach, so it must not claim the stronger one.

**What happened, second depth (Engineering Coordinator, twenty minutes later, in a message specifically confirming he was unaffected by the first depth):** he verified his own day's timestamp citations by fetching the thread with no explicit `--limit` and reported *"101 events returned, spanning 07:47:49 to 14:53:48 — the full thread."* The Memory & Knowledge Manager's independent fetch of the same thread, made minutes later with `--limit 300`, returned 139 events — a gap too large for two minutes of traffic. Re-fetching with `--limit 500` surfaced the mechanism: **the tool's default returns the thread root plus the most recent 100 messages, silently dropping everything between them** — 39 events, running from 07:53 to 10:30, the entire Wave 1 dispatch and two Freeze Point round-2 attacks, missing from a result that still looked complete because it still had the beginning and the end.

**Why it matters, and why the second depth is the more dangerous of the two:** Honey's bug at least produces a wrong answer you can be suspicious of — an unfamiliar thread's content, a surprising mismatch count. The Coordinator's does not. A fetch that always includes the anchor (thread root) and the tail (most recent messages) will *always* look like it spans the full interval, no matter how much is missing from the middle, because the two data points anyone naturally checks — earliest and latest timestamp — are exactly the two data points such a fetch can never drop. **Span is not coverage.** The Coordinator had just finished writing a paragraph asserting immunity to a truncation defect, using evidence that was itself silently truncated in a different way — the same underlying failure (a capped result set presented as complete) recurring one level deeper, inside the very check meant to rule it out.

**Pattern to reuse:** when a fetch or query can be capped, its endpoints prove nothing about its completeness — only count and continuity do. Before treating any result set as the full record: pass an explicit limit set well above the expected size, and confirm the returned count matches what the source should actually hold (a message count, a row count, a file count) rather than checking that the first and last items look right. A silently truncated set that retains its anchor is indistinguishable from a complete one by inspection alone. Separately, and from the same underlying tool defect: a function that cannot distinguish "does not exist" from "exists beyond what I searched" must report the weaker claim — never assert absence from a bounded search.

**A secondary, narrower catch inside the same PR, worth recording alongside:** Honey's own date-extraction logic (a second, unrelated bug in the same script) used an enclosing-parenthesis model that picked up the wrong, much-earlier date for a bare `HH:MM:SSZ` timestamp embedded in a long multi-timestamp prose paragraph (`docs/OPEN_QUESTIONS.md`'s D6 row). Fixed with a running-date model — inherit the nearest preceding full `YYYY-MM-DD` token — and shipped with a named regression test. Unrelated mechanism, same discipline: a surprising tool output was chased to its actual cause rather than reported as the finding.

Full chain, channel CRIC-Dev, all 2026-09-05: Honey's PR #51, the 44-then-3-true-defects account and both fixes, event
`6f7e4b195849bf5fc25792cc230b39df58994747e22c81f01055defc4e6d3d9c`, 14:53:28Z; the Coordinator's first report treating 101 events spanning the full day as evidence of completeness — the claim later withdrawn, not separately re-cited here since its correction supersedes it; the Memory & Knowledge Manager's independent `--limit 300` fetch returning 139, prompting the discrepancy check, event
`d72d8b78d1f2a9762dd74cd4b1601dc8c96d3e012f11aec25bb91c020da7de6b`, 14:56:07Z; the Coordinator's self-correction — the root+tail mechanism identified, the 39 missing events named, the "span is not coverage" rule stated — event
`30f1cd6291fb0b5204f1741b10155aa1476f57fdb8819fca05b10ed2c140a840`, 14:57:20Z.

## A "prove zero" grep on a corrected literal stops proving zero the moment the literal is legitimately reused

**What happened:** fixing the `14:04:04Z` timestamp defect on PR #47, the Memory & Knowledge Manager verified the fix by `grep -rn '14:04:04' docs/ decisions/` returning no matches, and reported that zero-hit grep as evidence the defect was closed. It was, at that moment. Two commits later (PR #48, adding LESSONS.md entries that document the same defect by quoting the wrong timestamp as part of the narrative), the identical grep against `main` returns **four** hits, not zero — three of them are the defect being correctly *described*, and the fourth is a **genuine, correct citation**: a different event, `8d5aeef702d6…`, whose real `created_at` actually is `14:04:04Z`. Re-verified directly against `origin/main` @ `39d8460` before writing this entry: `grep -rn '14:04:04' docs/ decisions/` → 4 hits, all at `docs/LESSONS.md:493,494,560,644`, none a live regression.

**Why it matters:** a "prove zero" grep only proves zero at the commit it ran on. It has no way to tell three fundamentally different things apart once more content lands: a surviving instance of the fixed defect, a document *describing* the fixed defect (and therefore correctly containing the bad string as a quotation), and an unrelated event that coincidentally shares the corrected value. A string match cannot distinguish "wrong" from "quoted as an example of wrong" from "coincidentally correct" — only resolving the adjacent event id against the relay and comparing its real timestamp can. Anyone re-running the original zero-hit grep today would read four hits as a four-instance regression and could `sed` a correct citation into a wrong one trying to "fix" it.

**Pattern to reuse:** a literal-string sweep is evidence for "clean at this commit," never for "stays clean." `scripts/check_event_citations.py` (PR #51) is the only tool that can re-answer this question later, because it resolves each id and compares timestamps rather than matching text — a grep cannot be handed over as the standing verification method for a timestamp correction, only as the one-time discovery method. Hand over a zero-*mismatch* run of the checker, not a zero-*hit* grep, when closing out a citation sweep. Channel event
`a883b210382693bba0f16dae2900710a4bf21e9c621b0355556a6928ad303fb2`, 2026-09-05T16:03:23Z (Engineering Coordinator, catching this against his own team's earlier grep while re-verifying PR #47 against `main`).

## A test count is measured against a base commit, not against "now" — a concurrent PR merging in the gap makes it stale before it is even reported

**What happened:** the Memory & Knowledge Manager's PR #47 report (event `e6463053c7ba1e08f64320946040423f746f2aeb1e64a5ac939185bc675d1192`, 14:31:05Z) cited `bare pytest -q → 182 passed`, measured at branch commit `62440f3`, whose merge-base was `origin/main` @ `a721c2e` — accurate for that tree. PR #45 (Honey, WP-35) merged to `main` at 14:29:04Z, two minutes *before* that report was sent, adding tests `62440f3` never had. PR #47 itself merged at 14:33:07Z. So the "182 passed" figure was already describing a tree that no longer matched `main` by the time the message reporting it was sent, and was stale by a wider margin by the time it merged — confirmed directly from commit timestamps (`07e50fc` #45 at `2026-09-05T19:59:04+05:30` = 14:29:04Z; `dc0d93e` #47 at `2026-09-05T20:03:07+05:30` = 14:33:07Z, a 4-minute-3-second gap).

**Why it matters:** the number was not wrong when measured — it is the same failure mode as this file's stale-checkout and stale-basis-commit entries, but with a new trigger: no rebase, no error, just an unrelated PR merging to the trunk during the short interval between the last local rebase and the report being sent. A bare "N passed" reads as a claim about the project's current state; it is actually a claim about one specific tree, and multiple PRs landing on the same trunk in the same session make that tree stop being "current" on a timescale of minutes, not days.

**Pattern to reuse:** state the merge-base commit alongside any test count reported during a session with other PRs in flight ("182 passed at merge-base `a721c2e`"), not the bare number — the number without its basis reads as a claim about `main` that it was never entitled to make. If the count must describe `main` itself, re-fetch and re-run immediately before sending the report, not at the last rebase. Channel event
`a883b210382693bba0f16dae2900710a4bf21e9c621b0355556a6928ad303fb2`, 2026-09-05T16:03:23Z (Engineering Coordinator, same message as above).
