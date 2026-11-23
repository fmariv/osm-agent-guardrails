# Evaluation and evidence: do the guardrails help?

## Three distinct levels of evidence

| Level | Evidence | Status | Permitted conclusion |
| --- | --- | --- | --- |
| 1 — fixture tests | Synthetic workload decisions + static-code warning expectations | **Implemented** (`benchmarks/scenarios.json`, `tools/evaluate_offline.py`) | Our own deterministic checks behave as expected on curated examples. |
| 2 — offline application integration | Localhost-only POI service; mocked client transports; no real OSM calls | **Implemented** (`tests/test_offline_app.py`, `tests/test_client.py`) | Those sample implementations behave as expected in local tests. |
| 3 — comparative agent study | Same prompts across agents, with and without these skills, blinded grading of generated projects | **Not yet performed** | Could provide evidence of improved agent architecture/code choices; cannot alone prove less actual public server traffic. |

**Never translate Level 1 results into claims such as "AI agents make X% fewer Overpass requests".** Scoring our own synthetic examples against our own rules risks confirmation bias and does not measure deployment behavior.

## Reproducible fixture runner

```bash
python -m pip install -e .
python tools/evaluate_offline.py
python tools/evaluate_offline.py --json > /tmp/osm-offline-results.json
```

The runner fails with nonzero exit code if a curated expected value does not match. The tests and demo use no public Overpass or tile servers.

## Controlled A/B agent evaluation (future)

1. Select at least 10 common application-development tasks from [`benchmarks/agent-tasks.md`](../benchmarks/agent-tasks.md); finalize prompts **before** running agents.
2. For each agent/model/version, run the identical prompt (A) without this repo installed and (B) with skills and AGENTS.md configured. Change no other context. Use a fresh workspace, same installed dependencies, and fixed randomness where possible.
3. Randomize order, repeat tasks across multiple runs, record date, model, agent version, skill activation logs when available, prompt, generated code, and scripts used to grade it.
4. Use only synthetic local OSM fixtures. Route all HTTP through local mocks/fake transports; never benchmark against public OSM services.
5. Review generated code blind to condition and report inter-rater disagreements. Do not mistake `osm-guard lint` findings for a full safety grade.
6. Measure local/mock HTTP calls during simulated flows (initial load, 20 pans, 20 filters, 429/406 error, scheduled refresh), API correctness and complete outputs. Disclose any differences in behavior/requirements.
7. Publish raw results with enough provenance to reproduce the test; if only some agents/versions were tested, report those exact bounds.

## Suggested scoring dimensions (each 0, 1 or 2 except counts)

- Data-source choice is appropriate for extent, workload, update frequency and SLA.
- Query bounds and result completeness (including relevant geometry: nodes, ways and relations where applicable).
- Responsible retries, quotas, caching and cross-user behavior.
- Tile provider, attribution and licensing compliance.
- Runnable correctness, quality and functionality of the generated app.
- **Mock HTTP request count** for fixed simulated workflows (numeric; distinguish client-side calls from upstream requests).

Use outcome statistics with confidence intervals and keep anecdotal examples separate from aggregate findings. Requests avoided in a local fixture are not automatically upstream cost or traffic savings in the wild.
