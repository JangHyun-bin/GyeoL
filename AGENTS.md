# Gyeol Agent Guide

## Project

Gyeol is a Korean/English native document stack for agents. It includes a skill entry point, HTML templates, design and writing references, and small Python verification scripts.

## Working Rules

- Do not fork Kami inside this repo. Use Kami as a credited reference and rewrite Gyeol-specific content.
- Keep Korean and English outputs first-class. Avoid treating Korean as a translation of English.
- Only add templates to `scripts/shared.py` when they have real files and pass `python scripts/build.py --check`.
- Keep templates self-contained so they can be copied into agent outputs without a build system.
- Run `python scripts/tests/test_build.py` and `python scripts/build.py --check` before reporting completion.

## Current Scope

Verified Phase 1 templates are one-pager, long-doc, and slides in English and Korean. Other document types belong in `references/roadmap.md` until implemented.
