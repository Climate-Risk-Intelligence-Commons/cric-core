"""Tests for the 23 spatial/domain relationship predicates (registry §8,
Freeze Point 5 / decisions/0010).

The 11 core + 1 structural predicates are covered separately in
test_core_and_structural_predicates.py -- registry §8 groups them as a
distinct list, and this split keeps each test file's positive-case
parametrize list matched one-to-one against the registry section it
verifies.
"""

import pytest

from cric_core.relationships import (
    SPATIAL_DOMAIN_PREDICATES,
    InvalidRelationshipPredicate,
    RelationshipPredicate,
)

# --- Spatial/domain: 23 values ------------------------------------------------

# Registry §8's own "Spatial/domain predicates may include" list, in the
# order it appears there. Used both as the parametrize source below and as
# the completeness guard's expected set -- if this list and the module's
# SPATIAL_DOMAIN_PREDICATES ever drift apart, the guard test fails instead
# of silently under-covering.
_SPATIAL_DOMAIN_VALUES = [
    "located_in",
    "part_of",
    "contains",
    "depends_on",
    "feeds",
    "fed_by",
    "drains_to",
    "upstream_of",
    "downstream_of",
    "adjacent_to",
    "intersects",
    "overlaps",
    "within",
    "terminates_at",
    "terminates_in",
    "dammed_by",
    "exposed_to",
    "exposes",
    "experienced",
    "impacted",
    "threatens",
    "triggered_by",
    "observed_by",
]


@pytest.mark.parametrize("value", _SPATIAL_DOMAIN_VALUES)
def test_parses_each_of_the_twenty_three_spatial_domain_predicates(value):
    # Exhaustive coverage of the 23, not a sample.
    result = RelationshipPredicate.parse(value)

    assert result.value == value


def test_exactly_twenty_three_spatial_domain_predicates_are_grouped():
    assert len(SPATIAL_DOMAIN_PREDICATES) == 23


def test_parametrized_values_are_exactly_the_spatial_domain_predicates():
    # Completeness guard: derive the expected set from this file's own
    # parametrize list rather than restating "23" as a bare number, so this
    # fails (not silently under-covers) if the module's set and this file's
    # list ever drift apart.
    assert {RelationshipPredicate(value) for value in _SPATIAL_DOMAIN_VALUES} == (
        SPATIAL_DOMAIN_PREDICATES
    )


# --- Negative cases ------------------------------------------------------------


def test_unrecognised_spatial_sounding_predicate_is_rejected():
    # "near" is named in registry §8's Deprecated Predicates section as one
    # of the anti-pattern predicate names the OKF spec warns against
    # (alongside connected_to, linked_to, ...) -- but it was never itself
    # one of the 35 ratified predicates, so it hits the generic
    # "not recognised" path rather than a deprecated-with-reason one.
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse("near")


def test_predicate_value_is_not_case_folded():
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse("Located_In")


def test_empty_predicate_string_is_rejected():
    with pytest.raises(InvalidRelationshipPredicate):
        RelationshipPredicate.parse("")
