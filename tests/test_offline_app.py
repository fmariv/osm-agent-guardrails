"""API-level smoke tests against 127.0.0.1 only; no public APIs or tiles."""
import importlib.util
import json
from http.server import ThreadingHTTPServer
from pathlib import Path
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "examples/offline-poi-app/server.py"


class OfflineAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("local_webapp", APP_PATH)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.handler = module.make_handler()
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), cls.handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get(self, path, headers=None):
        with urlopen(Request(self.base + path, headers=headers or {}), timeout=5) as response:
            return response.status, dict(response.headers), response.read()

    def test_pois_and_caching(self):
        before = self.handler.api_requests
        status, headers, body = self.get("/api/pois")
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(body)["features"]), 2)
        self.assertEqual(headers["Cache-Control"], "public, max-age=60")
        etag = headers["ETag"]
        self.assertEqual(len(etag), 66)
        request = Request(self.base + "/api/pois", headers={"If-None-Match": etag})
        try:
            urlopen(request, timeout=5)
        except HTTPError as exc:
            self.assertEqual(exc.code, 304)
            self.assertEqual(exc.headers["ETag"], etag)
            self.assertEqual(exc.read(), b"")
        else:
            self.fail("Expected conditional response 304")
        self.assertEqual(self.handler.api_requests - before, 2)

    def test_homepage_has_no_remote_imports(self):
        status, _, body = self.get("/")
        self.assertEqual(status, 200)
        content = body.decode()
        self.assertIn("Offline POI viewer", content)
        self.assertIn("fetch('/api/pois'", content)
        for forbidden in ("<script src=\"http", "<link href=\"http", "overpass-api.de", "tile.openstreetmap.org"):
            self.assertNotIn(forbidden, content)

    def test_health_and_unknown_route(self):
        status, _, body = self.get("/health")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["external_requests"], 0)
        with self.assertRaises(HTTPError) as exc:
            self.get("/not-found")
        self.assertEqual(exc.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
