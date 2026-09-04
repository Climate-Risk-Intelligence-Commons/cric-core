"""Knowledge-state vocabulary and transition graph (Architecture Freeze Points 6 + 7).

See `decisions/0007-freeze-points-6-7-knowledge-state-review-decision.md` on
`main` -- that ADR is the source of truth; if this module and the channel
thread ever disagree, the ADR wins.

Ratified decisions encoded below (Freeze Points 6 + 7 -- reversal after this
locks requires an explicit migration):

1. `KnowledgeStateStatus`: the seven-value vocabulary, unanimous everywhere
   it appears in the corpus. Unrecognised string rejected, never coerced.
2. `UNIVERSAL_TRANSITIONS`: the eight-edge transition envelope, universal
   across all 31 OKF node categories
   (`OKF-Knowledge-Graph-Specification.md:306`). No node type may use a
   transition outside these eight.
3. Per-type narrowing is *expressible* (`narrow_transitions`) but never
   *required* -- the universal envelope is the default for every type,
   including `ReviewDecision`, unless a future ratification narrows it.
4. `modify` is a compound transition, not a ninth edge: the source node's
   move to `SUPERSEDED` is validated through the *same* envelope as every
   other transition (so it only succeeds where `SUPERSEDED` is already
   reachable -- currently only from `DISPUTED`); the new node's `ACCEPTED`
   entry is direct construction, never passed through transition
   validation, because node origination is not a graph edge.
5. `modified_values` rejects a state field by name: both `status` and
   `knowledge_state.status` are excluded outright, explicitly, because
   `Claim` is the only one of the 31 node types with both
   (`Core-Ontology-Specification.md:214`, plus the inherited `CRICObject`
   block at `Core-Ontology-Specification.md:103-117`) and excluding one
   while permitting the other is the hole WP-15 found.
6. `Origin`: closed at three values (`agent`, `deterministic_pipeline`,
   `human`). Unrecognised rejected.
7. `VerificationMethod`: closed at four values, the exhaustive list of
   `Responsible-Autonomy-and-HITL.md`'s Level 3 promotion mechanisms.
   Unrecognised rejected.
8. `ReviewDecision.origin` is human-only (`REVIEW_DECISION_ALLOWED_ORIGINS`)
   and `ReviewDecision` enters directly at `ACCEPTED`, not `CANDIDATE`
   (`REVIEW_DECISION_ENTRY_STATUS`) -- its schema is an act of record, not
   something itself promoted through review.

Explicitly OPEN -- not decided anywhere in this module, on purpose:

- Whether `maintainer_approved_workflow` counts as human-originated.
  `VerificationMethod` and `Origin` are kept fully independent; nothing
  here validates one against the other.
- Whether `ReviewDecision` narrows the envelope for any non-entry state
  (`disputed`, `superseded`, `rejected`, `withdrawn`) is undetermined.
  `ReviewDecision` uses `UNIVERSAL_TRANSITIONS`, unnarrowed -- this module
  defines no `ReviewDecision`-specific transition envelope.
- Whether multiple reviewers produce one `ReviewDecision` node each or
  share one -- a node-cardinality question this module has no surface for.
- `Claim.status` versus `Claim.knowledge_state.status` as one field or two
  -- routed to the base-object-hierarchy work (build-order item 6). Both
  names are excluded from `modified_values` regardless of how that
  resolves.
- Excluding `id`/`provenance` from `modified_values` generally -- the
  Engineering Coordinator's own reasoning, explicitly not ratified because
  nobody has attacked it. Only `status` and `knowledge_state.status` are
  excluded here.

A silent choice among the above becomes the de facto ruling the moment it
has tests around it -- if implementing something upstream of this module
pushes toward closing one of them, stop and say so rather than encode it.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum
from typing import Final


class KnowledgeStateError(ValueError):
    """Base class for every validation error this module raises."""


class InvalidKnowledgeStateStatus(KnowledgeStateError):
    """Raised when a string is not one of the seven ratified status values."""


class InvalidOrigin(KnowledgeStateError):
    """Raised when a string is not one of the three ratified origin values,
    or when an origin fails a type-specific rule (e.g. ReviewDecision)."""


class InvalidVerificationMethod(KnowledgeStateError):
    """Raised when a string is not one of the four ratified verification
    methods."""


class InvalidTransition(KnowledgeStateError):
    """Raised when a status transition is not a legal edge in the envelope
    it is validated against."""


class InvalidModifiedValues(KnowledgeStateError):
    """Raised when a `modify` operation's `modified_values` names a field
    excluded by ADR-0007 (a state field, changeable only via the transition
    graph)."""


# Decision 1: the seven-value knowledge-state vocabulary. Closed; parsing an
# unrecognised string raises rather than coercing to the nearest value.
class KnowledgeStateStatus(StrEnum):
    CANDIDATE = "candidate"
    ACCEPTED = "accepted"
    DISPUTED = "disputed"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
    ARCHIVED = "archived"

    @classmethod
    def parse(cls, value: str) -> KnowledgeStateStatus:
        """Parse a raw string into a `KnowledgeStateStatus`.

        Raises `InvalidKnowledgeStateStatus` on any value outside the seven.
        Exact match only -- never case-folded or otherwise coerced.
        """
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidKnowledgeStateStatus(
                f"{value!r} is not one of the seven ratified knowledge-state "
                f"values: {[member.value for member in cls]}"
            ) from exc


# Decision 6: origin closed at three values.
class Origin(StrEnum):
    AGENT = "agent"
    DETERMINISTIC_PIPELINE = "deterministic_pipeline"
    HUMAN = "human"

    @classmethod
    def parse(cls, value: str) -> Origin:
        """Parse a raw string into an `Origin`.

        Raises `InvalidOrigin` on any value outside the three.
        """
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidOrigin(
                f"{value!r} is not one of the three ratified origin values: "
                f"{[member.value for member in cls]}"
            ) from exc


# Decision 7: verification method closed at four values -- the exhaustive
# list of Responsible-Autonomy-and-HITL.md's Level 3 promotion mechanisms.
class VerificationMethod(StrEnum):
    DETERMINISTIC_AUTHORITATIVE_SOURCE = "deterministic_authoritative_source"
    CORROBORATION_RULES = "corroboration_rules"
    HUMAN_REVIEW = "human_review"
    MAINTAINER_APPROVED_WORKFLOW = "maintainer_approved_workflow"

    @classmethod
    def parse(cls, value: str) -> VerificationMethod:
        """Parse a raw string into a `VerificationMethod`.

        Raises `InvalidVerificationMethod` on any value outside the four.
        """
        try:
            return cls(value)
        except ValueError as exc:
            raise InvalidVerificationMethod(
                f"{value!r} is not one of the four ratified verification "
                f"methods: {[member.value for member in cls]}"
            ) from exc


_S = KnowledgeStateStatus

# Decision 2: the eight-edge transition envelope, universal across all 31
# OKF node categories. No node type may use an edge outside this set.
UNIVERSAL_TRANSITIONS: Final[frozenset[tuple[KnowledgeStateStatus, KnowledgeStateStatus]]] = (
    frozenset(
        {
            (_S.CANDIDATE, _S.ACCEPTED),
            (_S.CANDIDATE, _S.REJECTED),
            (_S.CANDIDATE, _S.DISPUTED),
            (_S.ACCEPTED, _S.DISPUTED),
            (_S.ACCEPTED, _S.WITHDRAWN),
            (_S.DISPUTED, _S.ACCEPTED),
            (_S.DISPUTED, _S.SUPERSEDED),
            (_S.SUPERSEDED, _S.ARCHIVED),
        }
    )
)


def validate_transition(
    from_status: KnowledgeStateStatus,
    to_status: KnowledgeStateStatus,
    *,
    envelope: frozenset[tuple[KnowledgeStateStatus, KnowledgeStateStatus]] = UNIVERSAL_TRANSITIONS,
) -> None:
    """Raise `InvalidTransition` unless `from_status -> to_status` is a legal
    edge in `envelope` (the universal envelope by default).

    Per ADR-0007, `superseded -> candidate` and `withdrawn -> accepted` are
    required negative cases -- neither is in `UNIVERSAL_TRANSITIONS`, so
    both fail here by construction.
    """
    if (from_status, to_status) not in envelope:
        raise InvalidTransition(
            f"{from_status.value!r} -> {to_status.value!r} is not a legal "
            "transition in this envelope"
        )


def narrow_transitions(
    edges: Iterable[tuple[KnowledgeStateStatus, KnowledgeStateStatus]],
) -> frozenset[tuple[KnowledgeStateStatus, KnowledgeStateStatus]]:
    """Construct a per-type transition envelope narrower than the universal
    one (Decision 3: narrowing is expressible, never required).

    Raises `InvalidTransition` if `edges` contains anything outside
    `UNIVERSAL_TRANSITIONS` -- narrowing may only remove edges, never add
    one beyond the eight ratified by ADR-0007.

    Nothing in this module calls this for `ReviewDecision`: whether it
    narrows the envelope is an open item (see module docstring), and this
    function exists so a *future*, ratified narrowing has somewhere to go
    -- not so this module can pre-empt that ruling.
    """
    requested = frozenset(edges)
    outside_universal = requested - UNIVERSAL_TRANSITIONS
    if outside_universal:
        raise InvalidTransition(
            "a narrowed envelope may not add an edge outside the universal "
            f"eight: {sorted(outside_universal)}"
        )
    return requested


@dataclass(frozen=True)
class ModifyResult:
    """The two effects of a `ReviewDecision.decision: modify` operation."""

    superseded_status: KnowledgeStateStatus
    new_node_status: KnowledgeStateStatus


def apply_modify(
    source_status: KnowledgeStateStatus,
    *,
    envelope: frozenset[tuple[KnowledgeStateStatus, KnowledgeStateStatus]] = UNIVERSAL_TRANSITIONS,
) -> ModifyResult:
    """Apply a `ReviewDecision.decision: modify` compound transition.

    Decision 4: not a ninth edge. The source node's status change is
    validated through `validate_transition` -- the *same* function used for
    every other transition -- so this only succeeds where `SUPERSEDED` is
    already reachable from `source_status` (currently only `DISPUTED`).
    The new node's `ACCEPTED` entry is direct construction: it is never
    passed through `validate_transition`, because originating a node is not
    a graph edge.
    """
    validate_transition(source_status, KnowledgeStateStatus.SUPERSEDED, envelope=envelope)
    return ModifyResult(
        superseded_status=KnowledgeStateStatus.SUPERSEDED,
        new_node_status=KnowledgeStateStatus.ACCEPTED,
    )


# Decision 5: modified_values excludes both spellings of the state field by
# name. Only these two -- id/provenance exclusion is explicitly unratified.
RESERVED_MODIFY_FIELDS: Final[frozenset[str]] = frozenset({"status", "knowledge_state.status"})


def validate_modified_values(field_names: Iterable[str]) -> None:
    """Raise `InvalidModifiedValues` if `field_names` names a state field.

    Per ADR-0007, state changes happen exclusively through the transition
    graph, never through `modify`. Both `Claim.status` and
    `Claim.knowledge_state.status` are excluded explicitly -- `Claim` is the
    only one of the 31 node types with both, and excluding one while
    permitting the other is the hole WP-15 found.
    """
    named = frozenset(field_names)
    reserved_present = named & RESERVED_MODIFY_FIELDS
    if reserved_present:
        raise InvalidModifiedValues(
            f"modified_values may not name a state field: {sorted(reserved_present)}"
        )


# Decision 8: ReviewDecision-specific rules. Only what ADR-0007 ratified --
# entry status and origin. Its onward transitions are NOT narrowed here
# (see module docstring's open items).
REVIEW_DECISION_ENTRY_STATUS: Final[KnowledgeStateStatus] = KnowledgeStateStatus.ACCEPTED
REVIEW_DECISION_ALLOWED_ORIGINS: Final[frozenset[Origin]] = frozenset({Origin.HUMAN})


def validate_review_decision_origin(origin: Origin) -> None:
    """Raise `InvalidOrigin` unless `origin` is `Origin.HUMAN`.

    Per ADR-0007, `ReviewDecision.origin` is human-only: its schema
    (`reviewer`, `reviewer_role`, `signature_method`) is an act of record,
    not something itself promoted through review.
    """
    if origin not in REVIEW_DECISION_ALLOWED_ORIGINS:
        raise InvalidOrigin(
            f"ReviewDecision.origin must be human, got {origin.value!r}"
        )
