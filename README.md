# Gyeol / 결

## 한국어

**Gyeol은 에이전트가 한국어와 영어 비즈니스 문서를 바로 만들 수 있게 해주는 문서 스킬, 템플릿, 검증 저장소입니다.**

SaaS가 아니라 Codex, Claude Code, Claude Desktop, 그리고 `~/.agents/` 또는 로컬 스킬 폴더를 읽는 도구에 붙여 쓰는 문서 시스템입니다. 한국어는 영어 번역문이 아니라 처음부터 한국어 문서로 쓰고, 영어도 별도 네이티브 출력으로 다룹니다.

Gyeol은 [Kami](https://github.com/tw93/Kami)의 저장소 구조, 템플릿 중심 사고, 검증 루프에서 영향을 받았습니다. 포크는 아니며 한국어/영어 문장 규칙, 산세리프 중심 기업 문서 톤, 로컬 Cohere 디자인 분석을 기준으로 새로 작성했습니다.

### 바로 설치

`npx`는 편의 경로입니다. 직접 clone해서 스킬 폴더에 넣어도 됩니다.

**Codex, OpenCode, Pi 등 generic agents**

```bash
npx skills add JangHyun-bin/GyeoL -a '*' -g -y
```

**Claude Code**

```bash
npx skills add JangHyun-bin/GyeoL -a claude-code -g -y
```

**직접 clone해서 확인**

```bash
git clone https://github.com/JangHyun-bin/GyeoL.git
cd GyeoL
python scripts/package_skill.py
python scripts/tests/test_build.py
python scripts/build.py --check
```

**Claude Desktop**

`dist/gyeol.zip`을 Claude Desktop의 Customize > Skills > "+" > Create skill에서 업로드합니다. ZIP은 `python scripts/package_skill.py`로 다시 만들 수 있습니다.

자세한 설치와 문제 해결은 [docs/onboarding.md](docs/onboarding.md)를 보세요.

### 바로 호출

스킬이 설치되면 자연어로 요청하면 됩니다.

```text
Use Gyeol to make a Korean one-pager for this product brief.
Use Gyeol to turn this research into an English long document.
Use Gyeol to build a bilingual strategy deck.
Gyeol로 투자자용 한국어 원페이저를 만들어줘.
Gyeol로 이 리서치를 영어 장문 보고서로 정리해줘.
```

### 검증된 템플릿

현재 9개 유형을 한국어/영어로 검증합니다.

- `one-pager` / `one-pager-ko`
- `long-doc` / `long-doc-ko`
- `letter` / `letter-ko`
- `portfolio` / `portfolio-ko`
- `resume` / `resume-ko`
- `slides` / `slides-ko`
- `equity-report` / `equity-report-ko`
- `changelog` / `changelog-ko`
- `landing-page` / `landing-page-ko`

공개 미리보기는 영어 `index.html`, 한국어 `ko.html`입니다. 샘플 산출물은 `assets/demos/demo-*.html`에 있고, 렌더 QA 기록은 `docs/design-qa/2026-05-22-render-qa.md`에 있습니다.

### 검증 명령

```bash
python scripts/tests/test_build.py
python scripts/build.py --check
python scripts/package_skill.py
```

PDF 렌더링은 의도적으로 별도 경계입니다. PDF를 최종 산출물로 낼 때는 WeasyPrint와 PyPDF를 설치한 뒤 렌더 검증을 추가로 돌립니다.

### 출처

Gyeol은 Kami의 문서 스킬 구조와 검증 관점에서 영향을 받았기 때문에 명시적으로 출처를 남깁니다. 자세한 내용은 `CREDITS.md`, `NOTICE`, `references/kami.md`를 보세요.

## English

**Gyeol is a document skill, template, and verification repository for agents that need native Korean and English business deliverables.**

It is not a SaaS product. It is designed to be installed into Codex, Claude Code, Claude Desktop, and other tools that can read a skill from `~/.agents/` or a local checkout. Korean is treated as a native document language, not as an English translation. English outputs are native siblings.

Gyeol is structurally informed by [Kami](https://github.com/tw93/Kami): the repository shape, template-first workflow, and verification loop. It is not a fork. The writing rules, visual system, and Korean/English template stack are rewritten for Gyeol.

### Quick Start

`npx` is a convenience path, not a requirement. You can also clone the repository directly into a skill directory.

**Codex, OpenCode, Pi, and generic agents**

```bash
npx skills add JangHyun-bin/GyeoL -a '*' -g -y
```

**Claude Code**

```bash
npx skills add JangHyun-bin/GyeoL -a claude-code -g -y
```

**Local checkout**

```bash
git clone https://github.com/JangHyun-bin/GyeoL.git
cd GyeoL
python scripts/package_skill.py
python scripts/tests/test_build.py
python scripts/build.py --check
```

**Claude Desktop**

Upload `dist/gyeol.zip` through Customize > Skills > "+" > Create skill. Rebuild the ZIP with `python scripts/package_skill.py`.

See [docs/onboarding.md](docs/onboarding.md) for detailed setup, verification, and troubleshooting.

### Use

After installation, ask naturally:

```text
Use Gyeol to make a Korean one-pager for this product brief.
Use Gyeol to turn this research into an English long document.
Use Gyeol to build a bilingual strategy deck.
Gyeol로 투자자용 한국어 원페이저를 만들어줘.
Gyeol로 이 리서치를 영어 장문 보고서로 정리해줘.
```

### Verified Templates

Gyeol currently verifies the full 9-type Korean/English stack:

- `one-pager` / `one-pager-ko`
- `long-doc` / `long-doc-ko`
- `letter` / `letter-ko`
- `portfolio` / `portfolio-ko`
- `resume` / `resume-ko`
- `slides` / `slides-ko`
- `equity-report` / `equity-report-ko`
- `changelog` / `changelog-ko`
- `landing-page` / `landing-page-ko`

Public preview pages are `index.html` for English and `ko.html` for Korean. Demo outputs live in `assets/demos/demo-*.html`, and render QA notes live in `docs/design-qa/2026-05-22-render-qa.md`.

### Verify

```bash
python scripts/tests/test_build.py
python scripts/build.py --check
python scripts/package_skill.py
```

Render verification is intentionally separate. Install WeasyPrint and PyPDF before treating PDF output as fully verified.

### Attribution

Gyeol keeps strong attribution to Kami because its repository shape and verification mindset are informed by Kami. See `CREDITS.md`, `NOTICE`, and `references/kami.md`.
