"""Build a deterministic source archive from an explicit distribution allowlist."""

import argparse
import hashlib
from pathlib import Path
import re
import sys
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED


PATHS = (
    ".agents/skills", ".github", "docs", "scripts", "tests",
    "AGENTS.md", "AGENTS.snippet.md", "README.md", "LICENSE", "VERSION",
    "CHANGELOG.md", "CONTRIBUTING.md", "SECURITY.md", ".gitignore",
    ".gitattributes", "requirements-dev.txt",
)
EXCLUDED = {".git", ".venv", "venv", "__pycache__", ".DS_Store", "Thumbs.db"}


def collect_files(root):
    root = root.resolve()
    files = []
    for relative in PATHS:
        path = root / relative
        if not path.exists():
            raise ValueError("missing distribution path: {}".format(relative))
        try:
            path.resolve().relative_to(root)
        except ValueError:
            raise ValueError("distribution path escapes repository: {}".format(relative))
        if path.is_symlink():
            raise ValueError("distribution contains a symlink: {}".format(relative))
        candidates = path.rglob("*") if path.is_dir() else [path]
        for candidate in candidates:
            parts = candidate.relative_to(root).parts
            if any(part in EXCLUDED for part in parts):
                continue
            if candidate.is_symlink():
                raise ValueError("distribution contains a symlink: {}".format(candidate.relative_to(root)))
            if not candidate.is_file():
                continue
            if candidate.name.startswith(".env") or candidate.suffix in {".key", ".pem", ".pyc"}:
                continue
            files.append(candidate)
    return sorted(set(files))


def build_release(root):
    root = root.resolve()
    version = (root / "VERSION").read_text(encoding="utf-8").strip()
    if re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version) is None:
        raise ValueError("VERSION must use MAJOR.MINOR.PATCH")
    files = collect_files(root)
    output = root / "dist"
    if output.is_symlink():
        raise ValueError("dist must not be a symlink")
    output.mkdir(exist_ok=True)
    stem = "codex-developer-skills-" + version
    archive = output / (stem + ".zip")
    checksum = output / (stem + ".zip.sha256")
    if archive.is_symlink() or checksum.is_symlink():
        raise ValueError("distribution output must not be a symlink")
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        for source in files:
            name = stem + "/" + source.relative_to(root).as_posix()
            info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum.write_text(digest + "  " + archive.name + "\n", encoding="utf-8")
    return archive, checksum, len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        archive, checksum, count = build_release(args.root)
    except (OSError, ValueError) as exc:
        print("Build failed: {}".format(exc), file=sys.stderr)
        return 1
    print("Built {} ({} files)".format(archive.name, count))
    print("Checksum: {}".format(checksum.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
