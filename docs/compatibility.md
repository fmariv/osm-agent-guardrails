# Compatibility, 2026-11-23

Agent Skills is an open filesystem convention (`SKILL.md` with YAML metadata). Different hosts use different discovery paths and loading rules; copy-based installation is intentionally explicit.

| Host | Skills folder in project | Instructions | Notes |
|---|---|---|---|
| Cursor | `.cursor/skills/` | `AGENTS.md` or Cursor rules | Skills supported in Cursor Agent; feature availability varies by version |
| Claude Code | `.claude/skills/` | `CLAUDE.md` | Uses its own command/rule conventions in addition to standard skills |
| Codex | `.agents/skills/` | `AGENTS.md` | Scans project skills; behavior depends on current Codex client |
| Generic ChatGPT | No universal project folder | Supply content or use supported skills surface | A GitHub repository is **not** automatically loaded into all chats |

Commands:

```bash
python tools/install.py --agent all --target ./my-app --dry-run
python tools/install.py --agent all --target ./my-app --include-rules
```

By default the installer will not replace existing destination files or directories. With `--force`, it replaces only matching destination skill folders and templates it is explicitly configured to install; review before using.

### Official documentation

- https://agentskills.io/specification
- https://cursor.com/docs/skills
- https://code.claude.com/docs/en/skills
- https://developers.openai.com/codex/skills
- https://agents.md/

Do not assume downstream agents will apply a skill on every relevant task. Explicitly name the skill in high-stakes or evaluation tasks and verify the resulting program.
