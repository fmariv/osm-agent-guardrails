# Web maps without public Overpass as a production backend

Recommended production direction for a Svelte/MapLibre application:

```text
OSM PBF extract  --->  incremental local transform  --->  GeoParquet/PostGIS
                                                       |
                                                       v
                                             your indexed API/vector tiles
                                                       |
                                                       v
                              Svelte + MapLibre + provider-compliant basemap
```

For a **runnable, standard-library, offline teaching example**, see [`../offline-poi-app/`](../offline-poi-app/). It uses a synthetic OSM XML fixture and a local HTTP API with ETag caching. The UI loads POIs once and filters without making additional calls. It deliberately uses SVG, **not** a map basemap or real geographic renderer.

A Svelte/MapLibre frontend might use an application-owned bounded endpoint with an in-flight request deduplication pattern:

```ts
export type PoiCollection = GeoJSON.FeatureCollection;
let cachedPois: Promise<PoiCollection> | undefined;

export function loadPois(): Promise<PoiCollection> {
  if (!cachedPois) {
    cachedPois = fetch('/api/pois', { headers: { Accept: 'application/geo+json' } })
      .then(r => {
        if (!r.ok) throw new Error(`POI API status ${r.status}`);
        return r.json() as Promise<PoiCollection>;
      }).catch(err => {
        cachedPois = undefined;  // allow future explicit retry, no automatic loop
        throw err;
      });
  }
  return cachedPois;
}
```

This deduplicates calls within one application session, **not** across users or deployment replicas. A real production service needs indexed spatial queries, server-side caching, freshness/invalidation, request limits, and appropriate vector tile services. Do not serve unbounded city-wide GeoJSON repeatedly to a large user base. Display OSM attribution where required and honor the selected tile provider's terms.
