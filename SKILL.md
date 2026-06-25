---
name: wuthering-consultant
description: Analyze Wuthering Waves / 명조 account and resonator screenshots for Korean account consulting. Use when the user provides resonator detail, weapon, echo, skill, sequence, roster, inventory, convene history, Tower/Endstate, or resource screenshots, or asks for current web-cited target stats, Energy Regen/CRIT/element damage thresholds, weapon rankings, echo/sonata alternatives, Concerto/Intro/Outro/Forte/Tune Break rotation coaching, material plans, recommended teams, pull advice, or optional local PNG visual cards.
---

# Wuthering Consultant

## Fast vs Report Mode

Default mode is **rich text consulting**. For ordinary questions about builds, weapons, echoes, sonata effects, teams, pull value, target stats, rotations, or account progression, do this order:

1. Read the user request and current ownership/state.
2. Inspect every supplied screenshot or local image path. Do not invent unreadable values; mark them `확인 필요`.
3. Browse current sources when a claim is meta-sensitive, version-sensitive, banner-sensitive, or character-specific.
4. Produce Korean consulting with conclusion, assumptions/uncertainty, target stats, bottlenecks, echo/weapon/team/rotation guidance, pull/resource opportunity cost, and citations.
5. Use local inline asset previews when `scripts/query_asset_cache.py` finds a matching resonator, weapon, echo, sonata, or material placeholder/cache item. Cap visible inline assets to about 10-12 items.
6. If the user did not explicitly ask for an image report, end with a short optional offer such as `이미지 리포트도 만들어드릴까요?`.

Do **not** scan asset folders, build visual metadata, or render report PNGs in default rich text mode. Use `scripts/query_asset_cache.py` after the final recommendation list is known.

Lightweight inline asset previews are required in rich text mode whenever the answer names specific resonators, weapons, echoes, sonata sets, or farming materials and the local cache has a matching entry. This is a fixed output requirement, not optional decoration. After the text recommendation is finalized, run `scripts/query_asset_cache.py` with `--thumb-size 48` for the mentioned main resonators, final party members, top weapon recommendations, top echo recommendations, top sonata recommendations, and key material recommendations that will appear in the answer. The script returns square PNG thumbnails when possible, including generated local placeholder tiles for cache entries without real art. Use those returned paths in Markdown image tags.

Image/report mode is opt-in. Trigger only when the user explicitly asks for `리포트`, `report`, `이미지 리포트`, `카드`, `시각자료`, `PNG`, `한 장으로`, `그림으로`, `이미지로`, or `렌더링`. Ordinary words such as `추천`, `파티`, `에코`, `무기`, `종결`, `준종결`, and `스펙` are rich text mode unless a report trigger is present.

When report mode is triggered, first finish the text recommendation, then query local asset cache only for items in the final recommendation, localize card metadata to Korean, render card artifacts, and compose a page if multiple cards exist.

## Core Rules

- Prefer Korean output unless the user asks otherwise.
- Do not invent unreadable screenshot values. Use confidence labels: `confirmed`, `inferred`, `needs_confirmation`.
- Do not give uncited current-build advice. If a claim depends on current meta, current banners, new resonators, weapon rankings, endgame rotations, or version mechanics, browse first and cite.
- Use official Kuro notices/patch notes for factual release/banner details first; use wiki/reference databases for mechanics; use guide/meta sources for practical builds; label guide claims as meta opinions.
- Do not use leaks as authoritative. If the user asks about leaks, clearly separate rumor from confirmed data.
- Do not push spending. Pull advice must include opportunity cost, free/low-cost alternatives, existing roster constraints, pity/currency state, and uncertainty.
- Do not persist user account screenshots as long-term assets unless the user explicitly asks.
- Treat player UX failures as first-class: missing Energy Regen, wrong Concerto handoff, unbuilt support, bad Echo main stat, wrong Sonata set, untriggered Outro buff, Forte mismanagement, or missed Tune Break can matter more than raw CRIT.
- Keep tables compact. For grouped recommendations, prefer Codex-friendly image-card Markdown tables: role/header row, image row, bold name row, and one short caption row. Put longer explanations below the table with labels such as `핵심:`, `조건:`, `교체:`.
- In text consultations, attach cached square previews to the relevant recommendation text: resonator icons in party rows, weapon icons beside weapon names, echo icons beside active echo picks, and sonata icons beside set recommendations. If cached images exist but the final answer has no Markdown image tags for those named items, treat it as a formatting failure and fix it before responding.
- The Codex desktop renders Markdown image tags reliably, but not HTML image tags. Do not use HTML `<img>`, HTML `<br>`, relative paths, `~`, environment variables, or raw Windows backslash paths in visible image URLs. Use the concrete forward-slash absolute paths returned by `scripts/query_asset_cache.py`, or use `--format markdown`.

### Current Output Rules Override

These rules override any older garbled examples in this file.

- Prefer structured vertical sections: `결론`, `확인된 정보`, `추천 편성`, `무기`, `에코 / 소나타`, `파밍 재료`, `오늘 할 것`, `분석글`.
- In `추천 편성`, `무기`, `에코 / 소나타`, and `파밍 재료`, use image-card Markdown tables whenever two or more visual items are grouped or compared. Keep each table to 3-4 columns; split wider comparisons.
- For long team/weapon/echo/material explanations, put prose under the table with labels such as `핵심:`, `조건:`, `교체:`, `로테이션:`, `주옵:`, `부옵:`, `파밍:`.
- In text consultations, attach cached square previews to the relevant recommendation text: resonator icons in party rows, weapon icons beside weapon names, echo icons beside active echo picks, sonata icons beside set recommendations, and material icons beside farm items.
- If cached images exist but the final answer has no Markdown image tags for those named resonator/weapon/echo/sonata/material items, treat it as a formatting failure and fix it before responding.
- Do not end Korean answers with a terse `근거:` label. Use a vertical `분석글` section with source type, link, and what was checked.

## Workflow

### 1. Display and inspect screenshots

Use all provided images. If paths are local/Windows-style, translate to an accessible path when possible and inspect them. If an image is missing or blurry, ask for the specific missing screen instead of guessing.

Load `references/extraction-schema.md` when extracting. Produce a structured working object with:

- resonator identity, level, ascension, rarity, attribute, weapon type, sequence chain
- weapon name, level, rank/tuning, main/sub stat if visible
- skill/forte levels and unlocked inherent skills
- final stats: HP, ATK, DEF, CRIT Rate, CRIT DMG, Energy Regen, attribute damage bonus, healing bonus if visible
- echoes: cost pattern, active echo, sonata set, slot/cost, level, main stat, substats, tune status, confidence per echo
- account state: roster, weapons, echo inventory, waveplates/materials, Union Level, Data Bank level, Tower/Endstate progress if supplied
- missing fields and screenshot-quality notes
- `input_images[]` and `visual_artifacts[]` entries for any generated reports

### 2. Run Wuthering Waves consulting

Load `references/resonator-benchmarks.md` and `references/advanced-consulting.md`. Diagnose in this order:

1. Mechanics/rotation correctness: Concerto generation, Intro/Outro handoff, Forte loop, Resonance Skill/Liberation timing, Echo active use, swap-cancel safety, Tune Break use when relevant.
2. Energy/cycle minimum: Energy Regen needs by role and rotation length.
3. Character/weapon/skill investment: resonator level, weapon level, skill priorities, sequence value.
4. Echo main stats and cost: common 4-3-3-1-1 DPS pattern, support/healer variants, active echo fit.
5. Sonata set and substats: set fit, CRIT/ATK/ER/attribute bonus balance, role-specific stats.
6. Team fit: buffs, Outro targets, damage window alignment, sustain, grouping, shield/heal, endgame chamber needs.
7. Account progression: farming route, waveplate efficiency, pull/resource opportunity cost.

### 3. Search current sources

Load `references/source-policy.md` before browsing. For each current consultation, capture source type, URL, visible publication/update date, target game version if visible, and supported claim.

Normal character/build consultations should use a 5-source pack when available: official notice/profile, wiki/reference mechanics, at least two current practical guides/community build references, and one cross-check source. Precision ranking/report-mode advice should use 8+ sources when available.

### 4. Use local assets only after recommendations are finalized

For rich text inline previews, use `scripts/query_asset_cache.py` directly after the final recommendation list is known. Query each asset kind separately so the correct cache type is used. Always request `--thumb-size 48` for Codex-thread previews.

```bash
python wuthering-consultant/scripts/query_asset_cache.py Sanhua Mortefi Baizhi --kind resonator --variant icon --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py "Variation" "Commando of Conviction" --kind weapon --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py "Impermanence Heron" "Bell-Borne Geochelone" --kind echo --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py "Moonlit Clouds" "Rejuvenating Glow" --kind sonata --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py "Cadence Blossom" "Adagio Helix" "Advanced Resonance Potion" --kind material --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py Lucy Rebecca Baizhi --kind resonator --thumb-size 48 --format markdown
python wuthering-consultant/scripts/query_asset_cache.py Lucy Yangyang Baizhi --kind resonator --thumb-size 48 --format table --headers "메인딜|서브/배터리|힐러" --captions "딜 담당|몹몰이/에너지|회복"
```

Use concrete forward-slash filesystem paths returned by the script in Markdown image tags. Do not use HTML `<img>` or `<br>` tags.

Preferred compact rendering patterns:

```markdown
**추천 파티**
| 메인딜 | 서브/버퍼 | 힐러 |
|---|---|---|
| ![산화](/absolute/path/to/sanhua.png) | ![모르테피](/absolute/path/to/mortefi.png) | ![백지](/absolute/path/to/baizhi.png) |
| **산화** | **모르테피** | **백지** |
| 메인 딜링 | 협주/버프 | 회복/안정 |

핵심: 산화는 짧게 들어와 협주를 채우고, 백지는 힐과 버프를 담당합니다.

**무기**
| 1순위 | 2순위 | 임시 |
|---|---|---|
| ![무기 A](/absolute/path/to/weapon-a.png) | ![무기 B](/absolute/path/to/weapon-b.png) | ![무기 C](/absolute/path/to/weapon-c.png) |
| **무기 A** | **무기 B** | **무기 C** |
| 최고점 | 4성 추천 | 초반 대체 |

설명: 보유 무기와 역할에 따라 선택합니다.

**에코·소나타**
| 액티브 에코 | 소나타 | 세팅 방향 |
|---|---|---|
| ![반디의 군세](/absolute/path/to/impermanence-heron.png) | ![떠오르는 구름](/absolute/path/to/moonlit-clouds.png) | 4-3-3-1-1 |
| **반디의 군세** | **떠오르는 구름** | **서브/버퍼** |
| Outro 보조 | 다음 딜러 강화 | 공효/치명 균형 |
```


## Mode-Specific Mini-Playbooks

### Build consultation
- Confirm resonator, weapon, skill/Forte levels, Echo cost pattern, Sonata set, and ER/CRIT/attribute stats.
- Diagnose mechanics first: Concerto handoff, Outro target, Forte loop, active Echo timing, Liberation cycle.
- For current characters or rankings, browse before ranking weapons/echoes/teams.

### Pull consultation
- Require or state assumptions for pity, guarantee, Astrite/Tide count, current roster, spending boundary, and desired endgame target.
- Always include `추천도`, `조건`, `보류 이유`, `저비용 대체`, and `기회비용`.
- Do not frame paid pulls as mandatory.

### Account progression
- Prioritize Union Level/Sol3, Data Bank, main team investment, weapon levels, and two-team endgame coverage.
- Output `오늘/이번 주`, `이번 버전`, and `보류해도 되는 것` sections.

### Screenshot extraction
- Only visible values can be `confirmed`.
- Blurry, cropped, or language-ambiguous values must be `needs_confirmation`.
- Ask for the exact missing screen rather than guessing.

### Report mode
- Trigger only on explicit report/image/card/render language.
- Keep citations in text, not inside the card footer.
- Use local placeholders when official/wiki-safe images are unavailable.

## Source Pack Examples

Normal build consultation source pack:
1. Official notice/profile for identity, attribute, weapon, and role tags.
2. Wiki/reference page for skill text, Echo/Sonata mechanics, and materials.
3. Current guide source 1 for stat/weapon/echo priorities.
4. Current guide source 2 or community calculation for cross-check.
5. User screenshot/account state as the account-specific source of truth.

Precision ranking/report source pack should expand to 8+ sources when available.

## Currentness Warning

Bundled seed data is only a starting point. If the user asks for `최신`, `현재`, `메타`, `이번 버전`, banner status, or exact character rankings, browse current sources and cite them before answering.

## Output Shape

Use concise Korean sections:

1. `결론`
2. `확인한 정보 / 불확실한 정보`
3. `현재 병목`
4. `목표 스탯 / 에코 기준`
5. `무기 우선순위`
6. `에코·소나타 세팅`
7. `파티·로테이션`
8. `파밍/재화 우선순위`
9. `뽑기/과금 판단` when relevant
10. `출처` with citations

## Current Output Shape

Use concise Korean sections. Prefer visual image-card tables for recommendation blocks and vertical prose labels for explanations:

1. `결론`
2. `확인된 정보 / 확인 필요`
3. `추천 편성`
4. `무기`
5. `에코 / 소나타`
6. `파밍 재료`
7. `오늘 할 것`
8. `뽑기 / 과금 판단` when relevant
9. `분석글`

For party, weapon, Echo/Sonata, and material sections, use small image-card tables with images inside cells when assets are available. Put long explanations under the table with labels such as `핵심:`, `교체:`, `로테이션:`, `주옵:`, `부옵:`, `파밍:`. Do not use a final `근거:` line.

## Seed Context

This skill ships with a small official Version 3.4 seed under `data/seed/wuwa_official_3_4_seed.json`. It includes Lucy, Rebecca, Lucilla, Cartethyia Phase II, collab weapons, Freeze Frame, Shadow of Shattered Dreams, and official Convene rules. Treat it as seed context, not a substitute for browsing when the user asks for current/latest advice.
