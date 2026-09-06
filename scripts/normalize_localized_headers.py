#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
CORE=['index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html']
LABELS={
'en': [('international.html','International Development'),('digital-ai.html','Digital & AI'),('education-hr.html','Learning & HR'),('projects.html','Projects'),('blog.html','Insights'),('index.html#contact','Contact')],
'cz': [('international.html','Mezinárodní rozvoj'),('digital-ai.html','Digitalizace a AI'),('education-hr.html','Vzdělávání a HR'),('projects.html','Projekty'),('blog.html','Novinky'),('index.html#contact','Kontakt')],
}
ACTIVE={'international.html':0,'digital-ai.html':1,'education-hr.html':2,'projects.html':3,'blog.html':4}

def language_switch(filename,lang):
    if lang=='en':
        links=[('EN',filename,True),('CZ',f'../cz/{filename}',False),('RU',f'../{filename}',False)]
    else:
        links=[('EN',f'../en/{filename}',False),('CZ',filename,True),('RU',f'../{filename}',False)]
    chunks=[]
    for i,(label,href,current) in enumerate(links):
        if i: chunks.append(' <span class="lang-sep">/</span> ')
        attrs=' class="current" aria-current="page"' if current else ''
        chunks.append(f'<a href="{href}"{attrs}>{label}</a>')
    return '<span class="lang-switch">'+''.join(chunks)+'</span>'

for lang in ('en','cz'):
    folder=ROOT/lang
    for filename in CORE:
        p=folder/filename
        if not p.exists():
            raise SystemExit(f'Missing localized core page: {p}')
        s=p.read_text(encoding='utf-8')
        links=[]
        for i,(href,label) in enumerate(LABELS[lang]):
            classes=[]
            if i==5: classes.append('contact')
            if ACTIVE.get(filename)==i: classes.append('active')
            cls=f' class="{" ".join(classes)}"' if classes else ''
            links.append(f'<a{cls} href="{href}">{label}</a>')
        nav='<nav class="nav">'+''.join(links)+language_switch(filename,lang)+'</nav>'
        s,n=re.subn(r'<nav class="nav">.*?</nav>',nav,s,count=1,flags=re.S|re.I)
        if n!=1:
            raise SystemExit(f'Could not rebuild localized header nav: {p}')
        # Always keep the logo/home target within the current locale.
        s=re.sub(r'(<header class="gobig-unified-header".*?<a class="brand" href=")[^"]*(")',r'\1index.html\2',s,count=1,flags=re.S)
        p.write_text(s,encoding='utf-8')

print('Normalized localized core headers and same-language navigation')
