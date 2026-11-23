# Local data implementation notes

## Common patterns

- **Node POIs**: stream PBF with PyOsmium `SimpleHandler.node`, filter tags and check `node.location.valid()`. This is only a node subset; buildings and roads are typically ways, and multipolygons can be relations.
- **Road graph**: OSMnx 2.2.0 added local PBF graph construction. Check library docs and use relevant travel/network presets.
- **Analytics**: save normalized geospatial outputs in GeoParquet and query with spatial libraries or DuckDB spatial support. GeoParquet is a storage format, not a live OSM data API.
- **Production updates**: ingest diffs or refresh extracts with checkpointing, atomic swaps and monitoring for delayed data.

## Operational checklist

1. Record source URL, data date and licence.
2. Record extract size, output feature counts and transform version.
3. Add idempotent reprocessing and partial-failure recovery.
4. Avoid converting OSM ways/relations with naive node-only logic.
5. Cache locally and test offline.
