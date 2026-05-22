# Gyeol

**Give your agent a native Korean/English document system.**

Gyeol is an open document stack for agents that need to produce Korean and English business deliverables with the same level of care. It is not a SaaS product. It is a skill, template, and verification repository for documents that should read native in both languages.

Gyeol is structurally informed by [Kami](https://github.com/tw93/Kami): the idea of a document skill with templates, references, and verification scripts. Gyeol is not a fork. Code and templates are rewritten around Korean/English native writing, a sans-first enterprise visual system, and a stronger public-site influence from the local Cohere design analysis.

## Phase 1

Phase 1 ships a small verified core:

- `one-pager` and `one-pager-ko`
- `long-doc` and `long-doc-ko`
- `slides` and `slides-ko`
- English site at `/`
- Korean site at `/ko.html`
- fast structural checks through `python scripts/build.py --check`

The later Kami-scale set is planned in `references/roadmap.md`: letter, portfolio, resume, equity report, changelog, and landing page.

## Use

Ask an agent to use Gyeol when you need a polished Korean or English document:

```text
Use Gyeol to make a Korean one-pager for this product brief.
Use Gyeol to turn this research into an English long document.
Use Gyeol to build a bilingual strategy deck.
```

## Verify

```bash
python scripts/tests/test_build.py
python scripts/build.py --check
```

Render verification is intentionally separate. Add WeasyPrint and PyPDF before treating PDF output as fully verified.

## Attribution

Gyeol keeps strong attribution to Kami because its repository shape and verification mindset are informed by Kami. See `CREDITS.md`, `NOTICE`, and `references/kami.md`.
