# Visual Output Contract

Card metadata kinds:

- `build_report`
- `weapon_top5_card`
- `echo_showcase_card`
- `material_plan_card`
- `team_card`
- `party_list_card`
- `mechanics_card`

Each visual artifact should record:

```json
{"kind":"build_report", "path":"generated/report.png", "metadata_path":"generated/report.json", "sources":[...]}
```

If Pillow/Playwright is unavailable, scripts may create SVG/HTML fallback artifacts and clearly report the fallback.

## Required Local Assets

- Query final named resonators with `--kind resonator`.
- Query final named weapons with `--kind weapon`.
- Query active Echo picks with `--kind echo`.
- Query Sonata set picks with `--kind sonata`.
- Query ascension, weapon, Forte/skill, EXP, and boss materials with `--kind material`.

Use `--thumb-size 48 --format table` for grouped rich-text recommendations, `--format markdown` for individual previews, and concrete `image_path` values for card metadata. Do not use broad image search or fan art.

## Rich-text Fallback

If the user did not ask for image report mode, do not render PNG cards. Use compact Markdown image-card tables with cached thumbnails:

```markdown
**추천 편성**
| 메인딜 | 서브/배터리 | 힐러 |
|---|---|---|
| ![메인딜](path) | ![서브](path) | ![힐러](path) |
| **메인딜** | **서브** | **힐러** |
| 딜 담당 | 협주/버프 | 회복 |

**에코 / 소나타**
| 액티브 에코 | 소나타 | 세팅 방향 |
|---|---|---|
| ![에코](path) | ![소나타](path) | 4-3-3-1-1 |
| **액티브 에코** | **소나타명** | **주옵/부옵** |
| 운용 핵심 | 세트 목적 | 스탯 기준 |

**파밍 재료**
| 캐릭터 | 무기/스킬 | 경험치 |
|---|---|---|
| ![재료](path) | ![재료](path) | ![재료](path) |
| **재료명** | **재료명** | **재료명** |
| 지금 필요 | 필요할 때만 | 남는 재화로 |

**분석글**
- 공식: [제목](URL) - 확인한 내용
- 위키: [제목](URL) - 이미지/재료/스킬 확인
- 가이드: [제목](URL) - 세팅 판단
```

Keep citations and long explanations outside the tables. Do not use HTML `<br>` in table cells.
