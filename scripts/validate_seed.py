#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

REQUIRED_GROUPS = ('resonators', 'weapons', 'echoes', 'sonata_effects')

def fail(message: str, detail=None) -> int:
    print(json.dumps({'ok': False, 'error': message, 'detail': detail}, ensure_ascii=False, indent=2))
    return 1

def require_url(value: str | None) -> bool:
    return isinstance(value, str) and value.startswith(('http://', 'https://'))

def main() -> int:
    ap = argparse.ArgumentParser(description='Validate Wuthering Consultant official seed schema.')
    ap.add_argument('seed_json')
    args = ap.parse_args()
    path = Path(args.seed_json)
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        return fail('invalid json', str(exc))
    if data.get('game') != 'Wuthering Waves':
        return fail('game must be Wuthering Waves')
    missing_groups = [g for g in REQUIRED_GROUPS if not isinstance(data.get(g), list)]
    if missing_groups:
        return fail('missing required list groups', missing_groups)
    official_sources = data.get('official_sources')
    if not isinstance(official_sources, list) or not official_sources:
        return fail('official_sources[] required')
    source_ids = {s.get('id') for s in official_sources if require_url(s.get('url'))}
    problems = []
    for group in REQUIRED_GROUPS:
        for idx, item in enumerate(data.get(group, [])):
            loc = {'group': group, 'index': idx, 'name': item.get('name')}
            if not item.get('name'):
                problems.append({**loc, 'error': 'missing name'})
            if 'ko' not in item:
                problems.append({**loc, 'error': 'missing ko display marker'})
            if not require_url(item.get('source_url')):
                problems.append({**loc, 'error': 'missing source_url'})
            ids = item.get('source_ids', [])
            if not ids or not any(i in source_ids for i in ids):
                problems.append({**loc, 'error': 'source_ids do not reference official_sources'})
    rules = data.get('convene_rules', {})
    if not require_url(rules.get('source_url')):
        problems.append({'group': 'convene_rules', 'error': 'missing source_url'})
    if problems:
        return fail('seed validation problems', problems)
    print(json.dumps({'ok': True, 'file': str(path), 'groups': {g: len(data.get(g, [])) for g in REQUIRED_GROUPS}, 'official_sources': len(official_sources)}, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
