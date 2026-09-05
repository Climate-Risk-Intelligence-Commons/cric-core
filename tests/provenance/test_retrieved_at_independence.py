"""Tests for ADR-0013/D24: `acquisition.retrieved_at` carries no required
relationship to registry §7's `observation_time.acquisition_time` (which
belongs to the temporal model, build-order item 3 -- not built here).

WP-40's own dispatch: "a validator requiring retrieved_at ==
acquisition_time must be rejected outright." `ProvenanceRecord` has no
`observation_time` field at all -- there is nothing in this module *to*
couple `retrieved_at` to -- so the proof is structural: no such field
exists, and `retrieved_at` accepts any datetime, including ones that would
disagree wildly with an external observation time (the corpus's own
worked archival example: 1994 event, 2002 report, 2026 CRIC ingestion).
"""

from datetime import datetime

from cric_core.provenance import Acquisition, ProvenanceRecord

RECORD_ID = "CRIC:knowledge:provenance_record:01ARZ3NDEKTSV4RRFFQ69G5FAV"
CLAIM_OBJECT_ID = "CRIC:knowledge:claim:01ARZ3NDEKTSV4RRFFQ69G5FAV"
SOME_PARENT = "CRIC:knowledge:feature:01ARZ3NDEKTSV4RRFFQ69G5FAV"


def test_provenance_record_has_no_observation_time_field_to_couple_to():
    # If a future edit ever adds an observation_time field here, that is
    # exactly the FP2/FP3 boundary this module's docstring (Decision 5)
    # says is not this module's to decide -- this test documents the
    # absence so it fails loudly if that boundary is ever crossed silently.
    assert not hasattr(ProvenanceRecord, "observation_time")
    assert "observation_time" not in ProvenanceRecord.model_fields


def test_retrieved_at_accepts_a_time_decades_apart_from_any_notional_observation():
    # The corpus's own archival example: a 1994 GLOF, reported 2002,
    # ingested by CRIC in 2026 -- retrieved_at (2026) and the event's own
    # observation time (1994) are supposed to be able to differ by decades.
    # No validator here rejects this, because none exists to.
    acquisition = Acquisition(retrieved_at=datetime.fromisoformat("2026-01-15T00:00:00+00:00"))
    assert acquisition.retrieved_at.year == 2026


def test_two_records_with_wildly_different_retrieved_at_for_the_same_object_are_both_valid():
    # Nothing in ProvenanceRecord compares retrieved_at across records or
    # to any other field -- each record's acquisition time is independent.
    from cric_core.provenance import Integrity, LicenceStatus, Licensing, Source

    def make(retrieved_at: str) -> ProvenanceRecord:
        return ProvenanceRecord(
            id=RECORD_ID,
            object_id=CLAIM_OBJECT_ID,
            source=Source(node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"]),
            acquisition=Acquisition(retrieved_at=retrieved_at),
            parents=[SOME_PARENT],
            integrity=Integrity(),
            licensing=Licensing(licence=LicenceStatus.UNKNOWN),
        )

    first = make("2002-01-01T00:00:00Z")
    second = make("2026-01-01T00:00:00Z")
    assert first.acquisition.retrieved_at != second.acquisition.retrieved_at
