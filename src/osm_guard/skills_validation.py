"""Dependency-free basic checks for portable Agent Skill folders."""

from pathlib import Path
import re


def validate_skills(root: Path) -> list[str]:
    errors: list[str] = []
    skill_dirs = [p for p in root.iterdir() if p.is_dir()] if root.is_dir() else []
    if not skill_dirs:
        return [f"No skill directories under {root}"]
    for directory in sorted(skill_dirs):
        file = directory / "SKILL.md"
        if not file.is_file():
            errors.append(f"{file}: missing SKILL.md")
            continue
        text = file.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
        if match is None:
            errors.append(f"{file}: missing YAML frontmatter")
            continue
        frontmatter = match.group(1)
        name = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
        description = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        if name is None or name.group(1) != directory.name:
            errors.append(f"{file}: name must match directory")
        elif len(name.group(1)) > 64 or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1)) is None:
            errors.append(f"{file}: name must be kebab-case and at most 64 characters")
        if description is None or len(description.group(1).strip()) < 30:
            errors.append(f"{file}: description missing or too short")
        elif len(description.group(1).strip()) > 1024:
            errors.append(f"{file}: description exceeds 1024 characters")
        if not text[match.end():].strip():
            errors.append(f"{file}: empty skill instructions")
    return errors
