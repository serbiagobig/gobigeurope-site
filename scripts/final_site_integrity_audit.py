#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist').resolve()
CYR=re.compile(r'[А-Яа-яЁё]')
RETIRED='berry-harvesting.html'

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.visible=[]; self.attrs=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('script','style'): self.skip+=1
        for key in ('href','src'):
            v=d.get(key)
            if v: self.refs.append(v)
        for key in ('alt','title','placeholder','aria-label','value'):
            v=d.get(key)
            if v: self.attrs.append(v)
    def handle_endtag(self,tag):
        if tag in ('script','style') and self.skip: self.skip-=1
    def handle_data(self,data):
        if not self.skip and data.strip(): self.visible.append(data.strip())

pages=sorted(ROOT.glob('*.html'))+sorted(ROOT.glob('en/*.html'))+sorted(ROOT.glob('cz/*.html'))
errors=[]
if not pages: errors.append('No published HTML pages found')

for p in pages:
    rel=p.relative_to(ROOT)
    text=p.read_text(encoding='utf-8')
    parser=Parser(); parser.feed(text)

    if RETIRED.lower() in text.lower():
        errors.append(f'{rel}: retired berry route reference remains')

    locale='en' if p.parent.name=='en' else ('cz' if p.parent.name=='cz' else 'ru')
    if locale in ('en','cz'):
        leftovers=[x for x in parser.visible+parser.attrs if CYR.search(x)]
        if leftovers:
            errors.append(f'{rel}: visible Cyrillic remains: {leftovers[0][:120]}')

    for ref in parser.refs:
        if ref.startswith(('#','mailto:','tel:','javascript:','data:','http://','https://','//')): continue
        local=ref.split('#',1)[0].split('?',1)[0]
        if not local: continue
        target=(p.parent/unquote(local)).resolve()
        try: target.relative_to(ROOT)
        except ValueError: continue
        if not target.exists(): errors.append(f'{rel}: broken local reference {ref}')

    # Core pages must retain the final mobile authority after all localisation/post-build work.
    if p.name in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
        if 'gobig-mobile-master-v5' not in text:
            errors.append(f'{rel}: final mobile master layer missing')
        if 'gobig-unified-header' not in text:
            errors.append(f'{rel}: unified header missing')

for rel in (RETIRED,'en/'+RETIRED,'cz/'+RETIRED):
    if (ROOT/rel).exists(): errors.append(f'Retired page exists: {rel}')

if errors:
    for e in errors[:100]: print('ERROR:',e)
    raise SystemExit(f'FINAL SITE INTEGRITY AUDIT FAILED: {len(errors)} error(s)')

print(f'PASS: full-site integrity audit validated {len(pages)} published HTML pages')
print('PASS: no retired berry route or links')
print('PASS: all local page/assets references resolve')
print('PASS: EN/CZ visible text contains no Cyrillic')
print('PASS: final mobile/header layer present on all core RU/EN/CZ pages')
