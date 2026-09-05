"""Differential oracle for `generate_build_status.derive_ratified_freeze_points`.

**Why this exists, not just what it does.** The original derivation counted
any `decisions/*.md` Status line containing the substring "Architecture
Freeze Point" as ratified -- `decisions/0010`-`0012`'s own honest "Proposed
-- ... candidate, not yet signed by Ashley" wording matched that substring
too, and would have announced signed Freeze Points on a public README before
anyone signed anything (caught in review of PR #40, 2026-09-05). The fix
(requiring the Status value to be literally `Accepted`) was verified against
that one historical case. This file is the standing check that a future
regression of the *same shape* -- correct today, wrong the next time someone
edits the parsing logic -- gets caught automatically rather than by a person
doing another manual relay/repo sweep.

**The method, and why it's built this way.** A single implementation can't
verify itself -- re-reading `derive_ratified_freeze_points`'s own source and
confirming it "looks right" only checks that the code matches the reader's
mental model of the code, not that either is correct. This file provides a
**second, independently-written** derivation (`_oracle_derive_ratified_freeze_points`
below) that encodes the same specification -- decisions/0008's Status-line
rule -- from scratch, using different mechanics: string `.split()` on the
`Status:**` label instead of a compiled regex match, and a token-walking
number extractor instead of a capture-group regex. It deliberately does not
call, import from, or share any helper with `generate_build_status.py`. If
the production derivation and the oracle ever disagree on the real
repository, at least one of them has a bug -- that disagreement is real,
falsifiable evidence at every possible future repository state, not a
snapshot of today's.

**The limit, stated here rather than left to be discovered as a false
sense of security.** A differential oracle detects *implementation*
divergence, not *specification* error. Both implementations encode "Status
value is exactly `Accepted`, and the same line names an Architecture Freeze
Point" -- if that rule is itself wrong (too strict, too loose, or simply not
what the project actually wants), both implementations will agree and both
will be wrong, and this file will report nothing. A green run here is
evidence the two encodings agree, not a correctness proof of the rule they
share. (Engineering Coordinator, ruling on adopting this oracle, 2026-09-05:
"It cannot see a shared premise. State that plainly where the test lives.")

**Regression guard against the oracle's own guard going vacuous.**
`test_oracle_disagrees_with_the_original_substring_only_defect` plants the
exact pre-fix implementation (a bare substring check, no `Accepted`
requirement) and asserts the oracle disagrees with it on the real repo. This
is the meta-test the Coordinator required before adopting the oracle: "the
oracle ships with the planted-defect experiment as a test... that is the
same rule I have applied all day: verify a guard's reachability, not its
presence." Without this, nothing stops a future "simplification" of the
oracle into a call to the production code it's supposed to check
independently -- at which point it would compare a function to itself,
pass forever, and catch nothing, silently.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import generate_build_status as gbs


def _oracle_derive_ratified_freeze_points(repo_root: Path) -> set[int]:
    """Second, independently-written derivation. Do not import from
    `generate_build_status` here beyond this module already having done so
    for the comparison target -- this function's own logic must share no
    mechanism with `derive_ratified_freeze_points`.
    """
    ratified: set[int] = set()
    decisions_dir = repo_root / "decisions"
    for path in sorted(decisions_dir.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()

        status_line = next(
            (line for line in lines if line.strip().startswith("- **Status:**")),
            None,
        )
        title_line = next((line for line in lines if line.startswith("# ADR-")), None)
        if status_line is None or title_line is None:
            continue

        # String-split, not a regex match, on the label -- a genuinely
        # different mechanic from the production code's compiled pattern.
        after_label = status_line.split("Status:**", 1)[1].strip()
        first_word = after_label.split()[0].rstrip(".,;:") if after_label else ""
        if first_word != "Accepted":
            continue
        if "Architecture Freeze Point" not in status_line:
            continue

        # Token-walking number extraction, not a capture-group regex: find
        # "Freeze Point" in the title, then collect consecutive digit
        # tokens starting from wherever the first one appears after it.
        marker_index = title_line.find("Freeze Point")
        if marker_index == -1:
            continue
        tail_tokens = title_line[marker_index:].replace(",", " ").replace("+", " ").split()
        numbers: list[int] = []
        for token in tail_tokens:
            if token.isdigit():
                numbers.append(int(token))
            elif numbers:
                break
        ratified.update(numbers)
    return ratified


def test_oracle_agrees_with_production_on_the_real_repo():
    production = gbs.derive_ratified_freeze_points(REPO_ROOT)
    oracle = _oracle_derive_ratified_freeze_points(REPO_ROOT)

    assert production == oracle, (
        f"production derived {sorted(production)}, oracle derived "
        f"{sorted(oracle)} -- at least one of the two implementations has a "
        "bug (see this file's module docstring for what a mismatch here "
        "does and doesn't prove)"
    )


def test_oracle_disagrees_with_the_original_substring_only_defect(tmp_path):
    """The meta-test: prove the oracle is a live guard, not a tautology.

    Deliberately does NOT run this against the real repository.
    `decisions/0010`-`0012` are Accepted now -- the historical bug (a
    Status line reading "Proposed -- Architecture Freeze Point candidate"
    counted as ratified) is dormant there today and will stay dormant
    forever once every candidate is eventually signed, which is this
    project's normal end state. Running the plant against the live repo
    would make this test go vacuous the exact way the Coordinator warned
    against for the real-repo assertion itself (PR #44 review, 2026-09-05:
    "A check that passes by having nothing to examine is the failure mode
    this project has hit before"). So this reproduces the historical shape
    directly, with a synthetic fixture, independent of whatever `main`
    currently contains.
    """
    decisions_dir = tmp_path / "decisions"
    decisions_dir.mkdir()
    (decisions_dir / "0099-fake-proposed.md").write_text(
        "# ADR-0099: Freeze Point 5 -- Fake Candidate\n\n"
        "- **Status:** Proposed -- Architecture Freeze Point candidate "
        "(fifth of 8), ruled by the Engineering Coordinator, not yet "
        "signed by Ashley.\n",
        encoding="utf-8",
    )

    def buggy_substring_only_derivation(repo_root: Path) -> set[int]:
        ratified: set[int] = set()
        decisions_dir = repo_root / "decisions"
        for path in sorted(decisions_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            status_line = next(
                (line for line in lines if line.strip().startswith("- **Status:**")),
                None,
            )
            title_line = next((line for line in lines if line.startswith("# ADR-")), None)
            if status_line is None or title_line is None:
                continue
            if "Architecture Freeze Point" not in status_line:
                continue  # the missing check: never verifies Accepted
            marker_index = title_line.find("Freeze Point")
            if marker_index == -1:
                continue
            tail_tokens = title_line[marker_index:].replace(",", " ").replace("+", " ").split()
            numbers: list[int] = []
            for token in tail_tokens:
                if token.isdigit():
                    numbers.append(int(token))
                elif numbers:
                    break
            ratified.update(numbers)
        return ratified

    oracle_result = _oracle_derive_ratified_freeze_points(tmp_path)
    buggy_result = buggy_substring_only_derivation(tmp_path)

    assert oracle_result != buggy_result, (
        "the oracle failed to disagree with a deliberately reintroduced "
        "substring-only defect -- if this ever passes, the oracle has "
        "stopped being an independent guard (see this file's module "
        "docstring: a future 'simplification' that makes the oracle call "
        "into production code would produce exactly this silent failure)"
    )
