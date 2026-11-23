---
name: osm-local-extracts
description: Use when extracting, filtering, transforming, or analyzing OSM data repeatedly or at regional scale with local .osm.pbf extracts, PyOsmium, OSMnx, DuckDB, PostGIS, or GeoParquet instead of public Overpass requests.
license: MIT
---

# Build local-first OSM data pipelines

Local extracts are often the right choice for broad geographic coverage, repeatable analytics and production workloads.

## Workflow

1. Choose an extract provider and verify its download/update policies, provenance, region coverage and timestamp. Record snapshot date and licence attribution.
2. Download **once** to local/object storage and validate checksums where provided. Don't fetch a national PBF on every CI run.
3. Use PyOsmium to stream/filter large PBF files without loading all elements into memory. Extract only the tags/geometries needed.
4. For street networks, consider OSMnx >=2.2.0 local PBF graph loading; verify version-specific calls against installed documentation.
5. Store transformed data locally in GeoParquet or PostGIS, with appropriate spatial indexing for queries; distinguish full datasets from filtered outputs.
6. For freshness, plan periodic extract refreshes or replication diffs with a documented checkpoint/recovery policy. Applying diffs correctly can be nontrivial.
7. Test against **small local fixtures**, not public data endpoints.

## Example

Use `examples/python/pbf_pois_to_geojson.py` for a runnable optional-PyOsmium node-POI extraction. It intentionally handles **tagged nodes only**, not POIs mapped as ways or relations. Never describe it as a complete OSM POI inventory.

## Pitfalls

- POIs can be mapped as nodes, ways or relations. Node-only extraction is partial.
- OSM object ids and updates need stable handling across diffs.
- Clipping geometries to an AOI may require topology repair.
- Different projections and missing metadata can alter downstream interpretation.
- Local processing does not exempt projects from ODbL obligations.

See [local processing considerations](references/processing.md) and `osm-source-selection`.
