#!/usr/bin/env python3
from pathlib import Path
import re

TARGET='agro-tag.html'

for name in ('international.html','projects.html'):
    p=Path('dist')/name
    if not p.exists():
        raise SystemExit(f'Missing {name}')
    s=p.read_text(encoding='utf-8')

    if name=='international.html':
        # Find the AGRO TAG project card and make its visible action a direct link.
        pat=re.compile(r'(<[^>]+class="[^"]*project-card[^"]*"[^>]*>(?:(?!</(?:article|div)>).)*?<h3>\s*AGRO TAG\s*</h3>(?:(?!</(?:article|div)>).)*?)(</(?:article|div)>)',re.S)
        m=pat.search(s)
        if m:
            card=m.group(1)+m.group(2)
            card=re.sub(r'<button([^>]*class="[^"]*(?:project-more|flip-more)[^"]*"[^>]*)>\s*Подробнее(?:\s*→)?\s*</button>',
                        r'<a class="project-more" href="agro-tag.html">Подробнее →</a>',card,count=1)
            card=re.sub(r'<a([^>]*class="[^"]*project-more[^"]*"[^>]*)href="[^"]*"([^>]*)>',
                        r'<a\1href="agro-tag.html"\2>',card,count=1)
            s=s[:m.start()]+card+s[m.end():]
    else:
        # On the shared Projects page force AGRO TAG's primary CTA to the AGRO TAG page.
        pat=re.compile(r'(<article[^>]*>(?:(?!</article>).)*?<h3>\s*AGRO TAG\s*</h3>(?:(?!</article>).)*?</article>)',re.S)
        m=pat.search(s)
        if m:
            card=m.group(1)
            card=re.sub(r'<button([^>]*class="[^"]*(?:more|flip-more)[^"]*"[^>]*)>\s*Подробнее(?:\s*→)?\s*</button>',
                        r'<a class="more" href="agro-tag.html">Подробнее →</a>',card,count=1)
            card=re.sub(r'<a([^>]*class="[^"]*more[^"]*"[^>]*)href="[^"]*"([^>]*)>',
                        r'<a\1href="agro-tag.html"\2>',card,count=1)
            s=s[:m.start()]+card+s[m.end():]

    if 'AGRO TAG' not in s or 'href="agro-tag.html"' not in s:
        raise SystemExit(f'AGRO TAG link not fixed in {name}')
    p.write_text(s,encoding='utf-8')

print('AGRO TAG links fixed on International and Projects')
