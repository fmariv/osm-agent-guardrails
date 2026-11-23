# Web map checklist

- [ ] No HTTP call to public Overpass on pan/zoom/keypress/rerender
- [ ] Avoid public Overpass as a production multi-user backend
- [ ] Basemap provider and tile policy explicitly documented
- [ ] No bulk tile prefetch, cache-bypass headers, or false identity
- [ ] Visible OSM and any provider attribution
- [ ] ODbL obligations reviewed for downstream OSM-derived data
- [ ] Network errors do not cascade into retry loops
- [ ] Test with a local GeoJSON fixture, not public APIs
