#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

CONF = {'confirmed','inferred','needs_confirmation'}
TYPES = {'build','account','pull','rotation','report','weapon','echo'}
CURRENT_WORDS = ('current', 'latest', 'meta', '현재', '최신', '메타', '배너', '픽업')
PULL_WORDS = ('과금', '결제', '뽑', 'pull', 'convene', '픽업')
OPPORTUNITY_WORDS = ('기회비용', '대체', '보류', '조건', '리스크', 'opportunity')

def fail(msg, detail=None):
    print(json.dumps({'ok': False, 'error': msg, 'detail': detail}, ensure_ascii=False, indent=2))
    return 1

def has_source(data: dict) -> bool:
    return isinstance(data.get('sources'), list) and any(s.get('url') and s.get('type') for s in data['sources'])

def text_blob(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False).lower()

def validate_visuals(data: dict, problems: list):
    visuals = data.get('visual_artifacts', [])
    if visuals is None:
        return
    if not isinstance(visuals, list):
        problems.append('visual_artifacts must be a list')
        return
    for i, art in enumerate(visuals):
        if not isinstance(art, dict) or not art.get('kind') or not art.get('path'):
            problems.append({'visual_artifacts': i, 'error': 'kind and path required'})

def main() -> int:
    ap = argparse.ArgumentParser(description='Validate a Wuthering Consultant consultation/report JSON file.')
    ap.add_argument('json_path')
    args = ap.parse_args()
    path = Path(args.json_path)
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        return fail('invalid json', str(e))
    problems = []
    if data.get('game') not in {'Wuthering Waves','명조'}:
        problems.append('game must be Wuthering Waves or 명조')
    ctype = data.get('consultation_type')
    if ctype not in TYPES:
        problems.append({'consultation_type': ctype, 'error': 'unsupported consultation_type'})
    recs = data.get('recommendations')
    if not isinstance(recs, list) or not recs:
        problems.append('recommendations[] is required')
    else:
        for idx, rec in enumerate(recs):
            if not rec.get('claim') or not rec.get('rationale'):
                problems.append({'recommendation': idx, 'error': 'missing claim/rationale'})
            if rec.get('confidence') not in CONF:
                problems.append({'recommendation': idx, 'error': 'confidence must be confirmed/inferred/needs_confirmation', 'value': rec.get('confidence')})
    if not has_source(data):
        problems.append('sources[] with type/url is required')
    else:
        for idx, src in enumerate(data['sources']):
            if not src.get('url') or not src.get('type'):
                problems.append({'source': idx, 'error': 'missing type/url'})
            if src.get('type') in {'official','wiki','guide','community'} and not (src.get('title') and src.get('supports')):
                problems.append({'source': idx, 'error': 'title and supports[] recommended for non-screenshot sources'})
    blob = text_blob(data)
    if any(w in blob for w in CURRENT_WORDS) and not has_source(data):
        problems.append('current/latest/meta-sensitive claims require sources')
    if ctype == 'pull' or any(w in blob for w in PULL_WORDS):
        if not any(w in blob for w in OPPORTUNITY_WORDS):
            problems.append('pull/spending advice must include opportunity-cost or conservative alternative language')
    if ctype == 'report':
        validate_visuals(data, problems)
    if ctype == 'account' and not isinstance(data.get('account'), dict):
        problems.append('account consultation requires account{}')
    if ctype == 'build' and not isinstance(data.get('resonators'), list):
        problems.append('build consultation requires resonators[] or explicit needs_confirmation extraction')
    if problems:
        return fail('validation problems', problems)
    print(json.dumps({'ok': True, 'file': str(path), 'consultation_type': ctype, 'recommendations': len(recs), 'sources': len(data['sources'])}, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
