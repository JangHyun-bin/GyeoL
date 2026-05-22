---
name: gyeol
description: Create native Korean and English business documents using the Gyeol document stack. Use when asked to produce one-pagers, long documents, slide decks, or other professional deliverables that should read naturally in Korean and English, especially for agent-generated business reports, proposals, strategy notes, and presentations.
---

# Gyeol

Use Gyeol to produce professional Korean and English business documents from source material.

For installation, packaging, or cross-agent setup questions, read `docs/onboarding.md`.

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
3. Read `references/writing.md` for language-specific style rules before drafting.
4. Fill placeholders in the chosen template.
5. Run `python scripts/build.py --check`.
6. If PDF rendering is required, install render dependencies and run the relevant render verification before delivery.

## Design Rules

- Treat Korean and English as sibling native outputs, not translations.
- Use sans-first enterprise typography and restrained color.
- Keep public-site tone closer to Cohere-style enterprise clarity.
- Keep document templates denser and more printable than marketing pages.
- Keep Kami attribution visible in public docs and reference files.

## Verification Boundary

The registry in `scripts/shared.py` is the source of truth for verified templates. Do not claim a template exists unless it is registered and `python scripts/build.py --check` passes.
