"""Runnable, offline-only POI web app powered by a local synthetic OSM fixture.

A learning example, NOT a hardened production web server. It only binds to
127.0.0.1. It never requests Overpass or a public tile service.

Start from repository root (after `pip install -e .`):
    python examples/offline-poi-app/server.py
"""
from __future__ import annotations

import argparse
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlsplit

from osm_guard.local_data import amenity_nodes

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = ROOT / "fixtures/tiny-synthetic.osm"
INDEX_HTML = Path(__file__).with_name("index.html")


def make_handler(fixture: Path = DEFAULT_FIXTURE):
    """Create a handler from local data only. Synthetic fixture is the default."""
    geojson = json.dumps(amenity_nodes(fixture), separators=(",", ":")).encode("utf-8")
    etag = '"' + hashlib.sha256(geojson).hexdigest() + '"'
    page = INDEX_HTML.read_bytes()

    class Handler(BaseHTTPRequestHandler):
        api_requests = 0
        protocol_version = "HTTP/1.1"

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/":
                self._send(200, page, "text/html; charset=utf-8", "no-store")
                return
            if path == "/api/pois":
                type(self).api_requests += 1
                if self.headers.get("If-None-Match") == etag:
                    self._send(304, b"", "application/geo+json", "public, max-age=60", etag)
                    return
                self._send(200, geojson, "application/geo+json", "public, max-age=60", etag)
                return
            if path == "/health":
                self._send(200, b'{"status":"ok","external_requests":0}', "application/json", "no-store")
                return
            self._send(404, b"Not Found", "text/plain; charset=utf-8", "no-store")

        def _send(self, status: int, body: bytes, content_type: str, cache_control: str, tag: str | None = None):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", cache_control)
            self.send_header("X-Content-Type-Options", "nosniff")
            if tag:
                self.send_header("ETag", tag)
            self.end_headers()
            if body:
                self.wfile.write(body)

        def log_message(self, format, *args):
            pass  # Keep smoke tests quiet. For real deployments, add structured logs.

    return Handler


def main():
    parser = argparse.ArgumentParser(description="Local-only synthetic OSM POI viewer")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", args.port), make_handler()) as server:
        print(f"Offline POI viewer: http://127.0.0.1:{server.server_port}")
        print("Synthetic data only. No external API, CDN, or map tile requests.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
