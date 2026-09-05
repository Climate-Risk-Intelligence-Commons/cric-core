"""Relationship predicate vocabulary and direction representation (Architecture
Freeze Point 5).

See `decisions/0010-freeze-point-5-relationship-representation.md` on `main` --
that ADR is the source of truth; if this module and the channel thread ever
disagree, the ADR wins.

Ratified decisions encoded below (Freeze Point 5 -- reversal after this locks
requires an explicit migration):

1. `RelationshipPredicate`: the vocabulary is closed at exactly 35 --
   `CRIC-Schema-and-Vocabulary-Registry.md` §8's 11 core scientific/evidential
   predicates, 23 spatial/domain predicates, and 1 structural predicate.
   Unrecognised string rejected, never coerced. Future additions go through
   the extension mechanism already written into
   `OKF-Knowledge-Graph-Specification.md:271` ("domain repositories may
   extend predicates through ontology proposals") -- this module transcribes
   that path, it does not invent one, and it defines no such mechanism
   itself (there is nothing to extend yet).
2. `connected_to`, `associated_with` (deprecated as vague anti-pattern
   predicates) and `caused_by` (rejected as redundant with `triggered_by`)
   are explicitly excluded from the vocabulary, not merely absent from it --
   `.parse()` gives each a specific reason rather than a generic "not
   recognised" message, since ADR-0010 records why each was removed.
3. `affected` is invalid; `impacted` is canonical.
   `OKF-Knowledge-Graph-Specification.md:262` uses `affected`, registry
   §8:223 uses `impacted` -- registry is rank 1, so `affected` is rejected
   with a pointer to the correct spelling rather than a bare "not
   recognised."
4. Direction representation is structural, not name-based:
   `OKF-Knowledge-Graph-Specification.md:241`'s Adjacency Derivation section
   generates `out_edges`/`in_edges` traversal indices independently for
   every predicate from a single declaration; an author never has to also
   write the paired predicate on the other node. Named inverse pairs (e.g.
   `supports`/`supported_by`) are an authoring convenience layered on top of
   that mechanism, not a requirement of it -- most predicates have no
   registered inverse name at all, and the mechanism does not need one to
   work.
5. `KNOWN_INVERSE_PAIRS` names only the pairs the corpus actually states as
   pairs, nowhere more: `supports`/`supported_by` and `supersedes`/
   `superseded_by` (ADR-0010's own count -- "only 2 of the 11 core
   predicates have a registered paired inverse name"), plus `feeds`/
   `fed_by` (the OKF spec's own worked example of the mechanism, alongside
   `supports`/`supported_by`, at `OKF-Knowledge-Graph-Specification.md:243`).
   This is deliberately not a claim that no other predicate in the 35 has an
   inverse -- several read as plausible semantic opposites (e.g.
   `upstream_of`/`downstream_of`, `exposed_to`/`exposes`) -- only that
   nothing in the ratified sources registers them as a named pair, and
   inventing that mapping here would be closing a question FP5's signature
   does not cover.
6. `detect_duplicate_inverse_declarations` implements ADR-0010's testable
   requirement: "If both directions of what is semantically the same
   relationship are ever declared independently, the compiler must treat
   this as a duplicate edge." It only ever fires on a `KNOWN_INVERSE_PAIRS`
   member -- a predicate with no registered inverse cannot produce this
   ambiguity, because there is no second vocabulary word available to
   declare it with.
7. `consistent_with` and `inconsistent_with` are never treated as an
   inverse pair of each other: each derives its own symmetric
   `out_edges`/`in_edges` independently (ADR-0010, explicit).

Explicitly OPEN -- not decided anywhere in this module, on purpose:

- The relationship entry schema's `evidence` field
  (`Core-Ontology-Specification.md:440` requires "evidence and confidence
  where appropriate"; the schema has `confidence` but no field literally
  named `evidence`) -- tracked as `docs/OPEN_QUESTIONS.md` D19. This module
  defines no `evidence` field and no substitute for one.
- `Cryosphere-Ontology.md`'s existing use of the two deprecated predicates
  (`associated_with`, `connected_to`) -- tracked as `docs/OPEN_QUESTIONS.md`
  D20. Fixing that content is out of this module's scope.
- Whether any predicate beyond `KNOWN_INVERSE_PAIRS`'s three has an intended
  inverse -- see Decision 5. A silent choice here becomes the de facto
  ruling the moment it has tests around it; if implementing something
  upstream of this module pushes toward adding to `KNOWN_INVERSE_PAIRS`,
  stop and say so rather than encode it.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, NamedTuple


class RelationshipError(ValueError):
    """Base class for every validation error this module raises."""


class InvalidRelationshipPredicate(RelationshipError):
    """Raised when a string is not one of the 35 ratified predicates."""


# Decision 1: registry §8's 11 core scientific/evidential predicates.
class RelationshipPredicate(StrEnum):
    # -- Core scientific/evidential (11) --------------------------------
    SUPPORTS = "supports"
    SUPPORTED_BY = "supported_by"
    CONTRADICTS = "contradicts"
    REFINES = "refines"
    SUPERSEDES = "supersedes"
    SUPERSEDED_BY = "superseded_by"
    CORROBORATES = "corroborates"
    DISPUTES = "disputes"
    DERIVED_FROM = "derived_from"
    CONSISTENT_WITH = "consistent_with"
    INCONSISTENT_WITH = "inconsistent_with"

    # -- Spatial/domain (23) ---------------------------------------------
    LOCATED_IN = "located_in"
    PART_OF = "part_of"
    CONTAINS = "contains"
    DEPENDS_ON = "depends_on"
    FEEDS = "feeds"
    FED_BY = "fed_by"
    DRAINS_TO = "drains_to"
    UPSTREAM_OF = "upstream_of"
    DOWNSTREAM_OF = "downstream_of"
    ADJACENT_TO = "adjacent_to"
    INTERSECTS = "intersects"
    OVERLAPS = "overlaps"
    WITHIN = "within"
    TERMINATES_AT = "terminates_at"
    TERMINATES_IN = "terminates_in"
    DAMMED_BY = "dammed_by"
    EXPOSED_TO = "exposed_to"
    EXPOSES = "exposes"
    EXPERIENCED = "experienced"
    IMPACTED = "impacted"
    THREATENS = "threatens"
    TRIGGERED_BY = "triggered_by"
    OBSERVED_BY = "observed_by"

    # -- Structural (1) ----------------------------------------------------
    HAS_SNAPSHOT = "has_snapshot"

    @classmethod
    def parse(cls, value: str) -> RelationshipPredicate:
        """Parse a raw string into a `RelationshipPredicate`.

        Raises `InvalidRelationshipPredicate` on any value outside the 35.
        Exact match only -- never case-folded or otherwise coerced.

        `connected_to`, `associated_with`, `caused_by` and `affected` each
        get a specific reason in the error message rather than a generic
        "not recognised" -- ADR-0010 records why each was excluded, and a
        caller hitting one of these is very likely reaching for the excluded
        spelling rather than a typo.
        """
        try:
            return cls(value)
        except ValueError as exc:
            if value in _DEPRECATED_REASONS:
                raise InvalidRelationshipPredicate(
                    f"{value!r} is deprecated, not merely unrecognised: "
                    f"{_DEPRECATED_REASONS[value]}"
                ) from exc
            if value == "affected":
                raise InvalidRelationshipPredicate(
                    "'affected' is not canonical -- OKF-Knowledge-Graph-"
                    "Specification.md uses 'affected' but registry §8 (rank "
                    "1) uses 'impacted'; use RelationshipPredicate.IMPACTED"
                ) from exc
            raise InvalidRelationshipPredicate(
                f"{value!r} is not one of the 35 ratified relationship "
                f"predicates: {sorted(member.value for member in cls)}"
            ) from exc


# Decision 2: deprecated/rejected predicates, excluded from the enum itself,
# with the specific reason ADR-0010 records for each.
_DEPRECATED_REASONS: Final[dict[str, str]] = {
    "connected_to": (
        "removed as a vague, semantically-empty anti-pattern predicate "
        "(registry §8, Deprecated Predicates)"
    ),
    "associated_with": (
        "removed as a vague, semantically-empty anti-pattern predicate, "
        "same reason as 'connected_to' (registry §8, Deprecated Predicates)"
    ),
    "caused_by": (
        "considered and rejected as redundant with the existing "
        "'triggered_by' at CRIC's current level of ontological granularity "
        "(registry §8)"
    ),
}
DEPRECATED_PREDICATES: Final[frozenset[str]] = frozenset({"connected_to", "associated_with"})
REJECTED_PREDICATES: Final[frozenset[str]] = frozenset({"caused_by"})

# Group membership, matching registry §8's own three headings -- lets a
# caller (or a future fan-out) work with one group without re-deriving the
# split from the enum's declaration order.
CORE_PREDICATES: Final[frozenset[RelationshipPredicate]] = frozenset(
    {
        RelationshipPredicate.SUPPORTS,
        RelationshipPredicate.SUPPORTED_BY,
        RelationshipPredicate.CONTRADICTS,
        RelationshipPredicate.REFINES,
        RelationshipPredicate.SUPERSEDES,
        RelationshipPredicate.SUPERSEDED_BY,
        RelationshipPredicate.CORROBORATES,
        RelationshipPredicate.DISPUTES,
        RelationshipPredicate.DERIVED_FROM,
        RelationshipPredicate.CONSISTENT_WITH,
        RelationshipPredicate.INCONSISTENT_WITH,
    }
)
SPATIAL_DOMAIN_PREDICATES: Final[frozenset[RelationshipPredicate]] = frozenset(
    {
        RelationshipPredicate.LOCATED_IN,
        RelationshipPredicate.PART_OF,
        RelationshipPredicate.CONTAINS,
        RelationshipPredicate.DEPENDS_ON,
        RelationshipPredicate.FEEDS,
        RelationshipPredicate.FED_BY,
        RelationshipPredicate.DRAINS_TO,
        RelationshipPredicate.UPSTREAM_OF,
        RelationshipPredicate.DOWNSTREAM_OF,
        RelationshipPredicate.ADJACENT_TO,
        RelationshipPredicate.INTERSECTS,
        RelationshipPredicate.OVERLAPS,
        RelationshipPredicate.WITHIN,
        RelationshipPredicate.TERMINATES_AT,
        RelationshipPredicate.TERMINATES_IN,
        RelationshipPredicate.DAMMED_BY,
        RelationshipPredicate.EXPOSED_TO,
        RelationshipPredicate.EXPOSES,
        RelationshipPredicate.EXPERIENCED,
        RelationshipPredicate.IMPACTED,
        RelationshipPredicate.THREATENS,
        RelationshipPredicate.TRIGGERED_BY,
        RelationshipPredicate.OBSERVED_BY,
    }
)
STRUCTURAL_PREDICATES: Final[frozenset[RelationshipPredicate]] = frozenset(
    {RelationshipPredicate.HAS_SNAPSHOT}
)


class InverseNotRegistered(RelationshipError):
    """Raised when asking for the inverse of a predicate outside
    `KNOWN_INVERSE_PAIRS` -- most predicates simply have none registered."""


# Decision 5: only the pairs the corpus actually states as pairs. Not a
# closure over all 35 -- see the module docstring's Explicitly OPEN section.
_P = RelationshipPredicate
KNOWN_INVERSE_PAIRS: Final[frozenset[tuple[RelationshipPredicate, RelationshipPredicate]]] = (
    frozenset(
        {
            (_P.SUPPORTS, _P.SUPPORTED_BY),
            (_P.SUPERSEDES, _P.SUPERSEDED_BY),
            (_P.FEEDS, _P.FED_BY),
        }
    )
)

_INVERSE_LOOKUP: Final[dict[RelationshipPredicate, RelationshipPredicate]] = {
    forward: backward for forward, backward in KNOWN_INVERSE_PAIRS
} | {backward: forward for forward, backward in KNOWN_INVERSE_PAIRS}


def registered_inverse(predicate: RelationshipPredicate) -> RelationshipPredicate:
    """Return `predicate`'s registered inverse.

    Raises `InverseNotRegistered` for any predicate outside
    `KNOWN_INVERSE_PAIRS` (Decision 5) -- including `consistent_with` and
    `inconsistent_with`, which are explicitly never paired with each other
    or anything else (Decision 7).
    """
    try:
        return _INVERSE_LOOKUP[predicate]
    except KeyError as exc:
        raise InverseNotRegistered(
            f"{predicate.value!r} has no registered inverse in "
            "KNOWN_INVERSE_PAIRS -- this may mean none exists, not that "
            "one was omitted; see the module docstring's Decision 5"
        ) from exc


class RelationshipEdge(NamedTuple):
    """A single declared relationship: `source --predicate--> target`.

    Deliberately minimal -- this is the shape `detect_duplicate_inverse_
    declarations` operates on, not a re-statement of the full entry schema
    (`predicate, target, confidence, status, source_nodes, valid_time`,
    `OKF-Knowledge-Graph-Specification.md:226-235`). The full schema's
    `evidence` field gap (D19) is out of this module's scope.
    """

    source: str
    predicate: RelationshipPredicate
    target: str


def detect_duplicate_inverse_declarations(
    edges: list[RelationshipEdge],
) -> frozenset[tuple[RelationshipEdge, RelationshipEdge]]:
    """Find edge pairs that declare the same fact from both directions.

    Decision 6 / ADR-0010: "If both directions of what is semantically the
    same relationship are ever declared independently, the compiler must
    treat this as a duplicate edge." This can only happen for a predicate
    in `KNOWN_INVERSE_PAIRS` -- a predicate with no registered inverse has
    no second vocabulary word to declare the duplicate with, so it cannot
    produce this ambiguity by construction.

    Returns the set of `(edge, its_duplicate)` pairs found, each as a
    2-tuple in declaration order. Does not resolve or dedupe anything --
    resolution ("canonical-direction deduplication") is the compiler's job,
    this function only detects the condition it must act on.
    """
    edge_set = frozenset((e.source, e.predicate, e.target) for e in edges)
    found: set[tuple[RelationshipEdge, RelationshipEdge]] = set()
    for edge in edges:
        inverse_predicate = _INVERSE_LOOKUP.get(edge.predicate)
        if inverse_predicate is None:
            continue
        candidate = (edge.target, inverse_predicate, edge.source)
        if candidate in edge_set:
            duplicate = RelationshipEdge(edge.target, inverse_predicate, edge.source)
            pair = tuple(sorted((edge, duplicate), key=lambda e: (e.source, e.predicate, e.target)))
            found.add(pair)  # type: ignore[arg-type]
    return frozenset(found)
