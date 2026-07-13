#!/usr/bin/env python3
"""Build Prompt Architect plugin and portal-upload ZIPs."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


PLUGIN_NAME = "prompt-architect"
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
    if not re.search(r"(?m)^name:\s*prompt-architect\s*$", frontmatter):
        raise SystemExit(f"Skill name must be prompt-architect: {skill_md}")
    if not re.search(r"(?m)^description:\s*\S", frontmatter):
        raise SystemExit(f"Missing frontmatter description: {skill_md}")


def archive_names(archive_path: Path) -> set[str]:
    with zipfile.ZipFile(archive_path) as archive:
        return {entry.filename for entry in archive.infolist() if not entry.is_dir()}


def validate_plugin_archive(archive_path: Path) -> None:
    names = archive_names(archive_path)
    top_levels = {PurePosixPath(name).parts[0] for name in names}
    if top_levels != {PLUGIN_NAME}:
        raise SystemExit(f"Plugin ZIP must contain one {PLUGIN_NAME}/ top-level directory")
    required = {
        f"{PLUGIN_NAME}/.codex-plugin/plugin.json",
        f"{PLUGIN_NAME}/assets/logo.png",
        f"{PLUGIN_NAME}/skills/{PLUGIN_NAME}/SKILL.md",
        f"{PLUGIN_NAME}/skills/{PLUGIN_NAME}/agents/openai.yaml",
    }
    if missing := sorted(required - names):
        raise SystemExit(f"Plugin ZIP is missing required files: {', '.join(missing)}")


def validate_portal_archive(archive_path: Path) -> None:
    names = archive_names(archive_path)
    expected = {
        f"{PLUGIN_NAME}/SKILL.md",
        f"{PLUGIN_NAME}/agents/openai.yaml",
    }
    if names != expected:
        raise SystemExit(
            "Portal ZIP must contain only the final Prompt Architect skill tree; "
            f"found: {', '.join(sorted(names))}"
        )


def make_archive(source_parent: Path, base_dir: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.unlink(missing_ok=True)
    shutil.make_archive(
        str(destination.with_suffix("")),
        "zip",
        root_dir=source_parent,
        base_dir=base_dir,
    )


def build(version: str, output_dir: Path) -> tuple[Path, Path]:
    if SEMVER.fullmatch(version) is None:
        raise SystemExit(f"Version must be strict semver without a leading v: {version}")

    repo_root = Path(__file__).resolve().parent.parent
    template_root = repo_root / ".plugin" / "package" / PLUGIN_NAME
    skill_source = repo_root / PLUGIN_NAME
    manifest_source = template_root / ".codex-plugin" / "plugin.json"
    logo_source = template_root / "assets" / "logo.png"
    validate_skill(skill_source)
    if not manifest_source.is_file():
        raise SystemExit(f"Missing plugin manifest: {manifest_source}")
    if not logo_source.is_file():
        raise SystemExit(f"Missing plugin logo: {logo_source}")

    output_root = (repo_root / output_dir).resolve()
    plugin_archive = output_root / "plugin" / f"{PLUGIN_NAME}-{version}.zip"
    portal_archive = output_root / "portal" / f"{PLUGIN_NAME}.zip"

    with tempfile.TemporaryDirectory(prefix=f"{PLUGIN_NAME}-") as temporary:
        temporary_root = Path(temporary)
        plugin_root = temporary_root / "plugin" / PLUGIN_NAME
        shutil.copytree(template_root, plugin_root)
        shutil.copytree(
            skill_source,
            plugin_root / "skills" / PLUGIN_NAME,
            ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
        )

        manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
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
        make_archive(plugin_root.parent, PLUGIN_NAME, plugin_archive)

        portal_root = temporary_root / "portal" / PLUGIN_NAME
        shutil.copytree(
            skill_source,
            portal_root,
            ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"),
        )
        make_archive(portal_root.parent, PLUGIN_NAME, portal_archive)

    validate_plugin_archive(plugin_archive)
    validate_portal_archive(portal_archive)
    print(f"Plugin package: {plugin_archive}")
    print(f"Portal skill bundle: {portal_archive}")
    return plugin_archive, portal_archive


if __name__ == "__main__":
    options = parse_args()
    build(options.version, options.output_dir)
