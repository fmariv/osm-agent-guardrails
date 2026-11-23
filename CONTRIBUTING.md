# Contributing to OSM Agent Guardrails

Please read our [Code of Conduct](CODE_OF_CONDUCT.md). Discussions must respect volunteer operators and project contributors.

Before changing guidance, read the current official Overpass instance policy and OSMF service policies. Cite the source and the review date in your PR. Separate universal engineering recommendations from instance-specific limits.

Keep skills vendor-neutral and short. Add runnable, offline examples and tests for every behavioral change. Do not run benchmarks or CI requests against public OSM infrastructure. Use synthetic fixtures without copying OSM data, and preserve proper attribution for any later real sample datasets.

## Quality checks

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m osm_guard validate-skills skills
python -m compileall -q src tools examples/python examples/offline-poi-app
python tools/evaluate_offline.py
```

PR checklist: specific user scenario, expected behavior, official citations, offline tests, explanation of limits, no claims of guaranteed server protection.

## Disclosure and project governance

No affiliation with OSMF/OpenStreetMap España is implied. Follow the community's maintainer input; keep the project independent unless officially accepted. Security-sensitive bugs should be reported privately to the maintainer through GitHub private reporting once enabled.

## Pull request process

1. Open an issue describing the concrete geospatial workload and why the current advice falls short.
2. Keep PRs small, with a source link to an upstream policy or API documentation where applicable.
3. Add an offline test or reproducible local example whenever code behavior changes.
4. Run the quality commands and include their results in the PR description.
5. A maintainer reviews correctness, service impact, attribution and backward compatibility before merging.

Code and documentation contributed here are submitted under the repository's MIT licence. Do not submit copied OSM datasets, proprietary third-party code, credentials or personally identifying information. OSM-derived datasets retain their own ODbL obligations regardless of the project's code licence.
