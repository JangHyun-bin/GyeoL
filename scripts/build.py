from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import shared


def _error(message: str) -> str:
    return f"ERROR: {message}"


def _ok(message: str) -> str:
    return f"OK: {message}"


def _read(relative: str) -> str:
    return shared.project_path(relative).read_text(encoding="utf-8")


def check_registry() -> list[str]:
    errors: list[str] = []
    names = [template.name for template in shared.HTML_TEMPLATES]
    if len(names) != len(set(names)):
        errors.append("template registry contains duplicate names")

    planned = set(shared.PLANNED_TEMPLATES)
    overlap = planned.intersection(names)
    if overlap:
        errors.append(f"planned templates must not be registered yet: {sorted(overlap)}")

    for template in shared.HTML_TEMPLATES:
        path = shared.project_path(template.path)
        if not path.exists():
            errors.append(f"missing registered template {template.path}")
            continue
        html = path.read_text(encoding="utf-8")
        if f'lang="{template.language}"' not in html:
            errors.append(f"{template.path} missing lang={template.language}")
        if "{{" not in html or "}}" not in html:
            errors.append(f"{template.path} must expose replaceable placeholders")
    return errors


def check_pages() -> list[str]:
    errors: list[str] = []
    en_path = shared.project_path(shared.SCREEN_PAGES["en"])
    ko_path = shared.project_path(shared.SCREEN_PAGES["ko"])
    if not en_path.exists():
        errors.append("missing English public page index.html")
    if not ko_path.exists():
        errors.append("missing Korean public page ko.html")
    if not errors:
        en = en_path.read_text(encoding="utf-8")
        ko = ko_path.read_text(encoding="utf-8")
        if 'lang="en"' not in en or 'href="ko.html"' not in en:
            errors.append("index.html must be English and link to ko.html")
        if 'lang="ko"' not in ko or 'href="index.html"' not in ko:
            errors.append("ko.html must be Korean and link to index.html")
    return errors


def check_required_files() -> list[str]:
    return [
        f"missing required file {relative}"
        for relative in shared.REQUIRED_PROJECT_FILES
        if not shared.project_path(relative).exists()
    ]


def check_reference_json() -> list[str]:
    errors: list[str] = []
    for relative in shared.REFERENCE_JSON_FILES:
        path = shared.project_path(relative)
        if not path.exists():
            errors.append(f"missing JSON reference {relative}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{relative} is invalid JSON: {exc}")
            continue
        if not isinstance(data, dict) or not data:
            errors.append(f"{relative} must contain a non-empty object")
    return errors


def check_credit_language() -> list[str]:
    errors: list[str] = []
    for relative in ("README.md", "CREDITS.md", "NOTICE", "references/kami.md"):
        path = shared.project_path(relative)
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if "Kami" not in content or "Gyeol" not in content:
            errors.append(f"{relative} must mention both Kami and Gyeol")
    return errors


def run_check() -> int:
    errors: list[str] = []
    errors.extend(check_required_files())
    errors.extend(check_registry())
    errors.extend(check_pages())
    errors.extend(check_reference_json())
    errors.extend(check_credit_language())

    if errors:
        for message in errors:
            print(_error(message))
        return 1

    print(_ok(f"registry contains {len(shared.HTML_TEMPLATES)} verified template(s)"))
    print(_ok(f"public pages registered for {', '.join(sorted(shared.SCREEN_PAGES))}"))
    print(_ok(f"{len(shared.REFERENCE_JSON_FILES)} JSON reference file(s) are valid"))
    print(_ok("Kami credit and Gyeol identity references are present"))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gyeol build and verification entry point")
    parser.add_argument("--check", action="store_true", help="run fast structural checks")
    args = parser.parse_args(argv)

    if args.check:
        return run_check()

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
