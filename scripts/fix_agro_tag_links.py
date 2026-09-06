#!/usr/bin/env python3
from pathlib import Path
import re

TARGET='agro-tag.html'


def fix_international(s: str) -> str:
    # AGRO TAG is the first project card in the International showcase.
    marker='<h3>AGRO TAG</h3>'
    pos=s.find(marker)
    if pos == -1:
        raise SystemExit('AGRO TAG card not found in international.html')
    start=s.rfind('<', 0, pos)
    # Work in a bounded window around the card; this is intentionally tolerant of nested divs.
    left=max(0, pos-5000)
    right=min(len(s), pos+5000)
    chunk=s[left:right]
    rel=pos-left
    before=chunk[:rel]
    after=chunk[rel:]
    after_new=re.sub(
        r'<button[^>]*class="[^"]*(?:project-more|flip-more)[^"]*"[^>]*>\s*Подробнее(?:\s*→)?\s*</button>',
        '<a class="project-more" href="agro-tag.html">Подробнее →</a>',
        after,
        count=1,
    )
    if after_new == after:
        after_new=re.sub(
            r'<a[^>]*class="[^"]*project-more[^"]*"[^>]*>\s*Подробнее(?:\s*→)?\s*</a>',
            '<a class="project-more" href="agro-tag.html">Подробнее →</a>',
            after,
            count=1,
        )
    return s[:left] + before + after_new + s[right:]


def fix_projects(s: str) -> str:
    marker='<h3>AGRO TAG</h3>'
    pos=s.find(marker)
    if pos == -1:
        raise SystemExit('AGRO TAG card not found in projects.html')
    left=max(0, pos-3500)
    right=min(len(s), pos+3500)
    chunk=s[left:right]
    rel=pos-left
    before=chunk[:rel]
    after=chunk[rel:]
    after_new=re.sub(
        r'<button[^>]*class="[^"]*(?:more|flip-more)[^"]*"[^>]*>\s*Подробнее(?:\s*→)?\s*</button>',
        '<a class="more" href="agro-tag.html">Подробнее →</a>',
        after,
        count=1,
    )
    if after_new == after:
        after_new=re.sub(
            r'<a[^>]*class="[^"]*more[^"]*"[^>]*>\s*Подробнее(?:\s*→)?\s*</a>',
            '<a class="more" href="agro-tag.html">Подробнее →</a>',
            after,
            count=1,
        )
    return s[:left] + before + after_new + s[right:]

for name in ('international.html','projects.html'):
    p=Path('dist')/name
    if not p.exists():
        raise SystemExit(f'Missing {name}')
    s=p.read_text(encoding='utf-8')
    s=fix_international(s) if name=='international.html' else fix_projects(s)

    # Strong final verification: after the AGRO TAG heading, the first Подробнее action must be a direct anchor.
    pos=s.find('<h3>AGRO TAG</h3>')
    tail=s[pos:pos+5000]
    m=re.search(r'<(?:a|button)[^>]*>\s*Подробнее(?:\s*→)?\s*</(?:a|button)>', tail)
    if not m or not m.group(0).startswith('<a') or 'href="agro-tag.html"' not in m.group(0):
        raise SystemExit(f'AGRO TAG Подробнее is not a direct link in {name}')

    p.write_text(s,encoding='utf-8')

print('AGRO TAG Подробнее is a direct link on International and Projects')
