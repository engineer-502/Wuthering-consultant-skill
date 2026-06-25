#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, urllib.request
from pathlib import Path
from common import SKILL_DIR, load_official_seed

DEFAULT_ARTICLE_MENU = 'https://hw-media-cdn-mingchao.kurogame.com/akiwebsite/website2.0/json/G152/en/ArticleMenu.json'
DEFAULT_ARTICLE_URL = 'https://hw-media-cdn-mingchao.kurogame.com/akiwebsite/website2.0/json/G152/en/article/{id}.json'

KNOWN_SUPPORT = {
    4819: ['Version 3.4 official release/content seed', 'Lucy/Rebecca/Lucilla official role tags'],
    758: ['Featured Resonator/Weapon Convene guarantee rules'],
    4916: ['Cartethyia Phase II and Defier\'s Thorn schedule'],
    4836: ['Lucy collab resonator convene'],
    4852: ['Rebecca collab resonator convene'],
    4918: ['Cartethyia resonator review']
}

def load_json_url(url: str) -> object:
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))

def load_fixture(fixture_dir: Path, name: str) -> object:
    return json.loads((fixture_dir / name).read_text(encoding='utf-8'))

def article_to_source(article: dict, url: str) -> dict:
    source = {
        'id': article.get('articleId'),
        'title': article.get('articleTitle') or article.get('title') or 'Untitled',
        'date': article.get('startTime') or article.get('createTime') or 'unknown',
        'url': url,
        'supports': KNOWN_SUPPORT.get(article.get('articleId'), [])
    }
    if article.get('fetch_error'):
        source['fetch_error'] = article['fetch_error']
    return source

def main() -> int:
    ap = argparse.ArgumentParser(description='Update/normalize Wuthering Waves official source metadata and seed links.')
    ap.add_argument('--fixture-dir', type=Path, default=None, help='Use offline fixture directory containing ArticleMenu.json and articles/<id>.json')
    ap.add_argument('--ids', nargs='*', type=int, default=None, help='Article ids to normalize; defaults to existing official seed ids')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--write', action='store_true', help='Write data/sources/official_sources.json and optionally refreshed seed official_sources')
    ap.add_argument('--output', type=Path, default=None)
    args = ap.parse_args()
    seed = load_official_seed()
    ids = args.ids or [int(s['id']) for s in seed.get('official_sources', [])]
    articles = []
    if args.fixture_dir:
        menu = load_fixture(args.fixture_dir, 'ArticleMenu.json')
        menu_by_id = {int(a.get('articleId')): a for a in (menu if isinstance(menu, list) else menu.get('article', [])) if a.get('articleId')}
        for i in ids:
            article_path = args.fixture_dir / 'articles' / f'{i}.json'
            article = json.loads(article_path.read_text(encoding='utf-8')) if article_path.exists() else menu_by_id.get(i, {'articleId': i, 'articleTitle': f'Article {i}', 'startTime': 'unknown'})
            url = DEFAULT_ARTICLE_URL.format(id=i)
            articles.append(article_to_source(article, url))
    else:
        menu = load_json_url(DEFAULT_ARTICLE_MENU)
        menu_items = menu if isinstance(menu, list) else menu.get('article', [])
        menu_by_id = {int(a.get('articleId')): a for a in menu_items if a.get('articleId')}
        for i in ids:
            try:
                article = load_json_url(DEFAULT_ARTICLE_URL.format(id=i))
            except Exception as exc:
                article = dict(menu_by_id.get(i, {'articleId': i, 'articleTitle': f'Article {i}', 'startTime': 'unknown'}))
                article['fetch_error'] = f'{type(exc).__name__}: {exc}'
            articles.append(article_to_source(article, DEFAULT_ARTICLE_URL.format(id=i)))
    out = {'schema_version': 1, 'generated_by': 'update_official_seed.py', 'dry_run': bool(args.dry_run), 'sources': articles}
    if args.write and not args.dry_run:
        target = args.output or (SKILL_DIR / 'data' / 'sources' / 'official_sources.json')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
