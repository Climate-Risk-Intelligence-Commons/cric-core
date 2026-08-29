# CRIC Data Commons Architecture

## Purpose

The CRIC Data Commons provides a reproducible, provenance-aware registry and access architecture for raw, normalised, derived and training data used by the Climate Risk Intelligence Commons.

The Data Commons is not synonymous with storing all bytes in Git.

Its primary responsibility is to make datasets discoverable, versioned, attributable, reproducible and machine-addressable.

---

# Data Classes

CRIC should distinguish:

```text
Source Data
Acquired Data
Normalised Data
Derived Data
Feature Data
Training Data
Benchmark Data
Simulation Data
Reference Data
```

---

# Data Object Hierarchy

```text
Dataset
└── DatasetVersion
    ├── DataAsset
    ├── DataAsset
    └── Manifest
```

A Dataset is persistent identity.

A DatasetVersion is immutable.

---

# Storage Tiers

## Tier 1: Git

Appropriate for:

- metadata;
- manifests;
- schemas;
- small examples;
- test fixtures;
- small GeoJSON;
- controlled vocabularies.

## Tier 2: Local/Object Storage

Appropriate for:

- satellite imagery;
- DEMs;
- COGs;
- large GeoParquet;
- hydrodynamic outputs;
- training tensors;
- model weights.

## Tier 3: External Provider

Where licence or size makes copying inappropriate, CRIC may retain only:

- source URI;
- provider identifier;
- retrieval recipe;
- checksum if acquired;
- metadata.

---

# Data Registry

`cric-data` should publish a machine-readable registry.

Example:

```yaml
dataset_id:
name:
provider:
description:
domain:
spatial_coverage:
temporal_coverage:
update_frequency:
licence:
access_method:
versions: []
```

---

# Dataset Version

Required:

- version ID;
- parent dataset;
- release/acquisition time;
- manifest;
- schema;
- licence;
- source version;
- spatial extent;
- temporal extent;
- asset list;
- quality status.

---

# STAC

Earth-observation assets should use STAC where practical.

CRIC should not duplicate STAC concepts unnecessarily.

CRIC OKF nodes may reference STAC Items, Collections and Assets while adding CRIC-specific provenance, scientific relationships and knowledge lifecycle.

---

# Cloud-Optimised GeoTIFF

COG is preferred for large raster access where suitable.

---

# GeoParquet

GeoParquet is preferred for portable analytical vector/tabular geospatial data where appropriate.

---

# Raw Data Immutability

Acquired raw assets should be treated as immutable.

Reprocessing creates new derived assets.

---

# Normalisation

Normalisation may include:

- CRS transformation;
- unit conversion;
- schema harmonisation;
- timestamp normalisation;
- nodata standardisation;
- geometry repair.

Every scientifically material normalisation must retain lineage.

---

# Derived Data

Examples:

- lake polygons;
- lake-area time series;
- glacier termini;
- slope;
- flow path;
- rainfall accumulation;
- exposure summaries.

Derived datasets must record:

- source versions;
- code version;
- parameters;
- execution environment.

---

# Data Partitions

Large collections may partition by:

- domain;
- geography;
- basin;
- year;
- sensor;
- variable;
- processing level.

Partitioning must not alter canonical identity.

---

# Cache Versus Canonical Data

Caches are disposable.

Canonical data versions are immutable and manifested.

Agents must know whether a resource is:

- canonical;
- derived;
- cached;
- temporary.

---

# Data Discovery

Users and agents should search by:

- variable;
- geography;
- time;
- provider;
- sensor;
- licence;
- domain;
- processing level;
- quality;
- update frequency.

---

# Data Quality Metadata

Each DatasetVersion should support:

- completeness;
- spatial resolution;
- temporal resolution;
- positional accuracy;
- missingness;
- known biases;
- processing limitations;
- validation status.

---

# Data Access Abstraction

Applications should request data through logical dataset identifiers rather than hard-coded local paths.

Runtime dependency injection may resolve a logical asset to:

- local disk;
- object store;
- remote provider;
- institutional service.

---

# Offline Use

CRIC should support partial offline deployment.

A user should be able to materialise a selected geographic/data package containing:

- OKF nodes;
- manifests;
- selected assets;
- indexes;
- required models.

---

# Sovereign Deployment

The architecture should permit organisations to host:

- private data;
- controlled infrastructure layers;
- local model weights;
- local agent runtimes

without modifying public CRIC schemas.

---

# Training Data

Training datasets must be separately versioned.

They should record:

- sample IDs;
- label IDs;
- feature versions;
- split definitions;
- exclusion rules;
- leakage controls;
- provenance.

---

# v0.1 Acceptance Criteria

- data registry exists;
- Dataset and DatasetVersion are distinct;
- large assets are referenced rather than committed;
- manifests include hashes;
- STAC references are supported;
- one offline sample package can be materialised;
- derived data identifies source versions;
- training datasets are independently versioned.
