from __future__ import annotations

import html
import json
import re
from pathlib import Path

from scripts import shared

PLACEHOLDER_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")

COMMON_VALUES = {
    "date": "2026-05-22",
    "status": "Draft for review",
    "author": "Gyeol Team",
    "source_note": "Demo output generated from Gyeol sample data.",
    "reference_note": "Prepared with Gyeol's Korean/English document stack.",
    "sender_org": "Gyeol Studio",
    "sender_name": "Jang Hyun-bin",
    "sender_title": "Maintainer",
    "recipient": "Strategy Team",
    "contact": "seoul@example.com · github.com/JangHyun-bin/GyeoL",
    "cta_url": "#",
    "cta_label": "Start with the template",
}

SAMPLES = {
    "one-pager": {
        "kicker": "Market Brief",
        "title": "A quieter operating system for agent documents",
        "subtitle": "Gyeol gives teams a repeatable way to turn raw notes into native Korean and English business pages.",
        "decision": "Adopt Gyeol for investor notes, internal one-pagers, and weekly strategy briefs.",
        "evidence": "The current workflow produces inconsistent layouts, weak Korean phrasing, and no repeatable checks.",
        "risk": "A template system can become rigid if it optimizes for layout before content quality.",
        "plan": "Start with one-pagers and long documents, then add rendered demos after visual review.",
        "metric_1": "18",
        "metric_1_label": "verified templates",
        "metric_2": "2",
        "metric_2_label": "native languages",
        "metric_3": "0",
        "metric_3_label": "forked files",
    },
    "one-pager-ko": {
        "kicker": "시장 브리프",
        "title": "에이전트 문서를 위한 차분한 운영 체계",
        "subtitle": "결은 흩어진 메모를 한국어와 영어 비즈니스 문서로 안정적으로 바꾸는 문서 스택입니다.",
        "decision": "투자 메모, 내부 원페이지, 주간 전략 브리프에 결을 우선 적용합니다.",
        "evidence": "기존 워크플로는 레이아웃이 매번 달라지고 한국어 문장 호흡이 쉽게 어색해집니다.",
        "risk": "템플릿이 문서의 판단보다 형식을 앞세우면 실제 업무성이 떨어질 수 있습니다.",
        "plan": "원페이지와 긴 문서를 먼저 검증하고, 시각 리뷰 후 렌더 데모를 확장합니다.",
        "metric_1": "18",
        "metric_1_label": "검증 템플릿",
        "metric_2": "2",
        "metric_2_label": "네이티브 언어",
        "metric_3": "0",
        "metric_3_label": "fork 파일",
    },
    "long-doc": {
        "document_type": "Strategy Report",
        "title": "Building a native document layer for agents",
        "summary": "A practical report on why agent-generated documents need language-native templates, not only prompt instructions.",
        "executive_read": "The highest leverage move is to make document quality a repository concern: templates, references, demos, and checks live together.",
        "core_claim": "Native writing rules matter as much as layout when Korean and English outputs share one system.",
        "context": "Agent tools can draft quickly, but without stable constraints they drift across tone, hierarchy, and output shape.",
        "evidence": "Kami demonstrates that a skill plus template registry can make document generation repeatable. Gyeol adapts the pattern for Korean and English.",
        "implications": "The repo should track demos and QA notes so visual quality is visible, not implied.",
        "recommendation": "Treat each template as a product surface with sample data, browser review, and a render path.",
        "next_steps": "Generate filled demos, inspect them in browser, then add PDF rendering once dependencies are stable.",
    },
    "long-doc-ko": {
        "document_type": "전략 리포트",
        "title": "에이전트를 위한 네이티브 문서 레이어 만들기",
        "summary": "에이전트 문서 품질이 프롬프트만이 아니라 언어별 템플릿과 검증 체계에 달려 있다는 점을 정리한 리포트입니다.",
        "executive_read": "가장 큰 레버리지는 문서 품질을 repo의 책임으로 두는 것입니다. 템플릿, 레퍼런스, 데모, 검증을 함께 관리해야 합니다.",
        "core_claim": "한국어와 영어가 한 시스템 안에 있을수록 레이아웃만큼 네이티브 문장 규칙이 중요합니다.",
        "context": "에이전트는 빠르게 초안을 만들지만, 제약이 없으면 톤과 위계, 산출물 형태가 매번 달라집니다.",
        "evidence": "Kami는 skill과 template registry가 문서 생성을 반복 가능하게 만든다는 점을 보여줍니다. 결은 그 구조를 한국어와 영어에 맞게 다시 설계합니다.",
        "implications": "시각 품질을 암묵적으로 믿지 말고 데모와 QA 기록으로 확인해야 합니다.",
        "recommendation": "각 템플릿을 제품 화면처럼 다루고, 샘플 데이터와 브라우저 리뷰, 렌더 경로를 붙입니다.",
        "next_steps": "filled demo를 생성하고 브라우저에서 확인한 뒤, 의존성이 정리되면 PDF 렌더를 추가합니다.",
    },
    "letter": {
        "subject": "Request to adopt Gyeol for bilingual strategy documents",
        "opening": "Thank you for reviewing the current document workflow.",
        "body": "The team needs a repeatable way to create Korean and English deliverables without rebuilding layout decisions each time.",
        "request": "I recommend adopting Gyeol as the default starting point for briefs, reports, and decks.",
        "closing": "Please let me know which document type should be piloted first.",
    },
    "letter-ko": {
        "subject": "한국어/영어 전략 문서에 결 적용 요청",
        "opening": "현재 문서 워크플로를 검토해 주셔서 감사합니다.",
        "body": "팀은 매번 레이아웃을 다시 정하지 않고도 한국어와 영어 산출물을 안정적으로 만들 방법이 필요합니다.",
        "request": "브리프, 리포트, 발표자료의 기본 출발점으로 결을 적용하는 방안을 제안드립니다.",
        "closing": "우선 적용할 문서 타입을 알려주시면 파일럿 범위를 정리하겠습니다.",
    },
    "portfolio": {
        "name": "Gyeol Document Systems",
        "role": "Open document stack",
        "positioning": "A portfolio of templates that turn agent drafts into native Korean and English deliverables.",
        "project_1": "One-Pager System",
        "project_1_summary": "Condenses a decision, evidence, risk, and metrics into a single executive page.",
        "project_1_tag": "brief",
        "project_2": "Long Document System",
        "project_2_summary": "Shapes research and proposals into a readable report rhythm.",
        "project_2_tag": "report",
        "project_3": "Deck System",
        "project_3_summary": "Builds decision-oriented slides without decorative noise.",
        "project_3_tag": "slides",
        "project_4": "Release Notes System",
        "project_4_summary": "Keeps product changes compact, scannable, and bilingual.",
        "project_4_tag": "release",
    },
    "portfolio-ko": {
        "name": "결 문서 시스템",
        "role": "오픈 문서 스택",
        "positioning": "에이전트 초안을 한국어와 영어 네이티브 산출물로 정리하는 템플릿 묶음입니다.",
        "project_1": "원페이지 시스템",
        "project_1_summary": "결정, 근거, 리스크, 지표를 한 장의 임원용 페이지로 압축합니다.",
        "project_1_tag": "brief",
        "project_2": "긴 문서 시스템",
        "project_2_summary": "리서치와 제안서를 읽기 좋은 리포트 흐름으로 정리합니다.",
        "project_2_tag": "report",
        "project_3": "덱 시스템",
        "project_3_summary": "장식보다 의사결정에 집중한 발표자료를 만듭니다.",
        "project_3_tag": "slides",
        "project_4": "변경 기록 시스템",
        "project_4_summary": "제품 변경 사항을 간결하고 읽기 좋게 정리합니다.",
        "project_4_tag": "release",
    },
    "resume": {
        "name": "Jang Hyun-bin",
        "headline": "Document systems builder for Korean and English agent workflows",
        "profile": "Builds practical tooling that helps agents produce business documents with stable structure, checks, and language-native copy.",
        "role_1": "Maintainer",
        "company_1": "Gyeol",
        "period_1": "2026",
        "impact_1": "Created an 18-template bilingual registry with structural checks.",
        "impact_2": "Separated Kami attribution from Gyeol-specific implementation.",
        "role_2": "Research Operator",
        "company_2": "Independent",
        "period_2": "2024-2026",
        "impact_3": "Turned investment and product notes into reusable document systems.",
        "projects": "Gyeol, Kami analysis, Cohere design reference adaptation.",
        "skills": "Document systems, Korean business writing, agent workflows, HTML templates.",
    },
    "resume-ko": {
        "name": "장현빈",
        "headline": "한국어/영어 에이전트 문서 워크플로를 만드는 문서 시스템 빌더",
        "profile": "에이전트가 안정적인 구조, 검증, 네이티브 문장으로 비즈니스 문서를 만들도록 돕는 실용 도구를 만듭니다.",
        "role_1": "메인테이너",
        "company_1": "결",
        "period_1": "2026",
        "impact_1": "18개 한국어/영어 템플릿 registry와 구조 검증을 구축했습니다.",
        "impact_2": "Kami 출처 표기와 Gyeol 전용 구현을 명확히 분리했습니다.",
        "role_2": "리서치 오퍼레이터",
        "company_2": "Independent",
        "period_2": "2024-2026",
        "impact_3": "투자와 제품 메모를 재사용 가능한 문서 시스템으로 전환했습니다.",
        "projects": "결, Kami 분석, Cohere 디자인 레퍼런스 적용.",
        "skills": "문서 시스템, 한국어 비즈니스 글쓰기, 에이전트 워크플로, HTML 템플릿.",
    },
    "slides": {
        "deck_label": "Gyeol Deck",
        "title": "Native documents are infrastructure",
        "subtitle": "A small template registry can make agent output repeatable, testable, and language-aware.",
        "section_title": "What changes when demos exist",
        "section_summary": "The team can judge the actual page, not the promise of a template.",
        "point_1": "Visible quality",
        "point_1_detail": "Filled examples expose spacing, rhythm, and copy problems.",
        "point_2": "Repeatable checks",
        "point_2_detail": "Registry tests keep template drift from hiding.",
        "point_3": "Better prompts",
        "point_3_detail": "Agents can target concrete examples instead of abstract rules.",
    },
    "slides-ko": {
        "deck_label": "Gyeol Deck",
        "title": "네이티브 문서는 인프라입니다",
        "subtitle": "작은 템플릿 registry만 있어도 에이전트 산출물은 반복 가능하고 검증 가능한 문서가 됩니다.",
        "section_title": "데모가 생기면 달라지는 것",
        "section_summary": "팀은 템플릿의 약속이 아니라 실제 페이지를 보고 판단할 수 있습니다.",
        "point_1": "보이는 품질",
        "point_1_detail": "filled example은 간격, 호흡, 문장 문제를 바로 드러냅니다.",
        "point_2": "반복 검증",
        "point_2_detail": "registry 테스트가 템플릿 drift를 숨기지 못하게 합니다.",
        "point_3": "더 나은 프롬프트",
        "point_3_detail": "에이전트는 추상 규칙보다 구체 예시를 기준으로 작업합니다.",
    },
    "equity-report": {
        "ticker": "NVDA",
        "company": "NVIDIA Corporation",
        "thesis": "AI infrastructure demand remains strong, but expectations require sharper risk discipline.",
        "rating": "Watch",
        "target_price": "Scenario-based",
        "revenue": "+78%",
        "margin": "73%",
        "growth": "High",
        "investment_thesis": "The company remains central to accelerated computing, but valuation depends on durability of data center demand.",
        "risks": "Customer concentration, supply constraints, export controls, and faster-than-expected custom silicon adoption.",
        "watch_items": "Cloud capex commentary, gross margin direction, networking attach rate, and inference workload mix.",
    },
    "equity-report-ko": {
        "ticker": "NVDA",
        "company": "엔비디아",
        "thesis": "AI 인프라 수요는 강하지만, 높아진 기대치에는 더 엄격한 리스크 관리가 필요합니다.",
        "rating": "관찰",
        "target_price": "시나리오 기준",
        "revenue": "+78%",
        "margin": "73%",
        "growth": "높음",
        "investment_thesis": "엔비디아는 가속 컴퓨팅의 중심에 있지만, 밸류에이션은 데이터센터 수요의 지속성에 달려 있습니다.",
        "risks": "고객 집중도, 공급 제약, 수출 규제, 커스텀 실리콘 전환 속도가 핵심 리스크입니다.",
        "watch_items": "클라우드 capex 코멘트, 매출총이익률 방향, 네트워킹 attach rate, inference workload mix를 확인합니다.",
    },
    "changelog": {
        "version": "v0.2.0",
        "release_name": "Full Bilingual Stack",
        "summary": "This release expands Gyeol from a core starter set to a full nine-type Korean/English template stack.",
        "added_1": "Added letter, portfolio, resume, equity report, changelog, and landing-page templates.",
        "added_2": "Added Korean siblings for every verified template.",
        "changed_1": "Updated the registry from 6 to 18 verified templates.",
        "changed_2": "Updated README, SKILL, and roadmap language to match the new scope.",
        "fixed_1": "Removed the Phase 1-only planned template boundary.",
        "fixed_2": "Aligned structural checks with the full template set.",
    },
    "changelog-ko": {
        "version": "v0.2.0",
        "release_name": "전체 이중언어 스택",
        "summary": "이번 릴리스는 결을 핵심 3종에서 9종 한국어/영어 템플릿 스택으로 확장합니다.",
        "added_1": "서한, 포트폴리오, 이력서, 리서치 리포트, 변경 기록, 랜딩 페이지 템플릿을 추가했습니다.",
        "added_2": "모든 검증 템플릿에 한국어 sibling을 추가했습니다.",
        "changed_1": "registry를 6개에서 18개 검증 템플릿으로 확장했습니다.",
        "changed_2": "README, SKILL, roadmap 문구를 새 범위에 맞게 갱신했습니다.",
        "fixed_1": "Phase 1 전용 planned template 경계를 제거했습니다.",
        "fixed_2": "구조 검증을 전체 템플릿 집합에 맞췄습니다.",
    },
    "landing-page": {
        "product_name": "Gyeol",
        "headline": "Native Korean and English documents for agents.",
        "subhead": "Use one quiet stack to create briefs, reports, decks, release notes, and landing pages without rebuilding the design each time.",
        "proof_panel": "18 templates · 2 languages · structural checks · Kami credit preserved",
        "feature_1": "Korean and English are first-class outputs.",
        "feature_2": "Templates stay self-contained and easy to copy.",
        "feature_3": "Checks keep the registry honest.",
    },
    "landing-page-ko": {
        "product_name": "결",
        "headline": "에이전트를 위한 한국어와 영어 네이티브 문서.",
        "subhead": "브리프, 리포트, 덱, 변경 기록, 랜딩 페이지를 매번 다시 설계하지 않고 하나의 차분한 스택으로 만듭니다.",
        "proof_panel": "18개 템플릿 · 2개 언어 · 구조 검증 · Kami 출처 보존",
        "feature_1": "한국어와 영어를 모두 first-class 산출물로 다룹니다.",
        "feature_2": "템플릿은 self-contained 형태를 유지합니다.",
        "feature_3": "검증이 registry의 품질을 지킵니다.",
    },
}


def _fallback_value(name: str, template_name: str) -> str:
    label = name.replace("_", " ")
    if template_name.endswith("-ko"):
        return f"{label} 샘플"
    return f"Sample {label}"


def _values_for(template_name: str) -> dict[str, str]:
    values = dict(COMMON_VALUES)
    values.update(SAMPLES.get(template_name, {}))
    return values


def fill_template(template_name: str, source: str) -> str:
    values = _values_for(template_name)

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = values.get(key, _fallback_value(key, template_name))
        return html.escape(value, quote=False)

    return PLACEHOLDER_RE.sub(replace, source)


def generate_all() -> dict:
    demo_dir = shared.project_path("assets/demos")
    demo_dir.mkdir(parents=True, exist_ok=True)

    demos = []
    for template in shared.HTML_TEMPLATES:
        source = shared.project_path(template.path).read_text(encoding="utf-8")
        output = fill_template(template.name, source)
        output_name = f"demo-{template.name}.html"
        output_path = demo_dir / output_name
        output_path.write_text(output, encoding="utf-8", newline="\n")
        demos.append(
            {
                "name": template.name,
                "language": template.language,
                "kind": template.kind,
                "template": template.path,
                "path": f"assets/demos/{output_name}",
            }
        )

    manifest = {"generated_by": "scripts/demos.py", "demos": demos}
    manifest_path = demo_dir / "demo-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    manifest = generate_all()
    print(f"OK: generated {len(manifest['demos'])} demo HTML file(s)")
    print("OK: wrote assets/demos/demo-manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
