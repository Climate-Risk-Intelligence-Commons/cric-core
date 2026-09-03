"""Tests for ReviewDecision-specific rules (Freeze Point 7, ADR-0007 Decision 8)
and the open items this module must NOT silently close.
"""

import pytest

from cric_core.knowledge_state import (
    InvalidOrigin,
    KnowledgeStateStatus,
    Origin,
    REVIEW_DECISION_ALLOWED_ORIGINS,
    REVIEW_DECISION_ENTRY_STATUS,
    UNIVERSAL_TRANSITIONS,
    validate_review_decision_origin,
    validate_transition,
)

_S = KnowledgeStateStatus

# --- Ratified: entry status and origin ----------------------------------------


def test_review_decision_entry_status_is_accepted_not_candidate():
    assert REVIEW_DECISION_ENTRY_STATUS == _S.ACCEPTED


def test_review_decision_origin_must_be_human():
    validate_review_decision_origin(Origin.HUMAN)  # must not raise


@pytest.mark.parametrize("origin", [Origin.AGENT, Origin.DETERMINISTIC_PIPELINE])
def test_review_decision_origin_rejects_non_human_origins(origin):
    with pytest.raises(InvalidOrigin):
        validate_review_decision_origin(origin)


def test_review_decision_allowed_origins_names_exactly_human():
    assert REVIEW_DECISION_ALLOWED_ORIGINS == frozenset({Origin.HUMAN})


# --- Open item: ReviewDecision's onward transitions are NOT narrowed here ----


def test_review_decision_defines_no_narrowed_transition_envelope():
    # Open item (ADR-0007, Decision 3 / open items list): whether
    # ReviewDecision narrows the envelope for disputed/superseded/
    # rejected/withdrawn is undetermined. This module must not decide it
    # -- confirmed by the absence of any ReviewDecision-specific envelope
    # constant or function.
    import cric_core.knowledge_state as ks

    assert not hasattr(ks, "REVIEW_DECISION_TRANSITIONS")
    assert not hasattr(ks, "validate_review_decision_transition")


def test_transitions_from_review_decisions_accepted_entry_use_the_universal_envelope():
    # Because no narrower envelope exists for ReviewDecision anywhere in
    # this module, every edge the universal envelope permits out of
    # ACCEPTED must validate for a ReviewDecision exactly as it would for
    # any other node type -- there is no separate code path to diverge.
    from_accepted = {to for (frm, to) in UNIVERSAL_TRANSITIONS if frm == _S.ACCEPTED}

    assert from_accepted == {_S.DISPUTED, _S.WITHDRAWN}
    for to_status in from_accepted:
        validate_transition(REVIEW_DECISION_ENTRY_STATUS, to_status)  # must not raise
