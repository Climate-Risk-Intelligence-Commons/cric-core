# Stack Research

**Domain:** Schema/contract library — provenance-preserving knowledge infrastructure
**Researched:** 2026-09-04
**Confidence:** HIGH (brownfield project; Phase 0 shipped; actual pyproject.toml and source read directly)

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.12+ | Primary language | Non-negotiable — mandated by PRD; 3.12 brings `@override`, faster CPython, `tomllib` stdlib; matches CI images |
| Pydantic | v2 (≥2.7) | Runtime schema authority for all OKF/freeze-point models | Mandated by PRD; strict typed contracts caught at import time; `model_json_schema()` publishes JSON Schema as artefact without a separate step; v2 is the only version with long-term support |
| python-ulid | ≥3.0 (`python-ulid` by mdomke) | ULID generation for new `CRIC:<ns>:<type>:<ulid>` identifiers | Phase 0 identifiers code validates ULIDs via regex; a library is needed for *generation*; python-ulid is the most actively maintained pure-Python implementation against the canonical ulid/spec |
| hatchling | current | Build backend | Already in use; zero-config src-layout support; deterministic wheels; no reason to change |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `pyyaml` | ≥6.0 | Parse OKF frontmatter (YAML-delimited header in `.okf.yaml` / `.md` files) | FP2 (Base OKF frontmatter) — OKF nodes use YAML frontmatter; parse + round-trip required |
| `python-dateutil` or stdlib `datetime` | stdlib first | ISO 8601 timestamp parsing for temporal model | FP3 — prefer stdlib `datetime.fromisoformat()` (Python 3.11+ handles full ISO 8601 including timezone offsets); reach for `dateutil` only if sub-second precision edge cases arise |
| `typing-extensions` | ≥4.10 | Backport `TypedDict`, `Annotated`, `TypeAlias` for Pydantic field annotations | Pydantic v2 requires this; will be installed transitively; pin it explicitly to avoid surprise upgrades |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `ruff` | Lint + format | Already configured; `target-version = "py312"`; replace black + isort + flake8; enforce import ordering, unused imports, type-annotation style |
| `mypy` | Static type checking | Already configured for `python_version = "3.12"`; add `--strict` once Pydantic models are in place — Pydantic v2 ships `mypy` plugin that resolves field types correctly |
| `pytest` ≥ 8 | Test runner | Already in use; `pythonpath = ["src"]` in `pyproject.toml` means `src` layout resolves without install |
| `pytest-cov` | Coverage reporting | Add for Phase 1 — schema tests require branch coverage on every enum value and transition edge |
| `build` | sdist/wheel production | Already in dev deps; invoked as `python -m build` (or `env -u PYTHONHOME -u PYTHONPATH python3 -m build` on dev host) |

---

## Installation

```bash
# Runtime (add to pyproject.toml [project].dependencies)
pip install "pydantic>=2.7" "python-ulid>=3.0" "pyyaml>=6.0"

# Dev dependencies (already in pyproject.toml [project.optional-dependencies].dev)
pip install "pytest>=8" build ruff mypy pytest-cov
```

**pyproject.toml diff for Phase 1:**
```toml
[project]
dependencies = [
    "pydantic>=2.7",
    "python-ulid>=3.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov", "build", "ruff", "mypy"]

[tool.mypy]
python_version = "3.12"
plugins = ["pydantic.mypy"]  # add this line
```

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Pydantic v2 | `dataclasses` (stdlib) | Phase 0 identifiers already use dataclasses correctly — keep them there; the identifier is a value object with no schema-generation requirement. Use Pydantic only where JSON Schema publication is part of the contract (freeze points FP2–FP8) |
| Pydantic v2 | `attrs` | Never — attrs has no JSON Schema export; Pydantic is mandated by the PRD |
| Pydantic v2 | Pydantic v1 | Never — v1 is in maintenance-only mode; v2 is the only forward-supported path; the API is incompatible enough that starting on v2 is cheaper than any later migration |
| `python-ulid` (mdomke) | `ulid2`, `python-ulid-rs` | `ulid2` is unmaintained. `python-ulid-rs` (Rust extension) is faster but adds a C build dep — unnecessary for a schema library shipping string identifiers, not high-throughput event IDs |
| `pyyaml` | `ruamel.yaml` | Use `ruamel.yaml` if round-trip preservation of YAML comments is required (it is not for FP2 — OKF frontmatter is machine-read, not human-edited in place) |
| `hatchling` | `setuptools`, `flit` | No reason to switch; hatchling is already in use and works correctly |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| LangGraph (or any orchestration framework as a dep) | Explicit PRD prohibition — coupling cric-core to an orchestration framework's upgrade cycle would propagate a transitive dep to all 23 downstream agents | Agents implement their own loops; cric-core ships schemas only |
| `numpy` / `pandas` / `xarray` / scientific stack | These are domain-computation libraries — they belong in `cric-cryosphere` / `cric-glof` / `cric-models`; adding them here violates the dependency-direction rule | No cric-core code should need numerical computation |
| `networkx` / graph libraries | Graph materialisation and retrieval is Phase 6 (`cric-api`); cric-core ships schemas, not query execution | Schema + identifier types only |
| `fastapi` / `httpx` / `requests` | No HTTP surface in cric-core; API layer is `cric-api` | N/A |
| Pydantic v1 (`pydantic<2`) | v1 is in long-term-support / maintenance-only mode; v2 has a breaking API; starting on v2 eliminates a future migration | `pydantic>=2.7` |
| `json-schema-to-pydantic` or schema-first generators | CRIC's authority direction is **Pydantic → JSON Schema**, not the reverse; generating Pydantic from JSON Schema inverts the authority and breaks the contract | Write Pydantic models; publish JSON Schema via `model_json_schema()` |
| Second ID format (`CRIC-LAKE-001` style as production IDs) | Prohibited by Architecture Freeze Point 1 / ADR-0004; causes identifier proliferation across repos | `CRIC:<ns>:<type>:<ulid>` only |

---

## Stack Patterns by Variant

**For Architecture Freeze Point schemas (FP2–FP8):**
- Write a `pydantic.BaseModel` subclass per schema
- Export `model_json_schema()` as a versioned artefact in `src/cric_core/<domain>/schema.json`
- Include a `schema_version` literal field so downstream readers can guard on schema evolution
- Every enum is `str, Enum` (not `int`) — CRIC identifiers and vocabularies are always human-readable strings

**For identifier parsing (FP1 — already shipped):**
- Keep the stdlib `dataclass`; it is frozen, hash-able, and has no schema-generation requirement
- Do not migrate to Pydantic — the dataclass is intentionally minimal and its contract is locked

**For temporal model (FP3):**
- Use `datetime` with `timezone=UTC` always — never naive datetimes
- Store observation windows as `tuple[datetime, datetime | None]` (open-ended windows are valid)
- Represent epistemic uncertainty (`unknown` ≠ `false`) as an explicit enum member, never as `None` or absent field

**For knowledge-state vocabulary (FP6/FP7 — ratified, code pending WP-18):**
- `StrEnum` (Python 3.11+, stdlib) for the 7-value vocabulary — avoids the `.value` unpacking tax
- Pydantic `Literal` field for schema version; `StrEnum` field for state values
- State-transition graph lives in code as a `frozenset[tuple[KnowledgeState, KnowledgeState]]`, not in a config file

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| `pydantic>=2.7` | Python 3.12 | Pydantic v2 requires Python ≥3.8; 2.7+ is recommended for `model_config` stability |
| `python-ulid>=3.0` | Python 3.12 | Version 3.x dropped Python <3.9 support; use ≥3.0 |
| `mypy` with `pydantic.mypy` plugin | `pydantic>=2.0` | Plugin ships inside the `pydantic` package itself — no separate install |
| `ruff` | Python 3.12 target | `target-version = "py312"` already set in `tool.ruff`; no changes needed |
| `pytest>=8` | Python 3.12 | pytest 8 is the first release with native `asyncio` mode and improved collection; current version in dev deps is correct |

---

## Sources

- `pyproject.toml` (read directly) — confirmed hatchling, pytest ≥ 8, ruff, mypy, Python ≥ 3.12
- `src/cric_core/identifiers/__init__.py` (read directly) — confirmed stdlib dataclasses, regex-based ULID validation; no external library for generation yet
- `src/cric_core/__init__.py` (read directly) — Phase 0 scaffolding only; no runtime deps yet
- `CLAUDE.md` §7 — Pydantic mandate, Python 3.12+, TypeScript scope boundary, orchestration framework prohibition
- `PROJECT.md` — confirmed active freeze points, WP-18 pending, Phase 0 complete

---

*Stack research for: cric-core (CRIC contract-root Python package)*
*Researched: 2026-09-04*
