#!/usr/bin/env python3
"""Validate the Prompt Architect plugin directory or finished ZIP archive."""

from __future__ import annotations

import argparse
import json
import re
import stat
import struct
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

import yaml


PLUGIN_NAME = "prompt-architect"
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
TOP_LEVEL_FIELDS = {
    "id", "name", "version", "description", "skills", "apps", "mcpServers",
    "interface", "author", "homepage", "repository", "license", "keywords",
}
INTERFACE_FIELDS = {
    "displayName", "shortDescription", "longDescription", "developerName",
    "category", "capabilities", "websiteURL", "privacyPolicyURL",
    "termsOfServiceURL", "brandColor", "composerIcon", "logo", "logoDark",
    "screenshots", "defaultPrompt", "default_prompt",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--plugin-root", type=Path)
    group.add_argument("--archive", type=Path)
    parser.add_argument("--expected-version", required=True)
    return parser.parse_args()


def fail(message: str) -> None:
    raise SystemExit(f"Plugin validation failed: {message}")


def require_string(payload: dict[str, Any], key: str, prefix: str = "") -> str:
    value = payload.get(key)
    field = f"{prefix}.{key}" if prefix else key
    if not isinstance(value, str) or not value.strip():
        fail(f"`{field}` must be a non-empty string")
    return value


def validate_https_url(value: Any, field: str) -> None:
    parsed = urlparse(value) if isinstance(value, str) else None
    if parsed is None or parsed.scheme != "https" or not parsed.netloc:
        fail(f"`{field}` must be an absolute HTTPS URL")


def validate_required_image(plugin_root: Path, interface: dict[str, Any], field: str) -> None:
    relative = require_string(interface, field, "interface")
    path = PurePosixPath(relative)
    if not relative.startswith("./") or path.is_absolute() or ".." in path.parts:
        fail(f"`interface.{field}` must be a safe `./`-relative path")
    image_path = (plugin_root / relative).resolve()
    if plugin_root not in image_path.parents or not image_path.is_file():
        fail(f"`interface.{field}` must reference an image inside the plugin")
    header = image_path.read_bytes()[:26]
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        fail(f"`interface.{field}` must reference a PNG image")
    width, height = struct.unpack(">II", header[16:24])
    if width == 0 or width != height:
        fail(f"`interface.{field}` must reference a non-empty square image")
    bit_depth, color_type = header[24:26]
    if bit_depth != 8 or color_type != 6:
        fail(f"`interface.{field}` must reference an 8-bit RGBA PNG")


def validate_manifest(plugin_root: Path, expected_version: str) -> None:
    if plugin_root.name != PLUGIN_NAME:
        fail(f"plugin root must be named `{PLUGIN_NAME}`")

    manifest_path = plugin_root / ".codex-plugin" / "plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail("missing `.codex-plugin/plugin.json`")
    except json.JSONDecodeError as error:
        fail(f"plugin manifest is not valid JSON: {error}")

    if not isinstance(manifest, dict):
        fail("plugin manifest must contain a JSON object")
    unknown = sorted(set(manifest) - TOP_LEVEL_FIELDS)
    if unknown:
        fail(f"unsupported manifest fields: {', '.join(unknown)}")
    if "[TODO:" in json.dumps(manifest):
        fail("plugin manifest contains a TODO placeholder")

    name = require_string(manifest, "name")
    if name != PLUGIN_NAME or not KEBAB_RE.fullmatch(name):
        fail(f"`name` must be `{PLUGIN_NAME}`")
    version = require_string(manifest, "version")
    if version != expected_version or not SEMVER_RE.fullmatch(version):
        fail(f"`version` must be strict SemVer `{expected_version}`")
    require_string(manifest, "description")

    author = manifest.get("author")
    if not isinstance(author, dict):
        fail("`author` must be an object")
    if set(author) - {"name", "email", "url"}:
        fail("`author` contains unsupported fields")
    require_string(author, "name", "author")
    if "url" in author:
        validate_https_url(author["url"], "author.url")

    if manifest.get("skills") != "./skills/":
        fail("`skills` must be `./skills/`")
    for field in ("homepage", "repository"):
        if field in manifest:
            validate_https_url(manifest[field], field)

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        fail("`interface` must be an object")
    unknown = sorted(set(interface) - INTERFACE_FIELDS)
    if unknown:
        fail(f"unsupported interface fields: {', '.join(unknown)}")
    for field in (
        "displayName", "shortDescription", "longDescription", "developerName", "category",
    ):
        require_string(interface, field, "interface")
    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities or not all(
        isinstance(item, str) and item.strip() for item in capabilities
    ):
        fail("`interface.capabilities` must be a non-empty string array")
    prompts = interface.get("defaultPrompt", interface.get("default_prompt"))
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail("`interface.defaultPrompt` must contain one to three prompts")
    if not all(isinstance(prompt, str) and 0 < len(prompt) <= 128 for prompt in prompts):
        fail("each default prompt must contain 1-128 characters")
    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        if field in interface:
            validate_https_url(interface[field], f"interface.{field}")
    if "brandColor" in interface and not HEX_COLOR_RE.fullmatch(interface["brandColor"]):
        fail("`interface.brandColor` must use `#RRGGBB`")
    for field in ("composerIcon", "logo"):
        validate_required_image(plugin_root, interface, field)

    skills_root = plugin_root / "skills"
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if [path.name for path in skill_dirs] != [PLUGIN_NAME]:
        fail(f"skills directory must contain only `{PLUGIN_NAME}`")
    skill_path = skill_dirs[0] / "SKILL.md"
    skill_text = skill_path.read_text(encoding="utf-8")
    if not skill_text.startswith("---\n") or "\n---\n" not in skill_text[4:]:
        fail("SKILL.md must start with YAML frontmatter")
    frontmatter_text = skill_text.split("\n---\n", 1)[0][4:]
    frontmatter = yaml.safe_load(frontmatter_text)
    if not isinstance(frontmatter, dict):
        fail("SKILL.md frontmatter must be an object")
    if set(frontmatter) != {"name", "description"}:
        fail("SKILL.md frontmatter must contain only `name` and `description`")
    if frontmatter.get("name") != PLUGIN_NAME:
        fail(f"SKILL.md name must be `{PLUGIN_NAME}`")
    if not isinstance(frontmatter.get("description"), str) or not frontmatter["description"].strip():
        fail("SKILL.md description must be a non-empty string")


def validate_archive(archive: Path, expected_version: str) -> None:
    if not zipfile.is_zipfile(archive):
        fail("output is not a readable ZIP archive")
    with zipfile.ZipFile(archive) as bundle:
        entries = bundle.infolist()
        names = [entry.filename for entry in entries]
        if len(names) != len(set(names)):
            fail("ZIP contains duplicate entries")
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in entry.filename:
                fail(f"unsafe ZIP path: {entry.filename}")
            if stat.S_ISLNK(entry.external_attr >> 16):
                fail(f"ZIP contains a symbolic link: {entry.filename}")
        top_levels = {PurePosixPath(name).parts[0] for name in names if name}
        if top_levels != {PLUGIN_NAME}:
            fail(f"ZIP must contain exactly one `{PLUGIN_NAME}` top-level directory")
        required = {
            f"{PLUGIN_NAME}/.codex-plugin/plugin.json",
            f"{PLUGIN_NAME}/assets/icon.png",
            f"{PLUGIN_NAME}/skills/{PLUGIN_NAME}/SKILL.md",
        }
        if not required.issubset(names):
            fail("ZIP is missing the plugin manifest, icon, or SKILL.md")
        with tempfile.TemporaryDirectory() as directory:
            bundle.extractall(directory)
            validate_manifest(Path(directory) / PLUGIN_NAME, expected_version)


def main() -> None:
    args = parse_args()
    if args.plugin_root:
        validate_manifest(args.plugin_root.resolve(), args.expected_version)
    else:
        validate_archive(args.archive.resolve(), args.expected_version)
    print("Prompt Architect plugin validation passed")


if __name__ == "__main__":
    main()
