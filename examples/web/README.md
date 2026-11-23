# Web map architecture without public Overpass as a backend

Recommended high-level pattern for a Svelte/MapLibre application:

```text
OSM PBF extract  --->  local transform  --->  GeoParquet/PostGIS
                                              |
                                              v
                                      your API/vector tiles
                                              |
                                              v
                           Svelte + MapLibre + policy-compatible basemap
```

`src/lib/pois.ts` below illustrates the basic anti-pattern avoidance, fetching from **your own** application endpoint and retaining a cached promise rather than calling Overpass on every map event:

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
        cachedPois = undefined;  // allow explicit future retry, not a retry loop
        throw err;
      });
  }
  return cachedPois;
}
```

This is a **pattern** rather than a full runnable Svelte app; the backend and basemap provider must be selected for the actual audience and scale. Do not serve unbounded region-wide GeoJSON to all browser users. For large datasets use appropriate vector tiles or bounded indexed queries. Always display correct OSM and provider attribution and obey tile caching/usage policies.
