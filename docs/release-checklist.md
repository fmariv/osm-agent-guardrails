# Private-to-public release checklist

- [ ] Ask the relevant OSM/Overpass maintainers whether priorities and policy language are accurate.
- [ ] Confirm repository name does not imply OSMF/OSM Spain endorsement.
- [ ] Run offline tests on Python 3.11+ and add CI logs to a release.
- [ ] Manually smoke-test with a small locally downloaded PBF file (outside CI, recording provenance and attribution).
- [ ] Verify installs on current Cursor, Claude Code and Codex versions; report exact versions and screenshots or logs.
- [ ] Run at least 10 evaluation tasks with and without skills; manually score correctness and request footprint.
- [ ] Have a reviewer audit `OverpassClient` and Overpass guidance for network edge cases before recommending production use.
- [ ] Remove confidential review notes, URLs, access keys and personally identifying data.
- [ ] Create first release tag; verify MIT, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, and ODbL notices.
- [ ] Only then switch GitHub visibility to public and invite contributions.
