# OSM Agent Skills

**Better OpenStreetMap code. Less unnecessary load on community infrastructure.**

> **Independent community project:** OSM Agent Skills is an independent, community-oriented initiative. It is **not an official OpenStreetMap or Overpass project**, and is not affiliated with, sponsored by, or endorsed by the OpenStreetMap Foundation, OpenStreetMap España, or the Overpass API maintainers.
>
> **Status:** v0.1.0 community review candidate. The included reference client and guidance should be validated for each use case before production deployment.

OSM Agent Skills is a vendor-neutral set of [Agent Skills](https://agentskills.io/specification), portable agent instructions, tested Python utilities, and examples for building responsible applications around OpenStreetMap and the Overpass API.

It teaches coding agents **which data source to choose**, **how to query safely**, **how to handle throttling**, **how to process OSM locally**, and **how to build web maps without turning public APIs into a production database**.

## Install all five skills in one command

Once this repository is available through GitHub (private GitHub access requires valid Git credentials):

```bash
npx skills add fmariv/osm-agents-skills --all
```

To choose your coding agents interactively (Cursor, Claude Code, Codex, etc.):

```bash
npx skills add fmariv/osm-agents-skills
```

From a local clone, **before GitHub publication**, run this from the project where you want the skills available (replace the path with your local clone):

```bash
npx skills add /path/to/osm-agent-skills --all
```

No Node.js installed? You can also use the included **offline Python installer**:

```bash
python /path/to/osm-agent-skills/tools/install.py --agent all --target /path/to/your-project --include-rules
```

This copies all skills into Cursor, Claude Code and Codex's project directories. It refuses overwrites unless you explicitly use `--force`.

To install globally, follow the installer options (`-g`); to update, use `npx skills update`. There is **no MCP server to operate**. Compatibility is determined by the installed coding-agent version, not by this repository. Ordinary ChatGPT conversations do not automatically load files from a GitHub repo.

Want project-level guidance without installing skills? Copy [`templates/AGENTS.md`](templates/AGENTS.md) into your project. Claude Code users can copy [`templates/CLAUDE.md`](templates/CLAUDE.md) too. These are concise guardrails, not replacements for the full skills.

## What is included?

| Skill | When it activates | Key outcome |
| --- | --- | --- |
| [`osm-source-selection`](skills/osm-source-selection/SKILL.md) | Planning an OSM integration | Choose extracts, tiles, local stores or Overpass appropriately |
| [`overpass-query-safety`](skills/overpass-query-safety/SKILL.md) | Writing Overpass QL | Bounded queries and conservative output |
| [`overpass-client-design`](skills/overpass-client-design/SKILL.md) | Building API clients | Explicit opt-in, caching, response limits and throttling |
| [`osm-local-extracts`](skills/osm-local-extracts/SKILL.md) | Processing bulk/recurrent OSM data | PBF, PyOsmium and OSMnx workflows |
| [`osm-web-maps`](skills/osm-web-maps/SKILL.md) | Developing map frontends | Tile-policy compliance and offline-derived layers |

## Runnable software (offline by default)

This repository includes `osm_guard`, a dependency-free Python 3.11+ **reference implementation**, not a server or a substitute for operator-side throttling.

```bash
python -m pip install -e .
python -m osm_guard recommend --workflow scheduled --area-km2 800 --daily-runs 10
python -m osm_guard lint examples/python/unsafe_example.py
python -m unittest discover -s tests -v
```

`osm_guard` provides:

- A conservative source-selection decision helper with an explainable result.
- A static lint for *obvious* misuse patterns (not a complete Overpass QL parser).
- A safe-by-default optional Overpass client: network access must be explicitly enabled, a contactable user agent is required, results are cached in SQLite, requests are serialized, local per-run budgets are enforced, and 429/406 responses trigger a minimum 30-second cooldown **without automatic retries or endpoint rotation**.
- Sample local OSM XML and optional PBF processing with PyOsmium. Tests use local fakes, **never public Overpass**.

### Important security and operational limits

These controls only apply to applications that use them. They cannot block bots that call Overpass directly. Local caching does not coordinate quotas between servers/containers/users, and a single-process lock does not provide distributed rate limiting. Heuristics do not prove server safety. For multi-replica production workloads, use a coordinated cache/queue, a licensed commercial service, or your own OSM-derived data infrastructure, with operator approval where applicable.

**Do not run integration load tests against public Overpass or OSM tile endpoints.** The CI suite runs offline.

## GitHub repository

The project repository is [`fmariv/osm-agents-skills`](https://github.com/fmariv/osm-agents-skills). It is an independent, early community-review candidate; consult the [release checklist](docs/release-checklist.md) before making strong compatibility or performance claims. The project must not imply OSMF endorsement.

## Examples and docs

- [Source choice and decision matrix](docs/source-decision-guide.md)
- [Policy and official references](docs/policies-and-sources.md)
- [Evaluation plan](docs/evaluation.md)
- [Project architecture](docs/architecture.md)
- [Contributing](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md)
- [Local OSM XML / optional PBF sample](examples/python/README.md)
- [Map frontend guidance](examples/web/README.md)

## Why this project?

OpenStreetMap data is open; its community-operated API and tile infrastructure have finite capacity. AI-generated applications sometimes treat public Overpass endpoints as a free hosted production database. This project aims to make the **responsible choice the easy, default choice** for an AI coding agent.

The objective is to reduce unnecessary public requests **without forbidding legitimate occasional Overpass usage**. Actual impact must be demonstrated in controlled offline evaluations, not inferred from installing skills.

## Licences, attribution, status

Code and documentation: [MIT](LICENSE). OSM-derived data used by your application is separately governed by [ODbL](https://www.openstreetmap.org/copyright), with attribution and applicable share-alike obligations. The tiny test fixture is **synthetic** and contains no copied OSM data.

Proposed maintainer: `fmariv`. Community review and language improvements welcome once made public. See [ROADMAP](ROADMAP.md). No remote deployment or live public OSM infrastructure changes are required to use these skills.
