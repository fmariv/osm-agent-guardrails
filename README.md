# OSM Agent Guardrails

**Build better OpenStreetMap applications without overloading public infrastructure.**

Agent Skills, coding guidelines, offline examples, and automated checks for AI coding assistants that work with OpenStreetMap (OSM) and the Overpass API.

> **Independent community project.** OSM Agent Guardrails is **not an official OpenStreetMap or Overpass project** and is not affiliated with, sponsored by, or endorsed by the OpenStreetMap Foundation, OpenStreetMap España, or the Overpass API maintainers.
>
> **Status:** v0.2.0 release candidate for community feedback. The included client is a reference implementation, **not** a production-ready shared Overpass gateway. Agents are not guaranteed to follow any skill. See [limitations](#what-this-project-does-not-do).

## Why this exists

OSM **data** is open; community-run **services** have finite capacity. AI-generated apps may accidentally query a public Overpass server on every map interaction, repeatedly download a region, or aggressively retry after throttling. Overpass operators have explicitly asked for examples that help developers and AI coding agents make more efficient choices ([community request](https://community.openstreetmap.org/t/overpass-api-performance-issues/140598/163)).

**Our focus is on preventing avoidable calls at the code-generation stage.** This is not another MCP proxy or a general GIS toolkit.

| Before | Responsible alternative |
| --- | --- |
| Browser → public Overpass on every pan | Browser → own bounded data API or local/vector tiles |
| Nightly region-wide Overpass queries | Maintain a local PBF-derived dataset and update it appropriately |
| Tight retry loop after a 429/406 | Stop, honor operator signals, budget requests, and avoid automatic mirror hopping |
| Default OSMF raster tiles for high-volume traffic | Select a basemap provider whose policy and capacity fit the workload |

## Install all five skills with one command

**Current GitHub slug (before repository rename):** `fmariv/osm-agents-skills`.

```bash
npx skills add fmariv/osm-agents-skills --all
```

Or choose agents and skills interactively:

```bash
npx skills add fmariv/osm-agents-skills
```

The standard [Agent Skills](https://agentskills.io/specification) format can be used with compatible coding agents such as Cursor, Claude Code, and OpenAI Codex. **Compatibility depends on agent/tool version and configuration**; regular ChatGPT conversations do not automatically load skills from GitHub.

No npm? The repository also contains a **local, offline installer**:

```bash
python tools/install.py --agent all --target /path/to/your-project --include-rules
```

`--agent all` installs each skill in the supported project directories for Cursor, Claude Code and Codex and copies applicable `AGENTS.md`/`CLAUDE.md` templates. Existing files are not overwritten without `--force`. If you only want lightweight rules, copy [`templates/AGENTS.md`](templates/AGENTS.md) into your own repository; this is not the full set of skills.

After GitHub rename, the desired installation path is `fmariv/osm-agent-guardrails`. **Do not use that URL until the repository has actually been renamed.** See [rename steps](docs/rename-repository.md).

## What you get

| Skill | Job |
| --- | --- |
| [`osm-source-selection`](skills/osm-source-selection/SKILL.md) | Choose Overpass vs local extracts vs managed data APIs vs tiles |
| [`overpass-query-safety`](skills/overpass-query-safety/SKILL.md) | Bound Overpass QL and avoid expensive query patterns |
| [`overpass-client-design`](skills/overpass-client-design/SKILL.md) | Implement identity, caching, backpressure and error handling |
| [`osm-local-extracts`](skills/osm-local-extracts/SKILL.md) | Use PBF/PyOsmium/OSMnx for repeatable data pipelines |
| [`osm-web-maps`](skills/osm-web-maps/SKILL.md) | Design frontends without a public Overpass request per user interaction |

The five skills are installed together; agents choose which to load according to the task. They do not grant access to APIs or require running an MCP server.

## Run a complete offline web example

A small but **executable** end-to-end flow: synthetic local OSM XML → Python API → browser POI viewer. The API supports HTTP `ETag` caching; filtering is entirely client-side; no public Overpass, OSM tiles or external CDNs are used.

```bash
python -m pip install -e .
python examples/offline-poi-app/server.py
# Open http://127.0.0.1:8765
```

The viewer uses a **schematic SVG**, not a real basemap. It is deliberately a toy dataset and a local-only demo, not a production map platform. See [its README](examples/offline-poi-app/README.md) and [web map architecture](examples/web/README.md) for the production pattern.

Additional examples: [local OSM XML](examples/python/local_xml_pois_to_geojson.py), [optional PyOsmium PBF processing](examples/python/pbf_pois_to_geojson.py), and [a deliberately unsafe code sample for linting](examples/python/unsafe_example.py) (never executed).

## Check architecture and code offline

`osm_guard` is a dependency-free Python 3.11+ set of advisory developer helpers. These are not proof of policy compliance, distributed rate limits or a replacement for operator-side protections.

```bash
python -m pip install -e .

# Recommend a source based on a workload
osm-guard recommend --workflow scheduled --area-km2 800 --daily-runs 10

# Detect obvious bad patterns (heuristic; warnings require human review)
osm-guard lint examples/python/unsafe_example.py

# Validate all five skills
osm-guard validate-skills skills

# Test offline scenario fixtures; NOT an AI-agent benchmark
python tools/evaluate_offline.py --json

# All offline tests
python -m unittest discover -s tests -v
```

### Evaluation: distinguish checks from claims

The repo includes [synthetic scenarios](benchmarks/scenarios.json) and a deterministic evaluation runner for source selection and code-smell findings, plus a documented [agent comparison protocol](docs/evaluation.md) with repeatable prompts. **Fixture checks are not an A/B test of AI agents.** We have **not** established a measured reduction in real-world Overpass load. Such a claim would require independent controlled agent runs with offline/fake HTTP transports and a transparent comparison of generated applications.

## What this project does not do

- It does **not** block bots from Overpass, proxy public requests or guarantee safe queries.
- It does **not** make a public Overpass instance suitable for production, multi-user or bulk applications.
- It does **not** implement shared quotas across processes, users, hosts or organizations.
- It does **not** guarantee that an AI agent activates a skill or writes correct code.
- It does **not** include a complete OSM reader: the toy XML/PBF examples only cover amenity-tagged nodes.
- It does **not** perform live load tests against public OSM infrastructure.

## Documentation and community

- [Choosing the right data source](docs/source-decision-guide.md)
- [Official policies and references](docs/policies-and-sources.md)
- [Architecture and threat model](docs/architecture.md)
- [Evaluation protocol and evidence levels](docs/evaluation.md)
- [Related projects and differentiation](docs/competitive-landscape.md)
- [Compatibility and installation caveats](docs/compatibility.md)
- [Release checklist](docs/release-checklist.md)
- [Contributing](CONTRIBUTING.md) · [Code of Conduct](CODE_OF_CONDUCT.md) · [Security](SECURITY.md) · [Roadmap](ROADMAP.md)

**License:** [MIT](LICENSE) for this project's original code and documentation. Any real OSM-derived data remains governed separately by the [Open Database License (ODbL)](https://www.openstreetmap.org/copyright), including applicable attribution and share-alike obligations. All bundled fixtures are synthetic and do not include OSM database content. Consult provider-specific [tile usage](https://operations.osmfoundation.org/policies/tiles/) and [Overpass instance rules](https://wiki.openstreetmap.org/wiki/Overpass_API) before deployment.
