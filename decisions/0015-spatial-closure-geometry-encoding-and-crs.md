# ADR-0015: Spatial Closure — Geometry Encoding, Canonical CRS, Per-Asset Override (D14, WP-37)

- **Status:** Ruled by the Engineering Coordinator under Ashley's blanket approval — **not
  signed by Ashley**, and not to be read as his content. Not a Freeze Point. Reversible on one
  word from Ashley; the Wave 2 spatial package is required to verify this ruling against the
  corpus directly rather than inherit it from this ADR as already-settled truth.
- **Approver:** Engineering Coordinator, ruling made under Ashley's 2026-09-05 blanket
  ("Please consider all my signatures and all of the decisions as done. Go ahead") — that
  blanket named no CRS and no geometry closure, so there was nothing in it to ratify on this
  subject; this ADR's content is the Coordinator's own, exercised under the blanket's general
  cover, per the same reasoning recorded in `docs/OPEN_QUESTIONS.md` D14.
- **Date:** 2026-09-05
- **Evidence:** see Ratification chain below — every step cites its channel event id.

## Context

`docs/OPEN_QUESTIONS.md` D14: no canonical CRS is named anywhere in the corpus, yet
`DatasetVersion` must carry a spatial extent, V5 validation must check "valid CRS," and
normalisation must perform CRS transformation. A related, undecided gap: no document resolves
which geometry encoding format applies to which kind of spatial data. Assembled by Fizz as
WP-37 (children 37a geometry, 37b CRS — 37b independently re-derived after an anchoring-fix
redispatch, per a two-phase framing: derive independently first, only then compare against the
Coordinator's own prior reasoning); attacked by Pollen, who found a gap in the Coordinator's
first-pass CRS justification requiring one further verification pass from Fizz before this
ruling.

**This ADR supersedes the CRS justification first recorded in D14's own resolution note.** The
Coordinator's original reasoning — "GeoJSON's specification effectively forces WGS84, which is
the one format the registry actually names" — is corrected below; the second clause was false.

## Decision

**1. Geometry encoding, format-by-data-shape.** Vector geometry (lake/glacier/dam/breach/outlet
geometry) uses GeoJSON for small/single-feature data and GeoParquet for large/analytical
collections — a size/tier split the corpus already draws (`Data-Commons-Architecture.md`'s Tier
1 "Git: small GeoJSON" / Tier 2 "Local/Object Storage: COGs, large GeoParquet"), not an invented
rule. Raster/imagery (DEMs, satellite scenes) uses COG. STAC is a catalog/index layer only,
never a geometry container itself. Directly supported by the OKF frontmatter's own dual
`geometry`/`geometry_ref` fields (`:92-93`), which already structurally anticipate exactly this
inline-vs-referenced split. **"Small" is not defined anywhere in the corpus** — named as a gap
in this closure, not a blocker to it.

**Explicitly excluded from this signature: multi-dimensional array/mesh outputs** (NetCDF/Zarr,
unstructured hydraulic meshes) that hydrodynamic-model outputs and multi-variable climate/met
context blocks may produce. No corpus document resolves whether or how COG covers these. This
closure does not silently extend to them — new open item, not ruled here.

**2. Canonical storage CRS: EPSG:4326 (WGS84), with an explicit per-asset override field.**

**Corrected justification.** Registry §15 (`:358-361`) names **four** preferred formats —
GeoJSON, GeoParquet, COG, STAC — not one. Of those four, exactly **two** carry a spec-level
WGS84 constraint on their own geometry representation:

- **GeoJSON** — RFC 7946 §4 mandates WGS84/CRS84 exclusively; no CRS override is permitted
  within the format itself. Confirmed against the external spec directly, not recalled.
- **STAC, at the Item `geometry`/`bbox` level only** — verified against the primary spec
  (`radiantearth/stac-spec`, `item-spec/item-spec.md`), not recalled domain knowledge: "An Item
  is a GeoJSON Feature augmented with foreign members relevant to a STAC object," and the WGS84
  constraint is stated explicitly, twice — once for `geometry`, once for `bbox`
  ("Coordinates are specified in Longitude/Latitude ... based on WGS 84"). **The spec is
  silent on the CRS of a STAC Item's linked *assets*** — it governs the Item's own metadata
  representation only; the satellite imagery/DEM/raster an Item points to may use any native
  CRS.

**GeoParquet and COG are not spec-constrained to any CRS** — they carry native CRS internally,
which is exactly what decision 3 (the per-asset override) exists for.

**3. New content this ADR adds beyond the corrected justification: a mandatory geodesic or
projected-CRS requirement for area, volume, growth-rate, shoreline-migration and
flood-footprint calculations.** These are the quantities the GLOF/cryosphere ontologies actually
specify as core science, and a naive geographic CRS (plain lat/long) produces distorted,
non-metric results for exactly these calculation types. WGS84 remains the canonical *storage*
CRS under this ruling; any computation of these five quantity types must reproject to a
geodesic or suitable projected CRS first. This was not present in the Coordinator's first-pass
ruling and is the substantive product of Fizz's independent re-derivation, not a restatement of
it.

**4. Per-asset override field: confirmed zero textual basis anywhere in the corpus.** A
corpus-wide, case-insensitive search for "override" (including "overridden", "overriding")
returns four hits, none spatial — config precedence, licence policy, HITL assignment, a contact
decision. This field is **the Coordinator's own addition**, structurally compatible with the
OKF frontmatter's already-present, empty, unconstrained `spatial.crs` field
(`OKF-Knowledge-Graph-Specification.md:96` — the field's own definition site, not merely a
downstream processing target that presupposes it), but not established by that field's
existence.

## Alternatives considered

**CRS value:** no alternative CRS value was found or proposed anywhere in the corpus, and none
was proposed by any team member as a rival candidate — the corpus is genuinely silent. An
exhaustive sweep for `EPSG`, `WGS84`/`WGS 84`, `UTM`, "coordinate reference system", `reproject`,
`datum`, `geodetic` returned **zero hits, all seven terms**, confirmed independently twice (Fizz,
then Pollen re-running the same sweep). The choice of WGS84 is external domain reasoning applied
to a genuine gap, not a selection among corpus-named alternatives — stated explicitly so this
ADR is not misread as weighing options the corpus actually offered.

**Geometry encoding:** the only concrete alternative available was leaving format choice
unstated, per registry §15's own "preferred where appropriate" hedge. Rejected as not a closure
at all — it is the status quo the corpus already has, and the gap this ADR exists to close.

**Whether GeoParquet/COG should also be brought under one canonical CRS, not just GeoJSON/STAC:**
named explicitly as a **policy choice**, not a format requirement, since only GeoJSON and STAC's
Item-geometry level are spec-constrained. The canonical-value-plus-per-asset-override shape
(decision 4) is built for exactly this situation, even though nothing in the corpus mandates
that shape either.

## Consequences

1. **Not a Freeze Point.** Ruled by the Engineering Coordinator under Ashley's blanket approval
   (event `524472fa44b27d8f732d4033e444891120a5b7f155bef69e4ab21a19738482a3`, 2026-09-05T13:38:43Z)
   — not signed by him, and not his content; the blanket cleared the backlog but named nothing
   on this subject for it to ratify. One word from Ashley reverses this ruling in whole or in
   part.
2. **Supersedes the CRS justification first recorded in `docs/OPEN_QUESTIONS.md` D14** — that
   row is updated to point here rather than repeating the corrected reasoning a second time.
3. **The Wave 2 spatial package (build-order item 4) must verify this ruling against the corpus
   directly, not inherit it from this ADR as already-ratified truth** — the same discipline
   applied to every other Coordinator-authority ruling in this project, restated here because
   the Coordinator's own first attempt at this exact justification was found wrong before
   shipping.
4. Multi-dimensional array/mesh formats remain unresolved — not this ADR's to decide; a
   separate, future decision.
5. **A validator populating `spatial.geometry`/`centroid` while leaving `spatial.crs` empty must
   fail** both the V5 "valid CRS" check and the corpus's own general rule that every observation
   state its method and uncertainty. Stated deliberately CRS-value-agnostic, so it holds
   regardless of which value is ultimately ratified if this ruling is ever reversed.

## Ratification chain

- WP-37 assembled (Fizz, 37a geometry + 37b CRS, two-phase redo), event
  `5a31598482bb5126f5bac6aa74afb13ee27fd0bdd107cb441e2ff6ad7618b88b`, 2026-09-05T13:52:14Z.
- WP-37 attacked — corpus-silence finding confirmed, two citation-count corrections (four not
  five, twice), and a real gap found in the "one named format" claim, routing STAC's
  Item-geometry constraint back to Fizz for primary-source verification (Pollen), event
  `55f00dc314997e0104affe06bbc1c8e8709c5e7a757a32d811c52791ae4f5355`, 2026-09-05T13:55:28Z.
- Fizz verified the STAC point against the primary spec (`radiantearth/stac-spec`), confirming
  two formats carry the WGS84 constraint, not one, event
  `6f3f9b767f89a37eb4be6287c2602be029506b446b1629543e598c356cef9712`, 2026-09-05T13:56:17Z.
- Ruling — geometry closure adopted, CRS justification corrected, mandatory-reprojection
  requirement for the five named calculation types adopted, per-asset override confirmed as the
  Coordinator's own addition (Engineering Coordinator), event
  `f127c71c53d1c4ba5afd7d0870dc3e73f3175fa043f94f265b71876b5cc1f9af`, 2026-09-05T14:04:04Z.
