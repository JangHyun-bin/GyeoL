# Gyeol Phase 1 Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first working Gyeol repository: a Korean/English native document stack inspired by Kami's structure and verification workflow.

**Architecture:** Create a new `Gyeol` repo, not a fork. Keep Kami-style boundaries (`SKILL.md`, `references/`, `assets/templates/`, `scripts/`) but rewrite the implementation and public copy for Gyeol. Phase 1 ships working registry/check/test infrastructure and three complete template families: one-pager, long-doc, and slides, each in Korean and English.

**Tech Stack:** Static HTML/CSS, Python 3 standard library build/check scripts, optional WeasyPrint/PyPDF render verification later, plain Git repository.

---

### Task 1: Scaffold Contract Tests

**Files:**
- Create: `Gyeol/scripts/tests/test_build.py`
- Create: `Gyeol/scripts/shared.py`
- Create: `Gyeol/scripts/build.py`

- [ ] **Step 1: Write the failing scaffold tests**

Create tests that assert the agreed Phase 1 contract: six verified templates, two first-class site pages, planned later templates excluded from the registry, and credit/reference files present.

- [ ] **Step 2: Run tests to verify RED**

Run: `python scripts/tests/test_build.py`
Expected: FAIL because `scripts.shared` and project files do not exist yet.

- [ ] **Step 3: Implement minimal registry and build CLI**

Create `scripts/shared.py` with `HTML_TEMPLATES`, `SCREEN_PAGES`, `PLANNED_TEMPLATES`, and project path helpers. Create `scripts/build.py --check` to validate registry paths and required project files.

- [ ] **Step 4: Run tests and check to verify GREEN**

Run: `python scripts/tests/test_build.py`
Expected: PASS.

Run: `python scripts/build.py --check`
Expected: `OK:` lines for registry, pages, references, and templates.

### Task 2: Project Identity And Credits

**Files:**
- Create: `Gyeol/README.md`
- Create: `Gyeol/SKILL.md`
- Create: `Gyeol/AGENTS.md`
- Create: `Gyeol/LICENSE`
- Create: `Gyeol/CREDITS.md`
- Create: `Gyeol/NOTICE`
- Create: `Gyeol/references/kami.md`
- Create: `Gyeol/references/cohere.md`
- Create: `Gyeol/references/roadmap.md`

- [ ] **Step 1: Write identity and attribution docs**

Include the public Gyeol positioning, strong Kami reference, direct-copy-minimization policy, MIT license, and the Phase 1/Phase 2 roadmap.

- [ ] **Step 2: Run docs/credit checks**

Run: `python scripts/build.py --check`
Expected: PASS with required references found.

### Task 3: Design And Writing System

**Files:**
- Create: `Gyeol/references/design.md`
- Create: `Gyeol/references/writing.md`
- Create: `Gyeol/references/production.md`
- Create: `Gyeol/references/tokens.json`
- Create: `Gyeol/references/checks_thresholds.json`
- Create: `Gyeol/references/stabilizer_profiles.json`
- Create: `Gyeol/styles.css`

- [ ] **Step 1: Add Phase 1 design references**

Encode Cohere 70 / document-system 30 direction: white editorial canvas, deep enterprise band, action blue, sans-first enterprise documents, Korean/English native writing rules.

- [ ] **Step 2: Run token/reference checks**

Run: `python scripts/build.py --check`
Expected: PASS with valid JSON and CSS present.

### Task 4: Public Site

**Files:**
- Create: `Gyeol/index.html`
- Create: `Gyeol/ko.html`

- [ ] **Step 1: Build the English and Korean static pages**

`/` is English. `/ko.html` is Korean. Both present Gyeol as an open document stack for agents, link to the GitHub-ready repo sections, and expose Kami/Cohere references without making the page feel like a fork.

- [ ] **Step 2: Run page checks**

Run: `python scripts/build.py --check`
Expected: PASS with both pages found and cross-linked.

### Task 5: Phase 1 Templates

**Files:**
- Create: `Gyeol/assets/templates/one-pager.html`
- Create: `Gyeol/assets/templates/one-pager-ko.html`
- Create: `Gyeol/assets/templates/long-doc.html`
- Create: `Gyeol/assets/templates/long-doc-ko.html`
- Create: `Gyeol/assets/templates/slides.html`
- Create: `Gyeol/assets/templates/slides-ko.html`

- [ ] **Step 1: Add six self-contained HTML templates**

Each template includes inline CSS, stable page/screen dimensions, sample content, and language-native copy. Korean and English are siblings, not translations.

- [ ] **Step 2: Run template checks**

Run: `python scripts/build.py --check`
Expected: PASS with all six templates present and registered.

### Task 6: Repo Verification

**Files:**
- Modify: all created files as needed.

- [ ] **Step 1: Run full local verification**

Run: `python scripts/tests/test_build.py`
Expected: PASS.

Run: `python scripts/build.py --check`
Expected: PASS.

- [ ] **Step 2: Initialize git**

Run: `git init`, `git add .`, `git commit -m "feat: scaffold gyeol phase 1 foundation"` if verification passes.

- [ ] **Step 3: Report remaining Phase 2 work**

List the planned templates not yet in the verified registry: letter, portfolio, resume, equity-report, changelog, landing-page.
