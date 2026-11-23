from pathlib import Path
import tempfile
import math
import unittest

from osm_guard.client import (
    LocalBudgetExceeded,
    NetworkDisabled,
    OverpassClient,
    RequestThrottled,
    ResponseTooLarge,
    TransportResult,
    UpstreamFailure,
)


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class FakeTransport:
    def __init__(self, statuses=None, body=b'{"elements": []}'):
        self.statuses = statuses or [200]
        self.body = body
        self.calls = []

    def __call__(self, endpoint, query, headers, timeout, limit):
        self.calls.append((endpoint, query, headers, timeout, limit))
        idx = min(len(self.calls) - 1, len(self.statuses) - 1)
        return TransportResult(self.statuses[idx], self.body, {"Retry-After": "60"})


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.clock = Clock()
        self.fake = FakeTransport()

    def client(self, **overrides):
        options = dict(
            endpoint="https://example.invalid/api/interpreter",
            app_name="Test OSM Analysis",
            contact="maintainer@example.org",
            cache_path=Path(self.tmp.name) / "cache.sqlite3",
            allow_network=True,
            transport=self.fake,
            clock=self.clock,
        )
        options.update(overrides)
        return OverpassClient(**options)

    def test_offline_by_default(self):
        client = self.client(allow_network=False)
        with self.assertRaises(NetworkDisabled):
            client.query('[out:json];node(0,0,0.01,0.01);out;')
        self.assertEqual(len(self.fake.calls), 0)

    def test_cache_prevents_second_call(self):
        client = self.client()
        first = client.query('query-1')
        second = client.query('query-1')
        self.assertFalse(first.from_cache)
        self.assertTrue(second.from_cache)
        self.assertEqual(len(self.fake.calls), 1)
        self.assertIn('maintainer@example.org', self.fake.calls[0][2]['User-Agent'])
        self.assertEqual(client.stats, {"network_calls": 1, "cache_hits": 1})

    def test_min_interval_blocks_distinct_query(self):
        client = self.client()
        client.query('query-1')
        with self.assertRaises(LocalBudgetExceeded):
            client.query('query-2')
        self.assertEqual(len(self.fake.calls), 1)
        self.clock.advance(5)
        client.query('query-2')
        self.assertEqual(len(self.fake.calls), 2)

    def test_budget(self):
        client = self.client(max_calls_per_run=1)
        client.query('query-1')
        self.clock.advance(10)
        with self.assertRaises(LocalBudgetExceeded):
            client.query('query-2')

    def test_throttle_stops_without_retry(self):
        self.fake = FakeTransport(statuses=[429, 200])
        client = self.client()
        with self.assertRaises(RequestThrottled) as caught:
            client.query('query-1')
        self.assertEqual(caught.exception.retry_after_seconds, 60)
        self.assertEqual(len(self.fake.calls), 1)
        self.clock.advance(10)
        with self.assertRaises(RequestThrottled):
            client.query('query-2')
        self.assertEqual(len(self.fake.calls), 1)
        self.clock.advance(50)
        client.query('query-2')
        self.assertEqual(len(self.fake.calls), 2)

    def test_406_uses_minimum_cooldown(self):
        self.fake = lambda *args: TransportResult(406, b'no', {})
        client = self.client()
        with self.assertRaises(RequestThrottled) as ctx:
            client.query('query-1')
        self.assertEqual(ctx.exception.retry_after_seconds, 30)

    def test_5xx_not_automatically_retried(self):
        self.fake = FakeTransport(statuses=[504, 200])
        client = self.client()
        with self.assertRaises(UpstreamFailure):
            client.query('query-1')
        self.assertEqual(len(self.fake.calls), 1)

    def test_response_limit(self):
        self.fake = FakeTransport(body=b'x' * 100)
        client = self.client(max_response_bytes=64)
        with self.assertRaises(ResponseTooLarge):
            client.query('query-1')

    def test_cache_persists_between_client_objects(self):
        first = self.client()
        first.query('query-1')
        second = self.client()
        self.assertTrue(second.query('query-1').from_cache)
        self.assertEqual(len(self.fake.calls), 1)

    def test_requires_identification(self):
        with self.assertRaises(ValueError):
            self.client(contact='unknown')

    def test_rejects_nonfinite_config(self):
        for option in ({"timeout_seconds": math.inf}, {"cache_ttl_seconds": math.nan},
                       {"min_interval_seconds": math.nan}, {"max_calls_per_run": 1.5}):
            with self.subTest(option=option), self.assertRaises(ValueError):
                self.client(**option)

    def test_rejects_header_injection(self):
        with self.assertRaises(ValueError):
            self.client(app_name="bad\r\nX-Test: injected")

    def test_empty_results_are_cached(self):
        self.fake = FakeTransport(body=b"")
        client = self.client()
        self.assertEqual(client.query("empty").payload, b"")
        self.assertTrue(client.query("empty").from_cache)
        self.assertEqual(len(self.fake.calls), 1)

    def test_prevents_insecure_remote_http(self):
        with self.assertRaises(ValueError):
            self.client(endpoint='http://example.invalid/api/interpreter')


if __name__ == "__main__":
    unittest.main()
