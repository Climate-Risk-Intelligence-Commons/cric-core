"""Tests for the explicitly-excluded predicates (registry §8 Deprecated
Predicates + rejected `caused_by`), and the `affected`/`impacted` consequence
of ADR-0010 (Consequence 1: registry §8 wins over the OKF spec's `affected`).

These are ADR-0010's own negative tests, made real rather than left as
Alternatives-section prose: each excluded spelling must raise, and with a
reason, not silently coerce to the nearest real value.
"""

import pytest

from cric_core.relationships import (
    DEPRECATED_PREDICATES,
    REJECTED_PREDICATES,
    InvalidRelationshipPredicate,
    RelationshipPredicate,
)


@pytest.mark.parametrize("value", ["connected_to", "associated_with"])
def test_deprecated_predicates_are_rejected(value):
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse(value)


def test_deprecated_predicates_get_a_specific_reason_not_generic_rejection():
    with pytest.raises(InvalidRelationshipPredicate, match="deprecated"):
        RelationshipPredicate.parse("connected_to")


def test_caused_by_is_rejected():
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse("caused_by")


def test_caused_by_gets_the_triggered_by_redundancy_reason():
    with pytest.raises(InvalidRelationshipPredicate, match="triggered_by"):
        RelationshipPredicate.parse("caused_by")


def test_exactly_two_deprecated_predicates_are_recorded():
    assert DEPRECATED_PREDICATES == frozenset({"connected_to", "associated_with"})


def test_exactly_one_rejected_predicate_is_recorded():
    assert REJECTED_PREDICATES == frozenset({"caused_by"})


def test_none_of_the_excluded_predicates_are_in_the_enum():
    # A closed-set guard from the other direction: excluded strings must
    # never resolve to a real enum member by accident (e.g. via a stray
    # alias or a case-insensitive fallback introduced later).
    enum_values = {member.value for member in RelationshipPredicate}
    excluded = DEPRECATED_PREDICATES | REJECTED_PREDICATES | {"affected"}

    assert not (enum_values & excluded)


# --- affected -> impacted (ADR-0010 Consequence 1) ---------------------------


def test_affected_is_rejected():
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse("affected")


def test_affected_rejection_points_to_impacted():
    with pytest.raises(InvalidRelationshipPredicate, match="impacted"):
        RelationshipPredicate.parse("affected")


def test_impacted_is_the_canonical_spelling():
    assert RelationshipPredicate.parse("impacted") == RelationshipPredicate.IMPACTED
