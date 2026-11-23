import unittest
from pathlib import Path

from osm_guard.skills_validation import validate_skills


ROOT = Path(__file__).resolve().parents[1]


class TestSkills(unittest.TestCase):
    def test_skill_structure(self):
        self.assertEqual(validate_skills(ROOT / 'skills'), [])

    def test_expected_five_skills(self):
        names = {p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()}
        self.assertEqual(names, {
            'osm-source-selection', 'overpass-query-safety',
            'overpass-client-design', 'osm-local-extracts', 'osm-web-maps',
        })


if __name__ == "__main__":
    unittest.main()


class TestOfflineInstaller(unittest.TestCase):
    def test_one_install_copies_five_skills_per_agent(self):
        import importlib.util
        import tempfile
        installer_file = ROOT / "tools" / "install.py"
        spec = importlib.util.spec_from_file_location("local_skill_installer", installer_file)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as root:
            target = Path(root) / "my-project"
            total, conflicts = module.install(target, ["cursor", "claude", "codex"], include_rules=True)
            self.assertEqual(total, 17)  # 15 skill copies + AGENTS.md + CLAUDE.md
            self.assertEqual(conflicts, 0)
            for subdir in (".cursor/skills", ".claude/skills", ".agents/skills"):
                self.assertEqual(len(list((target / subdir).glob("*/SKILL.md"))), 5)
            self.assertTrue((target / 'AGENTS.md').exists())
            self.assertTrue((target / 'CLAUDE.md').exists())
            with self.assertRaises(FileExistsError):
                module.install(target, ["cursor"], include_rules=False)


class TestSkillValidatorNegativeCases(unittest.TestCase):
    def test_bad_skill_names_are_rejected(self):
        import tempfile
        for invalid in ("InvalidName", "invalid--name"):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as root:
                folder = Path(root) / invalid
                folder.mkdir()
                (folder / "SKILL.md").write_text(
                    f"---\nname: {invalid}\ndescription: This is an adequately long test description.\n---\nHello\n",
                    encoding="utf-8",
                )
                self.assertTrue(validate_skills(Path(root)))

    def test_missing_skill_file_is_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / "missing").mkdir()
            self.assertTrue(validate_skills(Path(root)))

class TestOfflineInstallerSafety(unittest.TestCase):
    def test_dry_run_creates_nothing(self):
        import importlib.util
        import tempfile
        spec = importlib.util.spec_from_file_location("local_skill_installer", ROOT / "tools" / "install.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as root:
            dest = Path(root) / "new"
            module.install(dest, ["codex"], include_rules=True, dry_run=True)
            self.assertFalse(dest.exists())

    def test_existing_rules_never_overwritten_by_default(self):
        import importlib.util
        import tempfile
        spec = importlib.util.spec_from_file_location("local_skill_installer", ROOT / "tools" / "install.py")
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as root:
            dest = Path(root)
            (dest / "AGENTS.md").write_text("my important rules", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                module.install(dest, ["cursor"], include_rules=True)
            self.assertEqual((dest / "AGENTS.md").read_text(), "my important rules")
            self.assertFalse((dest / ".cursor").exists())
