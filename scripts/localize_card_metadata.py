#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from common import load_official_seed

BASE = {
  'Wuthering Waves':'명조','Resonator':'공명자','Echo':'에코','Sonata Effect':'소나타 효과',
  'Concerto Energy':'협주 에너지','Intro Skill':'인트로 스킬','Outro Skill':'아웃트로 스킬',
  'Energy Regen':'에너지 회복','Spectro':'회절','Electro':'전도','Glacio':'응결','Aero':'기류',
  'Pistols':'권총','Rectifier':'증폭기','Sword':'직검'
}

def localize_obj(obj, mapping):
    if isinstance(obj, str):
        return mapping.get(obj, obj)
    if isinstance(obj, list):
        return [localize_obj(x, mapping) for x in obj]
    if isinstance(obj, dict):
        return {k: localize_obj(v, mapping) for k, v in obj.items()}
    return obj

def main() -> int:
    ap = argparse.ArgumentParser(description='Localize Wuthering Waves card metadata names into Korean where seed aliases exist.')
    ap.add_argument('json_path')
    ap.add_argument('--in-place', action='store_true')
    args = ap.parse_args()
    path = Path(args.json_path)
    data = json.loads(path.read_text(encoding='utf-8'))
    mapping = dict(BASE)
    seed = load_official_seed()
    for group in ('resonators','weapons','echoes','sonata_effects'):
        for item in seed.get(group, []):
            mapping[item.get('name')] = item.get('ko', item.get('name'))
    out = localize_obj(data, mapping)
    if args.in_place:
        path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'ok': True, 'path': str(path)}, ensure_ascii=False))
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
