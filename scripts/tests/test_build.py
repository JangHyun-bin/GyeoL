from __future__ import annotations

import json
import subprocess
import sys
import traceback
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts import shared


def test_full_registry_has_all_verified_templates() -> None:
    names = [template.name for template in shared.HTML_TEMPLATES]
    assert names == [
        "one-pager",
        "one-pager-ko",
        "long-doc",
        "long-doc-ko",
        "letter",
        "letter-ko",
        "portfolio",
        "portfolio-ko",
        "resume",
        "resume-ko",
        "slides",
        "slides-ko",
        "equity-report",
        "equity-report-ko",
        "changelog",
        "changelog-ko",
        "landing-page",
        "landing-page-ko",
    ]

    assert shared.PLANNED_TEMPLATES == ()


def test_registered_template_files_exist_and_match_language() -> None:
    for template in shared.HTML_TEMPLATES:
        path = ROOT / template.path
        assert path.exists(), f"missing template: {template.path}"
        html = path.read_text(encoding="utf-8")
        assert f'lang="{template.language}"' in html
        assert "{{" in html and "}}" in html


def test_public_pages_are_first_class_and_cross_linked() -> None:
    assert shared.SCREEN_PAGES == {"en": "index.html", "ko": "ko.html"}
    en = (ROOT / "index.html").read_text(encoding="utf-8")
    ko = (ROOT / "ko.html").read_text(encoding="utf-8")
    assert 'lang="en"' in en
    assert 'href="ko.html"' in en
    assert 'lang="ko"' in ko
    assert 'href="index.html"' in ko
    assert "Gyeol" in en
    assert "결" in ko


def test_required_credit_and_reference_files_exist() -> None:
    required = [
        "README.md",
        "SKILL.md",
        "AGENTS.md",
        "CREDITS.md",
        "NOTICE",
        "LICENSE",
        "references/kami.md",
        "references/cohere.md",
        "references/design.md",
        "references/writing.md",
        "references/production.md",
        "references/roadmap.md",
        "references/tokens.json",
        "references/checks_thresholds.json",
        "references/stabilizer_profiles.json",
        "styles.css",
    ]
    for relative in required:
        assert (ROOT / relative).exists(), f"missing required file: {relative}"

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    credits = (ROOT / "CREDITS.md").read_text(encoding="utf-8")
    notice = (ROOT / "NOTICE").read_text(encoding="utf-8")
    kami_reference = (ROOT / "references/kami.md").read_text(encoding="utf-8")
    for content in (readme, credits, notice, kami_reference):
        assert "Kami" in content
        assert "Gyeol" in content


def test_agent_onboarding_docs_cover_install_paths() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    onboarding_path = ROOT / "docs/onboarding.md"
    assert onboarding_path.exists(), "missing docs/onboarding.md"
    onboarding = onboarding_path.read_text(encoding="utf-8")

    assert readme.index("## 한국어") < readme.index("## English")
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
        assert snippet in readme, f"README.md missing onboarding snippet: {snippet}"
        assert snippet in onboarding, f"docs/onboarding.md missing onboarding snippet: {snippet}"

    assert "Codex" in readme and "Claude Code" in readme and "Claude Desktop" in readme
    assert "Codex" in onboarding and "Claude Code" in onboarding and "Claude Desktop" in onboarding


def test_agent_distribution_metadata_and_package_are_ready() -> None:
    required = [
        "agents/openai.yaml",
        ".claude-plugin/marketplace.json",
        ".claude/launch.json",
        "scripts/package_skill.py",
        "llms.txt",
    ]
    for relative in required:
        assert (ROOT / relative).exists(), f"missing agent distribution file: {relative}"

    openai_yaml = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")

    assert "allow_implicit_invocation: true" in openai_yaml
    assert marketplace["plugins"][0]["skills"] == ["./"]
    assert marketplace["plugins"][0]["source"] == "./"
    assert "Gyeol" in llms and "SKILL.md" in llms

    result = subprocess.run(
        [sys.executable, "scripts/package_skill.py", "--out", "dist/gyeol.zip"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: wrote dist/gyeol.zip" in result.stdout

    archive_path = ROOT / "dist/gyeol.zip"
    assert archive_path.exists()
    with zipfile.ZipFile(archive_path) as archive:
        names = set(archive.namelist())
    for relative in [
        "SKILL.md",
        "agents/openai.yaml",
        "assets/templates/one-pager.html",
        "assets/templates/one-pager-ko.html",
        "references/writing.md",
        "scripts/build.py",
    ]:
        assert relative in names, f"skill ZIP missing {relative}"
    assert not any(name.startswith(".git/") or "__pycache__/" in name for name in names)


def test_reference_json_files_are_valid() -> None:
    for relative in [
        "references/tokens.json",
        "references/checks_thresholds.json",
        "references/stabilizer_profiles.json",
    ]:
        with (ROOT / relative).open(encoding="utf-8") as handle:
            data = json.load(handle)
        assert isinstance(data, dict)
        assert data


def test_demo_generation_creates_filled_outputs() -> None:
    from scripts import demos

    manifest = demos.generate_all()
    assert len(manifest["demos"]) == len(shared.HTML_TEMPLATES)

    manifest_path = ROOT / "assets/demos/demo-manifest.json"
    assert manifest_path.exists()

    for item in manifest["demos"]:
        path = ROOT / item["path"]
        assert path.exists(), f"missing demo output: {item['path']}"
        html = path.read_text(encoding="utf-8")
        assert "{{" not in html and "}}" not in html
        assert f'lang="{item["language"]}"' in html

    result = subprocess.run(
        [sys.executable, "scripts/build.py", "--demos"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: generated 18 demo HTML file(s)" in result.stdout


def test_build_check_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: registry contains 18 verified template(s)" in result.stdout
    assert "OK: agent onboarding and distribution metadata are present" in result.stdout


def _run() -> int:
    failures = 0
    tests = [(name, value) for name, value in sorted(globals().items()) if name.startswith("test_") and callable(value)]
    for name, value in tests:
        try:
            value()
            print(f"OK: {name}")
        except Exception:
            failures += 1
            print(f"ERROR: {name}")
            traceback.print_exc()
    print(f"Passed: {len(tests) - failures} | Failed: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_run())
