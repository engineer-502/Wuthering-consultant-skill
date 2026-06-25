#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SEED_DIR = SKILL_DIR / "data" / "seed"
ASSET_MANIFEST = SEED_DIR / "asset_manifest.json"
MIRROR_ASSET_MANIFEST = SKILL_DIR / "assets" / "wuthering-assets" / "current" / "manifest.json"
OFFICIAL_SEED = SEED_DIR / "wuwa_official_3_4_seed.json"


def norm(text: str) -> str:
    folded = unicodedata.normalize("NFKC", text or "").casefold()
    return re.sub(r"[^0-9a-z\uac00-\ud7a3]+", "", folded)


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_asset_manifest() -> dict:
    path = ASSET_MANIFEST if ASSET_MANIFEST.exists() else MIRROR_ASSET_MANIFEST
    return load_json(path)


def load_official_seed() -> dict:
    return load_json(OFFICIAL_SEED)


def absolutize(path: str | None) -> str | None:
    if not path:
        return None
    p = Path(path)
    if p.is_absolute():
        return str(p)
    return str((SKILL_DIR / p).resolve())


def item_aliases(item: dict) -> list[str]:
    values = [
        item.get("name", ""),
        item.get("ko", ""),
        item.get("slug", ""),
        item.get("set_name", ""),
        item.get("attribute", ""),
        item.get("weapon", ""),
    ]
    values.extend(item.get("aliases") or [])
    return [str(value) for value in values if value]


def find_assets(names: list[str], kind: str | None = None, limit: int = 1) -> list[dict]:
    manifest = load_asset_manifest()
    items = manifest.get("items", [])
    results: list[dict] = []
    for name in names:
        q = norm(name)
        matches = []
        for item in items:
            if kind and item.get("kind") != kind:
                continue
            if any(q and (q == norm(a) or q in norm(a) or norm(a) in q) for a in item_aliases(item)):
                out = dict(item)
                out["query"] = name
                out["image_path"] = absolutize(out.get("image_path"))
                matches.append(out)
        results.extend(matches[:limit])
    return results
