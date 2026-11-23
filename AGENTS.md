# Repository development instructions

This `AGENTS.md` governs work ON this repository. For a template to put in another project, use `templates/AGENTS.md`.

- Primary objective: improve efficiency and reliability of code that consumes OpenStreetMap data while minimizing unnecessary traffic to community-run infrastructure.
- Treat upstream official policies as authoritative over suggestions in this repository. When rules change, update references and dated policy review notes.
- Never run tests against public Overpass, OSM API, Nominatim, or `tile.openstreetmap.org`. Tests and examples must run offline by default.
- Do not present the lint as an Overpass QL parser, a security boundary, a service-wide quota or a guarantee of safety.
- Preserve conservative behavior: explicit network opt-in, identified contact, no automatic retries on 429 or 406, no endpoint rotation or ban evasion.
- Prefer tiny dependency-free code for examples. Avoid adding network-dependent CI jobs.
- Skills use standard YAML frontmatter with `name` matching directory, brief `description`, and actionable, task-specific instructions. Longer supporting information goes in `references/`.
- All publicly shown examples must distinguish mock fixture data from real OSM-derived data and mention attribution requirements for the latter.
- Run `python -m unittest discover -s tests -v` and `python -m compileall -q src examples/python` before committing.
