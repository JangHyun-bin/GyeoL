from __future__ import annotations

import json
import subprocess
import sys
import traceback
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


def test_build_check_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/build.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK: registry contains 18 verified template(s)" in result.stdout


def _run() -> int:
    failures = 0
    for name, value in sorted(globals().items()):
        if not name.startswith("test_") or not callable(value):
            continue
        try:
            value()
            print(f"OK: {name}")
        except Exception:
            failures += 1
            print(f"ERROR: {name}")
            traceback.print_exc()
    print(f"Passed: {6 - failures} | Failed: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(_run())
