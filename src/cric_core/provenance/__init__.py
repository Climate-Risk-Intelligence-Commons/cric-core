"""Standalone `ProvenanceRecord` model (Architecture Freeze Point 4).

See `decisions/0011-freeze-point-4-provenance-model.md` (the promotion rule,
record shape, "significant" rule, source-hash rule), `decisions/0013-fp4-
interface-retrieved-at-vs-acquisition-time.md` (D24: `acquisition.retrieved_at`
is distinct from registry §7's `observation_time.acquisition_time`, no
required equality), and `decisions/0014-fp4-provenancerecord-field-
requiredness.md` (D29: the three field-requiredness tiers) -- these three
ADRs are the source of truth; if this module and the channel thread ever
disagree, the ADRs win.

**This is `cric-core`'s first runtime dependency (Pydantic).** Registry
§1:14: "Runtime schema authority: Pydantic" -- rank 1, so adopting it here
is transcription of an already-ratified instruction, not a new architecture
choice (Engineering Coordinator's ruling, WP-40 dispatch, 2026-09-05).

Ratified decisions encoded below:

1. **This module ships only the standalone `ProvenanceRecord` node** --
   ADR-0011 explicitly excludes the embedded-baseline field count (whether
   every `CRICObject` carries a nine-field embedded `provenance:` block).
   That number is one side of D10's still-open three-way disagreement about
   FP2's own subject, and FP4 does not settle an FP2 question as a side
   effect of answering its own. This module defines no embedded-provenance
   type and no CRICObject base class -- only `ProvenanceRecord` itself.
2. **Three field-requiredness tiers (ADR-0014):**
   - *Required (scoped):* `parents` -- the one field with unambiguous
     mandatory language in the source spec.
   - *Required-whenever-applicable:* `source`, `acquisition`, `integrity`,
     `licensing` -- all four carry the Requirements list's unqualified
     "should", with "applicable" unconditionally true for every record.
   - *Conditional on triggering event:* `agent`, `transformation`,
     `human_reviews` -- genuinely event-gated, may be entirely absent.
3. **"Significant" (Registry §9's "every significant derived object MUST
   support backward traversal") means a non-empty `parents` list**
   (ADR-0011 Decision 3), and this is enforced as a real constraint: any
   `ProvenanceRecord` whose `object_id` names something other than a
   `Source` (Registry §3's only type with nothing upstream by design) MUST
   have a non-empty `parents` list. A `Source`'s record is the sole
   exception, excluded by construction, not by an ad-hoc special case.
4. **The source-hash rule is conditional (ADR-0011 Decision 4), not a
   single field:** if `source.node_ids` is populated, `integrity.
   content_sha256` may be absent -- the hash is available by dereferencing
   the `Asset`/`DataAsset` the node id points to. If only `source.uris` is
   populated (no dereferenceable node), `integrity.content_sha256` is
   required on the record itself.
5. **`acquisition.retrieved_at` carries no required relationship to
   anything outside this module** (ADR-0013/D24) -- specifically, to
   registry §7's `observation_time.acquisition_time`, which belongs to the
   temporal model (build-order item 3, not yet built). The two are
   distinct concepts (pipeline retrieval time vs. instrument/observation
   capture time) and this module defines no validator coupling them; a
   validator requiring `retrieved_at == acquisition_time` would violate
   this ADR outright. See `test_no_validator_couples_retrieved_at_to_
   anything_external` for the negative proof.
6. **`licensing.licence` is a required field with no default.** The
   Licence Status vocabulary's own `unknown` value (`Evidence-Provenance-
   and-Trust.md:271`) is the explicit escape hatch for "not yet resolved"
   -- callers write `LicenceStatus.UNKNOWN` themselves rather than the
   model silently assuming it, matching this project's standing "unknown
   is not negative, and never a silent default" discipline.
7. **Every model in this module is frozen (D28).**
   `Evidence-Provenance-and-Trust.md:107` is a MUST-NOT: "Lineage records
   must not be rewritten to make a later workflow appear cleaner."
   `model_config = ConfigDict(frozen=True)` is transcription of that
   prohibition, not a new decision -- rule 11 in its "enforce at
   construction" form, since immutability is a property of the object.
   It is applied to `ProvenanceRecord` and to every nested block
   (`Source`, `Acquisition`, `Transformation`, `AgentInfo`, `Integrity`,
   `Licensing`), not only the outer record -- freezing only the outer
   model would still let `record.source.provider = ...` rewrite content
   reachable from an unchanged top-level reference.

   **What this does NOT close, stated so D28 is not recorded as settled:**
   - The *store* half of D28 -- append-only, WORM, hash-chaining so a
     *new* record cannot silently replace an old one -- is untouched.
     `frozen=True` constrains one in-memory object; it says nothing about
     what a caller does with the next `ProvenanceRecord` it constructs.
   - `frozen=True` blocks attribute *reassignment*. It does not make the
     mutable container fields (`parents`, `human_reviews`, `Source.
     node_ids`, `Source.uris`, `Integrity.parent_hashes`) immutable --
     `record.parents.append(...)` still mutates the same list object in
     place, because the frozen check only fires on `setattr`, never on a
     method called on an already-assigned value. See
     `test_frozen_blocks_reassignment_not_in_place_list_mutation`.

Explicitly OPEN -- not decided anywhere in this module, on purpose:

- **The falsification condition ADR-0014 states explicitly:** if a
  legitimate provenance record is found whose output genuinely cannot be
  hashed, `integrity.content_sha256` moves from required-whenever-
  applicable to conditional. That has not happened; this module still
  requires it per Decision 4 above. If implementing something upstream
  surfaces such a record, that is a finding for the Engineering
  Coordinator, not something to code around here.
- **D26** (`docs/OPEN_QUESTIONS.md`): whether the Provenance Requirements
  list's "epistemic status" item needs a dedicated `ProvenanceRecord`
  field, or is answered by the target object's own tag. This module
  defines no `epistemic_status` field either way.
- **D19** (`docs/OPEN_QUESTIONS.md`): the relationship entry schema's
  missing `evidence` field. Unrelated to `ProvenanceRecord`'s own shape;
  not touched here.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from cric_core.identifiers import CricId, InvalidCricId


# Decision 6 / Evidence-Provenance-and-Trust.md:265-275, "Licence Status,
# Recommended values" -- 8 values including the `unknown` escape hatch.
class LicenceStatus(StrEnum):
    OPEN_REDISTRIBUTION = "open_redistribution"
    ATTRIBUTION_REQUIRED = "attribution_required"
    SHARE_ALIKE = "share_alike"
    NONCOMMERCIAL = "noncommercial"
    REFERENCE_ONLY = "reference_only"
    RESTRICTED = "restricted"
    UNKNOWN = "unknown"
    PERMISSION_REQUIRED = "permission_required"


class Source(BaseModel):
    """`Evidence-Provenance-and-Trust.md`'s `source:` block.

    At least one of `node_ids`/`uris` must be populated -- the Provenance
    Requirements list names "source URI or source node" as an unqualified
    requirement, and an entirely empty `Source` describes nothing.
    """

    model_config = ConfigDict(frozen=True)

    node_ids: list[str] = Field(default_factory=list)
    uris: list[str] = Field(default_factory=list)
    provider: str | None = None
    version: str | None = None

    @model_validator(mode="after")
    def _require_a_node_id_or_a_uri(self) -> Source:
        if not self.node_ids and not self.uris:
            raise ValueError(
                "source requires at least one of node_ids or uris -- "
                "'source URI or source node' is an unqualified Provenance "
                "Requirements item, not optional"
            )
        return self


class Acquisition(BaseModel):
    """`acquisition:` block. `retrieved_at` is required-whenever-applicable
    (Provenance Requirements: "acquisition time", unqualified) and carries
    no relationship to registry §7's `observation_time.acquisition_time`
    (ADR-0013/D24) -- see this module's docstring, Decision 5."""

    model_config = ConfigDict(frozen=True)

    retrieved_at: datetime
    method: str | None = None
    actor: str | None = None


class Transformation(BaseModel):
    """`transformation:` block -- conditional on a transformation event
    having actually occurred (ADR-0014 tier 3)."""

    model_config = ConfigDict(frozen=True)

    workflow_id: str | None = None
    step_id: str | None = None
    software: str | None = None
    software_version: str | None = None
    parameters: dict[str, object] | None = None
    deterministic: bool | None = None


class AgentInfo(BaseModel):
    """`agent:` block -- conditional on an agent having actually run
    (ADR-0014 tier 3)."""

    model_config = ConfigDict(frozen=True)

    agent_id: str | None = None
    agent_version: str | None = None
    run_id: str | None = None
    model: str | None = None


class Integrity(BaseModel):
    """`integrity:` block. `content_sha256`'s requiredness is conditional
    on `Source.node_ids` (ADR-0011 Decision 4) -- enforced by
    `ProvenanceRecord`'s own cross-field validator, not here, since this
    model has no visibility into its sibling `source` block."""

    model_config = ConfigDict(frozen=True)

    content_sha256: str | None = None
    parent_hashes: list[str] = Field(default_factory=list)


class Licensing(BaseModel):
    """`licensing:` block. `licence` is required, no default -- see this
    module's docstring, Decision 6."""

    model_config = ConfigDict(frozen=True)

    licence: LicenceStatus
    redistribution: str | None = None
    derivative_use: str | None = None


class InvalidProvenanceRecord(ValueError):
    """Raised by `ProvenanceRecord`'s cross-field validators.

    Pydantic wraps this in its own `ValidationError` -- callers catch
    `pydantic.ValidationError`, matching standard Pydantic usage rather
    than this project's hand-rolled `InvalidX` exceptions elsewhere. The
    distinct type exists so the *message* is attributable to this module's
    own rules rather than a generic Pydantic type-coercion failure.
    """


# Decision 3: the one registry §3 type with nothing upstream by design
# (Evidence-Provenance-and-Trust.md's own Reference Chain: "Source ->
# Acquired Asset -> ... "). Excluded by construction from the
# non-empty-parents rule below.
_EXCLUDED_FROM_SIGNIFICANT_RULE: Literal["source"] = "source"


class ProvenanceRecord(BaseModel):
    """The standalone `ProvenanceRecord` node (ADR-0011 Decision 1+2).

    `id`/`object_id` are both canonical CRIC identifiers (Freeze Point 1):
    `id` is this record's own identity; `object_id` names the CRICObject
    this record describes. Both are validated with `identifiers.CricId`,
    the same module every other Freeze-Point-bearing type in this repo
    already uses -- reused, not re-implemented.
    """

    model_config = ConfigDict(frozen=True)

    id: str
    type: Literal["ProvenanceRecord"] = "ProvenanceRecord"
    object_id: str

    source: Source
    acquisition: Acquisition
    parents: list[str] = Field(default_factory=list)
    integrity: Integrity
    licensing: Licensing

    transformation: Transformation | None = None
    agent: AgentInfo | None = None
    human_reviews: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _validate_own_id(self) -> ProvenanceRecord:
        try:
            CricId.parse(self.id)
        except InvalidCricId as exc:
            raise InvalidProvenanceRecord(f"id is not a valid CRIC identifier: {exc}") from exc
        return self

    @model_validator(mode="after")
    def _validate_significant_requires_parents(self) -> ProvenanceRecord:
        """ADR-0011 Decision 3: non-empty `parents` unless `object_id`
        names a `Source` -- the one type structurally exempted because it
        has nothing upstream by design."""
        try:
            described = CricId.parse(self.object_id)
        except InvalidCricId as exc:
            raise InvalidProvenanceRecord(f"object_id is not a valid CRIC identifier: {exc}") from exc

        if described.type != _EXCLUDED_FROM_SIGNIFICANT_RULE and not self.parents:
            raise InvalidProvenanceRecord(
                f"parents must be non-empty for a record describing a "
                f"{described.type!r} object -- only a 'source'-typed "
                f"object_id is exempt (ADR-0011 Decision 3: 'significant' "
                f"means a non-empty parents list, and Source is the one "
                f"type with nothing upstream by design)"
            )
        return self

    @model_validator(mode="after")
    def _validate_conditional_source_hash(self) -> ProvenanceRecord:
        """ADR-0011 Decision 4: if `source.node_ids` is empty and only
        `source.uris` is populated, `integrity.content_sha256` is
        required (the externally-changing-URL case with no Asset node to
        dereference for a hash)."""
        if not self.source.node_ids and self.source.uris and self.integrity.content_sha256 is None:
            raise InvalidProvenanceRecord(
                "integrity.content_sha256 is required when source has only "
                "uris (no node_ids to dereference a hash from) -- ADR-0011 "
                "Decision 4's conditional source-hash rule"
            )
        return self
