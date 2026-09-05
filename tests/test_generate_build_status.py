"""Tests for scripts/generate_build_status.py (ADR-0008, WP-33a).

`scripts/` is not an installed package (this repo's `tests/` has no
`__init__.py` and `pyproject.toml` only puts `src` on `pythonpath`), so this
file adds `scripts/` to `sys.path` itself before importing the module under
test.

Recursion note: `derive_test_count` shells out to run the *entire* suite
with no path filter (rule 1 of WP-33a / ADR-0008). If a test in this very
suite called it for real, it would spawn a nested `pytest -q` that
re-collects this same test file, which would call it again -- recursing
without termination. So every test below that exercises `main()` or
`generate_block()` stubs `derive_test_count` out with a fixed value via
monkeypatch. The real subprocess-parsing behaviour of `derive_test_count`
(including its two raise-loudly paths) is covered separately with a faked
`subprocess.run`, never a live nested pytest. This is a deliberate design
choice, not an oversight -- the real, unstubbed call is only ever exercised
by an actual standalone invocation of the script (a human running it, or
CI's "Build-status freshness check" step, both of which run *outside* any
pytest process).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import generate_build_status as gbs

FAKE_TEST_COUNT = 4242

FIXTURE_EMPTY_MARKERS = "<!-- BUILD-STATUS:START -->\n<!-- BUILD-STATUS:END -->\n"


def _stub_test_count(monkeypatch: pytest.MonkeyPatch, count: int = FAKE_TEST_COUNT) -> None:
    monkeypatch.setattr(gbs, "derive_test_count", lambda repo_root: count)


# --- Required case 1 -------------------------------------------------------
# `--check` exits 0 immediately after a real generation run, against a
# fixture that starts with just the two markers and nothing between them.


def test_check_is_noop_immediately_after_generation(tmp_path, monkeypatch):
    _stub_test_count(monkeypatch)
    monkeypatch.chdir(REPO_ROOT)
    readme = tmp_path / "README.md"
    readme.write_text(FIXTURE_EMPTY_MARKERS, encoding="utf-8")

    rc_generate = gbs.main(["--readme-path", str(readme)])
    assert rc_generate == 0

    rc_check = gbs.main(["--check", "--readme-path", str(readme)])
    assert rc_check == 0


# --- Required case 2 -------------------------------------------------------
# `--check` exits non-zero when the fixture's committed block is stale.


def test_check_fails_on_stale_committed_block(tmp_path, monkeypatch, capsys):
    _stub_test_count(monkeypatch)
    monkeypatch.chdir(REPO_ROOT)
    readme = tmp_path / "README.md"
    stale = (
        "<!-- BUILD-STATUS:START -->\n"
        "- **0 tests passing** (full suite, `pytest`, no path filter).\n"
        "<!-- BUILD-STATUS:END -->\n"
    )
    readme.write_text(stale, encoding="utf-8")

    rc = gbs.main(["--check", "--readme-path", str(readme)])

    assert rc == 1
    err = capsys.readouterr().err
    assert "0 tests passing" in err
    assert f"{FAKE_TEST_COUNT} tests passing" in err


# --- Required case 3 -------------------------------------------------------
# No flags: rewrites the block in place; content outside the markers is
# untouched.


def test_generate_rewrites_block_leaving_surroundings_untouched(tmp_path, monkeypatch):
    _stub_test_count(monkeypatch)
    monkeypatch.chdir(REPO_ROOT)
    readme = tmp_path / "README.md"
    before = "# My Project\n\nSome real intro content.\n\n"
    after = "\n\nSome real outro content that must survive byte-for-byte.\n"
    readme.write_text(before + FIXTURE_EMPTY_MARKERS + after, encoding="utf-8")

    rc = gbs.main(["--readme-path", str(readme)])

    assert rc == 0
    updated = readme.read_text(encoding="utf-8")
    assert updated.startswith(before)
    assert updated.endswith(after)
    assert f"{FAKE_TEST_COUNT} tests passing" in updated


# --- Required case 4 -------------------------------------------------------
# No flags, markers absent: fails loudly rather than inserting them.


def test_generate_fails_loudly_when_markers_absent(tmp_path, monkeypatch, capsys):
    _stub_test_count(monkeypatch)
    monkeypatch.chdir(REPO_ROOT)
    readme = tmp_path / "README.md"
    original = "# My Project\n\nNo markers anywhere in this file.\n"
    readme.write_text(original, encoding="utf-8")

    rc = gbs.main(["--readme-path", str(readme)])

    assert rc != 0
    assert readme.read_text(encoding="utf-8") == original
    assert capsys.readouterr().err.strip() != ""


# --- Required case 5 -------------------------------------------------------
# Every number in the generated output is immediately followed by its unit
# word -- checked with a regex over the actual generated text.


def test_every_number_is_immediately_followed_by_its_unit_noun(monkeypatch):
    _stub_test_count(monkeypatch, count=7)
    block = gbs.generate_block(REPO_ROOT)

    assert re.search(r"\b7 tests passing\b", block)
    assert re.search(r"\d+ of \d+ Architecture Freeze Points ratified\b", block)
    assert re.search(r"\d+ module", block)

    # Restrict the "no bare digit" check to the generated bullet lines (the
    # `{...}` acceptance-criterion values) -- the boilerplate comment above
    # them cites "decisions/0008" by design, which is a document reference,
    # not one of this contract's counted values.
    bullet_lines = [line for line in block.splitlines() if line.startswith("- ")]
    for line in bullet_lines:
        for match in re.finditer(r"\d+", line):
            tail = line[match.end() : match.end() + 1]
            assert tail == " ", (
                f"digit run {match.group()!r} not immediately followed by a unit word "
                f"in bullet line: {line!r}"
            )


# --- Required case 6 -------------------------------------------------------
# ratified_count / total_fp derivation against this repository's real
# decisions/ and Sequence.md files, no mocking.


def test_ratified_and_total_freeze_points_against_real_repo():
    total_fp = gbs.derive_total_freeze_points(REPO_ROOT)
    ratified = gbs.derive_ratified_freeze_points(REPO_ROOT)

    assert total_fp == 8
    # Verified 2026-09-05 by reading decisions/0004 and decisions/0007 directly
    # (per WP-33a instructions, since the work package's own guess of "2" did
    # not match what the files actually said):
    #   - 0004's Status line reads "...Accepted -- **Architecture Freeze
    #     Point** (the first of 8 to lock...)" (singular, direct substring
    #     match) and its title is "Freeze Point 1 -- Object Identifier
    #     Format" -> extracts {1}.
    #   - 0007's Status line reads "...Accepted -- **Architecture Freeze
    #     Points** (second and third of the 8..." (plural, still a substring
    #     match of "Architecture Freeze Point") and its title is "Freeze
    #     Points 6 + 7 -- Knowledge-State Vocabulary and Review Decision
    #     Schema" -> extracts {6, 7}.
    #   - 0009 ("Any requirement naming a Freeze Point resolves to...") has a
    #     plain "- **Status:** Accepted" line with no "Architecture Freeze
    #     Point" substring, and its own Approver line says explicitly "not a
    #     Freeze Point" -- correctly excluded.
    # Union = {1, 6, 7} => ratified_count is 3, not 2.
    assert ratified == {1, 6, 7}
    assert len(ratified) <= total_fp


# --- Regression: a "Proposed" candidate must not count as ratified ---------
# Found in review of WP-34's PR #40 (Engineering Coordinator, 2026-09-05):
# decisions/0010-0012's actual Status lines read "Proposed -- Architecture
# Freeze Point candidate ..., not yet signed by Ashley" -- a pure substring
# match on "Architecture Freeze Point" would have counted all three as
# ratified before anyone signed anything. Reproduced here with synthetic
# fixtures rather than depending on those three files' exact wording staying
# unchanged.


def test_proposed_candidate_is_not_counted_as_ratified(tmp_path):
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    (decisions / "0099-fake-candidate.md").write_text(
        "# ADR-0099: Freeze Point 5 -- Fake Candidate\n\n"
        "- **Status:** Proposed -- Architecture Freeze Point candidate (fifth "
        "of 8), ruled by the Engineering Coordinator, not yet signed by "
        "Ashley.\n",
        encoding="utf-8",
    )

    assert gbs.derive_ratified_freeze_points(tmp_path) == set()


def test_superseded_status_naming_a_freeze_point_is_not_counted(tmp_path):
    # A second non-Accepted status word, so the fix isn't just "reject the
    # literal string 'Proposed'" -- it must require Accepted specifically.
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    (decisions / "0099-fake-superseded.md").write_text(
        "# ADR-0099: Freeze Point 5 -- Fake Superseded\n\n"
        "- **Status:** Superseded by ADR-0100 -- was an Architecture Freeze "
        "Point candidate.\n",
        encoding="utf-8",
    )

    assert gbs.derive_ratified_freeze_points(tmp_path) == set()


def test_accepted_status_naming_a_freeze_point_is_still_counted(tmp_path):
    # Positive control: the fix must not overcorrect into rejecting a
    # genuinely-ratified entry phrased exactly like ADR-0004/0007.
    decisions = tmp_path / "decisions"
    decisions.mkdir()
    (decisions / "0099-fake-ratified.md").write_text(
        "# ADR-0099: Freeze Point 5 -- Fake Ratified\n\n"
        "- **Status:** Accepted -- **Architecture Freeze Point** (fifth of 8 "
        "to lock; reversal requires explicit migration, not routine "
        "amendment)\n",
        encoding="utf-8",
    )

    assert gbs.derive_ratified_freeze_points(tmp_path) == {5}


# --- Required case 7 -------------------------------------------------------
# module_count / module_list against this repository's real
# src/cric_core/, derived independently in the test rather than hardcoded.


def test_modules_match_independently_derived_listing():
    expected = sorted(
        p.name
        for p in (REPO_ROOT / "src" / "cric_core").iterdir()
        if p.is_dir() and (p / "__init__.py").exists()
    )

    assert gbs.derive_modules(REPO_ROOT) == expected


# --- Extra coverage ---------------------------------------------------------
# derive_test_count's own parsing/raise-loudly behaviour, exercised against a
# faked subprocess.run so no nested real pytest is ever spawned.


def test_derive_test_count_parses_passed_count_from_stdout(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="...\n12 passed in 0.34s\n", stderr="")

    monkeypatch.setattr(gbs.subprocess, "run", fake_run)
    assert gbs.derive_test_count(REPO_ROOT) == 12


def test_derive_test_count_raises_on_nonzero_exit(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="boom")

    monkeypatch.setattr(gbs.subprocess, "run", fake_run)
    with pytest.raises(RuntimeError, match=r"\{test_count\}"):
        gbs.derive_test_count(REPO_ROOT)


def test_derive_test_count_raises_when_no_passed_summary(monkeypatch):
    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(cmd, 0, stdout="no summary line here\n", stderr="")

    monkeypatch.setattr(gbs.subprocess, "run", fake_run)
    with pytest.raises(RuntimeError, match=r"\{test_count\}"):
        gbs.derive_test_count(REPO_ROOT)


def test_module_list_is_none_yet_when_no_modules(tmp_path):
    empty_src = tmp_path / "src" / "cric_core"
    empty_src.mkdir(parents=True)
    assert gbs.derive_modules(tmp_path) == []


def test_apply_block_leaves_content_outside_markers_untouched():
    content = "before\n" + FIXTURE_EMPTY_MARKERS + "after\n"
    result = gbs.apply_block(content, "<!-- BUILD-STATUS:START -->\nX\n<!-- BUILD-STATUS:END -->")
    assert result == "before\n<!-- BUILD-STATUS:START -->\nX\n<!-- BUILD-STATUS:END -->\nafter\n"


def test_find_markers_raises_when_absent():
    with pytest.raises(RuntimeError):
        gbs.extract_block("no markers here")
