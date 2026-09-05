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
numbered steps in-channel, by the person on this team most careful about records.
The Coordinator's own first explanation for *that* mistake — "it compressed in the
direction that flatters whoever wrote the last message" — was itself a motive story
with no mechanism, the exact kind of placeholder this entry is about, reached for
one message after ruling the pattern out. The real mechanism, found by Pollen: each
event in the chain contained two things — the real content and a wrong first guess —
and the summary gave each event only one label, displacing the second content onto
the next event. A one-slot lag, not a bias toward anyone.

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
