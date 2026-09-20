#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
ALLOWED_TAG_GROUPS = {"language", "dimension", "genre", "feature", "platform"}
REQUIRED_TAG_GROUPS = {"language", "dimension", "platform"}
FORBIDDEN_PROJECT_PARTS = {".build", ".swiftpm", "dist", "workspace", ".DS_Store"}


def fail(message: str) -> None:
    print(f"catalog error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_catalog() -> dict:
    try:
        return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot read {CATALOG_PATH.relative_to(ROOT)}: {error}")


def validate_catalog(catalog: dict) -> None:
    if catalog.get("schemaVersion") != 1:
        fail("schemaVersion must be 1")

    definitions = catalog.get("tagDefinitions")
    if not isinstance(definitions, list) or not definitions:
        fail("tagDefinitions must be a non-empty array")

    tag_groups: dict[str, str] = {}
    for definition in definitions:
        tag_id = definition.get("id")
        group = definition.get("group")
        if not isinstance(tag_id, str) or not tag_id:
            fail("every tag definition needs a non-empty id")
        if tag_id in tag_groups:
            fail(f"duplicate tag definition: {tag_id}")
        if group not in ALLOWED_TAG_GROUPS:
            fail(f"unsupported tag group for {tag_id}: {group}")
        tag_groups[tag_id] = group

    items = catalog.get("items")
    if not isinstance(items, list):
        fail("items must be an array")

    item_ids: set[str] = set()
    item_paths: set[str] = set()
    item_archives: set[str] = set()
    for item in items:
        validate_item(item, tag_groups, item_ids, item_paths, item_archives)

    print(f"catalog ok: {len(items)} items, {len(definitions)} tag definitions")


def validate_item(
    item: dict,
    tag_groups: dict[str, str],
    item_ids: set[str],
    item_paths: set[str],
    item_archives: set[str],
) -> None:
    item_id = item.get("id")
    if not isinstance(item_id, str) or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", item_id) is None:
        fail(f"invalid item id: {item_id!r}")
    if item_id in item_ids:
        fail(f"duplicate item id: {item_id}")
    item_ids.add(item_id)

    kind = item.get("kind")
    expected_root = {"example": "Examples", "sample": "Samples"}.get(kind)
    if expected_root is None:
        fail(f"{item_id}: kind must be example or sample")

    relative_path = item.get("path")
    if not isinstance(relative_path, str) or not relative_path.startswith(f"{expected_root}/"):
        fail(f"{item_id}: path must be under {expected_root}")
    if relative_path in item_paths:
        fail(f"duplicate item path: {relative_path}")
    item_paths.add(relative_path)

    project_path = ROOT / relative_path
    if not project_path.is_dir():
        fail(f"{item_id}: project directory does not exist: {relative_path}")
    if not (project_path / ".ada" / "project.json").is_file():
        fail(f"{item_id}: missing .ada/project.json")

    preview = item.get("preview")
    if not isinstance(preview, str) or not preview.startswith("Assets/Previews/"):
        fail(f"{item_id}: preview must be under Assets/Previews")
    if not (ROOT / preview).is_file():
        fail(f"{item_id}: preview does not exist: {preview}")

    archive = item.get("archive")
    if not isinstance(archive, str) or re.fullmatch(r"[A-Za-z0-9-]+\.zip", archive) is None:
        fail(f"{item_id}: archive must be a safe .zip filename")
    if archive in item_archives:
        fail(f"duplicate archive filename: {archive}")
    item_archives.add(archive)

    tags = item.get("tags")
    if not isinstance(tags, list) or not tags:
        fail(f"{item_id}: tags must be a non-empty array")
    if len(tags) != len(set(tags)):
        fail(f"{item_id}: tags must be unique")
    unknown_tags = set(tags) - set(tag_groups)
    if unknown_tags:
        fail(f"{item_id}: unknown tags: {', '.join(sorted(unknown_tags))}")
    present_groups = {tag_groups[tag] for tag in tags}
    missing_groups = REQUIRED_TAG_GROUPS - present_groups
    if missing_groups:
        fail(f"{item_id}: missing tag groups: {', '.join(sorted(missing_groups))}")

    for path in project_path.rglob("*"):
        if any(part in FORBIDDEN_PROJECT_PARTS for part in path.relative_to(project_path).parts):
            fail(f"{item_id}: forbidden generated or workspace path: {path.relative_to(ROOT)}")

    package_manifest = project_path / "Package.swift"
    if package_manifest.is_file():
        manifest = package_manifest.read_text(encoding="utf-8")
        if ".package(path:" in manifest or re.search(r'path:\s*"/', manifest):
            fail(f"{item_id}: Package.swift contains a local package dependency")


if __name__ == "__main__":
    validate_catalog(load_catalog())
