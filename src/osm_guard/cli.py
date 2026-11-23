"""CLI for source guidance, static lint, and Agent Skill validation."""

import argparse
import json
from pathlib import Path

from .lint import scan_text
from .skills_validation import validate_skills
from .sources import Workload, recommend


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="osm-guard", description="Offline guidance for respectful OSM applications")
    sub = parser.add_subparsers(dest="command", required=True)
    choice = sub.add_parser("recommend", help="Conservative source guidance (no network)")
    choice.add_argument("--workflow", choices=["one-off", "scheduled", "interactive", "bulk"], default="one-off")
    choice.add_argument("--area-km2", type=float, default=1.0)
    choice.add_argument("--daily-runs", type=int, default=1)
    choice.add_argument("--users", type=int, default=1)
    choice.add_argument("--basemap", action="store_true")
    choice.add_argument("--strict-sla", action="store_true")
    lint = sub.add_parser("lint", help="Scan code/text for obvious misuse patterns (advisory)")
    lint.add_argument("files", nargs="+", type=Path)
    validator = sub.add_parser("validate-skills", help="Check basic SKILL.md structure")
    validator.add_argument("root", nargs="?", type=Path, default=Path("skills"))
    args = parser.parse_args(argv)

    if args.command == "recommend":
        try:
            advice = recommend(Workload(
                workflow=args.workflow,
                area_km2=args.area_km2,
                daily_runs=args.daily_runs,
                users=args.users,
                needs_basemap=args.basemap,
                strict_sla=args.strict_sla,
            ))
        except ValueError as exc:
            parser.error(str(exc))
        print(json.dumps({"recommendation": advice.source.value, "reasons": advice.reasons, "caveat": advice.caveat}, indent=2))
        return 0

    if args.command == "lint":
        issues = 0
        for file in args.files:
            if not file.is_file():
                print(f"{file}: file not found")
                issues += 1
                continue
            for f in scan_text(file.read_text(encoding="utf-8")):
                print(f"{file}:{f.line}: {f.severity}: {f.rule}: {f.message}")
                if f.severity == "warning":
                    issues += 1
        if not issues:
            print("No obvious warning patterns found (this does NOT prove safety).")
        return 1 if issues else 0

    if args.command == "validate-skills":
        errors = validate_skills(args.root)
        for error in errors:
            print(error)
        if errors:
            return 1
        print(f"Skill structure checks passed: {args.root}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
