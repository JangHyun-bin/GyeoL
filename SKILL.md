---
name: gyeol
description: Create native Korean and English business documents using the Gyeol document stack. Use when asked to produce one-pagers, long documents, slide decks, or other professional deliverables that should read naturally in Korean and English, especially for agent-generated business reports, proposals, strategy notes, and presentations.
---

# Gyeol

Use Gyeol to produce professional Korean and English business documents from source material.

For installation, packaging, or cross-agent setup questions, read `docs/onboarding.md`.

## Step 0 - Load Brand Profile

Check `~/.config/gyeol/brand.md`. If it exists, read `references/brand-profile.md` before applying it.

Key priority order: explicit prompt > document judgment > source material > brand profile frontmatter > brand profile notes > built-in defaults. The profile fills gaps silently. It never overrides the current request.

## Workflow

1. Identify the output language: Korean, English, or both.
2. Pick a verified template:
   - `one-pager` or `one-pager-ko` for concise briefs.
   - `long-doc` or `long-doc-ko` for reports and proposals.
   - `letter` or `letter-ko` for formal correspondence.
   - `portfolio` or `portfolio-ko` for project collections.
   - `resume` or `resume-ko` for career profiles.
   - `slides` or `slides-ko` for presentation decks.
   - `equity-report` or `equity-report-ko` for public-market research.
   - `changelog` or `changelog-ko` for release notes.
   - `landing-page` or `landing-page-ko` for screen-first product pages.
3. Read `CHEATSHEET.md` when you need a compact template selection or verification reminder.
4. Read `references/writing.md` for language-specific style rules before drafting.
5. Fill placeholders in the chosen template.
6. Run `python scripts/build.py --check`.
7. If PDF rendering is required, install render dependencies and run the relevant render verification before delivery.

## Design Rules

- Treat Korean and English as sibling native outputs, not translations.
- Use sans-first enterprise typography and restrained color.
- Keep public-site tone closer to Cohere-style enterprise clarity.
- Keep document templates denser and more printable than marketing pages.
- Keep Kami attribution visible in public docs and reference files.

## Theme Selection

Use `light` for print, memo, report, send-as-PDF, and formal investment documents. Consider `dark` for premium, board, keynote, launch, executive preview, and strategy deck requests. Document templates should emit one fixed theme per artifact. Landing pages may include a browser toggle.

## Hero Sample Context

For investment/strategy demos or examples, use `references/hero-haneul-npu.json`. Keep Haneul NPU Systems marked as fictional sample data.

## Verification Boundary

The registry in `scripts/shared.py` is the source of truth for verified templates. Do not claim a template exists unless it is registered and `python scripts/build.py --check` passes.
