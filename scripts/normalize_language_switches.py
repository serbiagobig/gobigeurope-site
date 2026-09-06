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
        return '<nav class="langs">' + ''.join(
            f'<a href="{href}"'+(' class="active" aria-current="page"' if active else '')+f'>{label}</a>'
            for label,href,active in links
        ) + '</nav>'
    parts=[]
    for i,(label,href,active) in enumerate(links):
        if i: parts.append(' <span class="lang-sep">/</span> ')
        parts.append(f'<a href="{href}"'+(' class="current" aria-current="page"' if active else '')+f'>{label}</a>')
    return '<span class="lang-switch">'+''.join(parts)+'</span>'

SPAN_OPEN_RE=re.compile(r'<span\b[^>]*>',re.I)
SPAN_TOKEN_RE=re.compile(r'</?span\b[^>]*>',re.I)
LANG_CLASS_RE=re.compile(r'\bclass=["\'][^"\']*\blang-switch\b[^"\']*["\']',re.I)


def replace_lang_switch(html,replacement):
    """Replace the actual lang-switch span, including nested separator spans.
    CSS/JS references such as .lang-switch do not count as an HTML switch.
    """
    start=None
    for m in SPAN_OPEN_RE.finditer(html):
        if LANG_CLASS_RE.search(m.group(0)):
            start=m
            break
    if not start:
        return html,0
    depth=0
    for tok in SPAN_TOKEN_RE.finditer(html,start.start()):
        tag=tok.group(0).lower()
        if tag.startswith('</span'):
            depth-=1
            if depth==0:
                return html[:start.start()]+replacement+html[tok.end():],1
        else:
            depth+=1
    raise SystemExit('Unclosed lang-switch span')

for locale,folder in [('ru',ROOT),('en',ROOT/'en'),('cz',ROOT/'cz')]:
    for filename in PAGES:
        p=folder/filename
        if not p.exists():
            continue
        s=p.read_text(encoding='utf-8')
        if locale=='cz':
            s=re.sub(r'<html\b([^>]*?)\blang=["\'](?:ru|cz|cs)["\']',r'<html\1lang="cs"',s,count=1,flags=re.I)
        elif locale=='en':
            s=re.sub(r'<html\b([^>]*?)\blang=["\'](?:ru|en)["\']',r'<html\1lang="en"',s,count=1,flags=re.I)

        s,n=replace_lang_switch(s,switch(filename,locale,'span'))
        if re.search(r'<nav\b[^>]*class=["\'][^"\']*\blangs\b[^"\']*["\'][^>]*>',s,re.I):
            s,n2=re.subn(r'<nav\b[^>]*class=["\'][^"\']*\blangs\b[^"\']*["\'][^>]*>.*?</nav>',switch(filename,locale,'nav'),s,count=1,flags=re.S|re.I)
            if n2!=1:
                raise SystemExit(f'Could not normalize berry language switch in {p}')
        p.write_text(s,encoding='utf-8')

print('Normalized language order/routing to EN / CZ / RU and standardized Czech lang=cs')
