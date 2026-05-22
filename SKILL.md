---
name: gyeol
description: Create native Korean and English business documents using the Gyeol document stack. Use when asked to produce one-pagers, long documents, slide decks, or other professional deliverables that should read naturally in Korean and English, especially for agent-generated business reports, proposals, strategy notes, and presentations.
---

# Gyeol

Use Gyeol to produce professional Korean and English business documents from source material.

## Workflow

1. Identify the output language: Korean, English, or both.
2. Pick a verified Phase 1 template:
   - `one-pager` or `one-pager-ko` for concise briefs.
   - `long-doc` or `long-doc-ko` for reports and proposals.
   - `slides` or `slides-ko` for presentation decks.
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

## Planned Templates

Letter, portfolio, resume, equity report, changelog, and landing page are planned for Phase 2. Do not claim they are verified until they are added to `scripts/shared.py` and pass checks.
