# Data provenance, freshness and geometry

## Provenance fields to keep

For every downloaded extract or cached result, record at least:

- Download/source URL, provider, attribution statement and any usage policy link
- Geographic region and clipping method
- Extract/snapshot timestamp and download timestamp (not necessarily the same)
- Filter predicates / query string and code version
- Completeness limits (e.g., node-only, incomplete clipped ways)
- Expected refresh and failure/rollback behavior

## Important geometry distinction

OSM has **nodes, ways, relations**. Many amenities are nodes, but a node-only extractor is *not* a complete POI extractor; building polygons generally need ways and possibly multipolygon relations. Way geometry requires resolving node locations; relations can require more complex assembly and incomplete clip handling. Be explicit in every schema and example.

## Local data options

- Regional PBF extracts, for example from Geofabrik, reduce load on public query services. Verify provider policies.
- PyOsmium streams raw OSM entities and can access history/change files; it is not a built-in polygonization engine.
- OSMnx can support graph workflows from local data in supported versions. Check the exact library version and API.
- GeoParquet / PostGIS / DuckDB are useful output/query stores **after** a suitable ETL step; they are not a source for the complete OSM model by themselves.

## Keeping data current

Use a snapshot+replication design if refresh needs are frequent; add replication sequence tracking, idempotent updates, recovery from missed sequences, feature deletions, metadata timestamps and tests. Re-running a large public Overpass query on every refresh tick is not equivalent to a replication pipeline.
