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

    # Digital & AI: add the same shared-projects CTA under the project cards if it is absent.
    if name == 'digital-ai.html' and 'Показать другие проекты' not in s:
        cta = '''<div class="projects-foot" style="display:flex;justify-content:center;margin-top:30px"><a class="projects-all" href="projects.html" style="display:inline-flex;align-items:center;gap:13px;min-height:52px;padding:0 28px;border:1px solid rgba(11,107,69,.45);border-radius:999px;color:#0B6B45;font-size:14px;font-weight:800;text-decoration:none">Показать другие проекты <span aria-hidden="true" style="font-size:20px;line-height:1">→</span></a></div>'''
        section_re = re.compile(r'(<section[^>]*id="projects"[^>]*>.*?)(</section>)', re.S)
        m = section_re.search(s)
        if not m:
            raise SystemExit('Projects section not found in digital-ai.html')
        s = s[:m.start()] + m.group(1) + cta + m.group(2) + s[m.end():]

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
        m=re.search(r'<a[^>]*class="[^"]*projects-all[^"]*"[^>]*>',s)
        if m and 'href="projects.html"' not in m.group(0):
            raise SystemExit(f'Projects CTA target not fixed in {name}')

    if name == 'digital-ai.html' and 'Показать другие проекты' not in s:
        raise SystemExit('Projects CTA missing in digital-ai.html')

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
