# Gyeol Premium Hero Lane Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first premium investment/strategy proof lane for Gyeol around a fictional Korean on-device AI fabless company, with static light/dark document themes and a web toggle for landing/demo surfaces.

**Architecture:** Keep the existing static HTML template architecture. Add a hero sample data reference, stronger structural tests, richer target templates, and generated hero demos. Use template-local CSS first; extract shared primitives only after the hero lane proves the pattern.

**Tech Stack:** Python standard library, static HTML/CSS/JS, existing `scripts/demos.py`, existing `scripts/build.py --check`, existing `scripts/tests/test_build.py`.

---

## Scope Check

This is one coherent implementation phase: the investment/strategy hero lane. Hiring and product/sales lanes are intentionally deferred. The first pass touches only the templates needed to prove the hero lane and the docs/tests that keep that proof visible.

## File Structure

- Modify `scripts/tests/test_build.py`: add hero-lane, theme-policy, and landing-toggle regression tests.
- Modify `scripts/shared.py`: register required hero/reference files.
- Modify `scripts/build.py`: include hero-lane checks in `--check`.
- Create `references/hero-haneul-npu.json`: fictional company sample data and hero demo definitions.
- Modify `references/design.md`: define Korean enterprise editorial sans direction and light/dark token policy.
- Modify `references/writing.md`: add investment/strategy quality bars.
- Modify `CHEATSHEET.md`: add hero lane and theme usage quick reference.
- Modify `SKILL.md`: add theme behavior and hero sample guidance.
- Modify `scripts/demos.py`: generate hero demos in addition to the existing registry demos.
- Modify `assets/templates/one-pager.html` and `assets/templates/one-pager-ko.html`: premium IR one-pager layout, static `data-theme`.
- Modify `assets/templates/long-doc.html` and `assets/templates/long-doc-ko.html`: investor memo layout.
- Modify `assets/templates/equity-report.html` and `assets/templates/equity-report-ko.html`: equity-style research layout.
- Modify `assets/templates/slides.html` and `assets/templates/slides-ko.html`: dark strategy deck layout.
- Modify `assets/templates/landing-page.html` and `assets/templates/landing-page-ko.html`: light/dark web toggle.
- Modify `README.md`, `index.html`, and `ko.html`: show the investment/strategy proof pack before generic demos.
- Update generated `assets/demos/hero-*.html`, `assets/demos/demo-manifest.json`, and selected `docs/design-qa/screenshots/hero-*.png`.
- Create `scripts/render_hero_screenshots.py`: deterministic Playwright screenshot capture for hero demos.
- Rebuild `dist/gyeol.zip`.

## Task 1: Add Hero Lane Contract Tests

**Files:**
- Modify: `scripts/tests/test_build.py`
- Modify: `scripts/build.py`
- Modify: `scripts/shared.py`

- [ ] **Step 1: Write failing tests for hero data, theme markers, and generated demos**

Add these tests to `scripts/tests/test_build.py` after `test_github_linguist_ignores_generated_outputs_only`:

```python
def test_premium_hero_lane_reference_and_demos_exist() -> None:
    reference_path = ROOT / "references/hero-haneul-npu.json"
    assert reference_path.exists(), "missing hero reference data"
    data = json.loads(reference_path.read_text(encoding="utf-8"))

    assert data["company"]["name"] == "Haneul NPU Systems"
    assert data["company"]["fictional"] is True
    assert "on-device NPU" in data["company"]["positioning"]
    assert "low-power inference chiplet" in data["company"]["moat"]

    required_demos = [
        "assets/demos/hero-haneul-ir-ko.html",
        "assets/demos/hero-haneul-investor-memo.html",
        "assets/demos/hero-haneul-equity-report.html",
        "assets/demos/hero-haneul-equity-report-ko.html",
        "assets/demos/hero-haneul-strategy-deck.html",
        "assets/demos/hero-haneul-landing-page.html",
    ]
    for relative in required_demos:
        path = ROOT / relative
        assert path.exists(), f"missing hero demo: {relative}"
        html = path.read_text(encoding="utf-8")
        assert "{{" not in html and "}}" not in html
        assert "Haneul NPU Systems" in html or "하늘 NPU 시스템즈" in html
        assert "fictional sample data" in html or "가상 샘플 데이터" in html


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
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python scripts/tests/test_build.py
```

Expected: failure mentioning missing `references/hero-haneul-npu.json`, missing hero demos, and missing theme markers.

- [ ] **Step 3: Add required files to the structural registry**

In `scripts/shared.py`, add the hero reference file to `REQUIRED_PROJECT_FILES`:

```python
"references/hero-haneul-npu.json",
```

- [ ] **Step 4: Add build-time hero checks**

In `scripts/build.py`, add:

```python
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
```

Call it inside `run_check()`:

```python
errors.extend(check_hero_lane())
```

Print a success line:

```python
print(_ok("premium hero lane references and demos are present"))
```

- [ ] **Step 5: Run tests and verify expected remaining failures**

Run:

```bash
python scripts/tests/test_build.py
```

Expected: still failing because hero data/demos/templates are not implemented yet.

- [ ] **Step 6: Commit**

```bash
git add scripts/tests/test_build.py scripts/build.py scripts/shared.py
git commit -m "test: add premium hero lane contracts"
```

## Task 2: Add Hero Sample Data

**Files:**
- Create: `references/hero-haneul-npu.json`
- Modify: `references/design.md`
- Modify: `references/writing.md`
- Modify: `CHEATSHEET.md`
- Modify: `SKILL.md`

- [ ] **Step 1: Create the hero sample reference**

Create `references/hero-haneul-npu.json` with this structure:

```json
{
  "company": {
    "name": "Haneul NPU Systems",
    "korean_name": "하늘 NPU 시스템즈",
    "fictional": true,
    "sample_notice": "Fictional sample data for Gyeol demos. Not an investment recommendation.",
    "korean_sample_notice": "Gyeol 데모를 위한 가상 샘플 데이터입니다. 투자 의견이 아닙니다.",
    "positioning": "Korean fabless company building on-device NPU silicon for smartphones and laptops.",
    "moat": "Low-power inference chiplet and reusable NPU IP platform.",
    "stage": "Private Series B/C-style company written with public-company research depth."
  },
  "themes": {
    "ir_one_pager": "light",
    "investor_memo": "light",
    "equity_report": "light",
    "strategy_deck": "dark",
    "landing_page": "dark"
  },
  "metrics": {
    "process_node": "4nm target",
    "power_reduction": "42%",
    "prototype_tops": "38 TOPS",
    "design_wins": "3 pilot OEMs",
    "runway": "24 months",
    "gross_margin_target": "58-62%"
  },
  "hero_demos": [
    "assets/demos/hero-haneul-ir-ko.html",
    "assets/demos/hero-haneul-investor-memo.html",
    "assets/demos/hero-haneul-equity-report.html",
    "assets/demos/hero-haneul-equity-report-ko.html",
    "assets/demos/hero-haneul-strategy-deck.html",
    "assets/demos/hero-haneul-landing-page.html"
  ]
}
```

- [ ] **Step 2: Update design reference with theme policy**

Append this section to `references/design.md`:

```markdown
## Light / Dark Theme Policy

Document templates use a fixed `data-theme` value per artifact. They may expose `{{theme}}`, but they do not include a browser toggle. Landing pages may include a browser toggle because they are screen-first outputs.

Light theme is the default for IR one-pagers, investor memos, reports, and PDF-oriented work. Dark theme is preferred for strategy decks, launch pages, board previews, and executive presentation surfaces.

Dark mode is not an inversion. It uses a deep graphite/navy canvas, warm foreground text, restrained blue or semiconductor green accents, and visible hairlines.
```

- [ ] **Step 3: Update writing reference with investment quality bars**

Append this section to `references/writing.md`:

```markdown
## Investment / Strategy Quality Bar

Investment and strategy documents must connect technology, market, economics, and risk in the same information architecture.

Required elements:

- company context and stage
- thesis or decision
- metrics with units
- market wedge
- technology moat
- go-to-market path
- risks and mitigations
- source or sample-data notice

Korean output must sound like Korean business writing. English output must sound like native investor prose. Do not translate headings mechanically.
```

- [ ] **Step 4: Update quick reference and skill guidance**

In `CHEATSHEET.md`, add a "Premium Hero Lane" section:

```markdown
## Premium Hero Lane

Use `references/hero-haneul-npu.json` for the first investment/strategy proof pack. The company is fictional and must stay clearly marked as sample data.

Default themes:

- Korean IR one-pager: light
- English investor memo: light
- Equity-style report: light
- Strategy deck: dark
- Landing page: dark with toggle
```

In `SKILL.md`, add:

```markdown
## Theme Selection

Use `light` for print, memo, report, send-as-PDF, and formal investment documents. Consider `dark` for premium, board, keynote, launch, executive preview, and strategy deck requests. Document templates should emit one fixed theme per artifact. Landing pages may include a browser toggle.

## Hero Sample Context

For investment/strategy demos or examples, use `references/hero-haneul-npu.json`. Keep Haneul NPU Systems marked as fictional sample data.
```

- [ ] **Step 5: Run tests**

Run:

```bash
python scripts/tests/test_build.py
```

Expected: hero reference tests advance, but hero demos and template theme tests still fail.

- [ ] **Step 6: Commit**

```bash
git add references/hero-haneul-npu.json references/design.md references/writing.md CHEATSHEET.md SKILL.md
git commit -m "docs: add premium hero sample context"
```

## Task 3: Upgrade One-Pager Templates for IR Proof

**Files:**
- Modify: `assets/templates/one-pager.html`
- Modify: `assets/templates/one-pager-ko.html`

- [ ] **Step 1: Replace one-pager shell with premium theme-aware layout**

For both one-pager templates, ensure the root element is:

```html
<html lang="en" data-theme="{{theme}}">
```

and for Korean:

```html
<html lang="ko" data-theme="{{theme}}">
```

The CSS must include these required token blocks:

```css
:root {
  --canvas: #fbfaf7;
  --surface: #ffffff;
  --ink: #17171c;
  --muted: #656779;
  --hairline: #dddfe8;
  --band: #071829;
  --accent: #1863dc;
  --semiconductor: #0f766e;
  --font: Pretendard, "Noto Sans KR", Inter, system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, monospace;
}
[data-theme="dark"] {
  --canvas: #080d14;
  --surface: #101824;
  --ink: #f5f7fb;
  --muted: #a8b0c2;
  --hairline: #263244;
  --band: #dfe8ff;
  --accent: #7fb4ff;
  --semiconductor: #6ee7c8;
}
```

Required component classes:

```css
.metric-rail {}
.thesis-block {}
.decision-bar {}
.risk-grid {}
.source-note {}
```

- [ ] **Step 2: Add required body structure**

The English template body must include these placeholders:

```html
{{company}}
{{sample_notice}}
{{thesis}}
{{market_wedge}}
{{technology_moat}}
{{metric_1}}
{{metric_2}}
{{metric_3}}
{{risk_1}}
{{risk_2}}
{{next_decision}}
```

The Korean template must include:

```html
{{company_ko}}
{{sample_notice_ko}}
{{thesis_ko}}
{{market_wedge_ko}}
{{technology_moat_ko}}
{{metric_1}}
{{metric_2}}
{{metric_3}}
{{risk_1_ko}}
{{risk_2_ko}}
{{next_decision_ko}}
```

- [ ] **Step 3: Run the theme marker test**

Run:

```bash
python scripts/tests/test_build.py
```

Expected: one-pager theme assertions pass; long-doc/report/slides/landing assertions may still fail.

- [ ] **Step 4: Commit**

```bash
git add assets/templates/one-pager.html assets/templates/one-pager-ko.html
git commit -m "feat: upgrade IR one-pager templates"
```

## Task 4: Upgrade Investor Memo and Equity Report Templates

**Files:**
- Modify: `assets/templates/long-doc.html`
- Modify: `assets/templates/long-doc-ko.html`
- Modify: `assets/templates/equity-report.html`
- Modify: `assets/templates/equity-report-ko.html`

- [ ] **Step 1: Add static theme markers and token sets**

Add `data-theme="{{theme}}"` to each `<html>` element. Do not add `data-theme-toggle`.

Each target template must include this token block:

```css
:root {
  --canvas: #fbfaf7;
  --surface: #ffffff;
  --ink: #17171c;
  --muted: #656779;
  --hairline: #dddfe8;
  --band: #071829;
  --accent: #1863dc;
  --semiconductor: #0f766e;
  --font: Pretendard, "Noto Sans KR", Inter, system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, monospace;
}
[data-theme="dark"] {
  --canvas: #080d14;
  --surface: #101824;
  --ink: #f5f7fb;
  --muted: #a8b0c2;
  --hairline: #263244;
  --band: #dfe8ff;
  --accent: #7fb4ff;
  --semiconductor: #6ee7c8;
}
```

- [ ] **Step 2: Convert long-doc into investor memo structure**

The English long-doc template must expose:

```html
{{company}}
{{sample_notice}}
{{memo_title}}
{{executive_summary}}
{{why_now}}
{{product_surface}}
{{market_wedge}}
{{business_model}}
{{technology_moat}}
{{risk_register}}
{{investment_view}}
```

The Korean long-doc template must expose:

```html
{{company_ko}}
{{sample_notice_ko}}
{{memo_title_ko}}
{{executive_summary_ko}}
{{why_now_ko}}
{{product_surface_ko}}
{{market_wedge_ko}}
{{business_model_ko}}
{{technology_moat_ko}}
{{risk_register_ko}}
{{investment_view_ko}}
```

- [ ] **Step 3: Convert equity reports into private-company research structure**

Both equity report templates must include:

```html
class="kpi-table"
class="risk-matrix"
class="roadmap-strip"
class="source-note"
```

English placeholders:

```html
{{company}}
{{sample_notice}}
{{rating}}
{{base_case}}
{{upside_case}}
{{downside_case}}
{{kpi_revenue}}
{{kpi_margin}}
{{kpi_design_wins}}
{{risk_supply}}
{{risk_customer}}
{{risk_competition}}
```

Korean placeholders:

```html
{{company_ko}}
{{sample_notice_ko}}
{{rating_ko}}
{{base_case_ko}}
{{upside_case_ko}}
{{downside_case_ko}}
{{kpi_revenue}}
{{kpi_margin}}
{{kpi_design_wins}}
{{risk_supply_ko}}
{{risk_customer_ko}}
{{risk_competition_ko}}
```

- [ ] **Step 4: Run tests**

Run:

```bash
python scripts/tests/test_build.py
```

Expected: document template theme assertions pass for one-pager, long-doc, and equity-report. Slides and landing may still fail.

- [ ] **Step 5: Commit**

```bash
git add assets/templates/long-doc.html assets/templates/long-doc-ko.html assets/templates/equity-report.html assets/templates/equity-report-ko.html
git commit -m "feat: upgrade investor memo and research templates"
```

## Task 5: Upgrade Strategy Deck and Landing Page Theme Behavior

**Files:**
- Modify: `assets/templates/slides.html`
- Modify: `assets/templates/slides-ko.html`
- Modify: `assets/templates/landing-page.html`
- Modify: `assets/templates/landing-page-ko.html`

- [ ] **Step 1: Add static deck theme markers**

For `slides.html` and `slides-ko.html`, add `data-theme="{{theme}}"`, dark/light tokens, and no browser toggle.

Required deck sections:

```html
{{deck_label}}
{{company}}
{{sample_notice}}
{{assertion_1}}
{{evidence_1}}
{{assertion_2}}
{{evidence_2}}
{{roadmap}}
{{risk_register}}
{{investor_ask}}
```

The Korean deck must use these placeholders instead of the English content placeholders:

```html
{{deck_label_ko}}
{{company_ko}}
{{sample_notice_ko}}
{{assertion_1_ko}}
{{evidence_1_ko}}
{{assertion_2_ko}}
{{evidence_2_ko}}
{{roadmap_ko}}
{{risk_register_ko}}
{{investor_ask_ko}}
```

- [ ] **Step 2: Add landing page toggle**

For both landing-page templates, add:

```html
<html lang="en" data-theme="{{theme}}">
```

Korean:

```html
<html lang="ko" data-theme="{{theme}}">
```

Add a toggle button:

```html
<button type="button" data-theme-toggle aria-label="Toggle theme">Theme</button>
```

Add this script before `</body>`:

```html
<script>
  const root = document.documentElement;
  const toggle = document.querySelector('[data-theme-toggle]');
  const saved = localStorage.getItem('gyeol-theme');
  if (saved) root.dataset.theme = saved;
  toggle?.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    localStorage.setItem('gyeol-theme', next);
  });
</script>
```

- [ ] **Step 3: Run tests**

Run:

```bash
python scripts/tests/test_build.py
```

Expected: all theme-policy tests pass except hero demos, which are generated in the next task.

- [ ] **Step 4: Commit**

```bash
git add assets/templates/slides.html assets/templates/slides-ko.html assets/templates/landing-page.html assets/templates/landing-page-ko.html
git commit -m "feat: add strategy deck and landing theme support"
```

## Task 6: Generate Hero Demos from Sample Data

**Files:**
- Modify: `scripts/demos.py`
- Update: `assets/demos/demo-manifest.json`
- Create/update: `assets/demos/hero-haneul-*.html`

- [ ] **Step 1: Add hero sample loading helpers**

Add to `scripts/demos.py`:

```python
def _hero_reference() -> dict:
    with shared.project_path("references/hero-haneul-npu.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def _hero_values(kind: str) -> dict[str, str]:
    ref = _hero_reference()
    company = ref["company"]
    metrics = ref["metrics"]
    common = {
        "theme": ref["themes"].get(kind, "light"),
        "company": company["name"],
        "company_ko": company["korean_name"],
        "sample_notice": company["sample_notice"],
        "sample_notice_ko": company["korean_sample_notice"],
        "metric_1": metrics["power_reduction"],
        "metric_2": metrics["prototype_tops"],
        "metric_3": metrics["design_wins"],
        "technology_moat": company["moat"],
        "technology_moat_ko": "저전력 추론 chiplet과 재사용 가능한 NPU IP 플랫폼",
        "market_wedge": "Premium mobile and AI PC OEMs need local inference within strict power envelopes.",
        "market_wedge_ko": "프리미엄 모바일과 AI PC OEM은 제한된 전력 예산 안에서 로컬 추론 성능을 요구합니다.",
    }
    return common
```

- [ ] **Step 2: Add hero demo definitions**

Add:

```python
HERO_DEMOS = [
    ("hero-haneul-ir-ko", "one-pager-ko", "ir_one_pager"),
    ("hero-haneul-investor-memo", "long-doc", "investor_memo"),
    ("hero-haneul-equity-report", "equity-report", "equity_report"),
    ("hero-haneul-equity-report-ko", "equity-report-ko", "equity_report"),
    ("hero-haneul-strategy-deck", "slides-ko", "strategy_deck"),
    ("hero-haneul-landing-page", "landing-page", "landing_page"),
]
```

Extend `generate_all()` so it writes these after the registry demos and appends them to the manifest with `"hero": true`.

- [ ] **Step 3: Fill hero-specific values**

Extend `_hero_values()` with this concrete content map:

```python
    common.update(
        {
            "thesis": "Haneul NPU Systems can become the Korean reference platform for on-device NPU adoption if pilot OEMs convert into 2027 design wins.",
            "thesis_ko": "하늘 NPU 시스템즈는 파일럿 OEM을 2027년 설계 채택으로 전환할 경우 한국 온디바이스 NPU 기준 플랫폼이 될 수 있습니다.",
            "risk_1": "Pilot concentration across three OEM programs.",
            "risk_1_ko": "3개 OEM 파일럿에 초기 수요가 집중되어 있습니다.",
            "risk_2": "Advanced-node wafer allocation remains the main execution bottleneck.",
            "risk_2_ko": "선단 공정 웨이퍼 배정이 핵심 실행 병목입니다.",
            "next_decision": "Approve Series C diligence focused on silicon validation, software tooling, and customer conversion.",
            "next_decision_ko": "실리콘 검증, 소프트웨어 툴링, 고객 전환율을 중심으로 Series C 실사를 진행합니다.",
            "memo_title": "Investor Memo: On-device AI silicon wedge",
            "memo_title_ko": "투자 메모: 온디바이스 AI 반도체 진입 전략",
            "executive_summary": "The company is fictional sample data, but the memo structure mirrors a real strategic investor review.",
            "executive_summary_ko": "회사는 가상 샘플 데이터이지만, 메모 구조는 실제 전략적 투자자 검토 흐름을 따릅니다.",
            "why_now": "AI PC and flagship smartphone roadmaps are moving inference from cloud-only workflows to local hybrid execution.",
            "why_now_ko": "AI PC와 플래그십 스마트폰 로드맵은 추론을 클라우드 단독 방식에서 로컬 하이브리드 실행으로 이동시키고 있습니다.",
            "product_surface": "A reusable low-power inference chiplet, compiler layer, and OEM integration kit.",
            "product_surface_ko": "재사용 가능한 저전력 추론 chiplet, 컴파일러 계층, OEM 통합 키트입니다.",
            "business_model": "IP licensing, reference chip revenue, and integration support for OEM platform teams.",
            "business_model_ko": "IP 라이선스, 레퍼런스 칩 매출, OEM 플랫폼팀 대상 통합 지원 모델입니다.",
            "risk_register": "Supply allocation, thermal envelopes, software maturity, and customer qualification cycles.",
            "risk_register_ko": "공급 배정, 열 설계 한계, 소프트웨어 성숙도, 고객 인증 주기가 주요 리스크입니다.",
            "investment_view": "Advance if validation data supports the 42% power-reduction claim across two independent OEM testbeds.",
            "investment_view_ko": "두 개의 독립 OEM 테스트베드에서 42% 전력 절감 주장이 검증되면 다음 단계로 진행합니다.",
            "rating": "Private-company view: Constructive / diligence required",
            "rating_ko": "비상장사 관점: 긍정적 / 실사 필요",
            "base_case": "Three pilot OEMs convert into two design wins by 2027.",
            "base_case_ko": "3개 파일럿 OEM 중 2개가 2027년 설계 채택으로 전환됩니다.",
            "upside_case": "AI PC attach rate accelerates and the IP platform becomes reusable across adjacent devices.",
            "upside_case_ko": "AI PC 채택률이 가속되고 IP 플랫폼이 인접 기기로 재사용됩니다.",
            "downside_case": "OEMs delay local inference features or shift to internal silicon programs.",
            "downside_case_ko": "OEM이 로컬 추론 기능을 지연하거나 자체 실리콘 프로그램으로 전환합니다.",
            "kpi_revenue": "KRW 18.5B 2027E sample revenue",
            "kpi_margin": "58-62% gross margin target",
            "kpi_design_wins": "2 of 3 pilot OEMs in base case",
            "risk_supply": "4nm capacity and packaging slots can compress launch timing.",
            "risk_supply_ko": "4nm 생산능력과 패키징 슬롯이 출시 일정을 압박할 수 있습니다.",
            "risk_customer": "OEM qualification cycles can stretch beyond the financing runway.",
            "risk_customer_ko": "OEM 인증 주기가 조달 runway보다 길어질 수 있습니다.",
            "risk_competition": "Large SoC vendors can bundle inference blocks into existing platforms.",
            "risk_competition_ko": "대형 SoC 업체가 기존 플랫폼에 추론 블록을 번들링할 수 있습니다.",
            "deck_label": "Strategy Deck",
            "deck_label_ko": "전략 덱",
            "assertion_1": "Local inference is becoming a product requirement, not a premium feature.",
            "assertion_1_ko": "로컬 추론은 프리미엄 기능이 아니라 제품 요구사항이 되고 있습니다.",
            "evidence_1": "OEM roadmaps increasingly ask for sub-5W sustained AI workloads.",
            "evidence_1_ko": "OEM 로드맵은 5W 이하 지속 AI 워크로드를 점점 더 요구합니다.",
            "assertion_2": "The moat is not the chip alone; it is the reusable integration layer.",
            "assertion_2_ko": "해자는 칩 자체가 아니라 재사용 가능한 통합 계층입니다.",
            "evidence_2": "The same compiler and SDK path can serve phone, laptop, and edge appliance designs.",
            "evidence_2_ko": "동일한 컴파일러와 SDK 경로가 스마트폰, 노트북, 엣지 장비 설계에 적용될 수 있습니다.",
            "roadmap": "2026 validation, 2027 first design wins, 2028 platform expansion.",
            "roadmap_ko": "2026년 검증, 2027년 첫 설계 채택, 2028년 플랫폼 확장.",
            "investor_ask": "Fund validation, customer engineering, and packaging capacity reservations.",
            "investor_ask_ko": "검증, 고객 엔지니어링, 패키징 생산능력 예약에 자금을 배정합니다.",
        }
    )
```

The generated demos must include these exact strings at least once:

```text
Haneul NPU Systems
fictional sample data
하늘 NPU 시스템즈
가상 샘플 데이터
low-power inference chiplet
on-device NPU
```

- [ ] **Step 4: Run demo generation**

Run:

```bash
python scripts/build.py --demos
```

Expected:

```text
OK: generated 24 demo HTML file(s)
OK: wrote assets/demos/demo-manifest.json
```

If the command still prints `18`, update the count assertion in `scripts/tests/test_build.py` to expect `len(shared.HTML_TEMPLATES) + len(demos.HERO_DEMOS)`.

- [ ] **Step 5: Run tests**

Run:

```bash
python scripts/tests/test_build.py
```

Expected: hero demo tests pass.

- [ ] **Step 6: Commit**

```bash
git add scripts/demos.py assets/demos/demo-manifest.json assets/demos/hero-haneul-ir-ko.html assets/demos/hero-haneul-investor-memo.html assets/demos/hero-haneul-equity-report.html assets/demos/hero-haneul-equity-report-ko.html assets/demos/hero-haneul-strategy-deck.html assets/demos/hero-haneul-landing-page.html
git commit -m "feat: generate premium hero demos"
```

## Task 7: Update README and Public Pages

**Files:**
- Modify: `README.md`
- Modify: `index.html`
- Modify: `ko.html`
- Create: `scripts/render_hero_screenshots.py`
- Update/create: `docs/design-qa/screenshots/hero-*.png`

- [ ] **Step 1: Make README lead with the proof pack**

In `README.md`, insert this heading before the existing install section:

```markdown
### Investment / Strategy Proof Pack
```

Add links to:

```markdown
- [Korean IR one-pager](assets/demos/hero-haneul-ir-ko.html)
- [English investor memo](assets/demos/hero-haneul-investor-memo.html)
- [Equity-style research report](assets/demos/hero-haneul-equity-report.html)
- [Korean strategy deck](assets/demos/hero-haneul-strategy-deck.html)
```

Move existing generic demos below this proof pack.

- [ ] **Step 2: Update public pages**

In `index.html` and `ko.html`, add a hero section that references:

```text
Haneul NPU Systems
Investment / Strategy Proof Pack
Light / Dark themes
```

Each page must link to the six `assets/demos/hero-haneul-*.html` files.

- [ ] **Step 3: Create deterministic screenshot script**

Create `scripts/render_hero_screenshots.py`:

```python
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    ("assets/demos/hero-haneul-ir-ko.html", "docs/design-qa/screenshots/hero-haneul-ir-ko.png"),
    ("assets/demos/hero-haneul-equity-report.html", "docs/design-qa/screenshots/hero-haneul-equity-report.png"),
    ("assets/demos/hero-haneul-strategy-deck.html", "docs/design-qa/screenshots/hero-haneul-strategy-deck.png"),
    ("assets/demos/hero-haneul-landing-page.html", "docs/design-qa/screenshots/hero-haneul-landing-page.png"),
]


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: Playwright is required. Run: python -m pip install playwright && python -m playwright install chromium")
        return 1

    output_dir = ROOT / "docs/design-qa/screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as browser_api:
        browser = browser_api.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100}, device_scale_factor=1)
        for html_relative, screenshot_relative in TARGETS:
            html_path = ROOT / html_relative
            screenshot_path = ROOT / screenshot_relative
            if not html_path.exists():
                print(f"ERROR: missing demo {html_relative}")
                return 1
            page.goto(html_path.as_uri(), wait_until="networkidle")
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"OK: wrote {screenshot_relative}")
        browser.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Capture hero screenshots**

Run:

```bash
python scripts/render_hero_screenshots.py
```

Expected:

```text
OK: wrote docs/design-qa/screenshots/hero-haneul-ir-ko.png
OK: wrote docs/design-qa/screenshots/hero-haneul-equity-report.png
OK: wrote docs/design-qa/screenshots/hero-haneul-strategy-deck.png
OK: wrote docs/design-qa/screenshots/hero-haneul-landing-page.png
```

If the command prints the Playwright install error, run:

```bash
python -m pip install playwright
python -m playwright install chromium
python scripts/render_hero_screenshots.py
```

Expected after installation: the same four `OK: wrote ...` lines above.

- [ ] **Step 5: Update render QA notes**

Append this section to `docs/design-qa/2026-05-22-render-qa.md`:

```markdown
## Premium Hero Lane - 2026-05-22

Captured with `scripts/render_hero_screenshots.py` at 1440 x 1100 CSS pixels.

- `docs/design-qa/screenshots/hero-haneul-ir-ko.png`
- `docs/design-qa/screenshots/hero-haneul-equity-report.png`
- `docs/design-qa/screenshots/hero-haneul-strategy-deck.png`
- `docs/design-qa/screenshots/hero-haneul-landing-page.png`
```

- [ ] **Step 6: Add screenshot existence assertions**

Extend `test_premium_hero_lane_reference_and_demos_exist()` with:

```python
for relative in [
    "docs/design-qa/screenshots/hero-haneul-ir-ko.png",
    "docs/design-qa/screenshots/hero-haneul-equity-report.png",
    "docs/design-qa/screenshots/hero-haneul-strategy-deck.png",
    "docs/design-qa/screenshots/hero-haneul-landing-page.png",
]:
    assert (ROOT / relative).exists(), f"missing hero screenshot: {relative}"
```

- [ ] **Step 7: Run tests**

Run:

```bash
python scripts/tests/test_build.py
python scripts/build.py --check
```

Expected: both pass.

- [ ] **Step 8: Commit**

```bash
git add README.md index.html ko.html scripts/render_hero_screenshots.py docs/design-qa/screenshots/hero-haneul-ir-ko.png docs/design-qa/screenshots/hero-haneul-equity-report.png docs/design-qa/screenshots/hero-haneul-strategy-deck.png docs/design-qa/screenshots/hero-haneul-landing-page.png scripts/tests/test_build.py docs/design-qa/2026-05-22-render-qa.md
git commit -m "docs: showcase premium investment proof pack"
```

## Task 8: Final Package and Verification

**Files:**
- Update: `dist/gyeol.zip`

- [ ] **Step 1: Rebuild the portable skill ZIP**

Run:

```bash
python scripts/package_skill.py
```

Expected:

```text
OK: wrote dist/gyeol.zip
OK: packaged N file(s)
```

`N` must be a positive integer and must be higher than the count printed before Task 1 because the hero reference, hero demos, screenshot script, and screenshots are now included.

- [ ] **Step 2: Run full verification**

Run:

```bash
python scripts/tests/test_build.py
python scripts/build.py --check
python C:\Users\user\.codex\skills\.system\skill-creator\scripts\quick_validate.py D:\HB\Kami_butKorean\Gyeol
git check-attr linguist-generated -- assets/demos/hero-haneul-ir-ko.html docs/design-qa/screenshots/hero-haneul-ir-ko.png dist/gyeol.zip assets/templates/one-pager.html
```

Expected:

```text
Passed: <all> | Failed: 0
OK: premium hero lane references and demos are present
Skill is valid!
assets/demos/hero-haneul-ir-ko.html: linguist-generated: true
docs/design-qa/screenshots/hero-haneul-ir-ko.png: linguist-generated: true
dist/gyeol.zip: linguist-generated: true
assets/templates/one-pager.html: linguist-generated: unspecified
```

- [ ] **Step 3: Commit final package**

```bash
git add dist/gyeol.zip
git commit -m "chore: package premium hero lane"
```

- [ ] **Step 4: Push**

```bash
git push
```

Expected: branch pushes to `origin/main` without rejection.

## Self-Review

Spec coverage:

- Hero fiction is covered in Task 2.
- Hero sample set is covered in Tasks 3-7.
- Korean enterprise editorial sans design direction is covered in Tasks 2-5.
- Light/dark policy is covered in Tasks 1, 3, 4, and 5.
- Implementation scope is limited to target templates and public docs.
- Verification strategy is covered in Tasks 1, 6, 7, and 8.

Ambiguity removed:

- The fictional company name is fixed as `Haneul NPU Systems`.
- Document themes are fixed per sample in `references/hero-haneul-npu.json`.
- Landing page toggles are browser-only; document templates use static `data-theme`.
