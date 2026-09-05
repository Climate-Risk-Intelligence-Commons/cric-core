"""Review vocabularies (build-order item 9): registry §10, canonical review states.

Source of truth: `docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md`
§10 "Canonical Review States" (`:260-287`), propagated here rather than
amended -- the registry states both vocabularies without a hedge ("include" /
"may include" appear nowhere in this section), unlike §8's relationship
predicates. That is the reason no new Freeze Point signature was required:
Engineering Coordinator's ruling, channel CRIC-Dev
(`17bd72a0-4d90-4e0b-b102-f9163f0cfd4b`), event
`90016f7651e2805312d1c51586551287edebf4d2f71b70a1dee939ed2d398955`,
2026-09-05T10:00:45Z. ADR-0007 (Freeze Points 6+7) does not enumerate either
list -- grepped for `approve`, `escalate`, `inbox`, `queue`, no hits -- so
this module does not touch a locked Freeze Point.

Object-class scope (registry §3's canonical core types):

- `ReviewQueueState` applies to **`ReviewRequest.status`**
  (`ai/Responsible-Autonomy-and-HITL.md:143`).
- `ReviewDecisionValue` applies to **`ReviewDecision.decision`**
  (`ai/Responsible-Autonomy-and-HITL.md:164-170`) -- registry §10's six
  values match that YAML's `decision:` list exactly, in the same order.

Both vocabularies are closed. `.parse()` on either raises rather than
coercing, and never case-folds -- the same contract as
`knowledge_state.KnowledgeStateStatus.parse`.

**The hyphen/underscore split is deliberate, not an inconsistency to fix.**
Registry §10, verbatim: "The queue folder name and decision value are
deliberately different grammatical forms." `needs-more-evidence` (queue,
hyphenated) and `needs_more_evidence` (decision, underscored) are two
different byte strings in two different closed sets -- normalising either
one would break byte-exact comparison, the same property Freeze Point 1
depends on. Ship them exactly as the registry writes them.

**One token appears unchanged in both vocabularies: `disputed`** (queue and
decision alike) -- and it is also a `KnowledgeStateStatus` value
(`knowledge_state/__init__.py`, Decision 1). Noted because shared tokens
across this project's state machines have been a recurring hazard; this
module makes no claim about whether the three `disputed`s mean the same
thing and defines no function relating them. Observation, not a ruling.

**Explicitly OUT OF SCOPE, per WP-32's `prohibited_changes` -- do not add
this.** No function maps a `ReviewDecisionValue` to a resulting
`KnowledgeStateStatus` (e.g. `approve -> accepted`, `reject -> rejected`).
That mapping is not ratified anywhere -- not in ADR-0007, not in registry
§10 -- and encoding it here would be inventing Freeze Point content this
module has no authority to close. This module also makes no edit to
`knowledge_state/`.
"""

from __future__ import annotations

from enum import StrEnum


class ReviewError(ValueError):
    """Base class for every validation error this module raises."""


class InvalidReviewQueueState(ReviewError):
    """Raised when a string is not one of the nine ratified queue/state
    values (`ReviewRequest.status`)."""


class InvalidReviewDecisionValue(ReviewError):
    """Raised when a string is not one of the six ratified decision values
    (`ReviewDecision.decision`)."""


# Registry §10, "Repository queue/state vocabulary" (:264-274). Applies to
# ReviewRequest.status. Closed; parsing an unrecognised string raises rather
# than coercing to the nearest value.
class ReviewQueueState(StrEnum):
    INBOX = "inbox"
    ASSIGNED = "assigned"
    IN_REVIEW = "in-review"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_MORE_EVIDENCE = "needs-more-evidence"
    DISPUTED = "disputed"
    ESCALATED = "escalated"
    ARCHIVED = "archived"

    @classmethod
    def parse(cls, value: str) -> ReviewQueueState:
        """Parse a raw string into a `ReviewQueueState`.

        Raises `InvalidReviewQueueState` on any value outside the nine.
        Exact match only -- never case-folded, and never coerced across the
        hyphen/underscore boundary from `ReviewDecisionValue`.
        """
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidReviewQueueState(
                f"{value!r} is not one of the nine ratified review queue "
                f"states: {[member.value for member in cls]}"
            ) from exc


# Registry §10, "Canonical ReviewDecision.decision values" (:276-285).
# Applies to ReviewDecision.decision. Closed; parsing an unrecognised string
# raises rather than coercing to the nearest value.
class ReviewDecisionValue(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    NEEDS_MORE_EVIDENCE = "needs_more_evidence"
    DISPUTED = "disputed"
    ESCALATE = "escalate"

    @classmethod
    def parse(cls, value: str) -> ReviewDecisionValue:
        """Parse a raw string into a `ReviewDecisionValue`.

        Raises `InvalidReviewDecisionValue` on any value outside the six.
        Exact match only -- never case-folded, and never coerced across the
        hyphen/underscore boundary from `ReviewQueueState`.
        """
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidReviewDecisionValue(
                f"{value!r} is not one of the six ratified review decision "
                f"values: {[member.value for member in cls]}"
            ) from exc
