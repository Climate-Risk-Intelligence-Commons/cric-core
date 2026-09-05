"""Tests for the two closed review vocabularies (registry §10, build-order item 9).

Source of truth: docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md §10
"""

import pytest

from cric_core.review import (
    InvalidReviewDecisionValue,
    InvalidReviewQueueState,
    ReviewDecisionValue,
    ReviewQueueState,
)

# --- ReviewQueueState: nine values -------------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "inbox",
        "assigned",
        "in-review",
        "approved",
        "rejected",
        "needs-more-evidence",
        "disputed",
        "escalated",
        "archived",
    ],
)
def test_parses_each_of_the_nine_ratified_queue_states(value):
    # Exhaustive coverage of the nine, not a sample.
    result = ReviewQueueState.parse(value)

    assert result.value == value


def test_unrecognised_queue_state_is_rejected():
    with pytest.raises(InvalidReviewQueueState):
        ReviewQueueState.parse("pending")


def test_queue_state_value_is_not_case_folded():
    with pytest.raises(InvalidReviewQueueState):
        ReviewQueueState.parse("In-Review")


def test_empty_queue_state_string_is_rejected():
    with pytest.raises(InvalidReviewQueueState):
        ReviewQueueState.parse("")


def test_exactly_nine_queue_state_members_exist():
    # Guards against a silent tenth value ever being added without ratifying
    # it first -- the vocabulary is closed, not "closed for now".
    assert len(ReviewQueueState) == 9


# --- ReviewDecisionValue: six values ------------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "approve",
        "reject",
        "modify",
        "needs_more_evidence",
        "disputed",
        "escalate",
    ],
)
def test_parses_each_of_the_six_ratified_decision_values(value):
    result = ReviewDecisionValue.parse(value)

    assert result.value == value


def test_unrecognised_decision_value_is_rejected():
    with pytest.raises(InvalidReviewDecisionValue):
        ReviewDecisionValue.parse("defer")


def test_decision_value_is_not_case_folded():
    with pytest.raises(InvalidReviewDecisionValue):
        ReviewDecisionValue.parse("Approve")


def test_empty_decision_value_string_is_rejected():
    with pytest.raises(InvalidReviewDecisionValue):
        ReviewDecisionValue.parse("")


def test_exactly_six_decision_value_members_exist():
    assert len(ReviewDecisionValue) == 6


# --- The hyphen/underscore trap: registry §10 states the split is deliberate -


def test_queue_state_rejects_the_decision_vocabularys_underscore_spelling():
    # "needs_more_evidence" (underscore) is a ReviewDecisionValue, not a
    # ReviewQueueState. Registry §10: "The queue folder name and decision
    # value are deliberately different grammatical forms." Coercing across
    # the boundary would silently merge two closed sets into one.
    with pytest.raises(InvalidReviewQueueState):
        ReviewQueueState.parse("needs_more_evidence")


def test_decision_value_rejects_the_queue_vocabularys_hyphen_spelling():
    # The reverse direction of the same trap.
    with pytest.raises(InvalidReviewDecisionValue):
        ReviewDecisionValue.parse("needs-more-evidence")


def test_disputed_is_a_valid_member_of_both_vocabularies_independently():
    # "disputed" is unchanged in both lists (registry §10) -- confirm both
    # parse it, as two independent closed sets, not because one implies the
    # other.
    assert ReviewQueueState.parse("disputed").value == "disputed"
    assert ReviewDecisionValue.parse("disputed").value == "disputed"


# --- Prohibited: no decision -> knowledge_state mapping exists ---------------


def test_no_mapping_from_decision_value_to_knowledge_state_exists():
    # WP-32's prohibited_changes, made a checkable assertion rather than a
    # promise left in a commit message: approve -> accepted, reject ->
    # rejected and the rest are NOT ratified anywhere -- not in ADR-0007,
    # not in registry §10. This module must not invent that Freeze Point
    # content, so no such function may exist on the module.
    from cric_core import review

    disallowed_names = {
        "decision_to_knowledge_state",
        "apply_decision",
        "resulting_knowledge_state",
        "decision_to_status",
        "APPROVE_MAPS_TO",
        "DECISION_TO_STATUS",
    }
    assert not (disallowed_names & set(dir(review)))
