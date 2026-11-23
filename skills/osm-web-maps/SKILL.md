---
name: osm-web-maps
description: Use when building interactive web maps that display OSM basemaps or OSM-derived POIs, roads, and buildings in Svelte, Leaflet, MapLibre or other browsers, especially to avoid public Overpass calls on map interactions and comply with tile usage policies.
license: MIT
---

# Build map frontends that respect OSM infrastructure

## Architecture first

Distinguish **basemap tiles**, **feature/data APIs**, **geocoding**, and **your application data**. They have separate endpoints and policies. Overpass is not a basemap tile server or a scalable replacement for an application database.

For a multi-user application:

1. Preprocess or ingest OSM-derived data using extracts or a provisioned provider.
2. Serve the map's thematic layers from a local datastore/API or vector tiles.
3. Use an appropriate basemap source with capacity and licensing for expected traffic.
4. Handle search and filtering locally/server-side. Do not query public Overpass on every pan, zoom, hover, component rerender, or route request.
5. Offer data freshness information, visible attribution and provider-correct cache behavior.

## Specific warnings for `tile.openstreetmap.org`

The OSMF Tile Usage Policy requires visible attribution, valid identity/referrer and honoring cache headers; it prohibits bulk downloads/prefetch and cache-bypass tricks. Do not turn OSMF tiles into an unbounded production tile backend; choose a policy-compatible provider or self-host when necessary. Tile rules differ by provider.

## Svelte/MapLibre project pattern

- Load a local `pois.geojson` or application endpoint once and reuse it for filters.
- React to map view changes by filtering rendered features / requesting your own bounded server endpoint, not Overpass.
- Choose the basemap through application configuration; do not hardcode a public OSM tile URL into reusable examples.
- Display data and basemap attribution in UI; preserve ODbL notices when required.

See [frontend checklist](references/web-checklist.md) and the [OSMF tile policy](https://operations.osmfoundation.org/policies/tiles/).
