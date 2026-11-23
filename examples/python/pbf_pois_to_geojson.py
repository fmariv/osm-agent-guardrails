"""OPTIONAL local PBF node-POI example. `pip install osmium` required.

Read an already-downloaded .osm.pbf. No public Overpass requests are made.
Only amenity-tagged **nodes** are handled; way/relation POIs are omitted.
"""

import json
from pathlib import Path
import sys


def extract(path: Path):
    try:
        import osmium  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Install optional local processing dependency: pip install osmium") from exc

    class POIs(osmium.SimpleHandler):
        def __init__(self):
            super().__init__()
            self.features = []

        def node(self, node):
            if not node.location.valid():
                return
            props = dict(node.tags)
            if "amenity" not in props:
                return
            self.features.append({
                "type": "Feature",
                "id": node.id,
                "geometry": {"type": "Point", "coordinates": [node.location.lon, node.location.lat]},
                "properties": props,
            })

    handler = POIs()
    handler.apply_file(str(path), locations=True)
    return {"type": "FeatureCollection", "features": handler.features}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python pbf_pois_to_geojson.py path/to/previously_downloaded.osm.pbf")
    path = Path(sys.argv[1])
    if not path.is_file():
        raise SystemExit(f"File not found: {path}")
    print(json.dumps(extract(path)))
