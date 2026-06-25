#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess, sys
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(description='Render party list card via visual-card fallback renderer.')
    ap.add_argument('parties_json')
    ap.add_argument('--output', default='wuthering-consultant/generated/party_list.svg')
    args = ap.parse_args()
    data = json.loads(Path(args.parties_json).read_text(encoding='utf-8'))
    parties = data.get('parties', [])
    lines = []
    for p in parties[:6]:
        if isinstance(p, dict):
            lines.append(f"{p.get('name','Team')}: {' / '.join(p.get('members', []))}")
    card = {
        'kind': 'party_list_card',
        'title': data.get('title', '추천 파티'),
        'subtitle': data.get('subtitle', 'Wuthering Waves'),
        'lines': lines,
    }
    tmp = Path(args.output).with_suffix('.metadata.json')
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(card, ensure_ascii=False, indent=2), encoding='utf-8')
    cmd = [sys.executable, str(Path(__file__).with_name('render_visual_card.py')), str(tmp), '--output', args.output]
    return subprocess.call(cmd)

if __name__ == '__main__':
    raise SystemExit(main())
