from __future__ import annotations

import html
import json
import re
from pathlib import Path

from scripts import shared

PLACEHOLDER_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")

COMMON_VALUES = {
    "date": "2026-05-22",
    "theme": "light",
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
    "company": "Gyeol Document Systems",
    "company_ko": "결 문서 시스템즈",
    "sample_notice": "Demo sample data for template review.",
    "sample_notice_ko": "템플릿 검토를 위한 가상 샘플 데이터입니다.",
    "thesis": "A reusable document layer makes agent output easier to review, compare, and ship.",
    "thesis_ko": "재사용 가능한 문서 레이어는 에이전트 산출물을 검토하고 비교하고 배포하기 쉽게 만듭니다.",
    "market_wedge": "Start with investor and strategy documents where structure, tone, and evidence density matter.",
    "market_wedge_ko": "구조, 톤, 근거 밀도가 중요한 투자자 및 전략 문서부터 시작합니다.",
    "technology_moat": "Template metadata, filled demos, and checks keep the system repeatable across languages.",
    "technology_moat_ko": "템플릿 메타데이터, 채워진 데모, 검증이 언어 간 반복성을 지킵니다.",
    "risk_1": "Teams may treat templates as final copy instead of a stronger review surface.",
    "risk_1_ko": "팀이 템플릿을 더 나은 검토 화면이 아니라 최종 원고로 오해할 수 있습니다.",
    "risk_2": "Visual quality can drift if generated examples are not inspected after template changes.",
    "risk_2_ko": "템플릿 변경 뒤 생성 예시를 확인하지 않으면 시각 품질이 흔들릴 수 있습니다.",
    "next_decision": "Pick one document family, review filled output, then standardize the workflow.",
    "next_decision_ko": "문서군 하나를 고르고 채워진 결과를 검토한 뒤 워크플로를 표준화합니다.",
    "memo_title": "Investor Memo for a Template-Native Document Stack",
    "memo_title_ko": "템플릿 네이티브 문서 스택 투자 메모",
    "executive_summary": "Gyeol demonstrates how templates, sample data, and checks can turn agent drafts into reviewable business documents.",
    "executive_summary_ko": "결은 템플릿, 샘플 데이터, 검증으로 에이전트 초안을 검토 가능한 비즈니스 문서로 바꾸는 방식을 보여줍니다.",
    "why_now": "Agent-generated deliverables are moving from experiments into repeatable operating workflows.",
    "why_now_ko": "에이전트 생성 산출물이 실험에서 반복 가능한 운영 워크플로로 이동하고 있습니다.",
    "product_surface": "The product surface is a registry of copy-ready templates with generated proof examples.",
    "product_surface_ko": "제품 표면은 생성된 증명 예시를 포함한 복사 가능한 템플릿 레지스트리입니다.",
    "business_model": "Adoption starts as an internal documentation standard before expanding into packaged workflows.",
    "business_model_ko": "도입은 내부 문서 표준에서 시작해 패키지형 워크플로로 확장됩니다.",
    "risk_register": "Template drift, weak sample data, and missing visual QA remain the main operating risks.",
    "risk_register_ko": "템플릿 드리프트, 약한 샘플 데이터, 누락된 시각 QA가 주요 운영 리스크입니다.",
    "investment_view": "The opportunity is strongest where bilingual writing quality and repeatable structure are both required.",
    "investment_view_ko": "이 기회는 이중언어 문장 품질과 반복 가능한 구조가 모두 필요한 곳에서 가장 큽니다.",
    "rating": "Constructive",
    "rating_ko": "긍정적",
    "base_case": "The document stack becomes a dependable starting point for recurring business deliverables.",
    "base_case_ko": "문서 스택이 반복 비즈니스 산출물의 신뢰 가능한 출발점이 됩니다.",
    "upside_case": "Teams treat generated demos as a design QA surface and expand usage across functions.",
    "upside_case_ko": "팀이 생성 데모를 디자인 QA 화면으로 보고 여러 기능 조직으로 사용을 넓힙니다.",
    "downside_case": "Templates are copied without review discipline, reducing consistency gains.",
    "downside_case_ko": "검토 규율 없이 템플릿만 복사되어 일관성 개선 효과가 줄어듭니다.",
    "kpi_revenue": "Template adoption across three recurring workflows",
    "kpi_revenue_ko": "반복 워크플로 3개에서 템플릿 도입",
    "kpi_margin": "Low maintenance burden through shared tokens",
    "kpi_margin_ko": "공유 토큰으로 낮은 유지보수 부담",
    "kpi_design_wins": "Validated one-pager, memo, deck, and landing-page surfaces",
    "kpi_design_wins_ko": "원페이지, 메모, 덱, 랜딩 페이지 화면 검증",
    "risk_supply": "Reference data and screenshots must stay current as templates change.",
    "risk_supply_ko": "템플릿 변경에 맞춰 참조 데이터와 스크린샷을 최신으로 유지해야 합니다.",
    "risk_customer": "Users may need clearer examples before trusting the workflow for external documents.",
    "risk_customer_ko": "외부 문서에 쓰기 전 사용자는 더 명확한 예시를 필요로 할 수 있습니다.",
    "risk_competition": "General document tools can imitate layout but often miss language-native rules.",
    "risk_competition_ko": "범용 문서 도구는 레이아웃은 흉내낼 수 있지만 언어 네이티브 규칙을 놓치기 쉽습니다.",
    "deck_label": "Strategy Deck",
    "deck_label_ko": "전략 발표자료",
    "assertion_1": "Filled examples expose quality faster than template screenshots.",
    "assertion_1_ko": "채워진 예시는 템플릿 스크린샷보다 품질을 더 빨리 드러냅니다.",
    "evidence_1": "Every generated demo exercises real placeholder data and language-specific copy.",
    "evidence_1_ko": "모든 생성 데모는 실제 플레이스홀더 데이터와 언어별 문장을 검증합니다.",
    "assertion_2": "A registry plus tests keeps document surfaces from drifting silently.",
    "assertion_2_ko": "레지스트리와 테스트는 문서 화면이 조용히 흔들리는 일을 막습니다.",
    "evidence_2": "Build checks fail when templates, manifest entries, or required generated outputs are missing.",
    "evidence_2_ko": "템플릿, 매니페스트 항목, 필수 생성물이 빠지면 빌드 검증이 실패합니다.",
    "roadmap": "Regenerate demos after template changes, review the hero lane, then update proof-pack screenshots.",
    "roadmap_ko": "템플릿 변경 뒤 데모를 다시 생성하고 히어로 레인을 검토한 다음 증명 팩 스크린샷을 갱신합니다.",
    "investor_ask": "Approve the hero sample set as the standard proof path for investment and strategy templates.",
    "investor_ask_ko": "투자 및 전략 템플릿의 표준 증명 경로로 히어로 샘플 세트를 승인합니다.",
}

HERO_DEMOS = [
    ("hero-haneul-ir-ko", "one-pager-ko", "ir_one_pager", shared.HERO_DEMOS[0]),
    ("hero-haneul-investor-memo", "long-doc", "investor_memo", shared.HERO_DEMOS[1]),
    ("hero-haneul-equity-report", "equity-report", "equity_report", shared.HERO_DEMOS[2]),
    ("hero-haneul-equity-report-ko", "equity-report-ko", "equity_report", shared.HERO_DEMOS[3]),
    ("hero-haneul-strategy-deck", "slides-ko", "strategy_deck", shared.HERO_DEMOS[4]),
    ("hero-haneul-landing-page", "landing-page", "landing_page", shared.HERO_DEMOS[5]),
]

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
        "company": "Gyeol Document Systems",
        "sample_notice": "Demo sample data for template review.",
        "title": "Native documents are infrastructure",
        "subtitle": "A small template registry can make agent output repeatable, testable, and language-aware.",
        "assertion_1": "Filled examples expose quality faster than template screenshots.",
        "evidence_1": "Every generated demo exercises real placeholder data and language-specific copy.",
        "assertion_2": "A registry plus tests keeps document surfaces from drifting silently.",
        "evidence_2": "Build checks fail when templates, manifest entries, or required generated outputs are missing.",
        "roadmap": "Regenerate demos after template changes, review the hero lane, then update proof-pack screenshots.",
        "risk_register": "Template drift, weak sample data, and missing visual QA remain the main operating risks.",
        "investor_ask": "Approve the sample set as the standard proof path for strategy templates.",
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
        "deck_label_ko": "결 전략 발표자료",
        "company_ko": "결 문서 시스템즈",
        "sample_notice_ko": "템플릿 검토를 위한 가상 샘플 데이터입니다.",
        "title": "네이티브 문서는 인프라입니다",
        "subtitle": "작은 템플릿 registry만 있어도 에이전트 산출물은 반복 가능하고 검증 가능한 문서가 됩니다.",
        "assertion_1_ko": "채워진 예시는 템플릿 스크린샷보다 품질을 더 빨리 드러냅니다.",
        "evidence_1_ko": "모든 생성 데모는 실제 플레이스홀더 데이터와 언어별 문장을 검증합니다.",
        "assertion_2_ko": "레지스트리와 테스트는 문서 화면이 조용히 흔들리는 일을 막습니다.",
        "evidence_2_ko": "템플릿, 매니페스트 항목, 필수 생성물이 빠지면 빌드 검증이 실패합니다.",
        "roadmap_ko": "템플릿 변경 뒤 데모를 다시 생성하고 히어로 레인을 검토한 다음 증명 팩 스크린샷을 갱신합니다.",
        "risk_register_ko": "템플릿 드리프트, 약한 샘플 데이터, 누락된 시각 QA가 주요 운영 리스크입니다.",
        "investor_ask_ko": "전략 템플릿의 표준 증명 경로로 샘플 세트를 승인합니다.",
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


def _load_hero_reference() -> dict:
    path = shared.project_path("references/hero-haneul-npu.json")
    return json.loads(path.read_text(encoding="utf-8"))


def _hero_values(kind: str) -> dict[str, str]:
    ref = _load_hero_reference()
    company = ref["company"]
    metrics = ref["metrics"]
    company_name = company["name"]
    company_ko = "하늘 NPU 시스템즈"
    sample_notice = "Fictional sample data for Gyeol demos. Not an investment recommendation."
    sample_notice_ko = "Gyeol 데모를 위한 가상 샘플 데이터입니다. 투자 의견이 아닙니다."

    return {
        "theme": ref["themes"][kind],
        "company": company_name,
        "company_ko": company_ko,
        "sample_notice": sample_notice,
        "sample_notice_ko": sample_notice_ko,
        "metric_1": metrics["power_reduction"],
        "metric_2": metrics["design_wins"],
        "metric_3": metrics["runway"],
        "thesis": f"{company_name} is a fictional Korean fabless company focused on on-device NPU adoption for premium mobile and laptop OEMs.",
        "thesis_ko": f"{company_ko}는 프리미엄 모바일과 노트북 OEM의 on-device NPU 채택에 집중하는 가상 한국 팹리스 기업입니다.",
        "market_wedge": "Start with OEMs that need private, low-latency AI features without sending sensitive user data to cloud inference.",
        "market_wedge_ko": "민감한 사용자 데이터를 클라우드 추론으로 보내지 않고 비공개 저지연 AI 기능이 필요한 OEM부터 진입합니다.",
        "technology_moat": f"The core moat is a {company['moat']} validated against {metrics['prototype_tops']} prototype targets.",
        "technology_moat_ko": f"핵심 방어력은 {metrics['prototype_tops']} 프로토타입 목표로 검증 중인 low-power inference chiplet과 재사용 가능한 NPU IP 플랫폼입니다.",
        "risk_1": "Customer conversion depends on qualification cycles with large device makers and their silicon roadmaps.",
        "risk_1_ko": "고객 전환은 대형 디바이스 제조사의 검증 주기와 실리콘 로드맵에 좌우됩니다.",
        "risk_2": "The plan assumes advanced-node supply access and sustained interest in local AI inference.",
        "risk_2_ko": "계획은 선단 공정 공급 접근성과 로컬 AI 추론 수요가 지속된다는 가정에 기대고 있습니다.",
        "next_decision": "Approve the next diligence sprint around customer pilots, foundry capacity, and power-per-token benchmarks.",
        "next_decision_ko": "고객 파일럿, 파운드리 용량, 토큰당 전력 벤치마크를 중심으로 다음 실사 스프린트를 승인합니다.",
        "memo_title": "Investor Memo: Haneul NPU Systems",
        "memo_title_ko": "투자 메모: 하늘 NPU 시스템즈",
        "executive_summary": f"{company_name} is presented with fictional sample data to test a premium investor memo for an on-device NPU company.",
        "executive_summary_ko": f"{company_ko}는 on-device NPU 기업용 프리미엄 투자 메모를 검증하기 위한 가상 샘플 데이터로 제시됩니다.",
        "why_now": "AI workloads are moving toward hybrid execution, and device makers need lower power inference close to the user.",
        "why_now_ko": "AI 워크로드가 하이브리드 실행으로 이동하면서 디바이스 제조사는 사용자 가까이에서 저전력 추론을 필요로 합니다.",
        "product_surface": "A low-power inference chiplet, reusable NPU IP, compiler support, and OEM integration kits.",
        "product_surface_ko": "저전력 추론 칩렛, 재사용 가능한 NPU IP, 컴파일러 지원, OEM 통합 키트입니다.",
        "business_model": "Licensing, NRE, and chiplet revenue tied to pilot OEM ramps and reference designs.",
        "business_model_ko": "파일럿 OEM 양산과 레퍼런스 디자인에 연동된 라이선스, NRE, 칩렛 매출 모델입니다.",
        "risk_register": "Foundry access, OEM concentration, benchmark credibility, and competition from in-house silicon remain the main risks.",
        "risk_register_ko": "파운드리 접근성, OEM 집중도, 벤치마크 신뢰도, 자체 실리콘 경쟁이 주요 리스크입니다.",
        "investment_view": "The opportunity is attractive if pilots convert into durable design wins before larger incumbents compress the wedge.",
        "investment_view_ko": "대형 경쟁사가 진입 폭을 좁히기 전에 파일럿이 지속적인 디자인 윈으로 전환된다면 매력적인 기회입니다.",
        "rating": "Constructive / diligence in progress",
        "rating_ko": "긍정적 / 실사 진행 중",
        "base_case": f"{metrics['design_wins']} validate the roadmap and support a {metrics['gross_margin_target']} gross-margin target.",
        "base_case_ko": f"{metrics['design_wins']}가 로드맵을 검증하고 {metrics['gross_margin_target']} 매출총이익률 목표를 뒷받침합니다.",
        "upside_case": "A flagship handset win makes the NPU IP platform a reference design for adjacent laptop and edge devices.",
        "upside_case_ko": "플래그십 스마트폰 채택이 NPU IP 플랫폼을 노트북 및 엣지 디바이스의 레퍼런스 디자인으로 확장합니다.",
        "downside_case": "Qualification delays push revenue recognition out while competitors bundle similar NPU blocks.",
        "downside_case_ko": "검증 지연으로 매출 인식이 밀리고 경쟁사가 유사한 NPU 블록을 번들로 제공합니다.",
        "kpi_revenue": "Pilot revenue from chiplet evaluation kits and OEM NRE",
        "kpi_revenue_ko": "칩렛 평가 키트와 OEM NRE 기반 파일럿 매출",
        "kpi_margin": f"Target gross margin of {metrics['gross_margin_target']} after IP reuse improves mix",
        "kpi_margin_ko": f"IP 재사용으로 믹스가 개선된 뒤 {metrics['gross_margin_target']} 매출총이익률 목표",
        "kpi_design_wins": f"{metrics['design_wins']} with a {metrics['process_node']} roadmap and {metrics['prototype_tops']} prototype target",
        "kpi_design_wins_ko": f"{metrics['design_wins']}, {metrics['process_node']} 로드맵, {metrics['prototype_tops']} 프로토타입 목표",
        "risk_supply": "Advanced-node wafer access could constrain launch timing and pilot allocation.",
        "risk_supply_ko": "선단 공정 웨이퍼 접근성이 출시 일정과 파일럿 배정을 제약할 수 있습니다.",
        "risk_customer": "A small number of OEM pilots can overstate true market pull if conversion evidence is thin.",
        "risk_customer_ko": "소수 OEM 파일럿은 전환 근거가 약할 경우 실제 시장 수요를 과대평가하게 만들 수 있습니다.",
        "risk_competition": "Large SoC vendors can bundle NPUs and pressure standalone chiplet economics.",
        "risk_competition_ko": "대형 SoC 벤더가 NPU를 번들로 제공하며 독립 칩렛 경제성을 압박할 수 있습니다.",
        "deck_label": "Premium Strategy Deck",
        "deck_label_ko": "프리미엄 전략 발표자료",
        "assertion_1": "The on-device NPU wedge is strongest where privacy, latency, and battery life all matter.",
        "assertion_1_ko": "on-device NPU 진입점은 개인정보, 지연시간, 배터리 수명이 모두 중요한 영역에서 가장 강합니다.",
        "evidence_1": f"The sample case uses {metrics['power_reduction']} lower power and {metrics['prototype_tops']} prototype throughput as diligence anchors.",
        "evidence_1_ko": f"샘플 케이스는 {metrics['power_reduction']} 전력 절감과 {metrics['prototype_tops']} 프로토타입 처리량을 실사 기준으로 둡니다.",
        "assertion_2": "A low-power inference chiplet can create a focused beachhead before full SoC integration.",
        "assertion_2_ko": "low-power inference chiplet은 전체 SoC 통합 전 집중된 교두보를 만들 수 있습니다.",
        "evidence_2": f"{metrics['design_wins']} and {metrics['runway']} runway frame the next financing and validation window.",
        "evidence_2_ko": f"{metrics['design_wins']}와 {metrics['runway']} 런웨이가 다음 투자 및 검증 기간을 규정합니다.",
        "roadmap": "Complete OEM pilot validation, lock foundry capacity, and publish power-per-token benchmarks for the next diligence gate.",
        "roadmap_ko": "OEM 파일럿 검증을 완료하고 파운드리 용량을 확보하며 다음 실사 게이트를 위한 토큰당 전력 벤치마크를 공개합니다.",
        "investor_ask": "Fund the diligence sprint around pilot conversion, supply capacity, and benchmark repeatability.",
        "investor_ask_ko": "파일럿 전환, 공급 역량, 벤치마크 반복성을 검증하는 실사 스프린트에 자금을 배정합니다.",
        "product_name": company_name,
        "headline": "On-device NPU silicon for private, low-power AI.",
        "subhead": f"{company_name} is a fictional sample company building a low-power inference chiplet and NPU IP platform for premium devices.",
        "proof_panel": f"{sample_notice} {metrics['process_node']} roadmap, {metrics['power_reduction']} power reduction target, {metrics['design_wins']} under review.",
        "feature_1": "Private AI workloads run closer to the user with lower latency.",
        "feature_2": "Reusable NPU IP supports smartphones, laptops, and edge devices.",
        "feature_3": "Pilot evidence is framed for investor-grade diligence.",
        "cta_label": "Review sample memo",
        "cta_url": "#investor-memo",
    }


def _template_by_name() -> dict[str, shared.Template]:
    return {template.name: template for template in shared.HTML_TEMPLATES}


def fill_template(template_name: str, source: str, explicit_values: dict[str, str] | None = None) -> str:
    values = _values_for(template_name)
    if explicit_values:
        values.update(explicit_values)

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = values.get(key, _fallback_value(key, template_name))
        return html.escape(str(value), quote=True)

    return PLACEHOLDER_RE.sub(replace, source)


def generate_all() -> dict:
    demo_dir = shared.project_path("assets/demos")
    demo_dir.mkdir(parents=True, exist_ok=True)

    demos = []
    templates = _template_by_name()
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

    for output_stem, template_name, hero_kind, output_relative in HERO_DEMOS:
        template = templates[template_name]
        source = shared.project_path(template.path).read_text(encoding="utf-8")
        output = fill_template(template.name, source, _hero_values(hero_kind))
        output_path = shared.project_path(output_relative)
        output_path.write_text(output, encoding="utf-8", newline="\n")
        demos.append(
            {
                "hero": True,
                "name": output_stem,
                "language": template.language,
                "kind": template.kind,
                "template": template.path,
                "path": output_relative,
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
