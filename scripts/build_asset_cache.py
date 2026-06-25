#!/usr/bin/env python3
"""Enrich the Wuthering Waves local asset cache with wiki images.

The seed manifest deliberately works without network access by using local
placeholder tiles. This helper mirrors the Genshin consultant workflow: when
network access is available, fetch official/wiki page images for known
resonators, weapons, echoes, sonata sets, and materials, store them locally, and update
the manifest to prefer real images. It does not scrape fan art.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
from collections import Counter
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

from common import ASSET_MANIFEST, MIRROR_ASSET_MANIFEST, SKILL_DIR, load_asset_manifest, norm

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


API_URL = "https://wutheringwaves.fandom.com/api.php"
USER_AGENT = "Mozilla/5.0 (Codex wuthering-consultant asset cache builder)"
ASSET_ROOT = SKILL_DIR / "assets" / "wuthering-assets" / "current"
IMAGE_ROOT = ASSET_ROOT / "images"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
WEAPON_CATEGORIES = {
    "Sword": "Category:Swords",
    "Broadblade": "Category:Broadblades",
    "Pistols": "Category:Pistols",
    "Gauntlets": "Category:Gauntlets",
    "Rectifier": "Category:Rectifiers",
}
DISCOVERY_CATEGORIES = [
    ("resonator", "Category:Playable Resonators", None),
    *[("weapon", category, weapon_type) for weapon_type, category in WEAPON_CATEGORIES.items()],
    ("echo", "Category:Echoes", None),
    ("sonata", "Category:Sonatas", None),
    ("material", "Category:Development Materials", "development"),
    ("material", "Category:Material", "material"),
    ("material", "Category:Weapon and Skill Material", "weapon-skill"),
    ("material", "Category:Resonator EXP Material", "resonator-exp"),
    ("material", "Category:Weapon EXP Material", "weapon-exp"),
]
ATTRIBUTE_NAMES = ("Spectro", "Fusion", "Glacio", "Electro", "Aero", "Havoc")


def slugify(text: str) -> str:
    slug = re.sub(r"[^0-9a-z]+", "-", (text or "").casefold()).strip("-")
    return slug or "asset"


def wiki_page_url(title: str) -> str:
    return "https://wutheringwaves.fandom.com/wiki/" + quote(title.replace(" ", "_"), safe="_()'")


def api_get(params: dict[str, Any]) -> dict[str, Any]:
    query = dict(params)
    query.setdefault("format", "json")
    url = API_URL + "?" + urlencode(query)
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=45) as resp:  # noqa: S310 - public MediaWiki API
        return json.loads(resp.read().decode("utf-8"))


def category_members(category_title: str) -> list[str]:
    titles: list[str] = []
    params: dict[str, Any] = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category_title,
        "cmnamespace": 0,
        "cmlimit": "500",
    }
    while True:
        data = api_get(params)
        titles.extend(member["title"] for member in data.get("query", {}).get("categorymembers", []))
        cont = data.get("continue")
        if not cont:
            break
        params.update(cont)
    return titles


def page_data(titles: list[str], *, include_categories: bool = False) -> dict[str, dict[str, Any]]:
    pages: dict[str, dict[str, Any]] = {}
    for idx in range(0, len(titles), 40):
        batch = titles[idx : idx + 40]
        props = "pageimages|categories" if include_categories else "pageimages"
        data = api_get(
            {
                "action": "query",
                "titles": "|".join(batch),
                "prop": props,
                "piprop": "original|name",
                "cllimit": "500",
            }
        )
        for page in data.get("query", {}).get("pages", {}).values():
            title = page.get("title")
            if isinstance(title, str):
                pages[title] = page
    return pages


def page_images(titles: list[str]) -> dict[str, dict[str, Any]]:
    return page_data(titles, include_categories=False)


def file_imageinfo(file_titles: list[str]) -> dict[str, dict[str, Any]]:
    infos: dict[str, dict[str, Any]] = {}
    for idx in range(0, len(file_titles), 40):
        batch = file_titles[idx : idx + 40]
        data = api_get(
            {
                "action": "query",
                "titles": "|".join(batch),
                "prop": "imageinfo",
                "iiprop": "url|mime|size|sha1",
            }
        )
        for page in data.get("query", {}).get("pages", {}).values():
            title = page.get("title")
            imageinfo = page.get("imageinfo") or []
            if isinstance(title, str) and imageinfo:
                infos[title] = imageinfo[0]
    return infos


def choose_page_title(item: dict[str, Any]) -> str:
    for value in (item.get("wiki_title"), item.get("name")):
        if value:
            return str(value)
    return str(item.get("query") or "Asset")


def preferred_file_titles(item: dict[str, Any]) -> list[str]:
    name = str(item.get("name") or "").strip()
    if not name:
        return []
    kind = item.get("kind")
    if kind == "resonator":
        return [f"File:Resonator {name}.png", f"File:{name} Icon.png"]
    if kind == "weapon":
        return [f"File:Weapon {name}.png", f"File:{name} Icon.png"]
    if kind == "echo":
        plain_name = name.replace(":", "")
        titles = [f"File:Echo {name}.png", f"File:{name} Icon.png"]
        if plain_name != name:
            titles.extend([f"File:Echo {plain_name}.png", f"File:{plain_name} Icon.png"])
        return titles
    if kind == "sonata":
        return [f"File:Icon {name}.png", f"File:{name} Icon.png"]
    if kind == "material":
        return [f"File:Item {name}.png", f"File:{name} Icon.png"]
    return []


def preferred_file_title(item: dict[str, Any]) -> str | None:
    titles = preferred_file_titles(item)
    return titles[0] if titles else None


def clean_title(title: str, kind: str) -> str:
    if kind == "echo" and title.endswith("/Echo"):
        return title.removesuffix("/Echo")
    return title


def category_titles(page: dict[str, Any]) -> set[str]:
    return {str(item.get("title", "")).removeprefix("Category:") for item in page.get("categories") or []}


def resonator_attribute(categories: set[str]) -> str | None:
    for attribute in ATTRIBUTE_NAMES:
        if f"{attribute} Resonators" in categories:
            return attribute
    return None


def resonator_weapon(categories: set[str]) -> str | None:
    for weapon in WEAPON_CATEGORIES:
        if f"{weapon} Resonators" in categories:
            return weapon
    return None


def upsert_item(manifest: dict[str, Any], item: dict[str, Any]) -> bool:
    items = manifest.setdefault("items", [])
    key = (item.get("kind"), norm(str(item.get("name", ""))))
    for existing in items:
        existing_key = (existing.get("kind"), norm(str(existing.get("name", ""))))
        if existing_key != key:
            continue
        for field in ("wiki_title", "attribute", "weapon", "type"):
            if item.get(field) and not existing.get(field):
                existing[field] = item[field]
        aliases = list(dict.fromkeys([*(existing.get("aliases") or []), *(item.get("aliases") or [])]))
        if aliases:
            existing["aliases"] = aliases
        return False
    items.append(item)
    return True


def discover_manifest_items(manifest: dict[str, Any]) -> dict[str, int]:
    discovered = Counter()
    for kind, category, type_hint in DISCOVERY_CATEGORIES:
        titles = category_members(category)
        pages = page_data(titles, include_categories=True)
        for title in titles:
            page = pages.get(title, {})
            cats = category_titles(page)
            name = clean_title(title, kind)
            if kind == "resonator" and name == "Resonator":
                continue
            item: dict[str, Any] = {
                "kind": kind,
                "name": name,
                "ko": name,
                "aliases": list(dict.fromkeys([title, name])),
                "wiki_title": title,
                "image_path": None,
                "source_url": wiki_page_url(title),
                "source_type": "wiki-discovered",
            }
            if kind == "weapon":
                item["type"] = type_hint
            if kind == "resonator":
                attr = resonator_attribute(cats)
                weapon = resonator_weapon(cats)
                if attr:
                    item["attribute"] = attr
                if weapon:
                    item["weapon"] = weapon
            if upsert_item(manifest, item):
                discovered[kind] += 1
    return dict(discovered)


def extension_for_url(url: str, content_type: str | None = None) -> str:
    if content_type:
        guessed = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if guessed and guessed.lower() in IMAGE_EXTENSIONS:
            return guessed.lower()
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return suffix
    return ".png"


def download_image(url: str, out_base: Path) -> Path:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=60) as resp:  # noqa: S310 - public wiki image URL
        content_type = resp.headers.get("Content-Type")
        raw = resp.read()
    out_path = out_base.with_suffix(".png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image

        with Image.open(BytesIO(raw)) as image:
            image.convert("RGBA").save(out_path, format="PNG")
        return out_path
    except Exception:
        ext = extension_for_url(url, content_type)
        out_path = out_base.with_suffix(ext)
        with out_path.open("wb") as f:
            f.write(raw)
    return out_path


def enrich_manifest(manifest: dict[str, Any], *, names: set[str] | None, download: bool) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    items = manifest.get("items", [])
    selected = []
    for item in items:
        title = choose_page_title(item)
        searchable = {str(item.get("name", "")), str(item.get("ko", "")), title}
        searchable.update(str(alias) for alias in item.get("aliases") or [])
        if names and not {value.casefold() for value in searchable} & names:
            continue
        selected.append(item)

    pages = page_images([choose_page_title(item) for item in selected]) if selected else {}
    preferred_titles = []
    for item in selected:
        preferred_titles.extend(preferred_file_titles(item))
    preferred_images = file_imageinfo(preferred_titles) if preferred_titles else {}
    results: list[dict[str, Any]] = []

    for item in selected:
        title = choose_page_title(item)
        page = pages.get(title, {})
        preferred_info = {}
        for preferred_title in preferred_file_titles(item):
            preferred_info = preferred_images.get(preferred_title, {})
            if preferred_info:
                break
        original = page.get("original") or {}
        asset_url = preferred_info.get("url") or original.get("source")
        status = "missing-image"
        local_path = None
        error = None

        if asset_url:
            status = "found"
            if download:
                try:
                    out_base = IMAGE_ROOT / str(item.get("kind") or "asset") / slugify(title) / "icon"
                    downloaded = download_image(asset_url, out_base)
                    local_path = downloaded.relative_to(SKILL_DIR).as_posix()
                    item["image_path"] = local_path
                    item["asset_url"] = asset_url
                    item["source_url"] = wiki_page_url(title)
                    item["source_type"] = "wiki-image"
                    status = "downloaded"
                except Exception as exc:  # noqa: BLE001
                    error = str(exc)
                    status = "download-failed"

        result = {
            "name": item.get("name"),
            "kind": item.get("kind"),
            "wiki_title": title,
            "source_url": wiki_page_url(title),
            "asset_url": asset_url,
            "image_path": local_path,
            "status": status,
        }
        if error:
            result["error"] = error
        results.append(result)

    if download:
        ASSET_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        MIRROR_ASSET_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MIRROR_ASSET_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return manifest, results


def main() -> int:
    ap = argparse.ArgumentParser(description="Summarize or enrich the Wuthering Waves asset cache.")
    ap.add_argument("names", nargs="*", help="Optional asset names to enrich; omit to process the whole manifest.")
    ap.add_argument("--download", action="store_true", help="Download wiki images and update both manifest copies.")
    ap.add_argument("--discover", action="store_true", help="Discover all wiki resonators, weapons, echoes, and sonatas before enrichment.")
    ap.add_argument("--summary-only", action="store_true", help="Only print manifest kind counts.")
    ap.add_argument("--json", action="store_true", help="Print JSON output.")
    args = ap.parse_args()

    manifest = load_asset_manifest()
    discovered = discover_manifest_items(manifest) if args.discover else {}
    counts = Counter(item.get("kind", "unknown") for item in manifest.get("items", []))
    if args.summary_only:
        out = {
            "ok": True,
            "summary": dict(counts),
            "discovered": discovered,
            "items": len(manifest.get("items", [])),
            "note": "Use --discover --download to enrich wiki-discovered entries with images; placeholders remain as fallback.",
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    names = {name.casefold() for name in args.names} if args.names else None
    _, results = enrich_manifest(manifest, names=names, download=args.download)
    ok = all(result["status"] in {"found", "downloaded", "missing-image"} for result in results)
    out = {
        "ok": ok,
        "download": args.download,
        "discover": args.discover,
        "discovered": discovered,
        "summary": dict(counts),
        "processed": len(results),
        "results": results,
    }
    print(json.dumps(out if args.json or args.download or args.names else manifest, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
