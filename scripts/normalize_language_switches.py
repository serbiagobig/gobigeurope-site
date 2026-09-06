#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
PAGES=['index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html','agro-tag.html','agro-tag-contact.html','readiness.html','berry-harvesting.html']


def switch(filename,locale,kind='span'):
    if locale=='ru':
        links=[('EN',f'en/{filename}',False),('CZ',f'cz/{filename}',False),('RU',filename,True)]
    elif locale=='en':
        links=[('EN',filename,True),('CZ',f'../cz/{filename}',False),('RU',f'../{filename}',False)]
    else:
        links=[('EN',f'../en/{filename}',False),('CZ',filename,True),('RU',f'../{filename}',False)]
    if kind=='nav':
        return '<nav class="langs">'+''.join(f'<a href="{href}"'+(' class="active"' if active else '')+f'>{label}</a>' for label,href,active in links)+'</nav>'
    parts=[]
    for i,(label,href,active) in enumerate(links):
        if i: parts.append('<span class="lang-sep">/</span>')
        parts.append(f'<a href="{href}"'+(' class="current" aria-current="page"' if active else '')+f'>{label}</a>')
    return '<span class="lang-switch">'+''.join(parts)+'</span>'

for locale,folder in [('ru',ROOT),('en',ROOT/'en'),('cz',ROOT/'cz')]:
    for filename in PAGES:
        p=folder/filename
        if not p.exists(): continue
        s=p.read_text(encoding='utf-8')
        # Main GO BIG headers.
        if 'class="lang-switch"' in s:
            s=re.sub(r'<span class="lang-switch"[^>]*>.*?</span>',switch(filename,locale,'span'),s,count=1,flags=re.S)
        # AGRO TAG berry header.
        if 'class="langs"' in s:
            s=re.sub(r'<nav class="langs">.*?</nav>',switch(filename,locale,'nav'),s,count=1,flags=re.S)
        p.write_text(s,encoding='utf-8')

print('Normalized language order and routing to EN / CZ / RU')
