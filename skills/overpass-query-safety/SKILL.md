---
name: overpass-query-safety
description: Use when writing, reviewing, optimizing, or debugging Overpass QL queries for OpenStreetMap features and when controlling query bounds, data volume, output, and server resource usage.
license: MIT
---

# Write resource-conscious Overpass queries

## First: verify Overpass is the right source

Read `osm-source-selection` if the task involves repeated, production, bulk, or country-scale extraction. Prefer local PBF data for such tasks. For occasional bounded queries, follow this process.

## Query construction

- Start from the **smallest useful geography**, with explicit bounding box where possible. Never generate whole-world extraction unless a dedicated appropriately provisioned operator has agreed.
- Use **selective OSM tags**, `nwr` only when the node/way/relation mix is required, and `out center` when centres suffice for objects with geometry.
- Use `out tags;` for tag information without unnecessary geometry; request `out geom;` only if complete geometry is required.
- Set reasonable `[timeout:...]` and `[maxsize:...]` for the expected workload; they are safety caps, not permissions to consume resources.
- Do not automatically repeat expensive queries after errors. A 504 may represent too much work; narrow the query, redesign it, or switch data sources.
- Do not split a large job into thousands of near-identical public calls to evade resource limits.
- Avoid Nominatim/Overpass misuse: geocoding (addresses/place names) and data queries are distinct workloads, governed by different service policies.

## Example: bounded tag query

```ql
[out:json][timeout:25];
(
  node["amenity"="drinking_water"](41.38,2.14,41.41,2.19);
  way["amenity"="drinking_water"](41.38,2.14,41.41,2.19);
);
out center;
```

This is **syntax illustration only**. Do not run it during CI or by default when testing generated code. The example is not a guaranteed safe request volume. The correct output mode depends on the downstream task.

## Review checklist

1. Does a public API request need to occur at all?
2. Is this one-off and small? Are geography and tags sufficiently selective?
3. Are geometry, metadata and recursive expansion strictly necessary?
4. Will consumers cache by query and freshness window?
5. What does the client do when receiving 429, 406 or 504?
6. Does the app identify itself and abide by the instance's current policy?

Refer to [query anti-patterns](references/anti-patterns.md). If local processing is more suitable, use `osm-local-extracts`.
