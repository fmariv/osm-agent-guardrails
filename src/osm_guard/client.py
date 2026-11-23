"""Explicit-opt-in Overpass client example with single-process safeguards.

NOT a distributed rate limiter or a guarantee of acceptable public-server use.
Never use this module in CI to contact public services. Tests inject fake transports.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import math
from pathlib import Path
import sqlite3
import threading
import time
from typing import Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


class OverpassError(Exception):
    """Base client error."""


class NetworkDisabled(OverpassError):
    """Network access not explicitly permitted."""


class LocalBudgetExceeded(OverpassError):
    """Local request budget or minimum spacing exceeded."""


class RequestThrottled(OverpassError):
    """Remote policy signal received; caller must stop until retry time."""

    def __init__(self, retry_after_seconds: float) -> None:
        self.retry_after_seconds = retry_after_seconds
        super().__init__(f"Operator throttled request; do not retry for at least {retry_after_seconds:.1f}s")


class UpstreamFailure(OverpassError):
    """Non-success HTTP response; no retries performed."""


class ResponseTooLarge(OverpassError):
    """Response exceeded configured byte limit."""


@dataclass(frozen=True)
class TransportResult:
    status: int
    body: bytes
    headers: Mapping[str, str]


@dataclass(frozen=True)
class Result:
    payload: bytes
    from_cache: bool


Transport = Callable[[str, str, Mapping[str, str], float, int], TransportResult]


def urllib_transport(
    endpoint: str, query: str, headers: Mapping[str, str], timeout: float, max_bytes: int
) -> TransportResult:
    """POST QL with bounded read. HTTP errors are reported without automatic retry."""
    request = Request(
        endpoint, data=urlencode({"data": query}).encode("utf-8"),
        headers=dict(headers), method="POST",
    )
    try:
        try:
            response = urlopen(request, timeout=timeout)
        except HTTPError as exc:
            response = exc
        with response:
            body = response.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise ResponseTooLarge(f"Response exceeded {max_bytes} byte limit")
            return TransportResult(response.status, body, dict(response.headers.items()))
    except URLError as exc:
        raise UpstreamFailure(f"Network unavailable: {exc.reason}") from exc


def _retry_after_seconds(headers: Mapping[str, str], now: float) -> float:
    value = next((v for k, v in headers.items() if k.lower() == "retry-after"), "")
    try:
        return max(30.0, float(value))
    except (TypeError, ValueError):
        pass
    if value:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            return max(30.0, date.timestamp() - now)
        except (TypeError, ValueError, OverflowError):
            pass
    return 30.0


class OverpassClient:
    """A per-process demonstration client, not a production multi-worker solution."""

    def __init__(
        self,
        *,
        endpoint: str = "https://overpass-api.de/api/interpreter",
        app_name: str,
        contact: str,
        cache_path: Path | str,
        allow_network: bool = False,
        cache_ttl_seconds: float = 86_400,
        min_interval_seconds: float = 5.0,
        max_calls_per_run: int = 10,
        timeout_seconds: float = 30.0,
        max_response_bytes: int = 2_000_000,
        transport: Transport | None = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        host = urlsplit(endpoint).hostname or ""
        valid_local = host in {"localhost", "127.0.0.1", "::1"}
        if urlsplit(endpoint).scheme != "https" and not (valid_local and urlsplit(endpoint).scheme == "http"):
            raise ValueError("Endpoint must use HTTPS except for localhost test servers")
        if any(c in app_name + contact for c in "\r\n") or not app_name.strip() or not contact.strip() or not ("@" in contact or contact.startswith("https://")):
            raise ValueError("Provide a non-empty application name and a contact email/URL")
        if not all(math.isfinite(value) and value > 0 for value in (cache_ttl_seconds, timeout_seconds)):
            raise ValueError("TTL and timeout must be finite and > 0")
        if not isinstance(max_response_bytes, int) or not isinstance(max_calls_per_run, int) or min(max_response_bytes, max_calls_per_run) <= 0:
            raise ValueError("Byte limit and request budget must be positive integers")
        if not math.isfinite(min_interval_seconds) or min_interval_seconds < 0:
            raise ValueError("min_interval_seconds must be finite and >= 0")
        self.endpoint = endpoint
        self.app_name = app_name
        self.contact = contact
        self.cache_path = Path(cache_path)
        self.allow_network = allow_network
        self.cache_ttl_seconds = cache_ttl_seconds
        self.min_interval_seconds = min_interval_seconds
        self.max_calls_per_run = max_calls_per_run
        self.timeout_seconds = timeout_seconds
        self.max_response_bytes = max_response_bytes
        self.transport = transport or urllib_transport
        self.clock = clock
        self._lock = threading.RLock()
        self._network_calls = 0
        self._last_call_at: float | None = None
        self._blocked_until = 0.0
        self._cache_hits = 0
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.cache_path) as con:
            con.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, saved REAL NOT NULL, payload BLOB NOT NULL)")

    def _key(self, query: str) -> str:
        return hashlib.sha256(f"{self.endpoint}\n{query}".encode("utf-8")).hexdigest()

    def _from_cache(self, key: str, now: float) -> bytes | None:
        with sqlite3.connect(self.cache_path) as con:
            row = con.execute("SELECT saved, payload FROM cache WHERE key=?", (key,)).fetchone()
        if row and 0 <= now - row[0] <= self.cache_ttl_seconds:
            return row[1]
        return None

    def _save(self, key: str, now: float, payload: bytes) -> None:
        with sqlite3.connect(self.cache_path) as con:
            con.execute("INSERT OR REPLACE INTO cache (key, saved, payload) VALUES (?, ?, ?)", (key, now, payload))

    @property
    def stats(self) -> dict[str, int]:
        return {"network_calls": self._network_calls, "cache_hits": self._cache_hits}

    def query(self, query: str) -> Result:
        if not query.strip():
            raise ValueError("Overpass query must not be blank")
        if len(query.encode("utf-8")) > 16_384:
            raise ValueError("Query exceeds demonstration client's 16KiB query limit")
        with self._lock:
            now = self.clock()
            key = self._key(query)
            cached = self._from_cache(key, now)
            if cached is not None:
                self._cache_hits += 1
                return Result(cached, True)
            if not self.allow_network:
                raise NetworkDisabled("Network disabled: explicitly opt in after reviewing the chosen provider's policy")
            if now < self._blocked_until:
                raise RequestThrottled(self._blocked_until - now)
            if self._network_calls >= self.max_calls_per_run:
                raise LocalBudgetExceeded("Maximum network calls reached for this client instance")
            if self._last_call_at is not None and now - self._last_call_at < self.min_interval_seconds:
                raise LocalBudgetExceeded("Local minimum interval not reached; do not busy-loop")
            headers = {
                "User-Agent": f"{self.app_name} (contact: {self.contact})",
                "Accept": "application/json",
            }
            self._last_call_at = now
            self._network_calls += 1
            response = self.transport(self.endpoint, query, headers, self.timeout_seconds, self.max_response_bytes)
            if len(response.body) > self.max_response_bytes:
                raise ResponseTooLarge(f"Response exceeded {self.max_response_bytes} bytes")
            if response.status in {406, 429}:
                pause = _retry_after_seconds(response.headers, self.clock())
                self._blocked_until = self.clock() + pause
                raise RequestThrottled(pause)
            if response.status < 200 or response.status >= 300:
                raise UpstreamFailure(f"Upstream status {response.status}; no automatic retry")
            self._save(key, self.clock(), response.body)
            return Result(response.body, False)
