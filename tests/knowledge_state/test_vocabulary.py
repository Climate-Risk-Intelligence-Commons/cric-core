"""Tests for the three closed vocabularies (Freeze Points 6 + 7).

Source of truth: decisions/0007-freeze-points-6-7-knowledge-state-review-decision.md
"""

import pytest

from cric_core.knowledge_state import (
    InvalidKnowledgeStateStatus,
    InvalidOrigin,
    InvalidVerificationMethod,
    KnowledgeStateStatus,
    Origin,
    VerificationMethod,
)

# --- KnowledgeStateStatus: seven values -------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "candidate",
        "accepted",
        "disputed",
        "superseded",
        "rejected",
        "withdrawn",
        "archived",
    ],
)
def test_parses_each_of_the_seven_ratified_status_values(value):
    # Decision 1: exhaustive coverage of the seven, not a sample.
    result = KnowledgeStateStatus.parse(value)

    assert result.value == value


def test_unrecognised_status_value_is_rejected():
    with pytest.raises(InvalidKnowledgeStateStatus):
        KnowledgeStateStatus.parse("in_review")


def test_status_value_is_not_case_folded():
    # Decision 1: exact match only, never coerced.
    with pytest.raises(InvalidKnowledgeStateStatus):
        KnowledgeStateStatus.parse("Candidate")


def test_empty_status_string_is_rejected():
    with pytest.raises(InvalidKnowledgeStateStatus):
        KnowledgeStateStatus.parse("")


def test_exactly_seven_status_members_exist():
    # Guards against a silent eighth value ever being added without a
    # migration -- the vocabulary is closed, not "closed for now".
    assert len(KnowledgeStateStatus) == 7


# --- Origin: three values ----------------------------------------------------


@pytest.mark.parametrize("value", ["agent", "deterministic_pipeline", "human"])
def test_parses_each_of_the_three_ratified_origin_values(value):
    result = Origin.parse(value)

    assert result.value == value


def test_unrecognised_origin_value_is_rejected():
    with pytest.raises(InvalidOrigin):
        Origin.parse("system")


def test_origin_value_is_not_case_folded():
    with pytest.raises(InvalidOrigin):
        Origin.parse("Human")


def test_exactly_three_origin_members_exist():
    assert len(Origin) == 3


# --- VerificationMethod: four values ------------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        "deterministic_authoritative_source",
        "corroboration_rules",
        "human_review",
        "maintainer_approved_workflow",
    ],
)
def test_parses_each_of_the_four_ratified_verification_methods(value):
    result = VerificationMethod.parse(value)

    assert result.value == value


def test_unrecognised_verification_method_is_rejected():
    # ADR-0007 requires this negative test explicitly.
    with pytest.raises(InvalidVerificationMethod):
        VerificationMethod.parse("peer_review")


def test_verification_method_value_is_not_case_folded():
    with pytest.raises(InvalidVerificationMethod):
        VerificationMethod.parse("Human_Review")


def test_exactly_four_verification_method_members_exist():
    assert len(VerificationMethod) == 4


# --- Cross-vocabulary independence (open item) --------------------------------


def test_verification_method_and_origin_are_not_cross_validated():
    # Open item (ADR-0007): whether maintainer_approved_workflow counts as
    # human-originated is undetermined. This is not a positive proof of
    # absence -- it documents that the module deliberately exposes no
    # function tying the two vocabularies together, so a reviewer checking
    # for a silently-decided open item knows where to look.
    import cric_core.knowledge_state as ks

    assert not hasattr(ks, "validate_maintainer_approved_workflow_origin")
    assert not hasattr(ks, "validate_verification_method_origin")
