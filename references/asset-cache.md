# Asset Cache Policy

Seed cache path: `assets/wuthering-assets/current/`.

- `data/seed/asset_manifest.json` is the script-friendly manifest.
- `assets/wuthering-assets/current/manifest.json` mirrors it for portable cache browsing.
- First pass uses local generated placeholders plus official source URLs; exhaustive image download is not required.
- If fetching images later, prefer official Kuro article images when the exact asset exists there, then reputable wiki/reference game icons. Avoid fanart and unsourced search results.
- Rich-text mode uses `scripts/query_asset_cache.py`; report mode may call `fetch_card_assets.py` only after final recommendations are known.

## Inline Codex Previews

Use `scripts/query_asset_cache.py` with `--thumb-size 48` for rich-text answers. The helper returns concrete absolute paths with forward slashes (`C:/...`) suitable for Codex Markdown image tags. Use `--format table` when you want a ready-to-paste image-card table, or `--format markdown` when you want individual image tags.

```bash
python wuthering-consultant/scripts/query_asset_cache.py Sanhua Mortefi Baizhi --kind resonator --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py Variation "Commando of Conviction" --kind weapon --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py "Impermanence Heron" --kind echo --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py "Moonlit Clouds" --kind sonata --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py "Cadence Blossom" "Adagio Helix" --kind material --thumb-size 48 --format paths
python wuthering-consultant/scripts/query_asset_cache.py Lucy Rebecca Baizhi --kind resonator --thumb-size 48 --format markdown
python wuthering-consultant/scripts/query_asset_cache.py Lucy Yangyang Baizhi --kind resonator --thumb-size 48 --format table --headers "메인딜|서브/배터리|힐러" --captions "딜 담당|몹몰이/에너지|회복"
```

The manifest may contain entries without a real `image_path`. For those, the query helper generates a deterministic square PNG tile under `assets/wuthering-assets/current/thumbnails/<size>/...`. This keeps Codex answers visually scannable while still making real-art gaps explicit through `source_type: generated-placeholder`.

Do not manually browse asset folders for ordinary rich-text answers. Query only the final named recommendations, cap visible previews to about 10-12 items, and skip true cache misses.

For `--format table`, keep headers and captions short. The output uses a header row, image row, bold name row, and optional caption row so Codex renders character, weapon, Echo, Sonata, and material recommendations as a visual block instead of a detached image gallery.

## Real Wiki Image Enrichment

When the user asks to improve the skill's visual cache, or when report mode needs real portraits/icons instead of generated tiles, use `scripts/build_asset_cache.py`. It queries the Wuthering Waves Fandom MediaWiki API for page images, downloads known manifest entries, and updates both manifest copies.

To mirror the Genshin asset-cache structure broadly, use `--discover` so the helper reads wiki categories for playable resonators, weapon types, echoes, sonatas, and common development/material items before downloading images.

Dry-run a few assets first:

```bash
python wuthering-consultant/scripts/build_asset_cache.py Sanhua Variation "Impermanence Heron" --json
```

Download and update the cache only after the dry-run looks right:

```bash
python wuthering-consultant/scripts/build_asset_cache.py Sanhua Variation "Impermanence Heron" --download --json
```

Full category refresh:

```bash
python wuthering-consultant/scripts/build_asset_cache.py --discover --download --json
```

Material refresh examples:

```bash
python wuthering-consultant/scripts/build_asset_cache.py "Cadence Blossom" "Adagio Helix" "Advanced Resonance Potion" --download --json
python wuthering-consultant/scripts/query_asset_cache.py "Cadence Blossom" "Adagio Helix" "Advanced Resonance Potion" --kind material --thumb-size 48 --format markdown
```

Placeholders remain the fallback when a wiki page has no suitable page image or network access is unavailable. Do not bulk scrape fan art or unsourced image search results. In final answers, say `분석글` for the source list rather than a terse `근거:` label.
