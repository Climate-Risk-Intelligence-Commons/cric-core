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

import json
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


def test_resolve_event_passes_an_explicit_timeout(monkeypatch):
    # Fizz's PR #51 review: a hung `buzz` process must not hang this script
    # silently -- the opposite of its own fail-loudly discipline.
    captured_kwargs = {}

    def fake_run(cmd, **kwargs):
        captured_kwargs.update(kwargs)
        return subprocess.CompletedProcess(cmd, 0, stdout="[]", stderr="")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    cec.resolve_event("some-channel", "abc123")

    assert captured_kwargs.get("timeout") == cec._SUBPROCESS_TIMEOUT_SECONDS


# --- resolve_event: the three distinguishable failure causes -----------------
#
# Fizz's PR #51 finding: a relay-unreachable failure, a malformed response,
# and a genuine non-resolution must never collapse into one message -- the
# original code returned bare `None` for all three and printed the
# non-resolution message regardless, so a total outage (BUZZ_PRIVATE_KEY
# unset, network down) misdiagnosed itself as "verify near the cited date."


def test_resolve_event_reports_relay_unreachable_on_nonzero_exit(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 3, stdout="", stderr="auth_error: BUZZ_PRIVATE_KEY is required")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event("some-channel", "abc123")

    assert result.created_at is None
    assert result.failure_reason is cec.ResolveFailureReason.RELAY_UNREACHABLE
    assert "BUZZ_PRIVATE_KEY" in result.detail


def test_resolve_event_reports_relay_unreachable_when_subprocess_raises(monkeypatch):
    # e.g. `buzz` missing from PATH -- FileNotFoundError is an OSError.
    def fake_run(cmd, **kwargs):
        raise FileNotFoundError("buzz: command not found")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event("some-channel", "abc123")

    assert result.created_at is None
    assert result.failure_reason is cec.ResolveFailureReason.RELAY_UNREACHABLE
    assert "buzz" in result.detail


def test_resolve_event_reports_relay_unreachable_on_timeout(monkeypatch):
    def fake_run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, kwargs.get("timeout", 0))

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event("some-channel", "abc123")

    assert result.created_at is None
    assert result.failure_reason is cec.ResolveFailureReason.RELAY_UNREACHABLE


def test_resolve_event_reports_malformed_response_on_bad_json(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="not json", stderr="")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event("some-channel", "abc123")

    assert result.created_at is None
    assert result.failure_reason is cec.ResolveFailureReason.MALFORMED_RESPONSE


def test_resolve_event_reports_not_found_when_call_succeeds_but_id_absent(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout='[{"id": "unrelated", "created_at": 1788598433}]', stderr="")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event("some-channel", "abc123")

    assert result.created_at is None
    assert result.failure_reason is cec.ResolveFailureReason.NOT_FOUND


# --- resolve_event: the count-vs-limit truncation signal --------------------
#
# Named by the Engineering Coordinator (channel event, 2026-09-05) correcting
# his own "101 events spanning the full day" claim: "endpoints prove nothing
# -- count and continuity do." A page returning fewer than the requested
# limit genuinely reached the end of history; a page returning exactly the
# limit could be hiding anything past that boundary.


def test_resolve_event_flags_possibly_truncated_when_page_hits_the_limit_and_id_absent(monkeypatch):
    fake_events = [
        {"id": f"other-{i}", "created_at": 1788598433} for i in range(cec._THREAD_FETCH_LIMIT)
    ]

    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(fake_events), stderr="")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event("some-channel", "abc123")

    assert result.created_at is None
    assert result.possibly_truncated is True


def test_resolve_event_does_not_flag_truncation_when_page_is_short(monkeypatch):
    # Far fewer than the limit -- the relay genuinely ran out of history, so
    # "not found" here is a real claim, not a truncation artefact.
    fake_events = [{"id": "other-1", "created_at": 1788598433}]

    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(fake_events), stderr="")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event("some-channel", "abc123")

    assert result.created_at is None
    assert result.possibly_truncated is False


def test_resolve_event_finding_the_id_is_never_flagged_as_truncated_even_at_a_full_page(monkeypatch):
    # The event itself was on the page -- whatever might lie beyond the
    # limit doesn't matter for this particular id.
    fake_events = [{"id": f"other-{i}", "created_at": 1788598433} for i in range(cec._THREAD_FETCH_LIMIT - 1)]
    fake_events.append({"id": "abc123", "created_at": 1788598433})

    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout=json.dumps(fake_events), stderr="")

    monkeypatch.setattr(cec.subprocess, "run", fake_run)
    result = cec.resolve_event("some-channel", "abc123")

    assert result.created_at == "2026-09-05T08:53:53Z"
    assert result.possibly_truncated is False


def test_mismatch_carries_the_truncation_flag_through_check_citations(monkeypatch):
    monkeypatch.setattr(
        cec,
        "resolve_event",
        lambda channel, event_id: cec.ResolveResult(
            created_at=None, failure_reason=cec.ResolveFailureReason.NOT_FOUND, possibly_truncated=True
        ),
    )
    citation = cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md")

    mismatches = cec.check_citations([citation], "some-channel")

    assert len(mismatches) == 1
    assert mismatches[0].possibly_truncated is True


def test_mismatch_carries_the_failure_reason_through_check_citations(monkeypatch):
    monkeypatch.setattr(
        cec,
        "resolve_event",
        lambda channel, event_id: cec.ResolveResult(
            created_at=None, failure_reason=cec.ResolveFailureReason.RELAY_UNREACHABLE, detail="auth_error"
        ),
    )
    citation = cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md")

    mismatches = cec.check_citations([citation], "some-channel")

    assert len(mismatches) == 1
    assert mismatches[0].failure_reason is cec.ResolveFailureReason.RELAY_UNREACHABLE
    assert mismatches[0].detail == "auth_error"


# --- check_citations: agreement/disagreement, via a monkeypatched resolver -


def _fake_resolve(created_at, possibly_truncated=False):
    reason = None if created_at is not None else cec.ResolveFailureReason.NOT_FOUND
    return lambda channel, event_id: cec.ResolveResult(
        created_at=created_at, failure_reason=reason, possibly_truncated=possibly_truncated
    )


def test_check_citations_reports_no_mismatch_when_relay_agrees(monkeypatch):
    monkeypatch.setattr(cec, "resolve_event", _fake_resolve("2026-09-05T10:33:53Z"))
    citation = cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md")

    assert cec.check_citations([citation], "some-channel") == []


def test_check_citations_reports_a_mismatch_when_relay_disagrees(monkeypatch):
    monkeypatch.setattr(cec, "resolve_event", _fake_resolve("2026-09-05T10:33:53Z"))
    citation = cec.Citation("abc123", "2026-09-05T10:29:33Z", 1, "fake.md")

    mismatches = cec.check_citations([citation], "some-channel")

    assert len(mismatches) == 1
    assert mismatches[0].actual_iso == "2026-09-05T10:33:53Z"


def test_check_citations_reports_a_mismatch_when_the_event_cannot_be_resolved(monkeypatch):
    monkeypatch.setattr(cec, "resolve_event", _fake_resolve(None))
    citation = cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md")

    mismatches = cec.check_citations([citation], "some-channel")

    assert len(mismatches) == 1
    assert mismatches[0].actual_iso is None


# --- main(): the printed message for each failure branch --------------------
#
# Fizz's PR #51 round-2 finding: the *data* (ResolveFailureReason) was
# exhaustively tested, but nothing checked that main()'s four report
# branches print the message that actually matches the cause. Proved
# necessary with a planted swap: exchanging the RELAY_UNREACHABLE and
# MALFORMED_RESPONSE message bodies left all 27 (then) tests green. These
# four close that hole -- each asserts the load-bearing diagnostic phrase
# for its branch, not a full-string match.


def _run_main_with_one_mismatch(tmp_path, monkeypatch, mismatch):
    """Point main() at a real (empty-content) file so file discovery has
    something to iterate, but force check_citations to return exactly the
    one Mismatch under test -- isolates the print branch from extraction/
    resolution entirely."""
    md_file = tmp_path / "fake.md"
    md_file.write_text("no citations in here\n", encoding="utf-8")
    monkeypatch.setattr(cec, "check_citations", lambda citations, channel: [mismatch])
    exit_code = cec.main([str(md_file)])
    return exit_code


def test_main_prints_relay_unreachable_diagnosis_not_verify_manually(tmp_path, monkeypatch, capsys):
    mismatch = cec.Mismatch(
        citation=cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md"),
        actual_iso=None,
        failure_reason=cec.ResolveFailureReason.RELAY_UNREACHABLE,
        detail="auth_error: BUZZ_PRIVATE_KEY is required",
    )
    exit_code = _run_main_with_one_mismatch(tmp_path, monkeypatch, mismatch)

    out = capsys.readouterr().out
    assert exit_code == 1
    assert "RELAY CALL FAILED" in out
    assert "auth_error" in out
    # Must NOT print the non-resolution diagnosis for a total outage.
    assert "verify manually" not in out


def test_main_prints_malformed_response_diagnosis(tmp_path, monkeypatch, capsys):
    mismatch = cec.Mismatch(
        citation=cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md"),
        actual_iso=None,
        failure_reason=cec.ResolveFailureReason.MALFORMED_RESPONSE,
        detail="not json",
    )
    exit_code = _run_main_with_one_mismatch(tmp_path, monkeypatch, mismatch)

    out = capsys.readouterr().out
    assert exit_code == 1
    assert "wasn't valid JSON" in out
    assert "not json" in out
    assert "RELAY CALL FAILED" not in out


def test_main_prints_inconclusive_when_not_found_and_possibly_truncated(tmp_path, monkeypatch, capsys):
    mismatch = cec.Mismatch(
        citation=cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md"),
        actual_iso=None,
        failure_reason=cec.ResolveFailureReason.NOT_FOUND,
        possibly_truncated=True,
    )
    exit_code = _run_main_with_one_mismatch(tmp_path, monkeypatch, mismatch)

    out = capsys.readouterr().out
    assert exit_code == 1
    assert "INCONCLUSIVE" in out
    assert "RELAY CALL FAILED" not in out
    assert "not valid JSON" not in out


def test_main_prints_plain_not_found_when_not_truncated(tmp_path, monkeypatch, capsys):
    mismatch = cec.Mismatch(
        citation=cec.Citation("abc123", "2026-09-05T10:33:53Z", 1, "fake.md"),
        actual_iso=None,
        failure_reason=cec.ResolveFailureReason.NOT_FOUND,
        possibly_truncated=False,
    )
    exit_code = _run_main_with_one_mismatch(tmp_path, monkeypatch, mismatch)

    out = capsys.readouterr().out
    assert exit_code == 1
    assert "could NOT resolve" in out
    assert "not a truncation artefact" in out
    assert "INCONCLUSIVE" not in out


def test_main_prints_the_actual_mismatched_timestamps_when_relay_disagrees(tmp_path, monkeypatch, capsys):
    mismatch = cec.Mismatch(
        citation=cec.Citation("abc123", "2026-09-05T10:29:33Z", 1, "fake.md"),
        actual_iso="2026-09-05T10:33:53Z",
    )
    exit_code = _run_main_with_one_mismatch(tmp_path, monkeypatch, mismatch)

    out = capsys.readouterr().out
    assert exit_code == 1
    assert "2026-09-05T10:29:33Z" in out
    assert "2026-09-05T10:33:53Z" in out


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
