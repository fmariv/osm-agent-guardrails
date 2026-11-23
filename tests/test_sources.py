import unittest
import math

from osm_guard.sources import Source, Workload, recommend


class TestSourceSelection(unittest.TestCase):
    def test_one_off_bounded(self):
        self.assertEqual(recommend(Workload()).source, Source.PUBLIC_OVERPASS)

    def test_scheduled_processing_uses_extract(self):
        self.assertEqual(recommend(Workload(workflow="scheduled", area_km2=25)).source, Source.LOCAL_EXTRACT)

    def test_large_one_off_still_uses_extract(self):
        self.assertEqual(recommend(Workload(area_km2=100)).source, Source.LOCAL_EXTRACT)

    def test_multi_user_avoids_public_api(self):
        self.assertEqual(recommend(Workload(users=100)).source, Source.LOCAL_DATABASE)

    def test_basemap_uses_tiles(self):
        self.assertEqual(recommend(Workload(needs_basemap=True)).source, Source.MAP_TILES)

    def test_non_finite_area(self):
        for area in (math.inf, math.nan, -math.inf):
            with self.subTest(area=area), self.assertRaises(ValueError):
                Workload(area_km2=area)

    def test_invalid_area(self):
        with self.assertRaises(ValueError):
            Workload(area_km2=0)


if __name__ == "__main__":
    unittest.main()
