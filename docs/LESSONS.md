# Lessons

Failures, the fixes that worked, recurring defects, and patterns worth reusing. A
lesson earns an entry when it would cost someone an hour to rediscover — not every
correction.

## Stale "not yet a git repository" fact carried by two independent agents

**What happened:** Both Fizz and the Memory & Knowledge Manager independently carried
a memory fact that `/home/ash/Eyekyam/CRIC-Core` was "not yet a git repository" — true
when first recorded, stale by the time it mattered (the repo was initialized, given an
`origin`, and had two PRs merged to `main` later the same day). Both agents caught and
corrected it themselves before it caused a bad decision, but only because each happened
to re-check `git status` while doing unrelated work.

**Why it matters:** a stale repo-state fact in memory is cheap to write and expensive
to silently rely on — the failure mode isn't "wrong once," it's "wrong in every
session that trusts the memory instead of the filesystem." Multi-agent projects with
persistent per-agent memory are structurally exposed to this: nothing forces a memory
write to be re-validated after the state it describes changes.

**Pattern to reuse:** for any fact about live repo/infra state (git-initialized,
current branch, CI status, protection rules), re-verify against the actual source
(`git status`, `gh`/API call) before relying on a memory file's claim, rather than
trusting the memory's timestamp as a freshness guarantee. Memory is a pointer to where
to look and what was true when written, not a cache that invalidates itself.
