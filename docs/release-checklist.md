# Public preview / stable release checklist

- [ ] Ask relevant OSM/Overpass maintainers for input; do not claim endorsement until confirmed.
- [ ] Confirm repository name does not imply OSMF/OSM Spain endorsement.
- [x] Run offline tests on the available local Python 3.13 runtime (32+ tests) and verify package build.
- [ ] Confirm GitHub CI success across Python 3.11, 3.12 and 3.13 before declaring stable.
- [ ] Manually smoke-test with a small locally downloaded PBF file (outside CI, recording provenance and attribution).
- [ ] Verify installs on current Cursor, Claude Code and Codex versions; report exact versions and screenshots or logs.
- [ ] Run at least 10 evaluation tasks with and without skills; manually score correctness and request footprint.
- [ ] Have a reviewer audit `OverpassClient` and Overpass guidance for network edge cases before recommending production use.
- [ ] Remove confidential review notes, URLs, access keys and personally identifying data.
- [ ] Create first release tag; verify MIT, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, and ODbL notices.
- [ ] Before switching visibility, check for secrets and licensing issues and mark the project as an experimental preview.
- [ ] Before declaring a stable release, complete the agent compatibility, PBF and external review steps above.
