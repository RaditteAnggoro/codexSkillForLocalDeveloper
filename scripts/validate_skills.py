"""Validate skill metadata and repository-local references without network access."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject ambiguous duplicate mapping keys while retaining SafeLoader behaviour."""


def _unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, (str, int, float, bool, type(None))):
            raise ValueError("YAML mapping keys must be scalar values")
        if key in result:
            raise ValueError("duplicate YAML key: {!r}".format(key))
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|$)", re.DOTALL)
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s)]+)")
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
IGNORED = {".git", ".venv", "venv", "dist", "__pycache__", ".pytest_cache"}


def read_mapping(text):
    value = yaml.load(text, Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError("expected a YAML mapping")
    return value


def inside(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def validate_skill(directory):
    errors = []
    entry = directory / "SKILL.md"
    try:
        if entry.is_symlink() or (directory / "agents").is_symlink() or (directory / "agents/openai.yaml").is_symlink():
            raise ValueError("skill metadata must not be a symlink")
        text = entry.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if match is None:
            raise ValueError("SKILL.md must start with YAML frontmatter")
        metadata = read_mapping(match.group(1))
        name = metadata.get("name")
        if not isinstance(name, str) or not NAME.fullmatch(name) or len(name) > 64:
            errors.append("invalid skill name")
        elif name != directory.name:
            errors.append("skill name must match its directory")
        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append("description must be a nonempty string")
        elif len(description) > 1024 or "<" in description or ">" in description:
            errors.append("description must fit 1024 characters and contain no angle brackets")
        if not text[match.end():].strip():
            errors.append("skill body is empty")
        if "[TODO:" in text:
            errors.append("unfinished scaffold placeholder")

        ui = read_mapping((directory / "agents/openai.yaml").read_text(encoding="utf-8"))
        interface = ui.get("interface")
        if not isinstance(interface, dict):
            raise ValueError("agents/openai.yaml requires an interface mapping")
        display_name = interface.get("display_name")
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append("UI display_name must be a nonempty string")
        short = interface.get("short_description")
        if not isinstance(short, str) or not 25 <= len(short) <= 64:
            errors.append("UI short_description must contain 25 to 64 characters")
        prompt = interface.get("default_prompt")
        if not isinstance(prompt, str) or "$" + str(name) not in prompt:
            errors.append("UI default_prompt must invoke its skill")
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        errors.append(str(exc))
    return ["{}: {}".format(directory.name, error) for error in errors]


def validate_links(document, root):
    if not inside(document, root):
        return ["document is outside repository: {}".format(document.name)]
    errors = []
    try:
        text = document.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [str(exc)]
    for raw in LINK.findall(text):
        target = raw.strip("<>")
        try:
            parsed = urlsplit(target)
        except ValueError:
            errors.append("malformed link target: {}".format(target))
            continue
        if parsed.scheme in {"https", "http", "mailto", "tel"}:
            continue
        if parsed.scheme or parsed.netloc or target.startswith("/"):
            errors.append("use a portable repository-relative link: {}".format(target))
            continue
        if not parsed.path:
            continue
        destination = document.parent / unquote(parsed.path)
        if not inside(destination, root):
            errors.append("local link escapes repository: {}".format(target))
        elif not destination.exists():
            errors.append("missing local link target: {}".format(target))
    return ["{}: {}".format(document.relative_to(root), error) for error in errors]


def validate_repository(root):
    root = root.resolve()
    skills_root = root / ".agents/skills"
    if not skills_root.is_dir():
        return ["missing .agents/skills directory"]
    directories = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if not directories:
        return ["no skills found"]
    errors = []
    for directory in directories:
        if not inside(directory, root):
            errors.append("skill directory escapes repository: {}".format(directory.name))
            continue
        errors.extend(validate_skill(directory))
    for path in sorted(root.rglob("*.md")):
        parts = path.relative_to(root).parts
        if any(part in IGNORED for part in parts):
            continue
        if parts[:2] == (".agents", "artifacts"):
            continue
        errors.extend(validate_links(path, root))
    for pattern in ("*.yml", "*.yaml"):
        for path in sorted((root / ".github").rglob(pattern)):
            try:
                if not inside(path, root):
                    raise ValueError("YAML path escapes repository")
                read_mapping(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
                errors.append("{}: {}".format(path.relative_to(root), exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = validate_repository(args.root)
    if errors:
        for error in errors:
            print("FAIL " + error, file=sys.stderr)
        return 1
    count = sum(path.is_dir() for path in (args.root / ".agents/skills").iterdir())
    print("Validated {} skills, UI metadata, GitHub YAML, and local links.".format(count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
