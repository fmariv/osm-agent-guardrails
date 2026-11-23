#!/usr/bin/env python3
"""Run deterministic, local guardrail checks against synthetic scenarios.

This does NOT invoke an LLM or public OSM services. Do not interpret these
pass counts as measured reductions of real Overpass traffic.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from osm_guard.lint import scan_text
from osm_guard.sources import Workload, recommend

ROOT = Path(__file__).resolve().parents[1]


def evaluate(path: Path) -> dict:
    cases = json.loads(path.read_text(encoding="utf-8"))
    outcomes: list[dict] = []
    for case in cases["source_cases"]:
        actual = recommend(Workload(**case["workload"])).source.value
        outcomes.append({"id": case["id"], "category": "source", "passed": actual == case["expected"], "actual": actual, "expected": case["expected"]})
    for case in cases["lint_cases"]:
        actual = sorted({f.rule for f in scan_text(case["snippet"])})
        expected = sorted(case["expected_rules"])
        outcomes.append({"id": case["id"], "category": "lint", "passed": actual == expected, "actual": actual, "expected": expected})
    return {
        "kind": "deterministic-offline-fixture-check",
        "disclaimer": "These checks do not compare agents, prove compliance, or quantify real Overpass traffic savings.",
        "passed": sum(int(o["passed"]) for o in outcomes),
        "total": len(outcomes),
        "cases": outcomes,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "benchmarks/scenarios.json")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON instead of a short summary")
    args = parser.parse_args(argv)
    result = evaluate(args.cases)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Offline scenario checks: {result['passed']}/{result['total']} passed")
        for c in result["cases"]:
            if not c["passed"]:
                print(f"FAIL {c['id']}: expected={c['expected']!r}; actual={c['actual']!r}")
        print(result["disclaimer"])
    return 0 if result["passed"] == result["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
