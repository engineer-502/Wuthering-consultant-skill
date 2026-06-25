#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, urllib.request
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(description='Fetch explicit official/wiki card assets. Does not bulk scrape.')
    ap.add_argument('manifest_json', help='JSON list/object with items containing asset_url and output_path')
    ap.add_argument('--download', action='store_true', help='Actually download; default only plans.')
    args = ap.parse_args()
    data = json.loads(Path(args.manifest_json).read_text(encoding='utf-8'))
    items = data.get('items', data if isinstance(data, list) else [])
    results = []
    for item in items:
        url = item.get('asset_url') or item.get('source_url')
        out = item.get('output_path')
        status = 'planned'
        error = None
        if args.download and url and out:
            p = Path(out)
            p.parent.mkdir(parents=True, exist_ok=True)
            try:
                urllib.request.urlretrieve(url, p)
                status = 'downloaded'
            except Exception as exc:
                status = 'failed'
                error = str(exc)
        result = {'name': item.get('name'), 'url': url, 'output_path': out, 'status': status}
        if error:
            result['error'] = error
        results.append(result)
    print(json.dumps({'ok': True, 'download': args.download, 'results': results}, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
