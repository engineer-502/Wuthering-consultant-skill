# Wuthering Consultant

Codex에서 사용하는 **명조: 워더링 웨이브 / Wuthering Waves 상담 보조 스킬**입니다. 공명자, 무기, 에코, 소나타, 파티 조합, 로테이션, 뽑기 판단, 계정 성장 우선순위에 대해 한국어 중심의 상담을 제공합니다.

> Fan-made / Unofficial project.
> This repository is not affiliated with, endorsed by, sponsored by, or approved by Kuro Games or any related right holder.

## 주요 기능

- 공명자 빌드, 무기, 에코, 소나타 세트, 파티 조합 진단
- 초보자/복귀자 기준 성장 우선순위와 재화 투자 방향 제안
- 스크린샷 기반 계정/캐릭터 상태 추출 보조
- 메타 민감 정보, 배너, 신규 캐릭터, 무기 추천 등은 웹 출처 확인 후 답변하도록 설계
- 로컬 이미지 캐시를 사용해 공명자, 무기, 에코, 소나타, 재료 아이콘을 Markdown 상담에 첨부
- 요청 시 시각 자료/카드/HTML 리포트 생성용 스크립트 제공

## 저장소 구조

```text
wuthering-consultant/
  SKILL.md                 # Codex가 읽는 메인 스킬 지침
  agents/                  # 보조 에이전트 프롬프트
  references/              # 상담 기준, 추출 스키마, 출력 규칙
  scripts/                 # 에셋 조회, 검증, 카드/리포트 렌더링 도구
  data/                    # 공식 seed, fixture, 에셋 메타데이터
  assets/wuthering-assets/ # 공명자/무기/에코/소나타/재료 이미지 캐시
  examples/                # 샘플 상담 JSON 및 렌더링 예시
  generated/               # 로컬 생성 결과용 폴더, Git에는 결과물 제외
```

## 설치

Codex skills 폴더에 이 저장소를 clone합니다.

### Windows PowerShell

```powershell
git clone https://github.com/engineer-502/Wuthering-consultant-skill.git "$env:USERPROFILE\.codex\skills\wuthering-consultant"
```

### macOS / Linux

```bash
git clone https://github.com/engineer-502/Wuthering-consultant-skill.git ~/.codex/skills/wuthering-consultant
```

이미 Codex를 켜둔 상태였다면 설치 후 Codex를 재시작하거나 스킬 목록을 다시 로드하세요.

## 기본 사용법

Codex 대화에서 스킬 이름을 직접 호출합니다.

```text
$wuthering-consultant 양양 추천 파티랑 무기, 에코 알려줘
```

스크린샷을 함께 제공하면 공명자 상세, 무기, 에코, 스킬, 돌파, 로스터, 인벤토리, 탑/엔드 콘텐츠 상태를 참고해 상담합니다.

예시:

```text
$wuthering-consultant 막 시작한 뉴비인데 개척자, 양양, 설지, 루시가 있어. 파티를 어떻게 짜고 뭐부터 키워야 해?
```

```text
$wuthering-consultant 루시 전용 무기까지 뽑았어. 무기, 에코, 소나타, 추천 파티랑 육성 순서 알려줘.
```

```text
$wuthering-consultant 이 캐릭터 스크린샷 보고 빌드 문제점이랑 목표 스탯을 한국어로 정리해줘.
```

## 동작 방식

1. `SKILL.md`가 요청을 일반 텍스트 상담 또는 리포트 모드로 분류합니다.
2. 스크린샷이 있으면 읽을 수 있는 값만 구조화하고, 불확실한 값은 확인 필요로 남깁니다.
3. `references/`의 상담 기준과 출력 규칙을 적용합니다.
4. 최신 메타, 배너, 신규 공명자, 무기 순위, 버전 의존 정보는 웹 출처 확인을 우선합니다.
5. 최종 추천에 등장하는 공명자, 무기, 에코, 소나타, 재료는 가능한 경우 로컬 이미지 캐시에서 아이콘을 찾아 Markdown에 첨부합니다.
6. 사용자가 이미지 리포트나 카드 생성을 명시적으로 요청하면 `scripts/`의 렌더링 도구를 사용합니다.

## 이미지 및 에셋 캐시

이 저장소에는 상담 표시를 위한 로컬 이미지 캐시가 포함되어 있습니다.

- 공명자 아이콘
- 무기 아이콘
- 에코 아이콘
- 소나타 세트 아이콘
- 육성/돌파/스킬 재료 아이콘
- Markdown 표에 쓰이는 작은 PNG 썸네일

에셋 조회 예시:

```powershell
python scripts\query_asset_cache.py "Lucy" --kind resonator --format markdown --thumb-size 48
python scripts\query_asset_cache.py "Freeze Frame" --kind weapon --format paths
```

## 검증

스킬 폴더에서 아래 명령을 실행할 수 있습니다.

### Windows PowerShell

```powershell
python scripts\validate_seed.py data\seed\wuwa_official_3_4_seed.json
python scripts\run_smoke_tests.py
```

### macOS / Linux

```bash
python scripts/validate_seed.py data/seed/wuwa_official_3_4_seed.json
python scripts/run_smoke_tests.py
```

## 의존성

기본 상담과 에셋 조회는 Python 표준 라이브러리 중심으로 동작하도록 구성되어 있습니다. 일부 이미지 카드/HTML 리포트 렌더링 기능은 환경에 따라 추가 패키지가 필요할 수 있습니다.

```powershell
python -m pip install pillow
python -m pip install playwright
python -m playwright install chromium
```

`Pillow`는 이미지 카드 렌더링에, `Playwright`는 HTML 리포트 캡처에 필요할 수 있습니다.

## 공개 배포 및 개인정보 원칙

이 저장소는 공개 설치를 전제로 합니다. 다음 항목은 저장소에 포함하지 않는 것을 원칙으로 합니다.

- 개인 계정 스크린샷 또는 플레이 기록 원본
- 로컬 사용자 경로, 개인 PC 경로, 작업 로그
- API key, access token, cookie, secret, credential
- Codex 내부 실행 폴더, 임시 산출물, 캐시성 bytecode
- 사용자가 명시적으로 배포 권한을 갖지 않은 제3자 자료

`.gitignore`는 생성 결과와 로컬 캐시가 실수로 포함되지 않도록 구성되어 있습니다.

## Legal Notice and Liability Disclaimer (Fan-made / Unofficial)

이 문서는 프로젝트의 공개 배포 목적 고지이며, 법률 자문이 아닙니다. 실제 법적 판단이나 분쟁 대응은 관할 법령과 전문가 검토를 따르세요.

### AI 판단 및 사용 책임 면책

이 프로젝트와 `wuthering-consultant` 스킬이 제공하는 빌드 진단, 무기/에코/소나타/파티 추천, 로테이션, 뽑기 조언, 리소스 투자 판단, 이미지 분석 결과, 웹 출처 요약 등은 AI가 생성하거나 보조한 참고 정보입니다.

사용자는 해당 정보를 최종 판단의 참고 자료로만 사용해야 하며, 실제 게임 플레이, 과금, 계정 운용, 콘텐츠 재배포, 제3자 자료 사용, 플랫폼 정책 준수 여부에 관한 결정은 전적으로 사용자 본인의 책임입니다.

본 프로젝트의 관리자 및 기여자는 AI 분석 결과의 정확성, 최신성, 완전성, 특정 목적 적합성, 게임 내 성능 향상, 계정 안전성, 외부 플랫폼 정책 준수 여부를 보증하지 않습니다. AI 판단을 신뢰하거나 적용하여 발생하는 손해, 손실, 계정 제재, 정책 위반, 권리 침해, 데이터 손상, 기회비용, 기타 직간접 결과에 대한 귀책사유는 법령상 허용되는 최대 범위에서 사용자 또는 해당 행위자 본인에게 있습니다.

### 팬메이드 비공식 프로젝트 고지

이 프로젝트는 팬메이드 비공식 Codex 스킬 및 Wuthering Waves / 명조 상담 보조 도구입니다.

`Wuthering Waves`, `명조: 워더링 웨이브`, `Kuro Games`, `KURO GAMES` 및 관련 명칭, 로고, 캐릭터, 공명자, 무기, 에코, 게임 이미지, 게임 데이터, 기타 콘텐츠의 권리는 각 권리자에게 있습니다.

이 저장소는 공식 제품이 아니며, Kuro Games, KURO GAMES 또는 그 관계사, 퍼블리셔, 라이선서, 권리자와 제휴, 승인, 후원, 보증 관계가 없습니다.

본 프로젝트는 비상업적 목적의 팬 활동과 개인 학습/도구화 목적을 전제로 하며, 사용자는 본 프로젝트와 포함 리소스를 상업적 목적으로 사용해서는 안 됩니다. 별도 권리를 보유한 사용자가 자신의 책임하에 이용하는 경우에도, 해당 사용자는 관련 약관, 라이선스, 플랫폼 정책, 관할 법령을 직접 확인해야 합니다.

본 프로젝트에 포함되거나 참조된 제3자 코드, 이미지, 데이터, 리소스, 문서, API, 라이브러리는 각 원저작자 및 해당 라이선스 조건을 따릅니다.

권리자 또는 대리인의 삭제, 수정, 비공개 요청이 접수될 경우, 관리자는 해당 콘텐츠를 지체 없이 제거하거나 비공개 처리할 수 있습니다. GitHub DMCA 또는 기타 권리침해 신고가 접수될 경우, 해당 플랫폼 정책과 관련 법령에 따라 즉각적인 조치를 취합니다.

사용자는 본 프로젝트 사용으로 발생할 수 있는 플랫폼 정책 위반, 저작권/상표권/초상권/기타 권리 침해 위험을 스스로 확인하고 책임져야 합니다.

### 면책 및 책임 범위

본 저장소는 "있는 그대로(AS IS)" 제공되며, 특정 목적 적합성, 정확성, 완전성, 지속적 동작, 무중단 제공, 오류 없음, 최신 게임 버전과의 호환성을 보증하지 않습니다.

사용자가 본 저장소를 다운로드, 설치, 실행, 수정, 재배포, 포크, 인용하거나 포함 리소스를 사용하는 과정에서 발생한 모든 결과(정책 위반, 권리 침해, 계정 제재, 데이터 손실, 금전적 손해, 법적 분쟁 포함)는 해당 사용자 또는 행위자 본인의 책임입니다.

저장소 관리자 및 기여자는 법령상 허용되는 최대 범위에서, 본 프로젝트 사용 또는 사용 불가로 인해 발생한 직간접적, 우발적, 특별, 결과적 손해에 대해 책임을 지지 않습니다.

제3자가 본 저장소를 재게시, 재배포, 수정 배포하거나 추가한 내용에 대한 법적 책임은 해당 게시자 또는 행위자에게 있으며, 원 저장소 관리자에게 자동 승계되지 않습니다.

### 권리자 문의 / 삭제 요청

권리자 또는 대리인은 아래 연락처로 삭제, 수정, 비공개 또는 권리 관련 요청을 보낼 수 있습니다.

Contact: axwhalesolution@gmail.com

권리자의 정당한 요청이 확인될 경우 즉각적인 조치(삭제/수정/비공개)를 진행합니다.
