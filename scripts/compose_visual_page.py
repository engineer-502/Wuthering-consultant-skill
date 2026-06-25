#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, html
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(description='Compose visual artifacts into a simple HTML index/page manifest.')
    ap.add_argument('page_json')
    ap.add_argument('--output', default='wuthering-consultant/generated/visual_page.html')
    args = ap.parse_args()
    data = json.loads(Path(args.page_json).read_text(encoding='utf-8'))
    cards = data.get('cards', [])
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    body = ''.join(f"<section><h2>{html.escape(c.get('title', c.get('path','Card')))}</h2><p>{html.escape(c.get('path',''))}</p></section>" for c in cards)
    out.write_text(f"<!doctype html><meta charset='utf-8'><title>WuWa Visual Page</title><body>{body}</body>", encoding='utf-8')
    print(json.dumps({'ok': True, 'path': str(out), 'cards': len(cards), 'format': 'html-index'}, ensure_ascii=False, indent=2))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
