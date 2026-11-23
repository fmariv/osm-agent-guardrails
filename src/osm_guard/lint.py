"""Simple advisory static scan for *obvious* OSM/Overpass anti-patterns.

Not a QL parser, a compliance scanner, or a safe-query guarantee.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    line: int
    message: str


def scan_text(text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    joined = text.lower()
    for index, line in enumerate(lines, start=1):
        lower = line.lower()
        if re.search(r"(?:api\.overpass-api\.de|overpass-api\.de|overpass\.kumi\.systems|overpass\.private\.coffee)/api/interpreter", lower):
            findings.append(Finding(
                "PUBLIC_OVERPASS_URL", "warning", index,
                "Public Overpass URL found; review necessity, caching and the operator's current policy.",
            ))
        if re.search(r"(?:node|way|relation|nwr)\s*;\s*out\b", lower):
            findings.append(Finding(
                "UNBOUNDED_QL_CANDIDATE", "warning", index,
                "Possibly unbounded Overpass QL. Add selective tags/area or use local extracts.",
            ))
        if re.search(r"tile\.openstreetmap\.org", lower):
            findings.append(Finding(
                "OSMF_TILE_HOST", "info", index,
                "OSMF tile host found; review attribution, user agent, caching and no bulk-prefetch.",
            ))
    if re.search(r"(?:moveend|zoomend|onmove|onzoom)", joined) and re.search(r"overpass", joined):
        findings.append(Finding(
            "MAP_EVENT_OVERPASS", "warning", 1,
            "Map movement and Overpass mentioned together: verify the app does not query public API on each view change.",
        ))
    if re.search(r"while\s+true\s*:", joined) and re.search(r"overpass|api/interpreter", joined):
        findings.append(Finding(
            "OVERPASS_TIGHT_LOOP", "warning", 1,
            "Unbounded loop with Overpass reference: inspect retry logic and request budgets.",
        ))
    return findings
