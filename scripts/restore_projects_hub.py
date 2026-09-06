#!/usr/bin/env python3
from pathlib import Path
import re

for name in ('international.html','digital-ai.html'):
    p=Path('dist')/name
    if not p.exists():
        raise SystemExit(f'Missing {name}')
    s=p.read_text(encoding='utf-8')

    # Top navigation: Projects must always open the shared projects hub.
    s=s.replace('href="#projects">Проекты</a>','href="projects.html">Проекты</a>')

    # Bottom CTA "Показать другие проекты": force the target regardless of whatever
    # href an earlier build/post-processing step may have written.
    s=re.sub(
        r'<a([^>]*\bclass="[^"]*projects-all[^"]*"[^>]*)\bhref="[^"]*"([^>]*)>',
        r'<a\1href="projects.html"\2>',
        s,
        count=1,
    )
    s=re.sub(
        r'<a([^>]*)\bhref="[^"]*"([^>]*\bclass="[^"]*projects-all[^"]*"[^>]*)>',
        r'<a\1href="projects.html"\2>',
        s,
        count=1,
    )

    # Fallback for known attribute orders.
    s=s.replace('href="#projects" class="projects-all"','href="projects.html" class="projects-all"')
    s=s.replace('class="projects-all" href="#projects"','class="projects-all" href="projects.html"')

    if 'projects-all' in s:
        # Verify the actual CTA now points to the shared hub.
        m=re.search(r'<a[^>]*class="[^"]*projects-all[^"]*"[^>]*>',s)
        if m and 'href="projects.html"' not in m.group(0):
            raise SystemExit(f'Projects CTA target not fixed in {name}')

    p.write_text(s,encoding='utf-8')

projects=Path('dist/projects.html')
if not projects.exists():
    raise SystemExit('Shared projects hub missing from dist')
text=projects.read_text(encoding='utf-8')
required=['Выход на рынок Сербии','Открытая лаборатория','Международные издательские проекты','Applied Research','Banking Transformation']
missing=[x for x in required if x not in text]
if missing:
    raise SystemExit('Projects hub is incomplete: '+', '.join(missing))

print('Restored shared Projects hub navigation and CTA links')
