"""Tests for D28's half that lives in the object: `ProvenanceRecord` and its
nested blocks are frozen (`model_config = ConfigDict(frozen=True)`),
transcribing `Evidence-Provenance-and-Trust.md:107`'s MUST-NOT ("Lineage
records must not be rewritten to make a later workflow appear cleaner").

Per the Coordinator's addition to the review routing: a frozen config
declared on the wrong class is invisible from the outside until something
tries to mutate -- so this plants an actual mutation on both the outer
record and a nested block, rather than asserting the config attribute is
present.

Also proves the boundary of what `frozen=True` actually covers, per this
module's own docstring (Decision 7). A first pass shipped `list[str]` for
the five sequence fields, which meant `record.parents.append(...)` could
still rewrite the exact thing `:107` prohibits despite `frozen=True` --
the Coordinator's review caught that appending to `parents` "to make a
later workflow appear cleaner" is the canonical case the prohibition
means, not a residue of it. Those fields are now `tuple[str, ...]`, so
this file proves the append now fails structurally (`AttributeError`,
tuples have no mutating method), and separately proves `Transformation.
parameters` (a plain `dict`, deliberately not converted -- Python has no
stdlib frozen mapping) still mutates in place, so the one remaining gap
stays visible rather than silently closed by a test that only checked the
five fields that were fixed.
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
    Transformation,
)

RECORD_ID = "CRIC:knowledge:provenance_record:01ARZ3NDEKTSV4RRFFQ69G5FAV"
CLAIM_OBJECT_ID = "CRIC:knowledge:claim:01ARZ3NDEKTSV4RRFFQ69G5FAV"
SOME_PARENT = "CRIC:knowledge:feature:01ARZ3NDEKTSV4RRFFQ69G5FAV"


def _record(**overrides) -> ProvenanceRecord:
    kwargs = {
        "id": RECORD_ID,
        "object_id": CLAIM_OBJECT_ID,
        "source": Source(node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"]),
        "acquisition": Acquisition(retrieved_at="2026-09-05T10:00:00Z"),
        "parents": [SOME_PARENT],
        "integrity": Integrity(),
        "licensing": Licensing(licence=LicenceStatus.UNKNOWN),
    }
    kwargs.update(overrides)
    return ProvenanceRecord(**kwargs)


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


# --- The five sequence fields are tuples: appending now fails structurally -


@pytest.mark.parametrize(
    ("build_record", "get_sequence"),
    [
        (lambda: _record(), lambda r: r.parents),
        (lambda: _record(human_reviews=["CRIC:knowledge:review:01BX5ZZKBKACTAV9WEVGEMMVRZ"]), lambda r: r.human_reviews),
    ],
    ids=["parents", "human_reviews"],
)
def test_top_level_sequence_fields_are_tuples_appending_raises(build_record, get_sequence):
    record = build_record()
    sequence = get_sequence(record)
    assert isinstance(sequence, tuple)
    with pytest.raises(AttributeError):
        sequence.append("CRIC:knowledge:feature:01BX5ZZKBKACTAV9WEVGEMMVRZ")


def test_source_node_ids_and_uris_are_tuples_appending_raises():
    source = Source(
        node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"],
        uris=["https://example.org/dataset.tif"],
    )
    assert isinstance(source.node_ids, tuple)
    assert isinstance(source.uris, tuple)
    with pytest.raises(AttributeError):
        source.node_ids.append("CRIC:knowledge:asset:01BX5ZZKBKACTAV9WEVGEMMVRZ")
    with pytest.raises(AttributeError):
        source.uris.append("https://example.org/other.tif")


def test_integrity_parent_hashes_is_a_tuple_appending_raises():
    integrity = Integrity(parent_hashes=["a" * 64])
    assert isinstance(integrity.parent_hashes, tuple)
    with pytest.raises(AttributeError):
        integrity.parent_hashes.append("b" * 64)


def test_reassigning_a_tuple_field_still_rejected_same_as_before():
    # The reassignment guard (frozen=True) and the container-type change
    # (tuple) are two separate mechanisms -- this confirms the first one
    # wasn't accidentally weakened while adding the second.
    record = _record()
    with pytest.raises(ValidationError, match="frozen"):
        record.parents = (*record.parents, "CRIC:knowledge:feature:01BX5ZZKBKACTAV9WEVGEMMVRZ")


# --- The one deliberately-remaining gap: `parameters` is a plain dict ------


def test_parameters_dict_remains_mutable_in_place_the_documented_gap():
    # `Transformation.parameters` is NOT converted to anything frozen --
    # Python's stdlib has no frozen mapping, and typing it as `Mapping`
    # would be a static-only hint, not a runtime guarantee. This test
    # exists so the gap stays an asserted fact, not something a later
    # "tidying" pass can quietly assume was closed alongside the tuples.
    transformation = Transformation(workflow_id="wf-1", parameters={"threshold": 0.5})
    transformation.parameters["threshold"] = 0.9
    assert transformation.parameters == {"threshold": 0.9}
