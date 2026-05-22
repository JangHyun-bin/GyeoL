from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Template:
    name: str
    path: str
    language: str
    kind: str
    max_pages: int


HTML_TEMPLATES = (
    Template("one-pager", "assets/templates/one-pager.html", "en", "document", 1),
    Template("one-pager-ko", "assets/templates/one-pager-ko.html", "ko", "document", 1),
    Template("long-doc", "assets/templates/long-doc.html", "en", "document", 8),
    Template("long-doc-ko", "assets/templates/long-doc-ko.html", "ko", "document", 8),
    Template("letter", "assets/templates/letter.html", "en", "document", 1),
    Template("letter-ko", "assets/templates/letter-ko.html", "ko", "document", 1),
    Template("portfolio", "assets/templates/portfolio.html", "en", "document", 8),
    Template("portfolio-ko", "assets/templates/portfolio-ko.html", "ko", "document", 8),
    Template("resume", "assets/templates/resume.html", "en", "document", 2),
    Template("resume-ko", "assets/templates/resume-ko.html", "ko", "document", 2),
    Template("slides", "assets/templates/slides.html", "en", "slides", 10),
    Template("slides-ko", "assets/templates/slides-ko.html", "ko", "slides", 10),
    Template("equity-report", "assets/templates/equity-report.html", "en", "document", 4),
    Template("equity-report-ko", "assets/templates/equity-report-ko.html", "ko", "document", 4),
    Template("changelog", "assets/templates/changelog.html", "en", "document", 2),
    Template("changelog-ko", "assets/templates/changelog-ko.html", "ko", "document", 2),
    Template("landing-page", "assets/templates/landing-page.html", "en", "screen", 0),
    Template("landing-page-ko", "assets/templates/landing-page-ko.html", "ko", "screen", 0),
)

SCREEN_PAGES = {
    "en": "index.html",
    "ko": "ko.html",
}

PLANNED_TEMPLATES = ()

HERO_DEMOS = (
    "assets/demos/hero-haneul-ir-ko.html",
    "assets/demos/hero-haneul-investor-memo.html",
    "assets/demos/hero-haneul-equity-report.html",
    "assets/demos/hero-haneul-equity-report-ko.html",
    "assets/demos/hero-haneul-strategy-deck.html",
    "assets/demos/hero-haneul-landing-page.html",
)

REQUIRED_PROJECT_FILES = (
    ".gitattributes",
    "README.md",
    "CHEATSHEET.md",
    "SKILL.md",
    "AGENTS.md",
    "docs/onboarding.md",
    "agents/openai.yaml",
    ".claude-plugin/marketplace.json",
    ".claude/launch.json",
    "llms.txt",
    "CREDITS.md",
    "NOTICE",
    "LICENSE",
    "styles.css",
    "scripts/package_skill.py",
    "references/brand-profile.md",
    "references/brand.example.md",
    "references/kami.md",
    "references/cohere.md",
    "references/design.md",
    "references/writing.md",
    "references/production.md",
    "references/roadmap.md",
    "references/hero-haneul-npu.json",
    "references/tokens.json",
    "references/checks_thresholds.json",
    "references/stabilizer_profiles.json",
)

REFERENCE_JSON_FILES = (
    "references/tokens.json",
    "references/checks_thresholds.json",
    "references/stabilizer_profiles.json",
)


def project_path(relative: str) -> Path:
    return ROOT / relative
