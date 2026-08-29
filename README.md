# cric-core

`cric-core` is the contract root of the **Climate Risk Intelligence Commons (CRIC)**:
an open-source, provenance-preserving, temporally aware knowledge, data, model and
agent infrastructure for climate-risk evidence. First domain: Himalayan cryosphere /
GLOF.

Every other CRIC repository depends on this one. `cric-core` may not depend on any
domain-specific repository.

## What's here today

- The authoritative PRD family (`docs/CRIC-PRD-v0.1/`)
- The build-time engineering team charter (`docs/CRIC-Implementation-Team/`)
- Decision records (`decisions/`) and project documentation (`docs/`)

Python package code lands here from Phase 1 of the build sequence onward.

## Clone

```sh
git clone https://github.com/Climate-Risk-Intelligence-Commons/cric-core.git
```

## Specification

The authoritative specification starts at
[`docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md`](docs/CRIC-PRD-v0.1/CRIC-PRD-MASTER.md).

## Contributing

Contribution and review process:
[`docs/CRIC-PRD-v0.1/community/Contribution-and-Review-Process.md`](docs/CRIC-PRD-v0.1/community/Contribution-and-Review-Process.md).

Machine-facing operating rules for this specific repository are in
[`CLAUDE.md`](CLAUDE.md) (how work is done) and [`AGENTS.md`](AGENTS.md) (who does
what).

## Licence

AGPL-3.0. See [`LICENSE`](LICENSE).
