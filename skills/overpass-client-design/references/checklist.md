# Before deploying any Overpass client

- [ ] Confirm this use case belongs on public Overpass (including aggregate traffic from all users).
- [ ] Identify the instance, current policy, and escalation/contact options.
- [ ] Document bounding boxes and expected output for every generated query template.
- [ ] Document client identity (`User-Agent` or applicable Referer).
- [ ] Enable successful-response cache, deduplication and query request budget.
- [ ] Serialize requests (or use an operator-approved concurrency policy).
- [ ] Stop on 429/406 and respect a minimum 30s cooldown; don't spin retries.
- [ ] No public endpoints in automated CI/load-testing environments.
- [ ] For multi-worker use, design coordinated rate limiting; local SQLite isn't shared across hosts.
- [ ] Add an operational switch to disable outbound queries immediately.
- [ ] Review data licensing/attribution for outputs.
