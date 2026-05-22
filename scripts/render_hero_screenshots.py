from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CAPTURES = [
    (
        "assets/demos/hero-haneul-ir-ko.html",
        "docs/design-qa/screenshots/hero-haneul-ir-ko.png",
    ),
    (
        "assets/demos/hero-haneul-equity-report.html",
        "docs/design-qa/screenshots/hero-haneul-equity-report.png",
    ),
    (
        "assets/demos/hero-haneul-strategy-deck.html",
        "docs/design-qa/screenshots/hero-haneul-strategy-deck.png",
    ),
    (
        "assets/demos/hero-haneul-landing-page.html",
        "docs/design-qa/screenshots/hero-haneul-landing-page.png",
    ),
]


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "ERROR: Playwright is required. Run: python -m pip install playwright && "
            "python -m playwright install chromium"
        )
        return 1

    output_dir = ROOT / "docs/design-qa/screenshots"
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1440, "height": 1100},
            device_scale_factor=1,
        )
        page = context.new_page()
        for source, target in CAPTURES:
            source_path = ROOT / source
            target_path = ROOT / target
            page.goto(source_path.as_uri(), wait_until="networkidle")
            page.screenshot(path=target_path, full_page=True)
            print(f"OK: captured {target}")
        browser.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
