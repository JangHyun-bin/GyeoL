# Production Notes

## Verification

Run:

```bash
python scripts/tests/test_build.py
python scripts/build.py --check
```

These checks confirm registry shape, required files, JSON references, public pages, placeholders, and attribution.

## Render Verification

PDF rendering needs extra dependencies. Before claiming PDF output is final, install WeasyPrint and PyPDF, then add a render-specific verification command.

## Template Rules

- Templates stay self-contained.
- Registered templates must contain `lang`.
- Registered templates must expose `{{placeholder}}` fields.
- Planned templates stay out of the registry until implemented.
