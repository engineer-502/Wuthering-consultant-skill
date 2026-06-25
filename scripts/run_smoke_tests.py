#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def run(name: str, cmd: list[str], expect: int = 0) -> dict:
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONUTF8'] = '1'
    env['PYTHONIOENCODING'] = 'utf-8'
    res = subprocess.run(cmd, cwd=REPO, text=True, encoding='utf-8', errors='replace', capture_output=True, env=env)
    return {'name': name, 'cmd': cmd, 'returncode': res.returncode, 'expected': expect, 'ok': res.returncode == expect, 'stdout': (res.stdout or '')[-2000:], 'stderr': (res.stderr or '')[-2000:]}

def cleanup_bytecode() -> None:
    for cache_dir in sorted((p for p in ROOT.rglob('__pycache__') if p.is_dir()), reverse=True):
        shutil.rmtree(cache_dir)
    for pyc in ROOT.rglob('*.pyc'):
        pyc.unlink(missing_ok=True)

def cache_artifacts() -> list[str]:
    paths = [p for p in ROOT.rglob('__pycache__') if p.is_dir()]
    paths.extend(ROOT.rglob('*.pyc'))
    return sorted(str(p.relative_to(ROOT)) for p in paths)

def main() -> int:
    cleanup_bytecode()
    py_files = sorted(str(p) for p in (ROOT/'scripts').glob('*.py'))
    checks = []
    checks.append(run('py_compile', [sys.executable, '-m', 'py_compile', *py_files]))
    cleanup_bytecode()
    checks.append(run('validate_seed', [sys.executable, str(ROOT/'scripts/validate_seed.py'), str(ROOT/'data/seed/wuwa_official_3_4_seed.json')]))
    checks.append(run('update_seed_fixture_dry_run', [sys.executable, str(ROOT/'scripts/update_official_seed.py'), '--fixture-dir', str(ROOT/'data/fixtures/official'), '--dry-run']))
    for ex in sorted((ROOT/'examples').glob('*.json')):
        if ex.name in {'report_card.json','showcase.json','party_list.json','visual_page.json'}:
            continue
        checks.append(run(f'validate_example:{ex.name}', [sys.executable, str(ROOT/'scripts/validate_consultation.py'), str(ex)]))
    for neg in sorted((ROOT/'examples/invalid').glob('*.json')):
        checks.append(run(f'negative_fixture:{neg.name}', [sys.executable, str(ROOT/'scripts/validate_consultation.py'), str(neg)], expect=1))
    with tempfile.TemporaryDirectory(prefix='wuwa-smoke-') as temp:
        out_dir = Path(temp)
        checks.extend([
            run('query_lucilla_en', [sys.executable, str(ROOT/'scripts/query_asset_cache.py'), 'Lucilla', '--kind', 'resonator', '--format', 'json']),
            run('query_lucilla_ko', [sys.executable, str(ROOT/'scripts/query_asset_cache.py'), '루실라', '--kind', 'resonator', '--format', 'json']),
            run('query_freeze_frame', [sys.executable, str(ROOT/'scripts/query_asset_cache.py'), 'Freeze Frame', '--kind', 'weapon', '--format', 'paths']),
            run('query_party_table', [sys.executable, str(ROOT/'scripts/query_asset_cache.py'), 'Lucy', 'Rebecca', 'Baizhi', '--kind', 'resonator', '--thumb-size', '48', '--format', 'table', '--headers', 'Main|Support|Healer']),
            run('render_visual', [sys.executable, str(ROOT/'scripts/render_visual_card.py'), str(ROOT/'examples/report_card.json'), '--output', str(out_dir/'wuwa-card.svg')]),
            run('render_showcase', [sys.executable, str(ROOT/'scripts/render_showcase_card.py'), str(ROOT/'examples/showcase.json'), '--output', str(out_dir/'wuwa-showcase.svg')]),
            run('render_party', [sys.executable, str(ROOT/'scripts/render_party_list_card.py'), str(ROOT/'examples/party_list.json'), '--output', str(out_dir/'wuwa-party.svg')]),
            run('render_html', [sys.executable, str(ROOT/'scripts/render_html_report.py'), str(ROOT/'examples/sample_consultation.json'), '--output', str(out_dir/'wuwa-report.html')]),
            run('compose_page', [sys.executable, str(ROOT/'scripts/compose_visual_page.py'), str(ROOT/'examples/visual_page.json'), '--output', str(out_dir/'wuwa-page.html')]),
        ])
    cleanup_bytecode()
    caches = cache_artifacts()
    checks.append({
        'name': 'cache_artifacts_absent',
        'cmd': ['find', 'wuthering-consultant', '-path', '*/__pycache__', '-o', '-name', '*.pyc'],
        'returncode': 0 if not caches else 1,
        'expected': 0,
        'ok': not caches,
        'stdout': '\n'.join(caches),
        'stderr': '',
    })
    ok = all(c['ok'] for c in checks)
    print(json.dumps({'ok': ok, 'checks': checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
