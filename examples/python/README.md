# Python examples (offline)

Test a tiny synthetic XML fixture with the standard library only:

```bash
python examples/python/local_xml_pois_to_geojson.py > /tmp/tiny-pois.geojson
```

To process an **already-downloaded** PBF of manageable scope:

```bash
python -m pip install osmium
python examples/python/pbf_pois_to_geojson.py /path/to/region.osm.pbf > region-node-amenities.geojson
```

The PBF demonstration handles amenity-tagged **nodes only**. It does not reconstruct way or relation geometry, cannot be used as an exhaustive POI extractor, and accumulates results in memory: avoid using it unchanged with huge regional extracts. For production ingestion, stream to an indexed datastore or files in chunks and handle ways/relations correctly.

Use `osm-guard lint examples/python/unsafe_example.py` to demonstrate actionable warnings without making network requests.

The XML sample is synthetic and is not copied from OpenStreetMap. For real OSM-derived datasets, include OSM attribution and assess ODbL obligations.
