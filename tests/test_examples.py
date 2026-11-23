"""End-to-end smoke tests for the deliberately offline examples."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


class OfflineExamplesTest(unittest.TestCase):
    def test_xml_example_returns_synthetic_pois(self):
        script = ROOT / "examples/python/local_xml_pois_to_geojson.py"
        spec = importlib.util.spec_from_file_location("local_example", script)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        data = module.convert(ROOT / "fixtures/tiny-synthetic.osm")
        features = data["features"]
        self.assertEqual(len(features), 2)
        self.assertEqual([f["id"] for f in features], [101, 103])
        self.assertTrue(all(f["geometry"]["type"] == "Point" for f in features))

    def test_example_script_prints_valid_geojson(self):
        import json
        result = subprocess.run(
            [sys.executable, str(ROOT / "examples/python/local_xml_pois_to_geojson.py")],
            capture_output=True, text=True, check=True, timeout=10,
        )
        self.assertEqual(json.loads(result.stdout)["type"], "FeatureCollection")

    def test_bad_example_is_flagged_by_linter(self):
        from osm_guard.lint import scan_text
        data = (ROOT / "examples/python/unsafe_example.py").read_text(encoding="utf-8")
        findings = {f.rule for f in scan_text(data)}
        self.assertIn("PUBLIC_OVERPASS_URL", findings)
        self.assertIn("UNBOUNDED_QL_CANDIDATE", findings)
        self.assertIn("OVERPASS_TIGHT_LOOP", findings)

    def test_example_programs_contain_no_live_public_network_calls(self):
        for path in (ROOT / "examples/python").glob("*.py"):
            if path.name == "unsafe_example.py":
                continue  # documented static lint fixture; never executed
            source = path.read_text(encoding="utf-8")
            for forbidden in ("urlopen(", "requests.get(", "requests.post(", "api/interpreter"):
                with self.subTest(path=path, forbidden=forbidden):
                    self.assertNotIn(forbidden, source)
