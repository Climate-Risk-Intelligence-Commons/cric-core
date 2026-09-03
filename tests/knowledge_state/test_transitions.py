"""Tests for the eight-edge transition envelope (Freeze Point 6).

Source of truth: decisions/0007-freeze-points-6-7-knowledge-state-review-decision.md
"""

import pytest

from cric_core.knowledge_state import (
    InvalidTransition,
    KnowledgeStateStatus,
    UNIVERSAL_TRANSITIONS,
    narrow_transitions,
    validate_transition,
)

_S = KnowledgeStateStatus
ALL_STATUSES = list(KnowledgeStateStatus)

# Independent restatement of the eight ratified edges -- NOT imported from
# the module under test, so a bug that adds a ninth edge to
# UNIVERSAL_TRANSITIONS is caught rather than silently agreeing with itself.
RATIFIED_EDGES = {
    (_S.CANDIDATE, _S.ACCEPTED),
    (_S.CANDIDATE, _S.REJECTED),
    (_S.CANDIDATE, _S.DISPUTED),
    (_S.ACCEPTED, _S.DISPUTED),
    (_S.ACCEPTED, _S.WITHDRAWN),
    (_S.DISPUTED, _S.ACCEPTED),
    (_S.DISPUTED, _S.SUPERSEDED),
    (_S.SUPERSEDED, _S.ARCHIVED),
}


def test_universal_transitions_matches_the_independently_stated_ratified_set():
    assert UNIVERSAL_TRANSITIONS == frozenset(RATIFIED_EDGES)


def test_universal_transitions_has_exactly_eight_edges():
    assert len(UNIVERSAL_TRANSITIONS) == 8


@pytest.mark.parametrize(
    "from_status,to_status",
    [(f, t) for f in ALL_STATUSES for t in ALL_STATUSES],
)
def test_transition_envelope_is_exhaustive_over_the_full_pair_space(from_status, to_status):
    # Assert reach, not count: every one of the 7x7=49 possible pairs is
    # checked individually against the independently-stated RATIFIED_EDGES,
    # so a spurious ninth edge fails this test even though it would still
    # pass a count-only assertion ("== 8 edges validate").
    should_be_legal = (from_status, to_status) in RATIFIED_EDGES

    if should_be_legal:
        validate_transition(from_status, to_status)  # must not raise
    else:
        with pytest.raises(InvalidTransition):
            validate_transition(from_status, to_status)


def test_superseded_to_candidate_fails_validation():
    # Required explicitly by ADR-0007.
    with pytest.raises(InvalidTransition):
        validate_transition(_S.SUPERSEDED, _S.CANDIDATE)


def test_withdrawn_to_accepted_fails_validation():
    # Required explicitly by ADR-0007.
    with pytest.raises(InvalidTransition):
        validate_transition(_S.WITHDRAWN, _S.ACCEPTED)


def test_self_transitions_are_not_legal_edges():
    # None of the eight ratified edges are a status to itself.
    for status in ALL_STATUSES:
        with pytest.raises(InvalidTransition):
            validate_transition(status, status)


# --- Per-type narrowing (Decision 3) ------------------------------------------


def test_narrow_transitions_accepts_a_subset_of_the_universal_envelope():
    narrowed = narrow_transitions({(_S.CANDIDATE, _S.ACCEPTED)})

    validate_transition(_S.CANDIDATE, _S.ACCEPTED, envelope=narrowed)  # must not raise
    with pytest.raises(InvalidTransition):
        validate_transition(_S.CANDIDATE, _S.REJECTED, envelope=narrowed)


def test_narrow_transitions_accepts_the_full_universal_envelope_unchanged():
    narrowed = narrow_transitions(UNIVERSAL_TRANSITIONS)

    assert narrowed == UNIVERSAL_TRANSITIONS


def test_narrow_transitions_rejects_an_edge_outside_the_universal_envelope():
    # Narrowing may only remove edges, never add one beyond the eight.
    with pytest.raises(InvalidTransition):
        narrow_transitions({(_S.SUPERSEDED, _S.CANDIDATE)})


def test_narrow_transitions_rejects_a_mix_of_legal_and_illegal_edges():
    with pytest.raises(InvalidTransition):
        narrow_transitions({(_S.CANDIDATE, _S.ACCEPTED), (_S.WITHDRAWN, _S.ACCEPTED)})


def test_narrow_transitions_of_empty_set_is_a_legal_envelope_with_nothing_reachable():
    narrowed = narrow_transitions(set())

    assert narrowed == frozenset()
    with pytest.raises(InvalidTransition):
        validate_transition(_S.CANDIDATE, _S.ACCEPTED, envelope=narrowed)
