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


def test_readme_has_demo_and_trust_surface() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert readme.index("## 한국어") < readme.index("## English")
    required_sections = [
        "### 결과 보기",
        "### 프롬프트 예시",
        "### 브랜드 프로필",
        "### 디자인 규칙",
        "### See It",
        "### Example Prompts",
        "### Brand Profile",
        "### Design Rules",
    ]
    for section in required_sections:
        assert section in readme, f"README.md missing section: {section}"

    demo_assets = [
        "docs/design-qa/screenshots/demo-one-pager-ko.png",
        "docs/design-qa/screenshots/demo-one-pager.png",
        "docs/design-qa/screenshots/demo-long-doc.png",
        "docs/design-qa/screenshots/demo-slides.png",
        "docs/design-qa/screenshots/demo-landing-page.png",
    ]
    for asset in demo_assets:
        assert (ROOT / asset).exists(), f"missing README demo asset: {asset}"
        assert asset in readme, f"README.md must showcase {asset}"

    for snippet in [
        "CHEATSHEET.md",
        "references/brand.example.md",
        "~/.config/gyeol/brand.md",
        "Use Gyeol to create a Korean equity report",
        "Gyeol로 한국어 이력서를 만들어줘",
        "Apply the Gyeol design system",
    ]:
        assert snippet in readme, f"README.md missing trust-surface snippet: {snippet}"


def test_brand_profile_and_cheatsheet_are_wired_into_skill() -> None:
    required = [
        "CHEATSHEET.md",
        "references/brand-profile.md",
        "references/brand.example.md",
    ]
    for relative in required:
        assert (ROOT / relative).exists(), f"missing skill support doc: {relative}"

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    cheatsheet = (ROOT / "CHEATSHEET.md").read_text(encoding="utf-8")
    brand_profile = (ROOT / "references/brand-profile.md").read_text(encoding="utf-8")
    brand_example = (ROOT / "references/brand.example.md").read_text(encoding="utf-8")

    for snippet in [
        "~/.config/gyeol/brand.md",
        "references/brand-profile.md",
        "CHEATSHEET.md",
    ]:
        assert snippet in skill, f"SKILL.md missing support doc reference: {snippet}"

    assert "explicit prompt" in brand_profile
    assert "document judgment" in brand_profile
    assert "built-in defaults" in brand_profile
    assert "language:" in brand_example
    assert "brand_color:" in brand_example
    assert "Template Selection" in cheatsheet
    assert "Verification" in cheatsheet


def test_agent_distribution_metadata_and_package_are_ready() -> None:
    required = [
        "agents/openai.yaml",
        ".claude-plugin/marketplace.json",
        ".claude/launch.json",
        "scripts/package_skill.py",
        "llms.txt",
        "CHEATSHEET.md",
        "references/brand-profile.md",
        "references/brand.example.md",
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
        "references/brand-profile.md",
        "references/brand.example.md",
        "CHEATSHEET.md",
        "scripts/build.py",
    ]:
        assert relative in names, f"skill ZIP missing {relative}"
    assert not any(name.startswith(".git/") or "__pycache__/" in name for name in names)


def test_github_linguist_ignores_generated_outputs_only() -> None:
    attributes_path = ROOT / ".gitattributes"
    assert attributes_path.exists(), "missing .gitattributes"
    attributes = attributes_path.read_text(encoding="utf-8")

    required_rules = [
        "assets/demos/** linguist-generated=true",
        "docs/design-qa/screenshots/** linguist-generated=true",
        "dist/** linguist-generated=true",
    ]
    for rule in required_rules:
        assert rule in attributes, f".gitattributes missing Linguist rule: {rule}"

    assert "assets/templates/** linguist-generated=true" not in attributes
    assert "assets/templates/*.html linguist-generated=true" not in attributes


def test_premium_hero_lane_reference_and_demos_exist() -> None:
    from scripts import demos

    reference_path = ROOT / "references/hero-haneul-npu.json"
    assert reference_path.exists(), "missing hero reference data"
    data = json.loads(reference_path.read_text(encoding="utf-8"))

    assert data["company"]["name"] == "Haneul NPU Systems"
    assert data["company"]["fictional"] is True
    assert "on-device NPU" in data["company"]["positioning"]
    assert "low-power inference chiplet" in data["company"]["moat"]
    assert len(demos.HERO_DEMOS) == len(shared.HERO_DEMOS)
    assert [path for _, _, _, path in demos.HERO_DEMOS] == list(shared.HERO_DEMOS)

    combined_html = ""
    for relative in shared.HERO_DEMOS:
        path = ROOT / relative
        assert path.exists(), f"missing hero demo: {relative}"
        html = path.read_text(encoding="utf-8")
        combined_html += html
        assert "{{" not in html and "}}" not in html
        assert "Haneul NPU Systems" in html or "하늘 NPU 시스템즈" in html

    for snippet in [
        "Haneul NPU Systems",
        "fictional sample data",
        "하늘 NPU 시스템즈",
        "가상 샘플 데이터",
        "low-power inference chiplet",
        "on-device NPU",
    ]:
        assert snippet in combined_html, f"hero demos missing required snippet: {snippet}"

    for relative in [
        "docs/design-qa/screenshots/hero-haneul-ir-ko.png",
        "docs/design-qa/screenshots/hero-haneul-investor-memo.png",
        "docs/design-qa/screenshots/hero-haneul-equity-report.png",
        "docs/design-qa/screenshots/hero-haneul-equity-report-ko.png",
        "docs/design-qa/screenshots/hero-haneul-strategy-deck.png",
        "docs/design-qa/screenshots/hero-haneul-landing-page.png",
    ]:
        assert (ROOT / relative).exists(), f"missing hero screenshot: {relative}"


def test_theme_policy_is_encoded_in_target_templates() -> None:
    document_templates = [
        "assets/templates/one-pager.html",
        "assets/templates/one-pager-ko.html",
        "assets/templates/long-doc.html",
        "assets/templates/long-doc-ko.html",
        "assets/templates/equity-report.html",
        "assets/templates/equity-report-ko.html",
        "assets/templates/slides.html",
        "assets/templates/slides-ko.html",
    ]
    for relative in document_templates:
        html = (ROOT / relative).read_text(encoding="utf-8")
        assert 'data-theme="{{theme}}"' in html, f"{relative} must expose a static theme marker"
        assert '[data-theme="dark"]' in html, f"{relative} must define dark theme tokens"
        assert 'data-theme-toggle' not in html, f"{relative} must not rely on browser theme toggle"

    for relative in ["assets/templates/landing-page.html", "assets/templates/landing-page-ko.html"]:
        html = (ROOT / relative).read_text(encoding="utf-8")
        assert 'data-theme="{{theme}}"' in html
        assert 'data-theme-toggle' in html
        assert "localStorage" in html


def test_readme_leads_with_investment_strategy_proof_pack() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Investment / Strategy Proof Pack" in readme
    assert readme.index("Investment / Strategy Proof Pack") < readme.index("### 바로 설치")
    for relative in [
        "assets/demos/hero-haneul-ir-ko.html",
        "assets/demos/hero-haneul-investor-memo.html",
        "assets/demos/hero-haneul-equity-report.html",
        "assets/demos/hero-haneul-strategy-deck.html",
    ]:
        assert relative in readme


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
    expected_demo_count = len(shared.HTML_TEMPLATES) + len(demos.HERO_DEMOS)
    assert len(manifest["demos"]) == expected_demo_count

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
    assert f"OK: generated {expected_demo_count} demo HTML file(s)" in result.stdout


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
    assert "OK: GitHub Linguist generated-output rules are present" in result.stdout


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
