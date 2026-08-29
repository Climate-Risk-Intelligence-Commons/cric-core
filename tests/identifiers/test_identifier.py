"""Tests for the canonical CRIC identifier type (Freeze Point 1).

Grammar under test (ratified, Engineering Coordinator + Ashley sign-off):

    CRIC-OBJECT-ID = "CRIC" ":" namespace ":" type ":" ulid

See docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md §2 and §12.
"""

import dataclasses

import pytest

from cric_core.identifiers import CricId, InvalidCricId

VALID_ULID = "01M170K23J3NSDPPZTZQ546JAE"


def test_parses_valid_canonical_id():
    result = CricId.parse(f"CRIC:core:claim:{VALID_ULID}")

    assert result.namespace == "core"
    assert result.type == "claim"
    assert result.ulid == VALID_ULID


@pytest.mark.parametrize(
    "namespace",
    [
        "core",
        "knowledge",
        "data",
        "ingest",
        "cryosphere",
        "glof",
        "models",
        "agents",
        "api",
        "ui",
        "docs",
        "review",
    ],
)
def test_parses_valid_id_for_each_of_the_twelve_closed_namespace_stems(namespace):
    # Decision 2: exhaustive coverage of the closed set of 12 canonical repo
    # stems (registry §12 "Canonical Repository Names"), not a sample.
    result = CricId.parse(f"CRIC:{namespace}:claim:{VALID_ULID}")

    assert result.namespace == namespace


def test_parses_registry_worked_example_cryosphere_glacial_lake():
    # Registry §2 / §5 worked example, with the real ULID substituted for
    # the truncated "01J..." placeholder.
    result = CricId.parse(f"CRIC:cryosphere:glacial_lake:{VALID_ULID}")

    assert result.namespace == "cryosphere"
    assert result.type == "glacial_lake"


def test_parses_registry_worked_example_glof_event():
    # Registry §2 / §5 worked example, with the real ULID substituted for
    # the truncated "01J..." placeholder.
    result = CricId.parse(f"CRIC:glof:event:{VALID_ULID}")

    assert result.namespace == "glof"
    assert result.type == "event"


def test_round_trip_str_matches_original_input():
    # Proves serialization does not silently mutate anything (decision 3:
    # byte-exact, no normalisation on read).
    original = f"CRIC:cryosphere:glacial_lake:{VALID_ULID}"

    result = CricId.parse(original)

    assert str(result) == original


def test_lowercase_cric_literal_is_rejected():
    # Decision 3 (case): the literal "CRIC" prefix is fixed-case, no fold on read.
    with pytest.raises(InvalidCricId):
        CricId.parse(f"cric:core:claim:{VALID_ULID}")


def test_uppercase_namespace_is_rejected():
    # Decision 3 (byte-exact case) and decision 2 (closed set) -- "Core" is
    # not a member of the 12 lowercase namespace stems.
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:Core:claim:{VALID_ULID}")


def test_uppercase_type_is_rejected():
    # Decision 3 (case): type segment must be lowercase, no fold on read.
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:core:Claim:{VALID_ULID}")


def test_hyphen_in_type_is_rejected():
    # Decision 3 / charset: type is lower-alnum plus "_", not "-".
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:core:glacial-lake:{VALID_ULID}")


def test_namespace_not_in_closed_set_is_rejected():
    # Decision 2 (closed set of 12 stems): "foo" is not one of them, even
    # though it is a syntactically-plausible lowercase namespace string.
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:foo:claim:{VALID_ULID}")


def test_short_ulid_is_rejected():
    # Decision 1 (ULID spec): canonical ULIDs are exactly 26 characters.
    with pytest.raises(InvalidCricId):
        CricId.parse("CRIC:core:claim:01ARZ3")


def test_lowercase_encoded_ulid_is_rejected():
    # Decision 3 (byte-exact, NO normalisation on read): a lowercase-encoded
    # ULID is a *different* string, not an equivalent one -- it must be
    # rejected outright, never silently uppercased and accepted.
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:core:claim:{VALID_ULID.lower()}")


def test_ulid_with_excluded_letter_o_is_rejected():
    # Decision 1 (Crockford Base32): the alphabet excludes I, L, O, U.
    # This fixture swaps in "O" (excluded) at a position in the valid ULID.
    bad_ulid = "O1M170K23J3NSDPPZTZQ546JAE"
    assert len(bad_ulid) == 26
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:core:claim:{bad_ulid}")


def test_short_human_facing_form_does_not_parse():
    # Registry §2: "CRIC-LAKE-001" style short IDs are explicitly NOT the
    # canonical form and must not parse as this grammar at all.
    with pytest.raises(InvalidCricId):
        CricId.parse("CRIC-LAKE-001")


def test_empty_namespace_segment_is_rejected():
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC::claim:{VALID_ULID}")


def test_empty_type_segment_is_rejected():
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:core::{VALID_ULID}")


def test_missing_type_segment_is_rejected():
    # Only 3 segments -- type is missing entirely.
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:core:{VALID_ULID}")


def test_extra_segment_is_rejected():
    # 5 segments -- one too many.
    with pytest.raises(InvalidCricId):
        CricId.parse(f"CRIC:core:claim:extra:{VALID_ULID}")


def test_equal_ids_from_identical_strings_are_equal_and_hash_equal():
    # Decision 3: comparison is byte-exact. Python's default string
    # equality already is -- no .lower()/.upper() normalisation anywhere
    # in the comparison path.
    a = CricId.parse(f"CRIC:core:claim:{VALID_ULID}")
    b = CricId.parse(f"CRIC:core:claim:{VALID_ULID}")

    assert a == b
    assert hash(a) == hash(b)


def test_cric_id_is_immutable():
    # Guardrail (Fizz's addition): once minted, an ID's segments are
    # immutable. Nothing in this module implies segments can be rewritten.
    result = CricId.parse(f"CRIC:core:claim:{VALID_ULID}")

    with pytest.raises(dataclasses.FrozenInstanceError):
        result.namespace = "glof"
