# Sources and operational policies

Last manual review: **2026-11-23**. All upstream rules can change. Before recommending live use, check the current official policy for the **specific service**.

- [OpenStreetMap Wiki — Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API): server list, usage policies, the importance of cache/rate-limiting, avoiding repeated or bulk requests. The public instance guidance explicitly warns on 429/406 and suggests waiting **at least 30 seconds**; consider longer according to Retry-After and repeated errors.
- [OSMF — Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/): distinct from Overpass. The OSMF tile server requires attribution, identifiable clients, caching and prohibits bulk scraping/prefetch.
- [OSMF — Copyright and licence](https://www.openstreetmap.org/copyright): ODbL and attribution.
- [OSMF — Attribution guidelines](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines): detailed attribution recommendations.
- [OSM Community — Overpass API performance issues](https://community.openstreetmap.org/t/overpass-api-performance-issues/140598): operator discussions and current community concerns.
- [OSMnx documentation](https://osmnx.readthedocs.io/en/stable/): supports local OSM PBF graph loading as of release 2.2.0 (2026-11-18); consult APIs for the installed version.
- [Agent Skills specification](https://agentskills.io/specification): the portable `SKILL.md` format.
- [skills CLI documentation](https://github.com/vercel-labs/skills/blob/main/docs/commands.md): local/private repository install support, `--all`, CLI agent options.
- [AGENTS.md format](https://agents.md/): convention for agent project instructions.

Note: OSM Foundation-hosted tile policy does **not** equal Overpass usage policy; different Overpass instances have distinct operators, quotas and conditions. Avoid hardcoding claims about fixed safe limits across instances.
