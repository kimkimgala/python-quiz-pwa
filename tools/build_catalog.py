#!/usr/bin/env python3
"""Validate course JSON files and generate catalog.json.

v1.5 rules:
- Existing Python course remains at questions.json for backward compatibility.
- New course cassettes are placed under courses/*.json.
- catalog.json is generated; do not edit it manually.
- New courses are never auto-added to each user's My Courses list.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
LEGACY_ROOT_COURSE = ROOT / "questions.json"
COURSES_DIR = ROOT / "courses"

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")

# v1.3 -> v1.4 migration compatibility. These two courses were already visible
# before the My Courses model was introduced, so they stay default-subscribed.
LEGACY_DEFAULT_SUBSCRIBED = {"python-basic-v1", "cassette-demo-v1"}
LEGACY_DESCRIPTIONS = {
    "python-basic-v1": "現在のPython基礎教材（49問）",
    "cassette-demo-v1": "教材切替と教材別成績保存を確認するための5問",
}


class ValidationError(ValueError):
    pass


def fail(path: Path, message: str) -> None:
    raise ValidationError(f"{path.relative_to(ROOT)}: {message}")


def require_nonempty_string(data: dict[str, Any], key: str, path: Path) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(path, f"{key} must be a non-empty string")
    return value.strip()


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        fail(path, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    except OSError as exc:
        fail(path, f"cannot read file: {exc}")

    if not isinstance(data, dict):
        fail(path, "top level must be a JSON object")
    return data


def validate_question(question: Any, index: int, seen_numbers: set[str], path: Path) -> None:
    if not isinstance(question, dict):
        fail(path, f"questions[{index}] must be an object")

    for key in ("day", "number", "question", "options", "answer", "explanation"):
        if key not in question:
            fail(path, f"questions[{index}] is missing {key}")

    number = question["number"]
    number_key = str(number)
    if not number_key.strip():
        fail(path, f"questions[{index}].number is empty")
    if number_key in seen_numbers:
        fail(path, f"duplicate question number: {number}")
    seen_numbers.add(number_key)

    if not isinstance(question["question"], str) or not question["question"].strip():
        fail(path, f"question {number}: question text must be non-empty")
    if not isinstance(question["explanation"], str):
        fail(path, f"question {number}: explanation must be a string")

    options = question["options"]
    if not isinstance(options, list) or len(options) < 2:
        fail(path, f"question {number}: options must contain at least 2 choices")

    option_keys: list[str] = []
    for option_index, option in enumerate(options):
        if not isinstance(option, list) or len(option) != 2:
            fail(path, f"question {number}: options[{option_index}] must be [key, text]")
        key, text = option
        if not isinstance(key, str) or not key.strip():
            fail(path, f"question {number}: option key must be a non-empty string")
        if not isinstance(text, str) or not text.strip():
            fail(path, f"question {number}: option text must be a non-empty string")
        option_keys.append(key)

    if len(option_keys) != len(set(option_keys)):
        fail(path, f"question {number}: option keys must be unique")

    answer = question["answer"]
    if not isinstance(answer, str) or answer not in option_keys:
        fail(path, f"question {number}: answer must match one option key")


def validate_course(path: Path) -> dict[str, Any]:
    data = load_json(path)

    course_id = require_nonempty_string(data, "course_id", path)
    if not ID_RE.fullmatch(course_id):
        fail(path, "course_id may contain only letters, numbers, '-' and '_'")

    title = require_nonempty_string(data, "title", path)

    section_label = data.get("section_label", "区分")
    if not isinstance(section_label, str) or not section_label.strip():
        fail(path, "section_label must be a non-empty string")

    clear_count = data.get("clear_count", 3)
    if not isinstance(clear_count, int) or isinstance(clear_count, bool) or clear_count <= 0:
        fail(path, "clear_count must be a positive integer")

    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        fail(path, "questions must be a non-empty array")

    seen_numbers: set[str] = set()
    for index, question in enumerate(questions):
        validate_question(question, index, seen_numbers, path)

    description = data.get("description")
    if description is None or (isinstance(description, str) and not description.strip()):
        description = LEGACY_DESCRIPTIONS.get(course_id) or data.get("subtitle") or title
    if not isinstance(description, str):
        fail(path, "description must be a string when specified")

    relative_path = path.relative_to(ROOT).as_posix()
    entry: dict[str, Any] = {
        "id": course_id,
        "title": title,
        "description": description.strip(),
        "file": relative_path,
    }
    if course_id in LEGACY_DEFAULT_SUBSCRIBED:
        entry["default_subscribed"] = True
    return entry


def discover_course_files() -> list[Path]:
    files: list[Path] = []
    if LEGACY_ROOT_COURSE.exists():
        files.append(LEGACY_ROOT_COURSE)
    if COURSES_DIR.exists():
        files.extend(sorted(COURSES_DIR.glob("*.json"), key=lambda p: p.name.lower()))
    if not files:
        raise ValidationError("no course JSON files found")
    return files


def build_catalog() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    seen_ids: dict[str, str] = {}

    for path in discover_course_files():
        entry = validate_course(path)
        course_id = entry["id"]
        if course_id in seen_ids:
            raise ValidationError(
                f"duplicate course_id '{course_id}' in {seen_ids[course_id]} and {path.relative_to(ROOT)}"
            )
        seen_ids[course_id] = str(path.relative_to(ROOT))
        entries.append(entry)

    return {
        "catalog_version": 3,
        "title": "配信教材一覧",
        "courses": entries,
    }


def main() -> int:
    try:
        catalog = build_catalog()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    text = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
    CATALOG_PATH.write_text(text, encoding="utf-8")
    print(f"OK: generated {CATALOG_PATH.relative_to(ROOT)} with {len(catalog['courses'])} courses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
