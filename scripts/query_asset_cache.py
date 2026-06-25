#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

from common import SKILL_DIR, find_assets


ASSET_ROOT = SKILL_DIR / "assets" / "wuthering-assets" / "current"

PALETTES = {
    "Spectro": ("#f8d66d", "#4f3f12"),
    "Fusion": ("#ff7a59", "#4a1512"),
    "Glacio": ("#7fd7ff", "#143449"),
    "Electro": ("#b794ff", "#28184f"),
    "Aero": ("#74e0a7", "#123a2b"),
    "Havoc": ("#d26bff", "#3c164f"),
    "resonator": ("#7dd3fc", "#0f172a"),
    "weapon": ("#fbbf24", "#1f2937"),
    "echo": ("#a78bfa", "#111827"),
    "sonata": ("#34d399", "#0f172a"),
    "material": ("#60a5fa", "#111827"),
}

KIND_LABELS = {
    "resonator": "RES",
    "weapon": "WPN",
    "echo": "ECHO",
    "sonata": "SET",
    "material": "MAT",
}


def slugify(text: str) -> str:
    slug = re.sub(r"[^0-9a-z]+", "-", (text or "").casefold()).strip("-")
    if slug:
        return slug[:80]
    digest = hashlib.sha1((text or "asset").encode("utf-8")).hexdigest()[:10]
    return f"asset-{digest}"


def asset_label(item: dict) -> str:
    return str(item.get("ko") or item.get("name") or item.get("query") or "Asset")


def codex_image_path(path: str | Path | None) -> str | None:
    if not path:
        return None
    try:
        return Path(path).resolve().as_posix()
    except Exception:
        return str(path).replace("\\", "/")


def markdown_alt(text: str) -> str:
    return text.replace("[", "(").replace("]", ")").replace("\n", " ").strip() or "asset"


def markdown_table_cell(text: str) -> str:
    return (text or "").replace("|", "/").replace("\n", " ").strip()


def ascii_label(item: dict) -> str:
    return str(item.get("name") or item.get("query") or item.get("ko") or "Asset")


def palette_for(item: dict) -> tuple[str, str]:
    return PALETTES.get(str(item.get("attribute")), PALETTES.get(str(item.get("kind")), PALETTES["resonator"]))


def load_font(size: int, bold: bool = False):
    from PIL import ImageFont

    candidates = [
        "C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def text_size(draw, text: str, font) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def fit_font(draw, text: str, max_width: int, start: int, minimum: int, bold: bool = False):
    size = start
    while size >= minimum:
        font = load_font(size, bold=bold)
        width, _ = text_size(draw, text, font)
        if width <= max_width:
            return font
        size -= 1
    return load_font(minimum, bold=bold)


def write_generated_tile(item: dict, out_path: Path, size: int) -> None:
    from PIL import Image, ImageDraw

    scale = 4
    canvas_size = max(size, 32) * scale
    primary, secondary = palette_for(item)
    image = Image.new("RGBA", (canvas_size, canvas_size), secondary)
    draw = ImageDraw.Draw(image)

    radius = max(8, canvas_size // 7)
    draw.rounded_rectangle((0, 0, canvas_size - 1, canvas_size - 1), radius=radius, fill=secondary)
    draw.rounded_rectangle(
        (scale * 3, scale * 3, canvas_size - scale * 3, canvas_size - scale * 3),
        radius=max(6, canvas_size // 8),
        outline=primary,
        width=max(2, scale * 2),
    )
    draw.ellipse(
        (canvas_size * 0.24, canvas_size * 0.18, canvas_size * 0.76, canvas_size * 0.70),
        fill=primary,
        outline=(255, 255, 255, 120),
        width=max(2, scale),
    )

    kind = KIND_LABELS.get(str(item.get("kind")), "WUWA")
    kind_font = load_font(max(7 * scale, 8), bold=True)
    draw.text((canvas_size // 2, canvas_size * 0.16), kind, anchor="mm", font=kind_font, fill=(255, 255, 255, 220))

    name = ascii_label(item)
    words = re.findall(r"[A-Za-z0-9]+", name)
    initials = "".join(word[0] for word in words[:2]).upper() or name[:2].upper()
    initials_font = fit_font(draw, initials, int(canvas_size * 0.48), 21 * scale, 10 * scale, bold=True)
    draw.text((canvas_size // 2, canvas_size * 0.45), initials, anchor="mm", font=initials_font, fill=(255, 255, 255, 245))

    detail = " / ".join(str(item.get(key)) for key in ("attribute", "weapon", "type") if item.get(key))
    if not detail:
        detail = asset_label(item)
    detail_font = fit_font(draw, detail, int(canvas_size * 0.82), 9 * scale, 5 * scale)
    draw.text((canvas_size // 2, canvas_size * 0.80), detail, anchor="mm", font=detail_font, fill=(255, 255, 255, 225))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    image.save(out_path)


def make_raster_thumbnail(src: Path, out_path: Path, size: int) -> bool:
    try:
        from PIL import Image, ImageOps
    except Exception as exc:
        print(f"WARN: Pillow unavailable for thumbnails: {exc}", file=sys.stderr)
        return False

    try:
        with Image.open(src) as image:
            image = image.convert("RGBA")
            bbox = image.getbbox()
            if bbox:
                image = image.crop(bbox)
            centering = (0.5, 0.62) if image.height > image.width * 1.25 else (0.5, 0.5)
            canvas = ImageOps.fit(image, (size, size), method=Image.Resampling.LANCZOS, centering=centering)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            canvas.save(out_path)
        return True
    except Exception as exc:
        print(f"WARN: thumbnail failed for {src}: {exc}", file=sys.stderr)
        return False


def preview_path(item: dict, size: int | None) -> str | None:
    raw_path = item.get("image_path")
    src = Path(raw_path) if raw_path else None
    needs_generated = not src or not src.is_file()
    if not size and not needs_generated:
        return str(src)

    preview_size = size or 64
    stem = slugify(str(item.get("name") or item.get("query") or "asset"))
    out_path = ASSET_ROOT / "thumbnails" / str(preview_size) / str(item.get("kind") or "asset") / f"{stem}.png"

    if not size and out_path.exists() and (needs_generated or (src and out_path.stat().st_mtime >= src.stat().st_mtime)):
        return str(out_path.resolve())

    if src and src.is_file() and src.suffix.lower() not in {".svg", ".svgz"}:
        if make_raster_thumbnail(src, out_path, preview_size):
            return str(out_path.resolve())

    try:
        write_generated_tile(item, out_path, preview_size)
        return str(out_path.resolve())
    except Exception as exc:
        print(f"WARN: generated preview failed for {item.get('name')}: {exc}", file=sys.stderr)
        return str(src) if src and src.exists() else None


def apply_previews(items: list[dict], thumb_size: int | None) -> list[dict]:
    out = []
    for item in items:
        copied = dict(item)
        path = preview_path(copied, thumb_size)
        if path:
            copied["image_path"] = path
            if thumb_size or path.endswith(".png"):
                copied["thumb_path"] = path
        out.append(copied)
    return out


def apply_render_root(items: list[dict], render_root: str | None) -> list[dict]:
    if not render_root:
        return items
    root = Path(render_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    out = []
    for item in items:
        copied = dict(item)
        src = Path(item.get("image_path") or "")
        if src.exists():
            dest = root / str(item.get("kind", "asset")) / src.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            copied["image_path"] = str(dest.resolve())
            copied["render_root"] = str(root)
        out.append(copied)
    return out


def split_table_values(raw: str | None, expected: int) -> list[str]:
    if not raw:
        return []
    separator = "|" if "|" in raw else ","
    values = [part.strip() for part in raw.split(separator)]
    return values[:expected]


def pad_values(values: list[str], expected: int, fallback_prefix: str) -> list[str]:
    padded = list(values)
    while len(padded) < expected:
        padded.append(f"{fallback_prefix} {len(padded) + 1}")
    return padded[:expected]


def render_markdown_table(items: list[dict], headers_raw: str | None, captions_raw: str | None) -> str:
    if not items:
        return ""

    count = len(items)
    headers = pad_values(split_table_values(headers_raw, count), count, "추천")
    captions = pad_values(split_table_values(captions_raw, count), count, "") if captions_raw else []

    rows = [
        "| " + " | ".join(markdown_table_cell(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        "| " + " | ".join(markdown_table_cell(item.get("markdown_image") or "") for item in items) + " |",
        "| " + " | ".join(f"**{markdown_table_cell(asset_label(item))}**" for item in items) + " |",
    ]
    if captions:
        rows.append("| " + " | ".join(markdown_table_cell(caption) for caption in captions) + " |")
    return "\n".join(rows)


def main() -> int:
    p = argparse.ArgumentParser(description="Query Wuthering Waves local seed/asset cache.")
    p.add_argument("names", nargs="+", help="Resonator, weapon, echo, sonata, or material names to find")
    p.add_argument("--kind", choices=["resonator", "weapon", "echo", "sonata", "material", "any"], default="any")
    p.add_argument("--variant", default="icon", help="Accepted for compatibility; icon previews are square PNGs when --thumb-size is used.")
    p.add_argument("--limit", type=int, default=1)
    p.add_argument("--thumb-size", type=int, default=None, help="Create square thumbnail PNGs and return those paths.")
    p.add_argument("--render-root", default=os.environ.get("WUTHERING_CODEX_RENDER_ROOT"), help="Copy returned preview files into a privacy-safe render root.")
    p.add_argument("--format", choices=["json", "paths", "markdown", "table", "manifest-items"], default="paths")
    p.add_argument("--headers", default=None, help="For --format table, pipe- or comma-separated column headers.")
    p.add_argument("--captions", default=None, help="For --format table, pipe- or comma-separated short caption row.")
    args = p.parse_args()

    kind = None if args.kind == "any" else args.kind
    results = find_assets(args.names, kind=kind, limit=args.limit)
    results = apply_previews(results, args.thumb_size)
    results = apply_render_root(results, args.render_root)
    matched_queries = {item.get("query") for item in results}
    missing_queries = [name for name in args.names if name not in matched_queries]

    for item in results:
        image_path = item.get("image_path")
        if image_path:
            item["codex_image_path"] = codex_image_path(image_path)
            item["markdown_image"] = f"![{markdown_alt(asset_label(item))}]({item['codex_image_path']})"

    if args.format == "json":
        print(json.dumps({"ok": bool(results), "count": len(results), "items": results, "missing_queries": missing_queries}, ensure_ascii=False, indent=2))
    elif args.format == "manifest-items":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        for item in results:
            if item.get("markdown_image"):
                print(item["markdown_image"])
    elif args.format == "table":
        rendered = render_markdown_table(results, args.headers, args.captions)
        if rendered:
            print(rendered)
    else:
        for item in results:
            if item.get("codex_image_path"):
                print(item["codex_image_path"])
        if not results:
            print(f"No cache match for: {', '.join(args.names)}")
    return 0 if results else 2


if __name__ == "__main__":
    raise SystemExit(main())
