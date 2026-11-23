# Overpass QL anti-patterns

- `node;out;` with no filter or bounds: unbounded. Change to a selective tag and area, or use PBF.
- Query on every map `moveend`/`zoomend`: live traffic multiplies with users. Serve precomputed/hosted data layers; for genuinely interactive search add explicit user action, debouncing and caching, subject to operator policy.
- `out geom` for large collections where only ids and tags are needed: avoid large responses; use `out tags` where suitable.
- Looping on `429`/`406`: back off at least 30 seconds according to published wiki guidance, and reconsider whether the use case fits the instance. Do not add retries that automatically hammer the instance.
- Rotating endpoints to escape limits: not acceptable. Alternative providers need their own policy and consent, not an evasive failover chain.
- Tight-looping Overpass to maintain local snapshots: use PBF plus diffs.

Caveat: Overpass QL is expressive. A lightweight regex-based analyzer is only a *warning* tool and cannot prove cost, safety or correctness; manual review is required.
