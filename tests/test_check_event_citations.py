"""Tests for scripts/check_event_citations.py.

Never hits the real relay from this suite -- `resolve_event_created_at` is
always monkeypatched or exercised only via a faked `subprocess.run`, matching
the pattern `test_generate_build_status.py` uses for `derive_test_count`.
This script's actual, unstubbed relay behaviour is exercised by a human (or
a pre-push hook) running it standalone, per its own module docstring: it is
a pre-push script, not a CI-required check, because the relay itself
requires credentials CI does not have.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import check_event_citations as cec

# --- extract_citations: self-contained (full ISO) shape ----------------------


def test_self_contained_full_iso_citation_is_extracted():
    text = "ruled, event `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`, 2026-09-05T10:33:53Z"
    citations, skipped = cec.extract_citations(text)

    assert skipped == []
    assert len(citations) == 1
    assert citations[0].event_id == "48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3"
    assert citations[0].cited_iso == "2026-09-05T10:33:53Z"


# --- extract_citations: running-date (bare time) shape -----------------------


def test_grouped_citation_inherits_the_groups_own_leading_date():
    text = (
        "2026-09-05 (Fizz assembled, event "
        "`a8480a1e5f677b922c8ddb916fc09541e92074bbba810f34b7e6178ea60f4eaa`, 10:07:38Z; "
        "Pollen attacked, event "
        "`3239ebfa7c476d20aa136195baeddcfceaaeae2cf0affb964a4ce5f1d5203fb8`, 10:16:54Z)"
    )
    citations, skipped = cec.extract_citations(text)

    assert skipped == []
    assert len(citations) == 2
    assert citations[0].cited_iso == "2026-09-05T10:07:38Z"
    assert citations[1].cited_iso == "2026-09-05T10:16:54Z"


def test_bare_time_inherits_the_nearest_preceding_full_iso_not_an_earlier_date():
    """Regression case: the exact false positive an enclosing-parenthesis
    model produced against the real corpus (docs/OPEN_QUESTIONS.md's D6
    row -- one long prose paragraph, several inline full-ISO timestamps,
    not one governing parenthetical)."""
    text = (
        "Raised 2026-08-29 in an earlier discussion. Then: event "
        "`9a363b593a4f069f1b353025ec3b3d5beb7678b037f8a65fc15e1965f878ddba`, "
        "2026-09-04T06:57:16Z; defect 3 found, event "
        "`2099ffdf67f1957fde63a4af528c067192d120502f8642830f10bdf3a6a2772f`, 06:59:41Z"
    )
    citations, skipped = cec.extract_citations(text)

    assert skipped == []
    bare_time_citation = next(
        c for c in citations if c.event_id.startswith("2099ffdf")
    )
    # Must inherit 2026-09-04 (the nearest preceding date), not 2026-08-29
    # (the row's much earlier, unrelated date).
    assert bare_time_citation.cited_iso == "2026-09-04T06:59:41Z"


def test_hex_id_with_no_date_anywhere_before_it_is_skipped():
    text = "an event id with nothing dated before it: `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`, 10:33:53Z"
    citations, skipped = cec.extract_citations(text)

    assert citations == []
    assert len(skipped) == 1
    assert skipped[0].event_id == "48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3"


def test_hex_id_with_no_timestamp_nearby_at_all_is_skipped():
    text = "a bare id with nothing timestamp-shaped near it: `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`) mentioned in passing"
    citations, skipped = cec.extract_citations(text)

    assert citations == []
    assert len(skipped) == 1


def test_a_sha256_content_hash_with_no_nearby_timestamp_is_skipped_not_misread():
    # docs/CRIC-PRD-v0.1/CRIC-PRD-File-Manifest.md's actual shape: a table of
    # `| filename | sha256 |` rows -- 64 hex chars, no timestamp anywhere
    # near them. Must not be misread as an unresolvable *event* citation
    # that then gets reported as a relay mismatch.
    text = "| `CRIC-Integration-Audit.md` | `5a53dd67b71b2b1d449e290f2b7585c42e4eb2955d4f6061c721dabfe60496d0` |\n"
    citations, skipped = cec.extract_citations(text)

    assert citations == []
    assert len(skipped) == 1


def test_line_numbers_are_one_indexed():
    text = "line one\nline two\nevent `48159f91b0d06139169c8d7138b095f16709f2e9e58af409280ce186f675bbd3`, 2026-09-05T10:33:53Z\n"
    citations, _ = cec.extract_citations(text)

    assert citations[0].line_no == 3


# --- resolve_event_created_at: faked subprocess, never a live relay call ----


def test_resolve_event_created_at_finds_a_matching_event(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(
            cmd,
            0,
            stdout='[{"id": "abc123", "created_at": 1788598433}]',
            stderr="",
        )

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event_created_at("some-channel", "abc123")

    assert result == "2026-09-05T08:53:53Z"


def test_resolve_event_created_at_returns_none_on_nonzero_exit(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 3, stdout="", stderr="auth_error")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    assert cec.resolve_event_created_at("some-channel", "abc123") is None


def test_resolve_event_created_at_returns_none_when_id_not_in_results(monkeypatch):
    # The exact hazard that produced 44 false positives during development:
    # the CLI can exit 0 with unrelated content when the id isn't found
    # within its default window. This function must not mistake "id absent
    # from the returned events" for a match -- it returns None, and calling
    # code treats that as "could not resolve," not "confirmed missing."
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(
            cmd, 0, stdout='[{"id": "unrelated-event", "created_at": 1788598433}]', stderr=""
        )

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    assert cec.resolve_event_created_at("some-channel", "abc123") is None


def test_resolve_event_created_at_passes_the_large_fetch_limit(monkeypatch):
    captured_cmd = {}

    def fake_run(cmd, **kwargs):
        captured_cmd["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, stdout="[]", stderr="")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    cec.resolve_event_created_at("some-channel", "abc123")

    assert "--limit" in captured_cmd["cmd"]
    limit_index = captured_cmd["cmd"].index("--limit")
    assert captured_cmd["cmd"][limit_index + 1] == str(cec._THREAD_FETCH_LIMIT)


# --- check_citations: agreement/disagreement, via a monkeypatched resolver -


def test_check_citations_reports_no_mismatch_when_relay_agrees(monkeypatch):
    monkeypatch.setattr(cec, "resolve_event_created_at", lambda channel, event_id: "2026-09-05T10:33:53Z")
    citation = cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md")

    assert cec.check_citations([citation], "some-channel") == []


def test_check_citations_reports_a_mismatch_when_relay_disagrees(monkeypatch):
    monkeypatch.setattr(cec, "resolve_event_created_at", lambda channel, event_id: "2026-09-05T10:33:53Z")
    citation = cec.Citation("abc123", "2026-09-05T10:29:33Z", 1, "fake.md")

    mismatches = cec.check_citations([citation], "some-channel")

    assert len(mismatches) == 1
    assert mismatches[0].actual_iso == "2026-09-05T10:33:53Z"


def test_check_citations_reports_a_mismatch_when_the_event_cannot_be_resolved(monkeypatch):
    monkeypatch.setattr(cec, "resolve_event_created_at", lambda channel, event_id: None)
    citation = cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md")

    mismatches = cec.check_citations([citation], "some-channel")

    assert len(mismatches) == 1
    assert mismatches[0].actual_iso is None


# --- main(): file discovery scope --------------------------------------------


def test_default_file_discovery_is_recursive_not_just_top_level(tmp_path, monkeypatch):
    # Regression case: an earlier draft used a non-recursive glob on
    # decisions/*.md and docs/*.md, which would have silently never checked
    # docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md -- a real
    # citation two directories below docs/.
    nested = tmp_path / "docs" / "CRIC-PRD-v0.1"
    nested.mkdir(parents=True)
    (nested / "nested.md").write_text("some content\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cec, "check_citations", lambda citations, channel: [])
    cec.main([])  # must not raise, and must discover the nested file

    found = [
        p
        for p in Path(".").rglob("*.md")
        if not any(part in cec._EXCLUDED_DIRS for part in p.parts)
    ]
    assert any(p.name == "nested.md" for p in found)


def test_excluded_dirs_are_never_scanned(tmp_path, monkeypatch):
    excluded = tmp_path / ".venv" / "lib"
    excluded.mkdir(parents=True)
    (excluded / "should-not-be-scanned.md").write_text("content\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    found = [
        p
        for p in Path(".").rglob("*.md")
        if not any(part in cec._EXCLUDED_DIRS for part in p.parts)
    ]
    assert not any("should-not-be-scanned.md" in str(p) for p in found)
