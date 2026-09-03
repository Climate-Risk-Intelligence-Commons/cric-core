"""Tests for the `modify` compound transition and `modified_values` exclusion
(Freeze Point 6, ADR-0007 Decision 4 + Decision 5).
"""

import pytest

from cric_core.knowledge_state import (
    RESERVED_MODIFY_FIELDS,
    InvalidModifiedValues,
    InvalidTransition,
    KnowledgeStateStatus,
    ModifyResult,
    apply_modify,
    validate_modified_values,
)

_S = KnowledgeStateStatus

# --- apply_modify: not a ninth edge -------------------------------------------


def test_modify_from_disputed_supersedes_and_creates_an_accepted_node():
    result = apply_modify(_S.DISPUTED)

    assert result == ModifyResult(
        superseded_status=_S.SUPERSEDED,
        new_node_status=_S.ACCEPTED,
    )


@pytest.mark.parametrize("source_status", [s for s in KnowledgeStateStatus if s != _S.DISPUTED])
def test_modify_from_any_non_disputed_status_fails(source_status):
    # SUPERSEDED is reachable only from DISPUTED in the universal envelope
    # (see test_transitions.py) -- modify must fail everywhere else,
    # exhaustively, not just for a sampled case or two.
    with pytest.raises(InvalidTransition):
        apply_modify(source_status)


def test_modify_uses_the_same_transition_validation_as_every_other_edge():
    # Decision 4: modify is implemented AS the existing DISPUTED->SUPERSEDED
    # edge, not a special-cased ninth edge -- narrowing that edge away also
    # removes modify's ability to succeed, with no separate code path to
    # patch back in.
    narrowed_without_supersede = frozenset({(_S.CANDIDATE, _S.ACCEPTED)})

    with pytest.raises(InvalidTransition):
        apply_modify(_S.DISPUTED, envelope=narrowed_without_supersede)


def test_modify_new_node_status_is_never_run_through_transition_validation():
    # The new node's ACCEPTED entry is direct construction (origination),
    # not a graph transition -- confirmed by the fact that an envelope
    # containing no edges into ACCEPTED at all still lets modify produce an
    # ACCEPTED new_node_status, as long as the DISPUTED->SUPERSEDED half
    # validates.
    envelope_with_no_edge_into_accepted = frozenset({(_S.DISPUTED, _S.SUPERSEDED)})

    result = apply_modify(_S.DISPUTED, envelope=envelope_with_no_edge_into_accepted)

    assert result.new_node_status == _S.ACCEPTED


# --- validate_modified_values: both spellings excluded ------------------------


def test_modified_values_rejects_status():
    with pytest.raises(InvalidModifiedValues):
        validate_modified_values(["value", "status"])


def test_modified_values_rejects_knowledge_state_status():
    with pytest.raises(InvalidModifiedValues):
        validate_modified_values(["claim_text", "knowledge_state.status"])


def test_modified_values_rejects_both_names_together():
    with pytest.raises(InvalidModifiedValues):
        validate_modified_values(["status", "knowledge_state.status"])


def test_excluding_only_status_does_not_let_knowledge_state_status_through():
    # WP-15's exact hole: an implementer who excludes `status` and believes
    # `knowledge_state.status` is therefore also blocked.
    with pytest.raises(InvalidModifiedValues):
        validate_modified_values(["knowledge_state.status"])


def test_modified_values_permits_the_ratified_evidentiary_fields():
    validate_modified_values(
        [
            "value",
            "claim_text",
            "subject",
            "predicate",
            "object",
            "confidence",
            "evidence_nodes",
            "claimant",
            "spatial_scope",
            "temporal_scope",
        ]
    )  # must not raise


def test_modified_values_with_no_fields_is_permitted():
    validate_modified_values([])  # must not raise


def test_reserved_modify_fields_names_exactly_the_two_ratified_spellings():
    # Decision 5 names id/provenance exclusion as explicitly unratified --
    # they must not appear here.
    assert RESERVED_MODIFY_FIELDS == frozenset({"status", "knowledge_state.status"})
