"""Tests for ADR-0014's three field-requiredness tiers.

- Required (scoped): `parents` -- covered in test_significant_parents_rule.py.
- Required-whenever-applicable: `source`, `acquisition`, `integrity`,
  `licensing` -- the field itself is mandatory, tested here.
- Conditional on triggering event: `agent`, `transformation`,
  `human_reviews` -- may be entirely absent, tested here.
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


def _base_kwargs() -> dict:
    return {
        "id": RECORD_ID,
        "object_id": CLAIM_OBJECT_ID,
        "source": Source(node_ids=["CRIC:knowledge:asset:01ARZ3NDEKTSV4RRFFQ69G5FAV"]),
        "acquisition": Acquisition(retrieved_at="2026-09-05T10:00:00Z"),
        "parents": [SOME_PARENT],
        "integrity": Integrity(),
        "licensing": Licensing(licence=LicenceStatus.UNKNOWN),
    }


# --- Required-whenever-applicable: the field itself is mandatory -----------


@pytest.mark.parametrize("missing_field", ["source", "acquisition", "integrity", "licensing"])
def test_required_whenever_applicable_fields_cannot_be_omitted(missing_field):
    kwargs = _base_kwargs()
    del kwargs[missing_field]
    with pytest.raises(ValidationError):
        ProvenanceRecord(**kwargs)


def test_a_minimal_valid_record_constructs_with_all_four_tier_two_fields_present():
    record = ProvenanceRecord(**_base_kwargs())
    assert record.source is not None
    assert record.acquisition is not None
    assert record.integrity is not None
    assert record.licensing is not None


# --- Conditional on triggering event: may be entirely absent ----------------


def test_agent_transformation_and_human_reviews_may_all_be_absent():
    record = ProvenanceRecord(**_base_kwargs())
    assert record.agent is None
    assert record.transformation is None
    assert record.human_reviews == []


def test_agent_may_be_populated_when_an_agent_actually_ran():
    from cric_core.provenance import AgentInfo

    kwargs = _base_kwargs()
    kwargs["agent"] = AgentInfo(agent_id="agent-007", model="claude")
    record = ProvenanceRecord(**kwargs)
    assert record.agent.agent_id == "agent-007"


def test_transformation_may_be_populated_when_one_actually_occurred():
    from cric_core.provenance import Transformation

    kwargs = _base_kwargs()
    kwargs["transformation"] = Transformation(workflow_id="wf-1", deterministic=True)
    record = ProvenanceRecord(**kwargs)
    assert record.transformation.workflow_id == "wf-1"


# --- Licensing: required field, no default (Decision 6) --------------------


def test_licence_is_required_with_no_default():
    with pytest.raises(ValidationError):
        Licensing()


def test_licence_unknown_is_a_legitimate_explicit_value_not_a_default():
    licensing = Licensing(licence=LicenceStatus.UNKNOWN)
    assert licensing.licence is LicenceStatus.UNKNOWN


@pytest.mark.parametrize(
    "value",
    [
        "open_redistribution",
        "attribution_required",
        "share_alike",
        "noncommercial",
        "reference_only",
        "restricted",
        "unknown",
        "permission_required",
    ],
)
def test_all_eight_licence_status_values_are_accepted(value):
    assert Licensing(licence=value).licence.value == value


def test_exactly_eight_licence_status_values_exist():
    assert len(LicenceStatus) == 8
