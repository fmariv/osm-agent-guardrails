# Responsible OpenStreetMap development

When implementing any feature involving OpenStreetMap, Overpass API, tiles, POIs, roads, buildings or OSM extracts:

1. Explain the geographic extent, intended audience, query frequency, expected data freshness and whether this is production usage.
2. Choose the data source before writing fetch code. For scheduled, high-volume or production tasks, prefer local PBF/GeoParquet/PostGIS or an appropriately provisioned service over public Overpass.
3. Do not call public Overpass on page render, pan, zoom, keystroke, or per-user request. Never bulk scrape it, run automatic endpoint rotation, or circumvent quotas.
4. For legitimate small occasional Overpass queries, bound the geography and output, identify the client, cache results, serialize access and respect server usage rules. On 429/406, stop and wait at least 30 seconds; do not retry in a loop.
5. For OSM map tiles, obey the provider's published tile policy, use visible OSM attribution and do not bulk-prefetch from `tile.openstreetmap.org`.
6. Prefer local fixtures, mocks and self-hosted infrastructure for tests. Do not run performance or load tests against public OSM services.
7. Identify applicable ODbL obligations for derived datasets and attribution requirements for maps.
8. Explain the chosen architecture and expected burden on public infrastructure before proposing deployment.

For detailed instructions, install the `osm-agent-skills` collection or consult its `skills/` directory. Official documentation and service policies override these general rules.
