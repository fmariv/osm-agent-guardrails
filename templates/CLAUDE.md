# OpenStreetMap project guidance for Claude Code

Read and follow `AGENTS.md` in this project. In particular, do not reach for public Overpass as the first option when designing repeated, bulk, interactive or production workloads. Explain the data-source choice, concurrency, caching, data freshness and licensing. Avoid calling public OSM infrastructure during tests. If `osm-agent-skills` are installed, load the relevant skill for the current task.
