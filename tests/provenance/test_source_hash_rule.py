"""Tests for ADR-0011 Decision 4: the source-hash rule is conditional on
which of `source.node_ids`/`source.uris` is populated, not a single
missing field.
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


def _record(source: Source, content_sha256: str | None) -> ProvenanceRecord:
    return ProvenanceRecord(
        id=RECORD_ID,
        object_id=CLAIM_OBJECT_ID,
        source=source,
        acquisition=Acquisition(retrieved_at="2026-09-05T10:00:00Z"),
        parents=[SOME_PARENT],
        integrity=Integrity(content_sha256=content_sha256),
        licensing=Licensing(licence=LicenceStatus.UNKNOWN),
    )


def test_hash_may_be_absent_when_source_node_ids_populated():
    # Satisfied by dereferencing the Asset the node id points to.
    source = Source(node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"])
    record = _record(source, content_sha256=None)
    assert record.integrity.content_sha256 is None


def test_hash_is_required_when_only_uris_populated():
    # The externally-changing-URL case: no Asset node to dereference.
    source = Source(uris=["https://example.org/dataset.tif"])
    with pytest.raises(ValidationError, match="content_sha256 is required"):
        _record(source, content_sha256=None)


def test_hash_may_be_present_when_only_uris_populated():
    source = Source(uris=["https://example.org/dataset.tif"])
    record = _record(source, content_sha256="a" * 64)
    assert record.integrity.content_sha256 == "a" * 64


def test_hash_may_be_present_even_when_node_ids_populated():
    # Not forbidden -- the rule is "required when only uris", not "must be
    # absent when node_ids is present."
    source = Source(node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"])
    record = _record(source, content_sha256="b" * 64)
    assert record.integrity.content_sha256 == "b" * 64


def test_source_requires_at_least_one_of_node_ids_or_uris():
    with pytest.raises(ValidationError, match="at least one of node_ids or uris"):
        Source()
