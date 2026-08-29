# CRIC Cryosphere Ontology Specification

## Purpose

This document defines the first domain extension of the Climate Risk Intelligence Commons core ontology.

The Cryosphere ontology represents glaciers, snow, ice, glacial lakes, permafrost, frozen-ground systems, moraine systems, glacier-related mass movements, their observations, and their relationships to terrain, hydrology, climate and downstream systems.

It is designed to support GLOF intelligence initially while remaining reusable for broader cryosphere-risk applications.

---

# Domain Boundary

The Cryosphere ontology extends CRIC Core. It must not redefine core concepts such as:

- Entity;
- Event;
- Observation;
- StateSnapshot;
- Claim;
- Evidence;
- Dataset;
- Asset;
- Hazard;
- Trigger;
- Exposure;
- Assessment.

Instead it creates domain-specific child types.

---

# Cryosphere Type Hierarchy

```text
CryosphereEntity
├── Glacier
├── GlacierComplex
├── GlacierTerminus
├── IceBody
├── IceCliff
├── Snowpack
├── Snowfield
├── GlacialLake
├── Moraine
├── MoraineDam
├── IceDam
├── PermafrostBody
├── FrozenGroundFeature
├── AvalanchePath
├── MassMovementSourceArea
└── CryosphereCatchmentFeature

CryosphereEvent
├── GlacierAdvance
├── GlacierRetreatEpisode
├── GlacierSurge
├── CalvingEvent
├── IceAvalanche
├── SnowAvalanche
├── RockIceAvalanche
├── LakeFormationEvent
├── LakeExpansionEpisode
├── LakeDrainageEvent
└── CryosphereMassMovement

CryosphereObservation
├── GlacierAreaObservation
├── GlacierTerminusObservation
├── GlacierVelocityObservation
├── GlacierElevationObservation
├── SnowCoverObservation
├── SnowWaterEquivalentObservation
├── LakeAreaObservation
├── LakeLevelObservation
├── LakeVolumeObservation
├── LakeDepthObservation
├── LakeTemperatureObservation
├── MoraineGeometryObservation
├── SurfaceDeformationObservation
└── PermafrostObservation
```

---

# `Glacier`

Represents a persistent glacier identity.

## Core attributes

- CRIC ID;
- canonical name;
- aliases;
- inventory IDs;
- glacier type;
- geometry reference;
- centroid;
- elevation range;
- basin;
- sub-basin;
- country/administrative units;
- parent glacier complex where applicable;
- associated glacial lakes;
- inventory sources.

## Relationships

Possible predicates:

- `located_in`;
- `drains_to`;
- `feeds`;
- `terminates_at`;
- `associated_with`;
- `upstream_of`;
- `contains`;
- `part_of`.

Changing measurements such as area or terminus position belong in Observation nodes.

---

# `GlacierTerminus`

Represents an identifiable glacier terminus feature.

May be useful where terminus identity and movement require explicit graph relationships.

Attributes:

- parent glacier;
- geometry;
- terminus type;
- contact with lake;
- observation references.

---

# Glacier Observation Variables

Recommended controlled variables include:

- area;
- length;
- terminus_position;
- surface_velocity;
- elevation;
- thickness;
- mass_balance;
- debris_cover_fraction;
- snow_cover_fraction;
- surface_temperature;
- albedo;
- crevasse_density where defensibly measurable.

Every observation must state method and uncertainty where available.

---

# `GlacialLake`

Represents persistent lake identity.

## Identity attributes

- canonical name;
- aliases;
- external registry identifiers;
- geometry reference;
- centroid;
- elevation;
- basin;
- sub-basin;
- country;
- administrative region.

## Lake classification

Potential controlled values:

- proglacial;
- supraglacial;
- moraine_dammed;
- ice_dammed;
- bedrock_dammed;
- landslide_dammed;
- composite;
- unclassified;
- unknown.

Classification must permit multiple claims if sources disagree.

## Relationships

- `fed_by`;
- `associated_with`;
- `dammed_by`;
- `located_in`;
- `drains_to`;
- `upstream_of`;
- `downstream_of`;
- `exposed_to`;
- `connected_to`.

---

# Glacial Lake Observations

Possible observation types:

- area;
- perimeter;
- shoreline geometry;
- water level;
- volume;
- mean depth;
- maximum depth;
- surface temperature;
- turbidity proxy;
- expansion rate;
- shoreline displacement;
- lake-glacier contact;
- outlet position.

Observed and estimated values must remain distinguishable.

---

# Lake Volume and Depth

Bathymetric measurements, empirical estimates and modelled estimates are epistemically different.

CRIC must represent:

```text
measured bathymetry
estimated depth
empirical volume estimate
modelled volume
```

as separate methods/statuses.

---

# `Moraine`

Represents a moraine feature.

Potential subtypes:

- lateral;
- medial;
- terminal;
- recessional;
- ground;
- composite;
- unknown.

Attributes may include:

- geometry;
- material description;
- crest elevation;
- width;
- slope;
- vegetation;
- erosion features.

---

# `MoraineDam`

A specialised moraine entity functioning as a lake-retaining structure.

Possible observations:

- crest width;
- freeboard;
- slope;
- seepage;
- erosion;
- outlet geometry;
- breach scars;
- ice core evidence;
- deformation.

---

# `IceDam`

Represents an ice body retaining water.

Must link to:

- lake;
- parent glacier/ice body;
- observations;
- known or suspected failure processes.

---

# Avalanche and Mass-Movement Context

## `AvalanchePath`

Represents a persistent or inferred pathway capable of delivering snow, ice or debris toward an exposed lake or downstream system.

Attributes:

- source area;
- runout geometry;
- slope;
- aspect;
- receiving lake;
- evidence;
- confidence.

## `MassMovementSourceArea`

Represents a slope or source region capable of landslide, rockfall or rock-ice failure.

---

# Permafrost

CRIC should permit representation of:

- permafrost extent;
- ground temperature;
- active-layer thickness;
- degradation observations;
- rock-wall temperature;
- freeze-thaw state.

These may become important for cascading slope instability.

---

# Snow and Ice

Relevant observations include:

- snow-covered area;
- snow-water equivalent;
- melt state;
- snowline elevation;
- ice cover;
- freeze-up;
- break-up.

---

# Cryosphere Processes

Potential process vocabulary:

- accumulation;
- ablation;
- retreat;
- advance;
- calving;
- thinning;
- thickening;
- lake expansion;
- lake drainage;
- snowmelt;
- ice melt;
- permafrost thaw;
- slope destabilisation.

---

# Spatial Relationships

Cryosphere reasoning requires topology.

Important predicates:

- upstream_of;
- downstream_of;
- adjacent_to;
- intersects;
- overlaps;
- within;
- connected_to;
- drains_to;
- feeds;
- terminates_in;
- exposed_to.

Each inferred spatial relationship should record its derivation.

---

# Observation Methods

Recommended method categories:

- optical_remote_sensing;
- SAR;
- LiDAR;
- photogrammetry;
- DEM_analysis;
- field_survey;
- GNSS;
- gauge;
- bathymetry;
- thermal_remote_sensing;
- literature_extraction;
- manual_digitisation;
- model_estimate.

---

# Uncertainty

Cryosphere observations should support:

- positional uncertainty;
- area uncertainty;
- classification confidence;
- temporal uncertainty;
- sensor limitations;
- cloud/snow confusion;
- shadow;
- SAR interpretation limitations;
- DEM error.

---

# Cryosphere StateSnapshot

A Cryosphere StateSnapshot may include:

- lake state;
- glacier state;
- snow state;
- moraine/dam state;
- slope/mass-movement state;
- meteorological context;
- hydrological context;
- upstream hazards;
- downstream exposure.

---

# Cross-Domain Extension

The ontology must support later links to:

- hydrology;
- meteorology;
- geology;
- seismicity;
- infrastructure;
- population;
- ecology;
- governance.

These should use CRIC Core relationships rather than duplicating domain concepts.

---

# v0.1 Acceptance Criteria

- Glacier and GlacialLake schemas exist;
- observation subtypes exist;
- lake-glacier relationships validate;
- moraine and dam concepts are distinct;
- observed and estimated volume/depth are distinguishable;
- avalanche/mass-movement exposure can be represented;
- StateSnapshots can link cryosphere context;
- example nodes validate against Pydantic schemas.
