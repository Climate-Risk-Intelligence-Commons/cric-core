# CLAUDE.md — `cric-core`

@AGENTS.md

The contract imported above is complete and harness-agnostic. It governs. What follows
is **Claude Code harness mechanics only** — never project rules, and never a place to
restate or override anything in `AGENTS.md`.

## Fan-out mechanism

`AGENTS.md` §18 sets the policy: when a work package may split, the four admission
tests, the vacuous-disjointness fix, and the redundant-fan-out anti-pattern. This is
how it is carried out here:

- Dispatch children with the **Agent tool**, one call per child, all in one message so
  they run concurrently.
- **One git worktree per child**, created off `origin/main` before dispatch, never a
  shared checkout.
- The integrator named in the `decomposition:` block merges the children and runs the
  **merged tree's** tests — not each branch's.

## Plan state

`.planning/` is written by GSD commands only. Never hand-write or hand-edit anything
under it.

## ADR discovery

`/gsd-ingest-docs` discovers ADRs with:

```text
find … \( -path '*/adr/*' -o -path '*/adrs/*' -o -name 'ADR-*.md' \
          -o -regex '.*/[0-9]\{4\}-.*\.md' \)
```

The fourth alternation matches `decisions/0001-adr-location.md`, which is why the
numbered-filename convention is auto-discovered wherever it lives (`AGENTS.md` §20).
Directory-convention discovery is skipped entirely when a `--manifest` is supplied.

## Machine-local notes

Host quirks, personal paths, private channel or relay identifiers and any other
environment-shaped detail belong in `CLAUDE.local.md`, which is gitignored. They do not
belong in this file or in `AGENTS.md` — both are public, and both are read by
contributors on machines that are not yours.
