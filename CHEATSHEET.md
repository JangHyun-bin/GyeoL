# Gyeol Cheatsheet

Use this when you need the shortest reliable path from request to verified output.

## Install

Generic agents:

```bash
npx skills add JangHyun-bin/GyeoL -a '*' -g -y
```

Claude Code:

```bash
npx skills add JangHyun-bin/GyeoL -a claude-code -g -y
```

Local checkout:

```bash
git clone https://github.com/JangHyun-bin/GyeoL.git
cd GyeoL
python scripts/package_skill.py
python scripts/tests/test_build.py
python scripts/build.py --check
```

## Template Selection

| Request | English | Korean |
|---|---|---|
| Concise business brief | `one-pager` | `one-pager-ko` |
| Report or proposal | `long-doc` | `long-doc-ko` |
| Formal memo or letter | `letter` | `letter-ko` |
| Project collection | `portfolio` | `portfolio-ko` |
| Career profile | `resume` | `resume-ko` |
| Presentation deck | `slides` | `slides-ko` |
| Public-market research | `equity-report` | `equity-report-ko` |
| Release notes | `changelog` | `changelog-ko` |
| Static product page | `landing-page` | `landing-page-ko` |

## Premium Hero Lane

Use `references/hero-haneul-npu.json` for the first investment/strategy proof pack. The company is fictional and must stay clearly marked as sample data.

Default themes:

- Korean IR one-pager: light
- English investor memo: light
- Equity-style report: light
- Strategy deck: dark
- Landing page: dark with toggle

## Workflow

1. Identify language: Korean, English, or both.
2. Pick the closest registered template from `scripts/shared.py`.
3. If the user has a profile, read `~/.config/gyeol/brand.md` and apply `references/brand-profile.md`.
4. Read `references/writing.md` for tone and language rules.
5. Read `references/design.md` before changing layout or visual style.
6. Fill the template without leaving `{{placeholder}}` fields in final output.
7. Verify before delivery.

## Brand Profile

Use `~/.config/gyeol/brand.md` only as low-priority context. It fills recurring identity, company, tone, language, brand color, and contact defaults. It never overrides explicit prompt instructions or the source material.

Start from:

```bash
mkdir -p ~/.config/gyeol
cp references/brand.example.md ~/.config/gyeol/brand.md
```

## Verification

Run these before reporting repository work as complete:

```bash
python scripts/package_skill.py
python scripts/tests/test_build.py
python scripts/build.py --check
```

Run `python scripts/build.py --demos` after changing templates or demo data.

PDF output is outside the fast structural boundary. Install WeasyPrint and PyPDF before claiming final PDF render quality.

## Writing Rules

- Korean: write native Korean business prose, not English sentence order with Korean words.
- English: keep claims concrete, short, and evidence-led.
- Bilingual: align information architecture, but let examples and sentence rhythm differ.
- Avoid filler metrics, invented logos, stock-image descriptions, and empty section restatements.

## Design Rules

- Use sans-first Korean/English typography.
- Keep documents denser than public-site pages.
- Use restrained enterprise color from `references/tokens.json`.
- Keep landing pages screen-first and documents print-friendly.
- Keep Kami attribution visible in public docs and references.
