"""Tests for ADR-0011 Decision 3: "significant" means a non-empty `parents`
list, and `Source` is the sole type excluded by construction.

These are the two negative tests the Engineering Coordinator named
explicitly in the WP-40 dispatch: "a Claim's record with empty parents must
reject; a Source's with empty parents must not (ADR-0011 Decision 3
excludes it by construction -- that positive control is what proves the
rule was implemented rather than approximated)."
"""

import pytest
from pydantic import ValidationError

from cric_core.provenance import (
    Acquisition,
    Integrity,
    LicenceStatus,
    Licensing,
    ProvenanceRecord,
    Source,
)

RECORD_ID = "CRIC:knowledge:provenance_record:01ARZ3NDEKTSV4RRFFQ69G5FAV"
CLAIM_OBJECT_ID = "CRIC:knowledge:claim:01ARZ3NDEKTSV4RRFFQ69G5FAV"
SOURCE_OBJECT_ID = "CRIC:knowledge:source:01ARZ3NDEKTSV4RRFFQ69G5FAV"


def _minimal_kwargs(object_id: str, parents: list[str]) -> dict:
    """A record that satisfies every rule except the one under test in
    each file -- callers override individual kwargs to isolate one rule."""
    return {
        "id": RECORD_ID,
        "object_id": object_id,
        "source": Source(node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"]),
        "acquisition": Acquisition(retrieved_at="2026-09-05T10:00:00Z"),
        "parents": parents,
        "integrity": Integrity(),
        "licensing": Licensing(licence=LicenceStatus.UNKNOWN),
    }


def test_a_claims_record_with_empty_parents_is_rejected():
    with pytest.raises(ValidationError, match="parents must be non-empty"):
        ProvenanceRecord(**_minimal_kwargs(CLAIM_OBJECT_ID, parents=[]))


def test_a_claims_record_with_non_empty_parents_is_accepted():
    record = ProvenanceRecord(
        **_minimal_kwargs(CLAIM_OBJECT_ID, parents=["CRIC:knowledge:feature:01ARZ3NDEKTSV4RRFFQ69G5FAV"])
    )
    assert record.parents == ["CRIC:knowledge:feature:01ARZ3NDEKTSV4RRFFQ69G5FAV"]


def test_a_sources_record_with_empty_parents_is_accepted():
    # The positive control: proves the rule excludes Source by construction
    # rather than by accident (e.g. a bug that never rejects anything).
    record = ProvenanceRecord(**_minimal_kwargs(SOURCE_OBJECT_ID, parents=[]))
    assert record.parents == []


def test_a_sources_record_with_non_empty_parents_is_also_accepted():
    # Non-empty parents for a Source isn't forbidden -- the rule only
    # excludes Source from the *requirement*, it doesn't ban the field.
    record = ProvenanceRecord(
        **_minimal_kwargs(SOURCE_OBJECT_ID, parents=["CRIC:knowledge:source:01BX5ZZKBKACTAV9WEVGEMMVRZ"])
    )
    assert record.parents == ["CRIC:knowledge:source:01BX5ZZKBKACTAV9WEVGEMMVRZ"]


def test_invalid_object_id_is_rejected_before_the_significant_rule_runs():
    with pytest.raises(ValidationError, match="object_id is not a valid CRIC identifier"):
        ProvenanceRecord(**_minimal_kwargs("not-a-cric-id", parents=[]))
