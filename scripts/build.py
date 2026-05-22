from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import shared
from scripts import demos


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


def check_agent_distribution() -> list[str]:
    errors: list[str] = []
    readme_path = shared.project_path("README.md")
    onboarding_path = shared.project_path("docs/onboarding.md")
    if not readme_path.exists() or not onboarding_path.exists():
        return errors

    readme = readme_path.read_text(encoding="utf-8")
    onboarding = onboarding_path.read_text(encoding="utf-8")
    if "## 한국어" not in readme or "## English" not in readme:
        errors.append("README.md must contain Korean and English sections")
    elif readme.index("## 한국어") > readme.index("## English"):
        errors.append("README.md must put Korean before English")

    required_snippets = [
        "npx skills add JangHyun-bin/GyeoL -a '*' -g -y",
        "npx skills add JangHyun-bin/GyeoL -a claude-code -g -y",
        "git clone https://github.com/JangHyun-bin/GyeoL.git",
        "python scripts/package_skill.py",
        "python scripts/tests/test_build.py",
        "python scripts/build.py --check",
        "docs/onboarding.md",
    ]
    for snippet in required_snippets:
        if snippet not in readme:
            errors.append(f"README.md missing onboarding snippet: {snippet}")
        if snippet not in onboarding:
            errors.append(f"docs/onboarding.md missing onboarding snippet: {snippet}")

    openai_path = shared.project_path("agents/openai.yaml")
    if openai_path.exists() and "allow_implicit_invocation: true" not in openai_path.read_text(encoding="utf-8"):
        errors.append("agents/openai.yaml must allow implicit invocation")

    marketplace_path = shared.project_path(".claude-plugin/marketplace.json")
    if marketplace_path.exists():
        try:
            marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f".claude-plugin/marketplace.json is invalid JSON: {exc}")
        else:
            plugins = marketplace.get("plugins", [])
            if not plugins or plugins[0].get("source") != "./" or plugins[0].get("skills") != ["./"]:
                errors.append(".claude-plugin/marketplace.json must expose the root skill")

    llms_path = shared.project_path("llms.txt")
    if llms_path.exists():
        llms = llms_path.read_text(encoding="utf-8")
        if "Gyeol" not in llms or "SKILL.md" not in llms:
            errors.append("llms.txt must describe Gyeol and point to SKILL.md")

    return errors


def check_linguist_attributes() -> list[str]:
    path = shared.project_path(".gitattributes")
    if not path.exists():
        return ["missing .gitattributes"]
    attributes = path.read_text(encoding="utf-8")
    errors: list[str] = []
    for rule in (
        "assets/demos/** linguist-generated=true",
        "docs/design-qa/screenshots/** linguist-generated=true",
        "dist/** linguist-generated=true",
    ):
        if rule not in attributes:
            errors.append(f".gitattributes missing Linguist rule: {rule}")
    if "assets/templates/** linguist-generated=true" in attributes:
        errors.append("assets/templates must remain part of GitHub language stats")
    return errors


def check_hero_lane() -> list[str]:
    errors: list[str] = []
    path = shared.project_path("references/hero-haneul-npu.json")
    if not path.exists():
        return ["missing hero reference references/hero-haneul-npu.json"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"references/hero-haneul-npu.json is invalid JSON: {exc}"]
    if data.get("company", {}).get("fictional") is not True:
        errors.append("hero company must be marked fictional")
    for relative in data.get("hero_demos", []):
        demo_path = shared.project_path(relative)
        if not demo_path.exists():
            errors.append(f"missing hero demo {relative}")
            continue
        html = demo_path.read_text(encoding="utf-8")
        if "{{" in html or "}}" in html:
            errors.append(f"{relative} contains unfilled placeholders")
    return errors


def run_check() -> int:
    errors: list[str] = []
    errors.extend(check_required_files())
    errors.extend(check_registry())
    errors.extend(check_pages())
    errors.extend(check_reference_json())
    errors.extend(check_credit_language())
    errors.extend(check_agent_distribution())
    errors.extend(check_linguist_attributes())
    errors.extend(check_hero_lane())

    if errors:
        for message in errors:
            print(_error(message))
        return 1

    print(_ok(f"registry contains {len(shared.HTML_TEMPLATES)} verified template(s)"))
    print(_ok(f"public pages registered for {', '.join(sorted(shared.SCREEN_PAGES))}"))
    print(_ok(f"{len(shared.REFERENCE_JSON_FILES)} JSON reference file(s) are valid"))
    print(_ok("Kami credit and Gyeol identity references are present"))
    print(_ok("agent onboarding and distribution metadata are present"))
    print(_ok("GitHub Linguist generated-output rules are present"))
    print(_ok("premium hero lane references and demos are present"))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gyeol build and verification entry point")
    parser.add_argument("--check", action="store_true", help="run fast structural checks")
    parser.add_argument("--demos", action="store_true", help="generate filled demo HTML outputs")
    args = parser.parse_args(argv)

    if args.demos:
        manifest = demos.generate_all()
        print(_ok(f"generated {len(manifest['demos'])} demo HTML file(s)"))
        print(_ok("wrote assets/demos/demo-manifest.json"))
        return 0

    if args.check:
        return run_check()

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
