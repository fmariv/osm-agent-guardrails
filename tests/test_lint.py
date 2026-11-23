import unittest

from osm_guard.lint import scan_text


class TestLint(unittest.TestCase):
    def test_public_overpass(self):
        findings = scan_text('url="https://overpass-api.de/api/interpreter"')
        self.assertIn("PUBLIC_OVERPASS_URL", [f.rule for f in findings])

    def test_obvious_unbounded_ql(self):
        self.assertIn("UNBOUNDED_QL_CANDIDATE", [f.rule for f in scan_text('node;out;')])

    def test_map_events(self):
        self.assertIn("MAP_EVENT_OVERPASS", [f.rule for f in scan_text('map.on("moveend", () => overpass())')])

    def test_not_a_complete_parser(self):
        self.assertEqual(scan_text('print("hello")'), [])


if __name__ == "__main__":
    unittest.main()
