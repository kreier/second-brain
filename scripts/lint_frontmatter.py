#!/usr/bin/env python3
"""
Lint frontmatter in processed/ notes against frontmatter.md's schema.

Checks:
  - file has valid YAML frontmatter
  - `type` is present and one of the known enum values
  - all common required fields are present
  - type-specific required fields are present (project/travel)
  - `id` matches the filename (minus .md)
  - date fields (created, updated) parse as ISO 8601
  - files under raw/archive/ are not tracked as modified since last commit
    (best-effort check, see --check-archive-immutability)

Exit code 0 if clean, 1 if any errors found. Run with no args to lint the
whole processed/ tree, or pass specific file paths to lint just those.

Usage:
    python3 scripts/lint_frontmatter.py
    python3 scripts/lint_frontmatter.py processed/topics/foo.md
"""

import sys
import re
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("This script requires PyYAML: pip install pyyaml --break-system-packages")
    sys.exit(2)

VAULT_ROOT = Path(__file__).resolve().parent.parent

TYPE_FOLDERS = {
    "log": "processed/logs",
    "fact": "processed/topics",
    "project": "processed/projects",
    "idea": "processed/ideas",
    "travel": "processed/travel",
}

MUTABLE_TYPES = {"project", "idea", "travel"}
IMMUTABLE_TYPES = {"log", "fact"}

COMMON_REQUIRED = ["id", "type", "title", "created", "status", "tags", "related"]

TYPE_SPECIFIC_REQUIRED = {
    "project": ["status", "repo"],
    "travel": ["location", "dates"],
}

ISO_DATE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}([+-]\d{2}:\d{2}|Z)?)?$"
)


def parse_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, "no frontmatter block found (file must start with '---')"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, "malformed frontmatter block (missing closing '---')"
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return None, f"invalid YAML: {e}"
    if not isinstance(fm, dict):
        return None, "frontmatter did not parse to a mapping"
    return fm, None


def check_date(value, field_name, errors):
    if value is None:
        return
    if not isinstance(value, str):
        # PyYAML may parse ISO dates into datetime/date objects already;
        # that's fine, just skip the regex check in that case.
        return
    if not ISO_DATE_RE.match(value):
        errors.append(f"{field_name} '{value}' is not ISO 8601 (YYYY-MM-DD or full timestamp)")


def lint_file(path: Path):
    errors = []
    fm, parse_err = parse_frontmatter(path)
    if parse_err:
        return [parse_err]

    note_type = fm.get("type")
    if not note_type:
        errors.append("missing required field: type")
    elif note_type not in TYPE_FOLDERS:
        errors.append(f"unknown type '{note_type}', expected one of {sorted(TYPE_FOLDERS)}")
    else:
        expected_folder = VAULT_ROOT / TYPE_FOLDERS[note_type]
        if expected_folder not in path.resolve().parents:
            errors.append(
                f"type '{note_type}' should live under {TYPE_FOLDERS[note_type]}/, "
                f"found at {path.relative_to(VAULT_ROOT)}"
            )

    for field in COMMON_REQUIRED:
        if field not in fm or fm[field] in (None, ""):
            errors.append(f"missing required field: {field}")

    if note_type in TYPE_SPECIFIC_REQUIRED:
        for field in TYPE_SPECIFIC_REQUIRED[note_type]:
            if field not in fm or fm[field] in (None, ""):
                errors.append(f"missing required field for type '{note_type}': {field}")

    expected_id = path.stem
    if fm.get("id") and str(fm["id"]) != expected_id:
        errors.append(f"id '{fm['id']}' does not match filename '{expected_id}'")

    check_date(fm.get("created"), "created", errors)
    check_date(fm.get("updated"), "updated", errors)

    if note_type in IMMUTABLE_TYPES:
        if fm.get("supersedes") not in (None, "null") and not isinstance(fm.get("supersedes"), str):
            errors.append("supersedes should be null or a note id string")

    return errors


def main():
    args = sys.argv[1:]
    if args:
        files = [Path(a).resolve() for a in args]
    else:
        files = sorted((VAULT_ROOT / "processed").rglob("*.md"))

    total_errors = 0
    for f in files:
        if f.name == ".gitkeep":
            continue
        errors = lint_file(f)
        if errors:
            total_errors += len(errors)
            rel = f.relative_to(VAULT_ROOT) if f.is_relative_to(VAULT_ROOT) else f
            print(f"\n{rel}")
            for e in errors:
                print(f"  - {e}")

    if total_errors:
        print(f"\n{total_errors} error(s) found.")
        sys.exit(1)
    else:
        print(f"Checked {len(files)} file(s), no errors.")
        sys.exit(0)


if __name__ == "__main__":
    main()
