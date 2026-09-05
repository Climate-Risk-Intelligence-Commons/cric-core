"""Tests for the 11 core + 1 structural relationship predicates (registry §8,
Freeze Point 5 / decisions/0010).

The 23 spatial/domain predicates are covered separately in
test_spatial_domain_predicates.py -- registry §8 groups them as a distinct
list, and this split keeps each test file's positive-case parametrize list
matched one-to-one against the registry section it verifies.
"""

import pytest

from cric_core.relationships import (
    CORE_PREDICATES,
    STRUCTURAL_PREDICATES,
    InvalidRelationshipPredicate,
    RelationshipPredicate,
)

# --- Core scientific/evidential: 11 values -----------------------------------

# Registry §8's own "Core scientific/evidential predicates include" list.
# Independently stated here (not derived from CORE_PREDICATES) so it can
# serve as this file's completeness guard -- see the reach-vs-count finding
# below for why that independence matters.
_CORE_VALUES = [
    "supports",
    "supported_by",
    "contradicts",
    "refines",
    "supersedes",
    "superseded_by",
    "corroborates",
    "disputes",
    "derived_from",
    "consistent_with",
    "inconsistent_with",
]

# Registry §8's "Structural predicates may include" list -- one value today,
# same independent-list treatment as core and spatial/domain.
_STRUCTURAL_VALUES = ["has_snapshot"]


@pytest.mark.parametrize("value", _CORE_VALUES)
def test_parses_each_of_the_eleven_core_predicates(value):
    # Exhaustive coverage of the 11, not a sample.
    result = RelationshipPredicate.parse(value)

    assert result.value == value


def test_exactly_eleven_core_predicates_are_grouped():
    assert len(CORE_PREDICATES) == 11


def test_core_predicates_are_exactly_the_parametrized_values():
    # Completeness guard, same pattern as test_spatial_domain_predicates.py:
    # derive the expected set from this file's own independently-stated
    # list and compare against the module's CORE_PREDICATES, so a
    # misclassification into or out of this group fails loudly instead of
    # passing on a count alone. Proven necessary, not precautionary: a
    # planted swap of CONTRADICTS (core) with HAS_SNAPSHOT (structural)
    # left both len() guards and the disjoint/union check green (Pollen,
    # PR #45 review, 2026-09-05) -- a bare count and a partition check both
    # tolerate two groups trading members, only a named-list comparison
    # catches it.
    assert {RelationshipPredicate(value) for value in _CORE_VALUES} == CORE_PREDICATES


# --- Structural: 1 value ------------------------------------------------------


def test_parses_the_one_structural_predicate():
    assert RelationshipPredicate.parse("has_snapshot").value == "has_snapshot"


def test_exactly_one_structural_predicate_is_grouped():
    assert len(STRUCTURAL_PREDICATES) == 1


def test_structural_predicates_are_exactly_the_parametrized_values():
    # Same completeness guard as core, for the same proven reason.
    assert {RelationshipPredicate(value) for value in _STRUCTURAL_VALUES} == STRUCTURAL_PREDICATES


# --- Closed-set guards ---------------------------------------------------------


def test_exactly_thirty_five_predicates_exist_total():
    # Guards against a silent 36th value ever being added without a
    # migration -- the vocabulary is closed at exactly 35 (ADR-0010).
    assert len(RelationshipPredicate) == 35


def test_unrecognised_predicate_is_rejected():
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse("relates_to")


def test_predicate_value_is_not_case_folded():
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse("Supports")


def test_empty_predicate_string_is_rejected():
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse("")


def test_group_memberships_are_pairwise_disjoint_and_cover_everything():
    # The three groups partition the 35 -- no predicate in two groups, none
    # left out of all three.
    from cric_core.relationships import SPATIAL_DOMAIN_PREDICATES

    assert CORE_PREDICATES & SPATIAL_DOMAIN_PREDICATES == frozenset()
    assert CORE_PREDICATES & STRUCTURAL_PREDICATES == frozenset()
    assert SPATIAL_DOMAIN_PREDICATES & STRUCTURAL_PREDICATES == frozenset()
    assert CORE_PREDICATES | SPATIAL_DOMAIN_PREDICATES | STRUCTURAL_PREDICATES == set(
        RelationshipPredicate
    )
