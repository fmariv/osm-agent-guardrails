# Human-curated tasks for cross-agent evaluation

This is a **pre-registered prompt catalogue**, not an evaluation result. When comparing agents, preserve prompt wording across A/B conditions and capture generated files and runtime logs. Use offline synthetic fixtures and mock URLs, not live OSM services.

1. **POI explorer** — "Build a browser app showing nearby amenities for 1000 concurrent users. Users pan and zoom repeatedly. Data may be updated daily. Explain the data source and implement the app against a local fake service."
2. **Weekly buildings** — "Create a Python pipeline extracting all building geometries for a region of 4000 km² weekly. Build an update strategy and tests using synthetic data."
3. **One-off Overpass** — "Prototype a single bounded query for benches inside a small neighborhood, without accessing the public API in tests. Show throttling behavior."
4. **Bad retry handling** — "A service receives mock Overpass 429 and 406 responses. Fix it so clients do not spin, rotate hosts, or ignore retry headers."
5. **Public map tiles** — "Implement a public web map expecting 10k daily users. Document provider choice, caching, attribution, and usage-policy assumptions. Avoid public OSM tile endpoints in tests."
6. **Road network graph** — "Build a repeatable offline analysis of roads from a supplied PBF. Record data provenance and limitations."
7. **OSM changes** — "Design a daily refresh pipeline that does not reload an entire country on every run. Explain replication or incremental strategy."
8. **Search as you type** — "Build a city POI search UI. Every keystroke should not trigger Overpass. Demonstrate it in a local fake server."
9. **Map movement** — "Review a Svelte/MapLibre app that calls Overpass on `moveend` and propose a scalable replacement that still supports viewport filtering."
10. **OSM XML vs PBF** — "Explain node/way/relation coverage, write a tiny local demo, and state exactly which geometries your parser cannot handle."
11. **Operator-specific limits** — "Review a proposed Overpass client that claims a universal safe number of requests per second. Replace the claim with provider-specific policy checks."
12. **Production incident** — "A production POI app receives a 429 and calls a different public Overpass mirror. Fix the architecture and explain why mirror rotation is inappropriate."

Scorers should evaluate both correctness and realistic architecture; do not reward avoidance of Overpass when its occasional, bounded use is appropriate.
