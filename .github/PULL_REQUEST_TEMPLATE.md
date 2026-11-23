## What problem does this solve?

Describe the OpenStreetMap/Overpass workload, the inefficient pattern being avoided, and the expected improvement. Link to an issue when available.

## Evidence and policy

Provide authoritative sources for API/policy claims and mark the date checked. Distinguish guidance for a particular instance from general recommendations.

## Verification

- [ ] `python -m unittest discover -s tests -v` passes
- [ ] `python -m osm_guard validate-skills skills` passes
- [ ] Examples/tests do not call public Overpass or OSMF tile servers
- [ ] Docs/examples use correct OSM attribution and note any ODbL requirements
- [ ] Any new network behavior is explicitly opt-in, bounded and failure-safe

## Notes for reviewers

List known limitations and follow-up work. Do not include credentials, private server logs or identifiable user data.
