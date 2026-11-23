"""Offline example: extract tagged point POIs from *synthetic* local OSM XML.

This is not complete POI extraction: ways and relations are deliberately ignored.
"""

from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET


def convert(path: Path) -> dict:
    features = []
    for event, element in ET.iterparse(path, events=("end",)):
        if element.tag != "node":
            continue
        tags = {tag.get("k"): tag.get("v") for tag in element.findall("tag")}
        if "amenity" in tags:
            features.append({
                "type": "Feature",
                "id": int(element.attrib["id"]),
                "geometry": {"type": "Point", "coordinates": [float(element.attrib["lon"]), float(element.attrib["lat"])]},
                "properties": tags,
            })
        element.clear()
    return {"type": "FeatureCollection", "features": features}


if __name__ == "__main__":
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "fixtures/tiny-synthetic.osm"
    print(json.dumps(convert(input_path), indent=2))
