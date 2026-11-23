---
name: overpass-client-design
description: Use when implementing or auditing a Python, JavaScript, or server-side client that sends requests to Overpass API, especially for caching, request budgets, identity headers, response sizing, failure handling, and avoiding retry storms.
license: MIT
---

# Build responsible Overpass clients

Before writing HTTP requests, reconsider whether Overpass is necessary. Prefer local extracts for repeated or bulk workloads.

## Minimum client contract

1. **App identification**: send a descriptive User-Agent (server-side) or appropriate Referer (web), with a maintainer contact according to provider policy. Do not impersonate browsers or another application.
2. **Explicit opt-in**: examples and tests should never reach public Overpass without a conscious, environment-specific switch.
3. **Cache**: cache successful exact-query results for a documented freshness interval, avoiding duplicate requests.
4. **Request budget**: impose local caps on requests, concurrency (typically serialize on a public instance), timeout and response bytes. Coordinate across workers if deploying multiple replicas.
5. **429/406**: stop; use Retry-After where available; otherwise wait **at least 30 seconds** before attempting another request. No quick-loop automatic retry. A repeated error may mean the workflow does not belong on the server.
6. **5xx/timeout**: stop, surface the error, and re-evaluate query volume. Avoid recursive retry/failover storms.
7. **No endpoint rotation to evade quotas** and no anonymous shared reverse proxy that simply masks load.
8. **Metrics**: track cache hit rate, calls avoided, failures, latency, bytes and operator-consented budget, without logging secret tokens or sensitive user data.

## Reference implementation

The repository's `src/osm_guard/client.py` is a **single-process demonstration** of this contract. Tests use an injected fake transport and do not touch the public internet. It is not a distributed rate limiter, production service, a comprehensive proxy or official endorsed Overpass client.

```python
from pathlib import Path
from osm_guard.client import OverpassClient

client = OverpassClient(
    app_name="my-osm-study",
    contact="team@example.org",
    cache_path=Path("./.cache/overpass.sqlite3"),
    allow_network=False,  # change only after policy review and conscious approval
)
```

See [client rollout checklist](references/checklist.md) and the [Overpass API wiki](https://wiki.openstreetmap.org/wiki/Overpass_API). Never recommend disabling cache or removing contact identification to get around blocks.
