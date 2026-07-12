#!/usr/bin/env python3
"""Build the release ZIP for the Prompt Architect & friends plugin."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path


PLUGIN_NAME = "prompt-architect-friends"
SKILLS = (
    "bootstrap-project",
    "challenge-me",
    "close-thread",
    "prompt-architect",
)
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Strict semver without a leading v")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    return parser.parse_args()


def validate_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"Missing required skill file: {skill_md}")
    contents = skill_md.read_text(encoding="utf-8")
    if not contents.startswith("---\n") or "\n---\n" not in contents[4:]:
        raise SystemExit(f"Invalid YAML frontmatter boundaries: {skill_md}")
    frontmatter = contents.split("\n---\n", 1)[0][4:]
    if not re.search(r"(?m)^name:\s*\S", frontmatter):
        raise SystemExit(f"Missing frontmatter name: {skill_md}")
    if not re.search(r"(?m)^description:\s*\S", frontmatter):
        raise SystemExit(f"Missing frontmatter description: {skill_md}")


def build(version: str, output_dir: Path) -> Path:
    if SEMVER.fullmatch(version) is None:
        raise SystemExit(f"Version must be strict semver without a leading v: {version}")

    repo_root = Path(__file__).resolve().parent.parent
    template_root = repo_root / "store-package" / PLUGIN_NAME
    manifest_source = template_root / ".codex-plugin" / "plugin.json"
    if not manifest_source.is_file():
        raise SystemExit(f"Missing plugin manifest: {manifest_source}")

    output_dir = (repo_root / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_base = output_dir / f"{PLUGIN_NAME}-{version}"
    archive_path = Path(f"{archive_base}.zip")
    archive_path.unlink(missing_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"{PLUGIN_NAME}-") as temporary:
        package_root = Path(temporary) / PLUGIN_NAME
        shutil.copytree(template_root, package_root)

        skills_root = package_root / "skills"
        skills_root.mkdir(exist_ok=True)
        for skill_name in SKILLS:
            source = repo_root / skill_name
            validate_skill(source)
            shutil.copytree(
                source,
                skills_root / skill_name,
                ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
            )

        manifest_path = package_root / ".codex-plugin" / "plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = version
        if manifest.get("name") != PLUGIN_NAME:
            raise SystemExit("Plugin manifest name does not match the package name")
        if manifest.get("skills") != "./skills/":
            raise SystemExit("Plugin manifest must point skills to ./skills/")
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        shutil.make_archive(str(archive_base), "zip", root_dir=package_root)

    print(archive_path)
    return archive_path


if __name__ == "__main__":
    options = parse_args()
    build(options.version, options.output_dir)
