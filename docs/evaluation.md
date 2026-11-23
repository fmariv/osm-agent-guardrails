# Evaluating whether the skills help

This is a **plan**, not published experimental results. Do not assert improved traffic until measured.

## Benchmark tasks (offline / mocked)

1. Display a city POI layer in a multi-user browser app.
2. Refresh all buildings for a large region weekly.
3. Build a road graph for repeated routing analyses.
4. Retrieve a bounded set of amenities once for exploration.
5. Handle a mocked 429/406 and Retry-After.
6. Store local datasets and refresh via extracts.
7. Deploy a map with correct tile provider, attribution and caching.
8. Generate a Python package that must never call public APIs in tests.

## Method

Run each task across a fixed set of models/configurations with (A) no skills and (B) all relevant skills. Keep prompts, context and model version controlled; randomize ordering and replicate runs to handle nondeterminism. Use fixtures and HTTP mocks; never use real public endpoints as a benchmark target.

## Scoring rubric

- Source selection matches requirements (0/1/2).
- Public Overpass HTTP requests in *simulated* user journeys (count; lower is better where not needed).
- Correct caching / rate/concurrency/error handling (0/1/2).
- Correct OSM attribution / licence and tile policy (0/1/2).
- Data completeness and code correctness (0/1/2).
- Latency/resource footprint in local mock environment (relative).

Store anonymized generated code, grader rationale and model metadata for reproducibility. Avoid conflating instruction-following scores with measured community-server savings.
