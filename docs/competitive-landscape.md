# Positioning relative to existing tools

Reviewed: **2026-11-23**. This is a practical distinction, **not a claim of being first or unique**. Re-check upstream capabilities before publishing competitive comparisons.

| Project | Link | Main emphasis | OSM Agent Guardrails focus |
| --- | --- | --- | --- |
| OpenMapStack Skills | https://github.com/jaakla/openmapstack-skills | General geospatial skills for modern data and map workflows | Narrowly OSM/Overpass, infrastructure-conscious code generation and evaluation |
| OpenStreetMap MCP Server | https://github.com/cyanheads/openstreetmap-mcp-server | Tools and guidance for interacting with live OSM services | Avoid unnecessary live requests before an app is built; no gateway required |
| Hermes maps skill | https://github.com/NousResearch/hermes-agent | Maps/place tools for an agent | Practices for developers who build OSM-powered applications, not live location answering |
| OSMnx | https://github.com/gboeing/osmnx | Network analysis and local graph algorithms | Deciding **when** to use these tools instead of public API calls |

## Difference to validate with evidence

1. A portable collection of task-triggered skills for OSM/Overpass development (not a generic GIS skills catalogue).
2. Concrete offline end-to-end examples, including HTTP cache behavior and an example app that never calls public Overpass.
3. Offline static and workload checks that **flag** problems, without pretending to enforce remote policy.
4. A documented reproducible A/B agent-evaluation protocol; **not yet an empirical demonstration of traffic savings**.

A good project can coexist with nearby skills and MCP servers. Reuse upstream projects and submit documentation improvements rather than duplicating their capabilities.
