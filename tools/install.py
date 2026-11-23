#!/usr/bin/env python3
"""Copy canonical Agent Skills into project-specific host directories.

No network access. Refuses to overwrite existing content by default.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
DESTINATIONS = {
    "cursor": Path(".cursor/skills"),
    "claude": Path(".claude/skills"),
    "codex": Path(".agents/skills"),
}
RULES = {"claude": ("CLAUDE.md", "CLAUDE.md"), "cursor": ("AGENTS.md", "AGENTS.md"), "codex": ("AGENTS.md", "AGENTS.md")}


def plan_install(target: Path, agents: list[str], include_rules: bool) -> list[tuple[Path, Path]]:
    """Return source/destination pairs; callers decide whether to copy."""
    tasks: list[tuple[Path, Path]] = []
    for agent in agents:
        for source in sorted(SKILLS.iterdir()):
            if source.is_dir() and (source / "SKILL.md").is_file():
                tasks.append((source, target / DESTINATIONS[agent] / source.name))
        if include_rules:
            src_name, dst_name = RULES[agent]
            rule_pair = (ROOT / "templates" / src_name, target / dst_name)
            if rule_pair not in tasks:
                tasks.append(rule_pair)
    return tasks


def install(target: Path, agents: list[str], include_rules: bool = False, *, dry_run: bool = False, force: bool = False) -> tuple[int, int]:
    if target.exists() and not target.is_dir():
        raise ValueError(f"Target is not a directory: {target}")
    tasks = plan_install(target, agents, include_rules)
    # Check for conflicts before making *any* changes.
    conflicts = [dest for _, dest in tasks if dest.exists() or dest.is_symlink()]
    if conflicts and not force:
        raise FileExistsError("Destination(s) already exist; use --force only after review:\n" + "\n".join(map(str, conflicts)))
    if conflicts and force:
        for dest in conflicts:
            if dest.is_symlink():
                raise ValueError(f"Refusing to overwrite a symlink: {dest}")
    if not dry_run:
        target.mkdir(parents=True, exist_ok=True)
    for src, dest in tasks:
        print(f"{'WOULD COPY' if dry_run else 'COPY'} {src.relative_to(ROOT)} -> {dest}")
        if dry_run:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.is_dir():
            shutil.rmtree(dest)
        elif dest.exists():
            dest.unlink()
        if src.is_dir():
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
    return len(tasks), len(conflicts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=[*DESTINATIONS, "all"], required=True)
    parser.add_argument("--target", type=Path, required=True, help="Existing project directory, or a new local directory")
    parser.add_argument("--include-rules", action="store_true", help="Install project AGENTS.md / CLAUDE.md templates")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Replace matching destination paths only")
    args = parser.parse_args()
    agents = list(DESTINATIONS) if args.agent == "all" else [args.agent]
    try:
        total, conflicts = install(args.target.resolve(), agents, args.include_rules, dry_run=args.dry_run, force=args.force)
    except (FileExistsError, ValueError, OSError) as exc:
        print(f"Installation not completed: {exc}", file=sys.stderr)
        return 2
    print(f"{'Planned' if args.dry_run else 'Installed'} {total} item(s); {conflicts} replaced/conflicting target(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
