"""Tiny, offline-only example reader for amenity-tagged OSM XML nodes.

NOT a general-purpose OSM importer: ways and relations are not processed.
For real production extracts, use a streaming PBF pipeline and indexed storage.
"""
from pathlib import Path
import xml.etree.ElementTree as ET


def amenity_nodes(path: Path) -> dict:
    """Convert a local OSM XML fixture to point GeoJSON. Makes no network calls."""
    features: list[dict] = []
    for _, element in ET.iterparse(path, events=("end",)):
        if element.tag != "node":
            continue
        tags = {tag.get("k"): tag.get("v") for tag in element.findall("tag")}
        if "amenity" in tags:
            features.append({
                "type": "Feature",
                "id": int(element.attrib["id"]),
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(element.attrib["lon"]), float(element.attrib["lat"])],
                },
                "properties": tags,
            })
        element.clear()
    return {"type": "FeatureCollection", "features": features}
