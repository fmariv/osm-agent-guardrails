# Rename plan: `osm-agents-skills` → `osm-agent-guardrails`

Project display name is now **OSM Agent Guardrails**. The current GitHub repository slug is still `fmariv/osm-agents-skills` until its owner renames it.

GitHub UI steps (repository administrator):

1. Open `https://github.com/fmariv/osm-agents-skills/settings`.
2. In **General → Repository name**, change it to `osm-agent-guardrails`, then confirm **Rename**.
3. Verify that `https://github.com/fmariv/osm-agent-guardrails` resolves and the visibility remains as intended.
4. Check the canonical default-branch links, GitHub Actions, repository description, issue templates and any secrets or external webhooks.
5. For local clones, run `git remote set-url origin https://github.com/fmariv/osm-agent-guardrails.git`.
6. Replace installation URLs in `README.md` and related docs after confirmation. Do not assume all third-party package managers follow GitHub redirects.

This instruction document is intentionally safe before the rename: it does not silently replace the current working installation URL with an unreachable one. The GitHub app connector used here does not expose a repository rename operation, so the admin UI step is required.
