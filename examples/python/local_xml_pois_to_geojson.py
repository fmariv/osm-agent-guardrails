"""Offline sample: turn synthetic local OSM XML amenity nodes into GeoJSON.

Only amenity-tagged nodes are considered; ways and relations are omitted.
"""
from pathlib import Path
import json
import sys

from osm_guard.local_data import amenity_nodes


def convert(path: Path) -> dict:
    return amenity_nodes(path)


if __name__ == "__main__":
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "fixtures/tiny-synthetic.osm"
    print(json.dumps(convert(input_path), indent=2))
