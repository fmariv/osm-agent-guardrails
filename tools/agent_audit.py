#!/usr/bin/env python3
"""Small offline heuristic scanner for potentially abusive OSM client code.

A finding is a review prompt, *not* proof that a program makes harmful requests.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    line: int
    message: str


PATTERNS = [
    ("hardcoded-overpass", "warning", re.compile(r"https?://(?:overpass-api\.de|overpass\.kumi\.systems|overpass\.nchc\.org\.tw)/", re.I), "Public Overpass host hard-coded: require policy review, configuration, caching and ownership."),
    ("web-map-event", "warning", re.compile(r"\b(?:moveend|zoomend|mousemove|onMove|onZoom|setInterval)\b", re.I), "Map/timer event detected: check that it does not trigger Overpass calls per interaction."),
    ("overpass-call", "info", re.compile(r"(?:overpass|/api/interpreter|overpassql)", re.I), "Overpass reference detected: review bounds, query cost, caching and service policy."),
    ("unbounded-query", "warning", re.compile(r"\b(?:node|way|relation|nwr)\s*\[.+?\]\s*;", re.I), "Possible unbounded Overpass QL selector: confirm an area or bbox restriction."),
    ("retry-loop", "warning", re.compile(r"\bwhile\s+True\b|\bwhile\s*\(\s*true\s*\)", re.I), "Potential endless loop: inspect retry/backpressure and exit conditions."),
]


def scan(content: str) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(content.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith(("#", "//")):
            continue
        for rule, severity, pattern, message in PATTERNS:
            if pattern.search(line):
                findings.append(Finding(rule=rule, severity=severity, line=number, message=message))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args()
    findings = scan(args.file.read_text(encoding="utf-8"))
    if args.format == "json":
        print(json.dumps({"file": str(args.file), "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        if not findings:
            print("No heuristic findings (not a safety guarantee).")
        for finding in findings:
            print(f"{args.file}:{finding.line}: {finding.severity.upper()} {finding.rule}: {finding.message}")
    return int(args.fail_on_warning and any(f.severity == "warning" for f in findings))


if __name__ == "__main__":
    raise SystemExit(main())
