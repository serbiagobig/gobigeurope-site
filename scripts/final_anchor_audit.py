#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist').resolve()

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.hrefs=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if d.get('id'): self.ids.add(d['id'])
        if tag == 'a' and d.get('href'): self.hrefs.append(d['href'])

pages = sorted(ROOT.glob('*.html')) + sorted(ROOT.glob('en/*.html')) + sorted(ROOT.glob('cz/*.html'))
parsed = {}
for page in pages:
    p=Parser(); p.feed(page.read_text(encoding='utf-8')); parsed[page.resolve()] = p

errors=[]
for page, parser in parsed.items():
    for href in parser.hrefs:
        if href.startswith(('http://','https://','mailto:','tel:','javascript:','data:','//')):
            continue
        local, sep, fragment = href.partition('#')
        if not sep or not fragment:
            continue
        local = local.split('?',1)[0]
        target = page if not local else (page.parent / unquote(local)).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            continue
        if target.suffix.lower() != '.html' or target not in parsed:
            continue
        if fragment not in parsed[target].ids:
            errors.append(f'{page.relative_to(ROOT)}: missing anchor target {href}')

if errors:
    for e in errors[:100]: print('ERROR:', e)
    raise SystemExit(f'FINAL ANCHOR AUDIT FAILED: {len(errors)} error(s)')
print(f'PASS: internal fragment links validated across {len(pages)} published HTML pages')
