# Architecture and threat model

## Repository components

`skills/*/SKILL.md` -> agent instruction pack, loaded according to the consuming agent's activation rules.

`templates/` -> small copyable project instructions (`AGENTS.md`, `CLAUDE.md`) for teams that do not install skills.

`src/osm_guard` -> optional offline-friendly, Python 3.11+ decision, static lint, and reference HTTP client. It is **not** mandatory to install it to use the skills.

`tests/` -> mock transport tests, synthetic fixtures; no public OSM network calls in CI.

## Threats addressed

- AI-generated calls to shared Overpass on every frontend interaction.
- Retry storms and endpoint rotation after throttling.
- Unnecessary repeated downloads and poor source choice.
- Using shared OSM tile servers like commercial production infrastructure.

## Explicit non-goals

- Operator-side bot blocking or global Overpass protection.
- Distributed locking or enforcement across all clients.
- General Overpass QL parsing/proof of query cost.
- A public Overpass MCP gateway or reverse proxy.
- Guaranteeing agent compliance or guaranteed impact on API load.

## Client design safety boundaries

- `OverpassClient` defaults to `allow_network=False`.
- Caller must supply a contactable identity.
- Local SQLite cached only successful responses, keyed by full query and endpoint.
- Requests serialized per client object; local rate/budget checks; cooldown on 429/406 with no automatic retry.
- No implicit endpoint changes, random proxy lists or unlimited body buffering.
- Tests inject fakes and do not use `api.overpass-api.de`.
