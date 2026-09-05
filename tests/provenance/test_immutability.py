"""Tests for D28's half that lives in the object: `ProvenanceRecord` and its
nested blocks are frozen (`model_config = ConfigDict(frozen=True)`),
transcribing `Evidence-Provenance-and-Trust.md:107`'s MUST-NOT ("Lineage
records must not be rewritten to make a later workflow appear cleaner").

Per the Coordinator's addition to the review routing: a frozen config
declared on the wrong class is invisible from the outside until something
tries to mutate -- so this plants an actual mutation on both the outer
record and a nested block, rather than asserting the config attribute is
present.

Also proves the boundary of what `frozen=True` covers, per this module's
own docstring (Decision 7): it blocks attribute *reassignment*, not
in-place mutation of a mutable container already held by a frozen
attribute. A test asserting only the positive case would let that gap
pass silently as "the record is immutable."
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
SOME_PARENT = "CRIC:knowledge:feature:01ARZ3NDEKTSV4RRFFQ69G5FAV"


def _record() -> ProvenanceRecord:
    return ProvenanceRecord(
        id=RECORD_ID,
        object_id=CLAIM_OBJECT_ID,
        source=Source(node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"]),
        acquisition=Acquisition(retrieved_at="2026-09-05T10:00:00Z"),
        parents=[SOME_PARENT],
        integrity=Integrity(),
        licensing=Licensing(licence=LicenceStatus.UNKNOWN),
    )


# --- The planted mutation the Coordinator asked for -------------------------


def test_reassigning_a_top_level_field_after_construction_is_rejected():
    record = _record()
    with pytest.raises(ValidationError, match="frozen"):
        record.object_id = "CRIC:knowledge:claim:01BX5ZZKBKACTAV9WEVGEMMVRZ"


def test_reassigning_the_id_field_after_construction_is_rejected():
    # object_id and id are separate fields with separate validators --
    # freezing one field is not evidence the model itself is frozen.
    record = _record()
    with pytest.raises(ValidationError, match="frozen"):
        record.id = "CRIC:knowledge:provenance_record:01BX5ZZKBKACTAV9WEVGEMMVRZ"


# --- Nested blocks: freezing only the outer record would still allow -------
# --- rewriting content reachable through an unchanged top-level reference --


def test_reassigning_a_field_on_the_nested_source_block_is_rejected():
    record = _record()
    with pytest.raises(ValidationError, match="frozen"):
        record.source.provider = "a different provider entirely"


def test_reassigning_a_field_on_the_nested_licensing_block_is_rejected():
    record = _record()
    with pytest.raises(ValidationError, match="frozen"):
        record.licensing.licence = LicenceStatus.OPEN_REDISTRIBUTION


def test_reassigning_a_field_on_the_nested_integrity_block_is_rejected():
    record = _record()
    with pytest.raises(ValidationError, match="frozen"):
        record.integrity.content_sha256 = "c" * 64


def test_standalone_nested_models_are_frozen_independent_of_a_parent_record():
    # Proves the config lives on each nested class itself, not something
    # inherited transiently by virtue of being embedded in a frozen parent.
    source = Source(node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"])
    with pytest.raises(ValidationError, match="frozen"):
        source.provider = "x"


# --- The boundary: frozen blocks reassignment, not in-place list mutation --


def test_frozen_blocks_reassignment_not_in_place_list_mutation():
    # Documents the gap named in this module's docstring (Decision 7)
    # rather than leaving it implicit: `frozen=True` does not make
    # `parents` itself immutable, only the `parents` *attribute*
    # unreassignable. This is not a defect in this PR -- ADR-0011/0013/
    # 0014 name no requirement for deep/structural immutability -- but a
    # test that only proved the positive case would let a reader believe
    # more was closed here than actually was.
    record = _record()
    with pytest.raises(ValidationError, match="frozen"):
        record.parents = [*record.parents, "CRIC:knowledge:feature:01BX5ZZKBKACTAV9WEVGEMMVRZ"]

    record.parents.append("CRIC:knowledge:feature:01BX5ZZKBKACTAV9WEVGEMMVRZ")
    assert record.parents == [
        SOME_PARENT,
        "CRIC:knowledge:feature:01BX5ZZKBKACTAV9WEVGEMMVRZ",
    ]
