# Source Policy - Wuthering Waves / 명조

Use this reference before web research. Current character build advice, weapon ranking, Echo/Sonata choice, material routing, banner value, and endgame team advice are time-sensitive, so browse for character-specific claims.

## Source Tiers

### Tier A - facts and mechanics

Use for confirmed release details, kit text, material data, Echo/Sonata mechanics, item names, and image provenance.

- Official Kuro / Wuthering Waves notices, patch notes, convene notices, event pages, launcher/news JSON, official socials
- In-game screenshots supplied by the user
- Wuthering Waves Fandom / wiki-style structured pages for item, Echo, Sonata, weapon, and material data
- Prydwen character pages when they expose mechanics, priorities, and assumptions clearly

### Tier B - practical build guidance

Use for Korean-friendly explanation, rotations, weapon comparisons, Echo/Sonata priorities, target stats, and team fit.

- WutheringLab
- Prydwen build sections and team sections
- Maygi / calculation posts or community theorycrafting with visible assumptions
- Korean YouTube, Naver, Tistory, DC/Arca guide posts when date/version/context is visible
- Game8, Beebom, Icy Veins, or similar guide databases as cross-checks, not as the sole source

### Tier C - weak signals

Use only as supporting color. Never make a firm recommendation from Tier C alone.

- Tier lists without visible assumptions
- Reddit/Discord summaries without calculations
- Short social posts, comments, or unsourced rankings

## Minimum Source Packs

Normal build consultation: use 5 sources when available.

1. Official source for identity, release, attribute, weapon type, or event rule.
2. Wiki/reference page for skill text, Echo/Sonata, or material data.
3. Current practical guide source 1.
4. Current practical guide or calculation source 2.
5. Team/rotation or ownership-context source.

Precision consultation: use 8+ sources when available. Trigger this for weapon rankings, team rankings, Echo/Sonata comparisons, target stat thresholds, exact material/farming plans, or visual-card/image-source-backed answers.

Recommended mix:

1. Official patch/profile/banner source.
2. Wiki/reference mechanics source.
3. Wiki/reference material or image source.
4. Prydwen or equivalent build source.
5. WutheringLab or equivalent build source.
6. Korean practical guide or video/blog.
7. Calculation/community source with assumptions.
8. Cross-check guide database or chamber/team usage source.

If fewer credible sources exist, say `확인 가능한 최신 분석글이 부족함` and narrow the advice.

## Search Breadth

Search Korean and English. Try official first, then wiki, then practical/meta sources.

### Build, stats, and rotations

- `명조 {character} 공략 무기 에코 조합 최신`
- `명조 {character} 치확 치피 에너지 공명효율 스펙`
- `Wuthering Waves {character} guide weapons echoes teams rotation`
- `Wuthering Waves {character} build Prydwen WutheringLab`
- `Wuthering Waves {character} calculations rotation team`

### Echo, Sonata, and farming

- `명조 {character} 에코 세트 소나타 파밍`
- `Wuthering Waves {character} best Echo Sonata stats`
- `site:wutheringwaves.fandom.com {character} materials`
- `site:wutheringwaves.fandom.com {echo} Echo`
- `site:wutheringwaves.fandom.com {sonata} Sonata`

### Weapon rankings

- `명조 {character} 무기 순위 전무 대체`
- `Wuthering Waves {character} weapon ranking signature alternative`
- `Wuthering Waves {weapon} best users`

### Materials

- `명조 {character} 돌파 재료 스킬 재료`
- `Wuthering Waves {character} ascension materials skill materials`
- `site:wutheringwaves.fandom.com {character} Ascension Materials`

### Korean practical sources

- `명조 {character} 유튜브 공략 최신`
- `명조 {character} 블로그 공략 최신`
- `명조 {character} 아카라이브 공략`
- `명조 {character} DC 공략`

### Image sources

- `site:wutheringwaves.kurogames.com {character} official`
- `site:wutheringwaves.fandom.com {character} icon`
- `site:wutheringwaves.fandom.com {weapon} icon`
- `site:wutheringwaves.fandom.com {echo} icon`
- `site:wutheringwaves.fandom.com {material} icon`

## Image Source Policy

Use the local cache first. If missing, prefer:

1. Official Kuro article/profile/event image for the exact asset when available.
2. Wuthering Waves Fandom game icon or page image for the exact asset.
3. User-provided in-game screenshot.
4. Placeholder tile only after official/wiki-safe discovery fails.

Do not broad-scrape fan art, generic image search, Pinterest, wallpaper sites, or unsourced reposts. Do not claim licensing is guaranteed; record source URL and direct asset URL in the manifest when possible.

## Output Source Label

Do not end Korean answers with a terse `근거:` line. Use a short vertical section named `분석글`:

```markdown
**분석글**
- 공식: [제목](URL) - 확인한 내용
- 위키: [제목](URL) - 스킬/재료/이미지 확인
- 가이드: [제목](URL) - 무기/에코/파티 판단
- 교차확인: [제목](URL) - 다른 관점이나 조건
```

Keep citations out of tables. Put them after the relevant section or in the final `분석글` list.

## Reject or Downgrade

Reject or downgrade claims when:

- the only support is a leak or rumor;
- a screenshot value is unreadable;
- a ranking lacks date/version/context;
- a pull recommendation omits opportunity cost;
- a guide conflicts with official mechanics and no explanation is available;
- the image source is not official/wiki/user-provided.
