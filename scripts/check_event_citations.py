"""Check every channel-event citation in this repository against the relay.

Mechanism named by the Engineering Coordinator (channel event `e19fb6d8...`,
2026-09-05): "a timestamp written beside an event id is derived data that was
typed. The id already determines the time. Writing both creates a second
field that can be independently wrong" -- and it has been, twice, in
permanent records (`decisions/0011`/`0012`'s `10:29:33Z`, then all three of
`decisions/0013`/`0014`/`0015`'s `14:04:04Z`), both times caught only by a
person doing a manual relay sweep. This script is that sweep, made
repeatable.

**Determined, not assumed, before building this:** the relay requires
authentication even for reads -- `buzz messages get` with `BUZZ_PRIVATE_KEY`
unset fails with `auth_error: BUZZ_PRIVATE_KEY is required` (exit code 3,
verified empirically on this host, 2026-09-05). GitHub Actions' clean CI
image has no legitimate reason to hold a Buzz private key -- that would be a
real secret from an unrelated system landing in a public, open-source
repository's CI. So this stays a pre-push script, never a `test`-job step;
see `decisions/0008`'s "no CI job without a subject" rule -- this has a
subject, but no credential-safe way to run it in CI.

Usage:
    python scripts/check_event_citations.py [--channel UUID] [PATH ...]

With no PATH arguments, scans every `*.md` file in the repository (excluding
`_EXCLUDED_DIRS` -- generated/vendored/build paths, never hand-written).
That is deliberately not "every `*.md` file under `decisions/` and `docs/`"
-- an earlier draft of this script scoped the default that way, which is
the exact "checked where I already looked" defect this tool exists to catch
in the *records*, reproduced in the *tool* (caught in review,
2026-09-05: `docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md`
carries a genuine citation two directories below `docs/`, which a
non-recursive glob on `docs/*.md` would have silently never checked).

Exits 0 if every citation with a checkable timestamp matches the relay's
`created_at` for that event id, and every event id resolves at all. Exits 1
and prints a report otherwise. Citations with no checkable timestamp (an
event id with no date anchor anywhere before it in the file) are listed as
skipped, not treated as failures -- this script does not guess a date, per
the same "fails loudly rather than inventing a default" discipline as
`generate_build_status.py`.

Two citation shapes are recognised, both seen throughout this corpus:

1. Self-contained: `` `<64-hex-id>`, 2026-09-05T10:23:29Z `` -- the
   timestamp is a full ISO-8601 string immediately after the id.
2. Running-date: a bare `` event `<64-hex-id>`, 10:23:29Z `` citation
   inherits its date from the most recent `YYYY-MM-DD` token appearing
   anywhere earlier in the same file -- **not** from whichever parenthesis
   happens to textually enclose it. An earlier version of this script used
   an enclosing-parenthetical model and it produced three false positives
   against the real corpus: `docs/OPEN_QUESTIONS.md`'s D6 row is one long
   prose paragraph, not a flat citation list, and states several full-ISO
   timestamps inline as the narrative proceeds -- a bare time later in that
   same paragraph inherits the *nearest preceding* one of those, not the
   row's very first, much earlier date. The running-date model handles both
   this shape and the simpler `2026-09-05 (event X, ...; event Y, ...)`
   grouped-citation shape used throughout `decisions/*.md`'s Ratification
   chains, because both are just "a date token appeared somewhere before
   this citation" -- confirmed against the real corpus (see
   `_most_recent_date_before`'s docstring), not merely reasoned about.

A citation is only checked if a timestamp can be established one of these
two ways. This script does not attempt to detect a date from file mtime,
git blame, or any other proxy -- an unresolvable citation is reported as
skipped, and a human decides whether it needs a fix.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

DEFAULT_CHANNEL = "17bd72a0-4d90-4e0b-b102-f9163f0cfd4b"  # CRIC-Dev

# Directories with no citation-bearing prose of ours -- generated, vendored,
# or build output. Not "places we don't expect citations", which would just
# be the same blind-spot mistake at a finer grain; these are excluded
# because nothing here is ever hand-written by this project.
_EXCLUDED_DIRS = {".venv", ".git", "dist", "build", "__pycache__", "node_modules", ".pytest_cache"}

_HEX_ID_RE = re.compile(r"[0-9a-f]{64}")
_FULL_ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
_BARE_TIME_RE = re.compile(r"\d{2}:\d{2}:\d{2}Z")

# How far past an id we'll look for its timestamp before giving up -- citations
# in this corpus put the timestamp within a few characters of the id, never
# across a paragraph break.
_LOOKAHEAD_CHARS = 40


@dataclass(frozen=True)
class Citation:
    """One `<event-id>, <timestamp>` pair found in a document."""

    event_id: str
    cited_iso: str
    line_no: int
    source: str  # path:line, for reporting


@dataclass(frozen=True)
class Skipped:
    """A hex id found with no timestamp this script could establish."""

    event_id: str
    line_no: int
    source: str


_DATE_ANCHOR_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _most_recent_date_before(anchors: list[tuple[int, str]], position: int) -> str | None:
    """Return the date string of the last anchor at or before `position`.

    `anchors` is a list of (offset, date) sorted by offset. This is the
    "sticky running date" a bare `HH:MM:SSZ` time inherits -- not the date
    that opens whichever parenthetical happens to textually enclose it.
    Both the `2026-09-05 (Fizz assembled, event ..., 10:07:38Z; ...)` group
    shape and the long, unparenthesised prose shape (a running paragraph
    that states "2026-09-04T06:57:16Z" once and then several more bare
    times after it) resolve correctly under this one rule, because both are
    just "a YYYY-MM-DD token appeared somewhere earlier in the file" --
    confirmed necessary by a real false positive this model replaced (see
    module docstring / commit history: an enclosing-parenthesis model
    picked up an unrelated, much earlier date for three real citations in
    `docs/OPEN_QUESTIONS.md`'s D6 row, which is one long prose paragraph
    with several inline full-ISO timestamps rather than one governing
    parenthetical).
    """
    result = None
    for offset, date in anchors:
        if offset > position:
            break
        result = date
    return result


def extract_citations(text: str, source: str = "<text>") -> tuple[list[Citation], list[Skipped]]:
    """Extract every (event id, resolvable timestamp) pair from `text`.

    Returns (citations, skipped) -- `skipped` lists hex ids found with no
    timestamp this function could establish (see module docstring for the
    two shapes it recognises).
    """
    anchors = [(m.start(), m.group(0)) for m in _DATE_ANCHOR_RE.finditer(text)]
    citations: list[Citation] = []
    skipped: list[Skipped] = []

    for id_match in _HEX_ID_RE.finditer(text):
        event_id = id_match.group(0)
        line_no = text.count("\n", 0, id_match.start()) + 1
        window_end = min(len(text), id_match.end() + _LOOKAHEAD_CHARS)
        window = text[id_match.end() : window_end]

        full_iso_match = _FULL_ISO_RE.search(window)
        if full_iso_match is not None:
            citations.append(Citation(event_id, full_iso_match.group(0), line_no, source))
            continue

        bare_match = _BARE_TIME_RE.search(window)
        if bare_match is not None:
            running_date = _most_recent_date_before(anchors, id_match.start())
            if running_date is not None:
                cited_iso = f"{running_date}T{bare_match.group(0)}"
                citations.append(Citation(event_id, cited_iso, line_no, source))
                continue

        skipped.append(Skipped(event_id, line_no, source))

    return citations, skipped


# `buzz messages thread` truncates silently rather than erroring when an
# event sits further back in a channel's history than its *default* window
# reaches -- confirmed empirically, not assumed: the day-1 event
# `feb934ea...` was unfindable at the default limit, returned a *different*,
# unrelated thread's content with exit code 0 (no error to catch), and was
# found intact the moment `--limit` was raised. `--limit 2000` returns the
# same result as `--limit 500` for that event (241 entries either way), so
# it is not itself truncating for this repository's current history size --
# but "large enough today" is exactly the kind of bound this project keeps
# rediscovering the hard way as a channel keeps growing. Documented as a
# known limitation below rather than presented as a guarantee.
_THREAD_FETCH_LIMIT = 2000


def resolve_event_created_at(channel: str, event_id: str) -> str | None:
    """Return the event's real `created_at` as a full ISO-8601 string.

    Returns None if the event id does not resolve within
    `_THREAD_FETCH_LIMIT` entries of its thread -- report this as "could not
    resolve," never as a confirmed non-existence claim. A large fetch limit
    makes silent truncation unlikely for this repository's history today; it
    does not make it impossible, and this function has no way to distinguish
    "genuinely does not exist" from "exists further back than the limit
    reaches" -- both look identical from here.
    """
    result = subprocess.run(
        [
            "buzz", "messages", "thread",
            "--channel", channel,
            "--event", event_id,
            "--limit", str(_THREAD_FETCH_LIMIT),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        events = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    for event in events:
        if event.get("id") == event_id:
            dt = datetime.fromtimestamp(event["created_at"], tz=UTC)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return None


@dataclass(frozen=True)
class Mismatch:
    citation: Citation
    actual_iso: str | None  # None means the event id did not resolve at all


def check_citations(
    citations: list[Citation], channel: str
) -> list[Mismatch]:
    """Resolve every citation against the relay; return the ones that disagree."""
    mismatches = []
    for citation in citations:
        actual = resolve_event_created_at(channel, citation.event_id)
        if actual != citation.cited_iso:
            mismatches.append(Mismatch(citation, actual))
    return mismatches


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", default=DEFAULT_CHANNEL, help="channel UUID to resolve events against")
    parser.add_argument(
        "--verbose", action="store_true", help="also list every skipped (unresolvable-timestamp) citation"
    )
    parser.add_argument("paths", nargs="*", help="files to check (default: every *.md file in the repo)")
    args = parser.parse_args(argv)

    if args.paths:
        files = [Path(p) for p in args.paths]
    else:
        # Whole repository, not decisions/+docs/ -- even that pair would be
        # defensible today (every current citation happens to live under
        # one of them, and both were rglob'd, not glob'd, catching
        # docs/CRIC-PRD-v0.1/CRIC-Requirements-Traceability-Matrix.md two
        # directories down). But "defensible today" is exactly the failure
        # named in review of this script (Engineering Coordinator,
        # 2026-09-05): a checker's default scope must be everywhere the
        # thing it checks could appear, not wherever its author already
        # checked by hand -- that boundary is itself a blind spot waiting
        # to be inherited by the next person who trusts the default.
        files = sorted(
            path
            for path in Path(".").rglob("*.md")
            if not any(part in _EXCLUDED_DIRS for part in path.parts)
        )

    all_citations: list[Citation] = []
    all_skipped: list[Skipped] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        citations, skipped = extract_citations(text, source=str(path))
        all_citations.extend(citations)
        all_skipped.extend(skipped)

    print(f"Checking {len(all_citations)} citation(s) with a resolvable timestamp "
          f"across {len(files)} file(s), against channel {args.channel}...")
    if all_skipped:
        print(f"({len(all_skipped)} event id occurrence(s) had no resolvable timestamp "
              f"nearby -- not checked, not failed: pass --verbose to list them)")
        if args.verbose:
            for s in all_skipped:
                print(f"    {s.source}:{s.line_no}  {s.event_id}")

    mismatches = check_citations(all_citations, args.channel)

    if not mismatches:
        print("All citations resolve and match the relay's created_at. Clean.")
        return 0

    print(f"\n{len(mismatches)} mismatch(es) found:\n")
    for m in mismatches:
        c = m.citation
        if m.actual_iso is None:
            print(f"  {c.source}:{c.line_no}  {c.event_id}  cited {c.cited_iso} -- "
                  f"could NOT resolve this event within the fetch limit. This "
                  f"is NOT a confirmed non-existence claim -- verify manually "
                  f"(e.g. `buzz messages get --since <window around the cited "
                  f"date>`) before treating it as a citation defect.")
        else:
            print(f"  {c.source}:{c.line_no}  {c.event_id}  cited {c.cited_iso}, "
                  f"actual {m.actual_iso}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
