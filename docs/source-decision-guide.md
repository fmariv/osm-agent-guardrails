# Picking the right OSM source

## Four questions before starting

1. How large is the geographic scope and how many elements are expected?
2. How frequently will the result be regenerated, and for how many users?
3. How fresh does the result need to be?
4. What are the guarantees, uptime, and licence/attribution obligations?

## Architecture recommendations

- **Small ad hoc low-frequency search**: Overpass may be reasonable, with bounded query, client identification and caching, subject to selected instance's policies.
- **Scheduled/countrywide/high-volume extraction**: local PBF and transforms; keep the data instead of repeatedly extracting it.
- **Persistent application data**: PostGIS/GeoParquet; use incremental ingestion and spatial indices.
- **Web map backdrop**: tiles from a provider whose policy fits the workload; public Overpass isn't a tile service.
- **Network analysis**: offline PBF with OSMnx 2.2.0+ or dedicated graph processing.
- **Near-real-time OSM edits**: replication/update pipeline or dedicated provider; ensure update correctness.

Do not treat the source selector in `osm_guard` as universal policy. It is an example of transparent conservative heuristics: people and agents must review real operator constraints.
