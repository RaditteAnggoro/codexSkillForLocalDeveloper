import hashlib
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from scripts.build_release import PATHS, build_release, collect_files


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        for name in PATHS[:5]:
            (self.root / name).mkdir(parents=True)
        for name in PATHS[5:]:
            (self.root / name).write_text("example\n", encoding="utf-8")
        (self.root / "VERSION").write_text("0.1.0\n")
        sample = self.root / ".agents/skills/example/SKILL.md"
        sample.parent.mkdir(parents=True)
        sample.write_text("example skill\n")

    def test_archive_includes_hidden_skills_and_checksum(self):
        archive, checksum, count = build_release(self.root)
        with ZipFile(archive) as bundle:
            self.assertIn("codex-developer-skills-0.1.0/.agents/skills/example/SKILL.md", bundle.namelist())
            self.assertEqual(len(bundle.namelist()), count)
            self.assertIsNone(bundle.testzip())
        expected = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.assertEqual(checksum.read_text().split()[0], expected)

    def test_excludes_local_and_sensitive_files(self):
        for name in (".git/config", ".venv/lib/local.py", ".agents/artifacts/task/private.md", "docs/.DS_Store", "scripts/__pycache__/cache.pyc", "docs/.env", "docs/token.key"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("not distributable\n")
        files = [path.relative_to(self.root).as_posix() for path in collect_files(self.root)]
        self.assertFalse(any(".git/" in name or ".venv/" in name or "artifacts/" in name for name in files))
        self.assertNotIn("docs/.DS_Store", files)
        self.assertNotIn("scripts/__pycache__/cache.pyc", files)
        self.assertNotIn("docs/.env", files)
        self.assertNotIn("docs/token.key", files)

    def test_archive_is_reproducible(self):
        first, _, _ = build_release(self.root)
        data = first.read_bytes()
        second, _, _ = build_release(self.root)
        self.assertEqual(data, second.read_bytes())

    def test_rejects_invalid_version(self):
        (self.root / "VERSION").write_text("../outside\n")
        with self.assertRaisesRegex(ValueError, "VERSION"):
            build_release(self.root)

    def test_rejects_missing_distribution_file(self):
        (self.root / "LICENSE").unlink()
        with self.assertRaisesRegex(ValueError, "missing distribution path"):
            collect_files(self.root)

    def test_rejects_symlink_source(self):
        target = self.root / "docs/guide.md"
        target.write_text("guide\n")
        try:
            (self.root / "docs/alias.md").symlink_to(target)
        except OSError:
            self.skipTest("symlinks unavailable")
        with self.assertRaisesRegex(ValueError, "symlink"):
            collect_files(self.root)


if __name__ == "__main__":
    unittest.main()
