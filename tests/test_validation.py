from pathlib import Path
import tempfile
import unittest

from scripts.validate_skills import read_mapping, validate_links, validate_repository, validate_skill


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.skill = self.root / ".agents/skills/sample-skill"
        (self.skill / "agents").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(
            '---\nname: sample-skill\ndescription: "Investigate a specific test failure."\n---\n\nRun the relevant check.\n',
            encoding="utf-8",
        )
        (self.skill / "agents/openai.yaml").write_text(
            'interface:\n  display_name: "Sample Skill"\n'
            '  short_description: "Investigate a specific test failure"\n'
            '  default_prompt: "Use $sample-skill to investigate this failure."\n',
            encoding="utf-8",
        )

    def test_accepts_valid_skill_and_repository(self):
        self.assertEqual(validate_skill(self.skill), [])
        self.assertEqual(validate_repository(self.root), [])

    def test_rejects_missing_frontmatter(self):
        (self.skill / "SKILL.md").write_text("# No metadata\n", encoding="utf-8")
        self.assertTrue(any("frontmatter" in error for error in validate_skill(self.skill)))

    def test_rejects_directory_name_mismatch(self):
        entry = self.skill / "SKILL.md"
        entry.write_text(entry.read_text().replace("name: sample-skill", "name: other-skill"))
        self.assertTrue(any("match its directory" in error for error in validate_skill(self.skill)))

    def test_rejects_duplicate_yaml_keys(self):
        with self.assertRaisesRegex(ValueError, "duplicate YAML key"):
            read_mapping("name: first\nname: second\n")

    def test_rejects_unsafe_yaml_objects(self):
        import yaml
        with self.assertRaises(yaml.YAMLError):
            read_mapping("value: !!python/object:builtins.object {}\n")

    def test_rejects_wrong_invocation(self):
        ui = self.skill / "agents/openai.yaml"
        ui.write_text(ui.read_text().replace("$sample-skill", "$wrong-skill"))
        self.assertTrue(any("invoke its skill" in error for error in validate_skill(self.skill)))

    def test_accepts_existing_local_link_and_ignores_external_url(self):
        (self.root / "guide.md").write_text("# Guide\n")
        document = self.root / "README.md"
        document.write_text("[Guide](guide.md#section) [Web](https://example.invalid/guide)\n")
        self.assertEqual(validate_links(document, self.root), [])

    def test_rejects_missing_local_link(self):
        document = self.root / "README.md"
        document.write_text("[Missing](missing.md)\n")
        self.assertTrue(any("missing local" in error for error in validate_links(document, self.root)))

    def test_rejects_path_escape(self):
        document = self.root / "README.md"
        document.write_text("[Outside](../outside.md)\n")
        self.assertTrue(any("escapes repository" in error for error in validate_links(document, self.root)))

    def test_rejects_absolute_file_url(self):
        document = self.root / "README.md"
        document.write_text("[Local](file:///tmp/private.txt)\n")
        self.assertTrue(any("portable" in error for error in validate_links(document, self.root)))

    def test_rejects_symlink_link_escape(self):
        with tempfile.TemporaryDirectory() as other:
            secret = Path(other) / "outside.md"
            secret.write_text("outside\n")
            try:
                (self.root / "linked.md").symlink_to(secret)
            except OSError:
                self.skipTest("symlinks unavailable")
            document = self.root / "README.md"
            document.write_text("[Outside](linked.md)\n")
            self.assertTrue(any("escapes repository" in error for error in validate_links(document, self.root)))

    def test_reports_malformed_github_yaml(self):
        workflow = self.root / ".github/workflows/check.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text("jobs: [\n")
        self.assertTrue(any("check.yml" in error for error in validate_repository(self.root)))


if __name__ == "__main__":
    unittest.main()
