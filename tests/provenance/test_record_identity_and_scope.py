"""Tests for ProvenanceRecord's own identity fields and the ADR-0011
exclusion of the embedded-baseline field count (this module ships only the
standalone node, nothing FP2/D10 would decide).
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


def _base_kwargs(**overrides) -> dict:
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
    return kwargs


def test_type_defaults_to_provenance_record_and_cannot_be_anything_else():
    record = ProvenanceRecord(**_base_kwargs())
    assert record.type == "ProvenanceRecord"

    with pytest.raises(ValidationError):
        ProvenanceRecord(**_base_kwargs(type="SomethingElse"))


def test_own_id_must_be_a_valid_cric_identifier():
    with pytest.raises(ValidationError, match="id is not a valid CRIC identifier"):
        ProvenanceRecord(**_base_kwargs(id="not-a-cric-id"))


def test_own_id_and_object_id_are_independent_identifiers():
    record = ProvenanceRecord(**_base_kwargs())
    assert record.id != record.object_id
    assert record.id == RECORD_ID
    assert record.object_id == CLAIM_OBJECT_ID


# --- ADR-0011's explicit exclusion: no embedded-baseline shape ---------------


def test_module_defines_no_embedded_provenance_or_cricobject_base_type():
    # ADR-0011: "the embedded-baseline field count" (whether every
    # CRICObject carries a nine-field embedded provenance: block) is
    # explicitly excluded -- one side of D10's still-open FP2 disagreement.
    # This module must not define anything answering that question.
    import cric_core.provenance as provenance_module

    disallowed_names = {"EmbeddedProvenance", "CRICObject", "CricObject", "BaseObject"}
    assert not (disallowed_names & set(dir(provenance_module)))


def test_provenance_record_has_no_field_named_provenance():
    # A field literally called "provenance" nested inside some other model
    # would be exactly the embedded-block shape ADR-0011 excludes.
    assert "provenance" not in ProvenanceRecord.model_fields
