# Output Template - Wuthering Waves / 명조

Use this shape for ordinary rich-text consulting. The default visual style is a compact Markdown "image-card table": images inside table cells, a bold name row, and one short caption row. Keep explanations outside the table so the answer remains readable in Codex.

```markdown
**결론**
한두 문장으로 지금 계정에서 할 일을 먼저 말한다.

**확인된 정보**
- 보유/무돌/무기/계정 상태:
- 확인 필요:

**추천 편성**
| 메인딜 | 서브/배터리 | 힐러/안정 |
|---|---|---|
| ![캐릭터 A](path) | ![캐릭터 B](path) | ![캐릭터 C](path) |
| **캐릭터 A** | **캐릭터 B** | **캐릭터 C** |
| 딜 담당 | 협주/버프/몹몰이 | 회복/보호 |

핵심: 왜 이 조합인지 1-2문장.
교체: 없을 때 대체 캐릭터.
로테이션: 짧게.

**무기**
| 1순위 | 2순위 | 임시 |
|---|---|---|
| ![무기 A](path) | ![무기 B](path) | ![무기 C](path) |
| **무기 A** | **무기 B** | **무기 C** |
| 최고점/보유 시 | 4성 추천 | 초반 임시 |

설명: 어떤 조건에서 어느 무기를 고르는지 짧게 정리.

**에코 / 소나타**
| 액티브 에코 | 소나타 | 세팅 방향 |
|---|---|---|
| ![에코](path) | ![소나타](path) | 4-3-3-1-1 |
| **에코명** | **소나타명** | **주옵/부옵 기준** |
| 운용 핵심 | 세트 목적 | 치명/피증/공효 우선순위 |

주옵: 4코스트 / 3코스트 / 1코스트.
부옵: 우선순위.
임시안: 데이터 뱅크 낮을 때 쓸 것.

**파밍 재료**
| 캐릭터 돌파 | 무기/스킬 | 경험치 |
|---|---|---|
| ![재료 A](path) | ![재료 B](path) | ![재료 C](path) |
| **재료 A** | **재료 B** | **재료 C** |
| 지금 필요 | 필요할 때만 | 남는 재화로 |

**오늘 할 것**
1. 캐릭터/무기 레벨
2. 스킬 우선순위
3. 에코는 몇 레벨까지만
4. 재료/웨이브플레이트 사용처

**분석글**
1. 공식: [제목](URL) - 확인한 내용
2. 위키: [제목](URL) - 스킬/에코/소나타/재료 확인
3. 가이드: [제목](URL) - 무기/에코/파티 판단
4. 교차확인: [제목](URL) - 조건 차이 확인
```

## Layout Rules

- Use image-card tables for `추천 편성`, `무기`, `에코 / 소나타`, and `파밍 재료` whenever at least two visual items are grouped or compared.
- A visual table should be no wider than 3-4 columns. Split into multiple small tables instead of making one wide table.
- Each visual table should use this row order: role/header row, image row, bold name row, short caption row.
- Keep long explanations outside the table under labels such as `핵심:`, `교체:`, `로테이션:`, `주옵:`, `부옵:`, `파밍:`.
- Do not put citations inside tables.
- Do not use `근거:` as the final label. Use `분석글`.
- Attach images to the relevant item, not as a detached gallery.
- Query each asset kind separately: resonator, weapon, echo, sonata, material.
- Use `--format table --thumb-size 48` for ready-to-paste Codex image-card tables, or `--format markdown --thumb-size 48` for individual icons.

## Helper Examples

```bash
python wuthering-consultant/scripts/query_asset_cache.py Lucy Yangyang Baizhi --kind resonator --thumb-size 48 --format table --headers "메인딜|서브/배터리|힐러" --captions "딜 담당|몹몰이/에너지|회복"
python wuthering-consultant/scripts/query_asset_cache.py "Emerald of Genesis" "Commando of Conviction" "Sword of Voyager" --kind weapon --thumb-size 48 --format table --headers "1순위|4성 추천|임시" --captions "있으면 사용|뉴비 추천|초반 대체"
python wuthering-consultant/scripts/query_asset_cache.py "Impermanence Heron" --kind echo --thumb-size 48 --format markdown
python wuthering-consultant/scripts/query_asset_cache.py "Moonlit Clouds" --kind sonata --thumb-size 48 --format markdown
```
