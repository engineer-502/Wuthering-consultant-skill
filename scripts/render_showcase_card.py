#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(description='Render weapon/echo showcase card via visual-card fallback renderer.')
    ap.add_argument('showcase_json')
    ap.add_argument('--output', default='wuthering-consultant/generated/showcase.svg')
    args = ap.parse_args()
    data = json.loads(Path(args.showcase_json).read_text(encoding='utf-8'))
    data.setdefault('kind', 'showcase')
    data.setdefault('title', data.get('title', 'WuWa Showcase'))
    tmp = Path(args.output).with_suffix('.metadata.json')
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    cmd = [sys.executable, str(Path(__file__).with_name('render_visual_card.py')), str(tmp), '--output', args.output]
    return subprocess.call(cmd)

if __name__ == '__main__':
    raise SystemExit(main())
