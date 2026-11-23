# Runnable offline POI web app

An executable vertical slice: **local synthetic OSM XML** → **Python standard-library API** → **browser-based SVG POI viewer**. It does not require Docker, external JS/CDN packages, a basemap, or any Overpass requests.

```bash
python -m pip install -e .
python examples/offline-poi-app/server.py --port 8765
# Open http://127.0.0.1:8765
```

The API supports `/api/pois` with `ETag`, `If-None-Match`, HTTP 304 and a 60-second cache TTL, plus `/health`. The app fetches a single collection once, then filters locally as the user types. The test suite starts a **localhost-only** test server and checks cache behavior, routes and payloads. Neither CI nor the example connects to public OSM servers.

**Limits:** deliberately synthetic, tiny and node-only; simplistic coordinate projection; default bind to loopback; no authentication, persistence, geo-index, database, clustering, vector tiles, real map projection or hardened server operations. For a real production web map, transform PBF to an indexed store and serve bounded API results or vector tiles, with an appropriate licensed basemap and proper OSM attribution. Do not copy this toy app unchanged into production.
