#!/usr/bin/env python3
from pathlib import Path

for name in ('international.html','digital-ai.html'):
    p=Path('dist')/name
    if not p.exists():
        raise SystemExit(f'Missing {name}')
    s=p.read_text(encoding='utf-8')
    s=s.replace('href="#projects">Проекты</a>','href="projects.html">Проекты</a>')
    s=s.replace('href="#projects" class="projects-all"','href="projects.html" class="projects-all"')
    s=s.replace('class="projects-all" href="#projects"','class="projects-all" href="projects.html"')
    p.write_text(s,encoding='utf-8')

projects=Path('dist/projects.html')
if not projects.exists():
    raise SystemExit('Shared projects hub missing from dist')
text=projects.read_text(encoding='utf-8')
required=['Выход на рынок Сербии','Открытая лаборатория','Международные издательские проекты','Applied Research','Banking Transformation']
missing=[x for x in required if x not in text]
if missing:
    raise SystemExit('Projects hub is incomplete: '+', '.join(missing))

print('Restored shared Projects hub navigation')
