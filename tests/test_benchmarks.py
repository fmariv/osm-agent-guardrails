"""Deterministic scenario tests: NOT empirical agent-comparison benchmarks."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("offline_evaluator", ROOT / "tools/evaluate_offline.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class BenchmarkFixturesTest(unittest.TestCase):
    def test_fixture_suite(self):
        result = MODULE.evaluate(ROOT / "benchmarks/scenarios.json")
        self.assertGreaterEqual(result["total"], 15)
        self.assertEqual(result["total"], result["passed"], [r for r in result["cases"] if not r["passed"]])

    def test_report_does_not_claim_real_impact(self):
        result = MODULE.evaluate(ROOT / "benchmarks/scenarios.json")
        self.assertEqual(result["kind"], "deterministic-offline-fixture-check")
        self.assertIn("do not compare agents", result["disclaimer"])


if __name__ == "__main__":
    unittest.main()
