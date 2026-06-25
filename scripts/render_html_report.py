#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, html
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(description='Render a dependency-free HTML build report.')
    ap.add_argument('report_json')
    ap.add_argument('--output', default='wuthering-consultant/generated/report.html')
    args = ap.parse_args()
    data = json.loads(Path(args.report_json).read_text(encoding='utf-8'))
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    recs = ''.join(f"<li><b>{html.escape(r.get('claim',''))}</b><p>{html.escape(r.get('rationale',''))}</p></li>" for r in data.get('recommendations', []))
    html_doc = f"""<!doctype html><meta charset='utf-8'><title>Wuthering Consultant Report</title>
<style>body{{font-family:system-ui,sans-serif;background:#06111f;color:#e5f9ff;padding:32px}}.card{{max-width:900px;border:1px solid #155e75;border-radius:24px;padding:28px;background:#0f172a}}a{{color:#67e8f9}}</style>
<div class='card'><h1>{html.escape(data.get('title','Wuthering Consultant Report'))}</h1><p>{html.escape(data.get('summary',''))}</p><ol>{recs}</ol></div>"""
    out.write_text(html_doc, encoding='utf-8')
    print(json.dumps({'ok': True, 'path': str(out), 'format': 'html'}, ensure_ascii=False, indent=2))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
