#!/usr/bin/env python3
from __future__ import annotations
import argparse, html, json
from pathlib import Path

def render_svg(data: dict, out: Path) -> None:
    title = data.get('title') or data.get('kind') or 'Wuthering Consultant'
    subtitle = data.get('subtitle') or data.get('conclusion') or 'Functional seeded report'
    lines = data.get('lines') or data.get('recommendations') or []
    text_lines = []
    for item in lines[:6]:
        if isinstance(item, dict):
            text_lines.append(item.get('claim') or item.get('text') or str(item))
        else:
            text_lines.append(str(item))
    y = 150
    body_lines = []
    for line in text_lines:
        body_lines.append(f'<text x="64" y="{y}" font-size="24" fill="#dbeafe">• {html.escape(line[:72])}</text>')
        y += 38
    body = '\n'.join(body_lines)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720">
<defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#06111f"/><stop offset="1" stop-color="#164e63"/></linearGradient></defs>
<rect width="1200" height="720" rx="36" fill="url(#g)"/>
<text x="64" y="90" font-size="44" fill="#ffffff" font-weight="700" font-family="Arial">{html.escape(title)}</text>
<text x="64" y="126" font-size="24" fill="#67e8f9" font-family="Arial">{html.escape(subtitle[:90])}</text>
{body}
<text x="64" y="660" font-size="18" fill="#94a3b8">Generated fallback SVG · citations remain in text answer</text>
</svg>'''
    out.write_text(svg, encoding='utf-8')

def main() -> int:
    ap = argparse.ArgumentParser(description='Render a Wuthering Consultant visual card. SVG fallback is dependency-free.')
    ap.add_argument('card_json')
    ap.add_argument('--output', default=None)
    args = ap.parse_args()
    data = json.loads(Path(args.card_json).read_text(encoding='utf-8'))
    out = Path(args.output or data.get('output_path') or 'wuthering-consultant/generated/visual_card.svg')
    out.parent.mkdir(parents=True, exist_ok=True)
    render_svg(data, out)
    print(json.dumps({'ok': True, 'path': str(out), 'format': 'svg-fallback'}, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
