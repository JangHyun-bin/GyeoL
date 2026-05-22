# Gyeol Onboarding

## 한국어

이 문서는 Gyeol을 Codex, Claude Code, Claude Desktop, 또는 로컬 스킬을 읽는 다른 에이전트에서 바로 쓰기 위한 설치와 검증 절차입니다.

문서 경로는 `docs/onboarding.md`입니다.

### 준비물

- Git
- Python 3.11 이상
- Node.js와 `npx`는 선택 사항입니다. `npx skills add`를 쓰지 않을 경우 직접 clone하면 됩니다.

### Codex와 generic agents

Codex, OpenCode, Pi처럼 `~/.agents/` 또는 호환 스킬 디렉터리를 읽는 도구는 generic agent 경로로 설치합니다.

```bash
npx skills add JangHyun-bin/GyeoL -a '*' -g -y
```

설치 후 다음처럼 요청합니다.

```text
Use Gyeol to make a Korean one-pager for this product brief.
Gyeol로 한국어 투자자용 원페이저를 만들어줘.
```

### Claude Code

Claude Code만 대상으로 설치할 때는 다음 명령을 씁니다.

```bash
npx skills add JangHyun-bin/GyeoL -a claude-code -g -y
```

설치 후 자연어 요청에서 `Gyeol` 또는 `$gyeol`을 언급하면 `SKILL.md`가 진입점이 됩니다.

### 직접 clone

`npx`가 없거나 저장소를 직접 검토하고 싶으면 clone해서 검증합니다.

```bash
git clone https://github.com/JangHyun-bin/GyeoL.git
cd GyeoL
python scripts/package_skill.py
python scripts/tests/test_build.py
python scripts/build.py --check
```

PowerShell에서 Codex 로컬 스킬 폴더에 직접 넣는 예시는 다음과 같습니다.

```powershell
git clone https://github.com/JangHyun-bin/GyeoL.git "$env:USERPROFILE\.codex\skills\gyeol"
```

Bash 계열 셸에서는 다음처럼 둘 수 있습니다.

```bash
git clone https://github.com/JangHyun-bin/GyeoL.git "${CODEX_HOME:-$HOME/.codex}/skills/gyeol"
```

### Claude Desktop

Claude Desktop은 ZIP 업로드 경로가 가장 단순합니다.

1. 저장소에서 `dist/gyeol.zip`을 준비합니다.
2. 없거나 최신화가 필요하면 `python scripts/package_skill.py`를 실행합니다.
3. Claude Desktop에서 Customize > Skills > "+" > Create skill로 이동합니다.
4. `dist/gyeol.zip`을 업로드합니다.

### 설치 확인

로컬 저장소에서는 다음 세 가지를 통과해야 합니다.

```bash
python scripts/package_skill.py
python scripts/tests/test_build.py
python scripts/build.py --check
```

성공하면 스킬 진입점, 템플릿 레지스트리, 공개 페이지, 레퍼런스 JSON, 온보딩 문서, Claude/Codex 배포 메타데이터가 모두 확인된 상태입니다.

### 첫 문서 만들기

자료를 붙여 넣고 다음처럼 요청합니다.

```text
Use Gyeol to turn this Korean product brief into a one-pager.
Use Gyeol to make an English long document from these notes.
Use Gyeol to build a bilingual strategy deck.
```

Gyeol은 `SKILL.md`에서 언어와 문서 유형을 고르고, `references/writing.md`와 `references/design.md`를 참고한 뒤 `assets/templates/`의 검증된 템플릿을 채웁니다.

### 문제 해결

- `npx`가 없으면 직접 clone 경로를 쓰세요.
- 스킬이 자동으로 안 잡히면 요청에 `Use Gyeol` 또는 `$gyeol`을 명시하세요.
- `python scripts/build.py --check`가 실패하면 누락 파일, 템플릿 등록, JSON 레퍼런스, 출처 표기를 먼저 확인하세요.
- PDF 렌더링은 별도 경계입니다. PDF까지 최종 검증하려면 WeasyPrint와 PyPDF를 설치한 뒤 렌더 테스트를 추가로 돌리세요.

## English

This guide explains how to use Gyeol from Codex, Claude Code, Claude Desktop, or another agent that can read local skills.

This file lives at `docs/onboarding.md`.

### Prerequisites

- Git
- Python 3.11 or newer
- Node.js and `npx` are optional. If you do not want to use `npx skills add`, clone the repository directly.

### Codex and Generic Agents

For Codex, OpenCode, Pi, and tools that read from `~/.agents/` or a compatible skills directory, use the generic agent install path.

```bash
npx skills add JangHyun-bin/GyeoL -a '*' -g -y
```

Then ask naturally:

```text
Use Gyeol to make a Korean one-pager for this product brief.
Gyeol로 한국어 투자자용 원페이저를 만들어줘.
```

### Claude Code

For Claude Code-specific installation:

```bash
npx skills add JangHyun-bin/GyeoL -a claude-code -g -y
```

After installation, mention `Gyeol` or `$gyeol` in a request. The agent should load `SKILL.md` as the entry point.

### Direct Clone

If `npx` is unavailable or you want to inspect the repository first, clone and verify it locally.

```bash
git clone https://github.com/JangHyun-bin/GyeoL.git
cd GyeoL
python scripts/package_skill.py
python scripts/tests/test_build.py
python scripts/build.py --check
```

PowerShell example for a local Codex skills folder:

```powershell
git clone https://github.com/JangHyun-bin/GyeoL.git "$env:USERPROFILE\.codex\skills\gyeol"
```

Bash example:

```bash
git clone https://github.com/JangHyun-bin/GyeoL.git "${CODEX_HOME:-$HOME/.codex}/skills/gyeol"
```

### Claude Desktop

Claude Desktop works best through ZIP upload.

1. Use `dist/gyeol.zip`.
2. Rebuild it with `python scripts/package_skill.py` when needed.
3. Open Customize > Skills > "+" > Create skill.
4. Upload `dist/gyeol.zip`.

### Verify Installation

In a local checkout, all three commands should pass:

```bash
python scripts/package_skill.py
python scripts/tests/test_build.py
python scripts/build.py --check
```

When they pass, the skill entry point, template registry, public pages, reference JSON files, onboarding docs, and Claude/Codex distribution metadata are present.

### Create a First Document

Paste source material and ask:

```text
Use Gyeol to turn this Korean product brief into a one-pager.
Use Gyeol to make an English long document from these notes.
Use Gyeol to build a bilingual strategy deck.
```

Gyeol chooses the language and document type from `SKILL.md`, reads the relevant writing and design references, then fills a verified template from `assets/templates/`.

### Troubleshooting

- If `npx` is unavailable, use the direct clone path.
- If the skill does not auto-trigger, mention `Use Gyeol` or `$gyeol` explicitly.
- If `python scripts/build.py --check` fails, check missing files, template registration, JSON references, and attribution text first.
- PDF rendering is separate. Install WeasyPrint and PyPDF before treating PDF output as fully verified.
