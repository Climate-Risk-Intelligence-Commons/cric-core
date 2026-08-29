"""Canonical CRIC identifier type (Architecture Freeze Point 1).

Grammar, ratified by the Engineering Coordinator with Ashley's sign-off:

    CRIC-OBJECT-ID = "CRIC" ":" namespace ":" type ":" ulid

See docs/CRIC-PRD-v0.1/CRIC-Schema-and-Vocabulary-Registry.md §2, §12.

Ratified decisions encoded below (Freeze Point 1 -- reversal after this
locks requires an explicit migration):

1. ULID: community spec at github.com/ulid/spec -- 26 characters, Crockford
   Base32, uppercase canonical.
2. Namespace: closed set of the 12 canonical repo stems from the registry's
   §12 "Canonical Repository Names". Any other value is invalid; extension
   requires amending §12, not this code.
3. Case: lowercase namespace and type, uppercase ULID, byte-exact
   comparison -- NEVER normalise/case-fold on read. A lowercase-encoded
   ULID (or wrong-case namespace/type) is REJECTED, not silently coerced.
4. Separators: segments cannot contain ":". No escape mechanism.
5. Type-registry membership is explicitly OUT of scope for this package --
   the <type> segment gets format validation only (^[a-z][a-z0-9_]*$),
   never checked against a registry (there is no registry yet).
6. The PascalCase->snake_case transform for type names is a
   registration-time concern of a later package; it is irrelevant here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Decision 2: closed set of the 12 canonical repo stems (registry §12).
_VALID_NAMESPACES = frozenset(
    {
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
    }
)

# Decision 5: type segment is format-only, no registry-membership check.
_TYPE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

# Decision 1: Crockford Base32, uppercase canonical, excludes I, L, O, U.
_ULID_PATTERN = re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$")


class InvalidCricId(ValueError):
    """Raised when a string does not conform to the canonical CRIC ID grammar."""


@dataclass(frozen=True)
class CricId:
    """A parsed, validated canonical CRIC identifier.

    Equality and hashing are the dataclass-generated field-tuple comparison,
    which is byte-exact string equality on `namespace`/`type`/`ulid` --
    no case-folding is ever applied (decision 3).
    """

    namespace: str
    type: str
    ulid: str

    @classmethod
    def parse(cls, value: str) -> CricId:
        """Parse a canonical `CRIC:<namespace>:<type>:<ulid>` string.

        Raises `InvalidCricId` on any malformed input. Never coerces or
        normalises a segment to a "corrected" valid form.
        """
        parts = value.split(":")
        if len(parts) != 4:
            raise InvalidCricId(
                f"expected 4 colon-separated segments, got {len(parts)}: {value!r}"
            )

        literal, namespace, type_, ulid = parts

        if literal != "CRIC":
            raise InvalidCricId(f"expected literal 'CRIC', got {literal!r}")

        if namespace not in _VALID_NAMESPACES:
            raise InvalidCricId(
                f"namespace {namespace!r} is not one of the closed set: "
                f"{sorted(_VALID_NAMESPACES)}"
            )

        if not _TYPE_PATTERN.match(type_):
            raise InvalidCricId(f"type {type_!r} does not match ^[a-z][a-z0-9_]*$")

        if not _ULID_PATTERN.match(ulid):
            raise InvalidCricId(
                f"ulid {ulid!r} is not 26 uppercase Crockford Base32 characters"
            )

        return cls(namespace=namespace, type=type_, ulid=ulid)

    def __str__(self) -> str:
        return f"CRIC:{self.namespace}:{self.type}:{self.ulid}"
