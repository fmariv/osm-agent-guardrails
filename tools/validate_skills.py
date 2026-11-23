#!/usr/bin/env python3
"""Offline Agent Skills metadata and local reference validator (stdlib only)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK = re.compile(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)")


def validate_skill(folder: Path) -> list[str]:
    errors: list[str] = []
    p = folder / "SKILL.md"
    if not p.is_file():
        return [f"{folder}: missing SKILL.md"]
    content = p.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return [f"{p}: missing YAML frontmatter"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return [f"{p}: missing frontmatter closing ---"]
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line or line.startswith(" ") or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"{p}: invalid top-level frontmatter line {line!r}")
            continue
        key, value = line.split(":", 1)
        if key in fields:
            errors.append(f"{p}: duplicate field {key}")
        fields[key] = value.strip().strip('"\'')
    for key in ("name", "description"):
        if not fields.get(key):
            errors.append(f"{p}: missing {key}")
    name = fields.get("name", "")
    if not NAME.fullmatch(name) or len(name) > 64 or name != folder.name:
        errors.append(f"{p}: invalid/mismatching name {name!r}")
    if len(fields.get("description", "")) > 1024:
        errors.append(f"{p}: description >1024 chars")
    if len(fields.get("compatibility", "")) > 500:
        errors.append(f"{p}: compatibility >500 chars")
    for key in fields.keys() - ALLOWED_FIELDS:
        errors.append(f"{p}: unsupported frontmatter key {key}")
    if not any(line.strip().startswith("# ") for line in lines[end+1:]):
        errors.append(f"{p}: body missing a title")
    # Only validate relative links that must remain valid after a skill is installed on its own.
    for f in folder.rglob("*.md"):
        raw = f.read_text(encoding="utf-8")
        # Ignore fenced code blocks: Overpass QL tag filters resemble Markdown links.
        prose = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$", "", raw)
        for link in MD_LINK.findall(prose):
            if "://" in link or link.startswith(("mailto:", "#")):
                continue
            target = (f.parent / link).resolve()
            if not target.exists():
                errors.append(f"{f}: broken link {link}")
            elif not target.is_relative_to(folder.resolve()):
                errors.append(f"{f}: non-portable cross-skill/repo link {link}")
    return errors


def main() -> int:
    errors: list[str] = []
    folders = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    for folder in folders:
        errors.extend(validate_skill(folder))
    if not folders:
        errors.append("No skill folders found")
    if errors:
        print("Skill validation FAILED:\n" + "\n".join(f"- {e}" for e in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(folders)} skills, their metadata and portable local links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
