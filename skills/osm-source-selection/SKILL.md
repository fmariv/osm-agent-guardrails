---
name: osm-source-selection
description: Use when choosing how an application, script, AI agent, or data pipeline should obtain OpenStreetMap data, especially to decide between local PBF extracts, Overpass, tiles, and databases and to avoid unnecessary public API traffic.
license: MIT
---

# Select an OSM data source before coding

Use the following procedure whenever the request involves OpenStreetMap data. Do not automatically recommend Overpass merely because it is convenient.

## Intake

Establish these requirements or explicitly state assumptions:

- Scope: one POI, local bounding box, city, region, country, or planet; expected number of features.
- Workload: one-off exploration, scheduled pipeline, public interactive web app, background analytics, or bulk ingestion.
- Freshness: minutes, hourly, daily, weekly, historical snapshot.
- Concurrency and deployment: local prototype, many users, production, commercial workload.
- Data shape: vector features, network graph, rendered map, change stream.
- Legal/operational constraints: attribution, ODbL obligations, hosting budget, provider policies.

## Decision procedure

1. **Map display only?** Choose a map tile provider with a compatible published policy, attribution, usage level and caching. Do not use Overpass to draw basemaps.
2. **Country/region/bulk/scheduled?** Prefer downloadable `.osm.pbf` extracts, incremental updates, and a local store (GeoParquet, PostGIS, or application DB). Query your own data store, not public Overpass on every run.
3. **Local street graph and repeatable analysis?** Consider OSMnx local PBF support (OSMnx 2.2.0+), or direct PyOsmium followed by local graph processing.
4. **Small ad hoc query with bounded output and low frequency?** A public Overpass instance may be reasonable if its **current** usage policy permits it. Follow `overpass-query-safety` and `overpass-client-design`.
5. **High-volume, public application or strict SLA?** Use a contracted provider, a self-hosted service, or a locally maintained data pipeline. Do not shift load from one public Overpass instance to another.
6. **Need changes/diffs?** Look into replication streams and appropriate tooling rather than repeated full downloads or repeated expensive queries.

## Response format

State: recommended source, rejected options and reasons, freshness mechanism, likely resource burden, cache/updates, correct attribution/licensing, and a fallback if the selected service is unavailable.

If undecided, explicitly rank two alternatives. Do not present assumptions as official Overpass quotas; those may change by instance and over time. For operational details read [decision guide](references/decision-matrix.md) and the official [Overpass API wiki](https://wiki.openstreetmap.org/wiki/Overpass_API).
