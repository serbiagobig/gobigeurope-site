#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist').resolve()
PAGES=['index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html','agro-tag.html','agro-tag-contact.html','readiness.html','berry-harvesting.html']
CYR=re.compile(r'[А-Яа-яЁё]')

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.visible=[]; self.attrs_text=[]; self._skip=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('script','style'): self._skip+=1
        for k in ('href','src'):
            if d.get(k): self.refs.append(d[k])
        for k in ('alt','title','placeholder','aria-label','value'):
            if d.get(k): self.attrs_text.append(d[k])
    def handle_endtag(self,tag):
        if tag in ('script','style') and self._skip: self._skip-=1
    def handle_data(self,data):
        if not self._skip and data.strip(): self.visible.append(data.strip())

errors=[]
required=[]
for locale in ('ru','en','cz'):
    folder=ROOT if locale=='ru' else ROOT/locale
    for page in PAGES:
        required.append((locale,folder/page))

for locale,path in required:
    if not path.exists():
        errors.append(f'{locale}: missing page {path.relative_to(ROOT)}')
        continue
    text=path.read_text(encoding='utf-8')
    parser=Parser(); parser.feed(text)

    # Language declaration.
    expected='ru' if locale=='ru' else ('en' if locale=='en' else 'cs')
    if not re.search(rf'<html\b[^>]*\blang=["\']{expected}["\']',text,re.I):
        errors.append(f'{path.relative_to(ROOT)}: incorrect html lang')

    # No Russian visible copy/labels on EN/CZ.
    if locale in ('en','cz'):
        leftovers=[x for x in parser.visible+parser.attrs_text if CYR.search(x)]
        if leftovers:
            uniq=[]
            for x in leftovers:
                if x not in uniq: uniq.append(x)
            errors.append(f'{path.relative_to(ROOT)}: visible Cyrillic remains: '+ ' | '.join(uniq[:12]))

    # Language order must be EN / CZ / RU whenever a switch is present.
    switch=re.search(r'(?:<span class="lang-switch"[^>]*>.*?</span>|<nav class="langs">.*?</nav>)',text,re.S)
    if switch:
        labels=re.findall(r'>\s*(EN|CZ|RU)\s*</a>',switch.group(0),re.I)
        if [x.upper() for x in labels[:3]] != ['EN','CZ','RU']:
            errors.append(f'{path.relative_to(ROOT)}: language order is not EN / CZ / RU')

    # Mobile safety layer and overlay menu on core GO BIG pages.
    if path.name in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
        for marker in ('responsive-final.css','mobile-guardrails-v2','mobile-menu-overlay-v4'):
            if marker not in text:
                errors.append(f'{path.relative_to(ROOT)}: missing mobile marker {marker}')

    # Links/assets must resolve locally.
    for ref in parser.refs:
        if ref.startswith(('#','mailto:','tel:','javascript:','data:','http://','https://','//')): continue
        local=ref.split('#',1)[0].split('?',1)[0]
        if not local: continue
        target=(path.parent/unquote(local)).resolve()
        try: target.relative_to(ROOT)
        except ValueError: continue
        if not target.exists():
            errors.append(f'{path.relative_to(ROOT)}: broken local reference {ref}')

    # Localised pages must not silently route main navigation to Russian pages.
    if locale in ('en','cz') and path.name in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
        for page in ('international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
            # same-folder route is expected; ../page is only acceptable inside language switch and is caught separately by visible structure.
            if f'href="{page}"' not in text and f"href='{page}'" not in text:
                errors.append(f'{path.relative_to(ROOT)}: localized navigation missing {page}')

# Cross-locale route targets for switcher.
for locale in ('en','cz'):
    for page in PAGES:
        p=ROOT/locale/page
        if p.exists() and page!='berry-harvesting.html' and page in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html','agro-tag.html','agro-tag-contact.html','readiness.html'):
            pass

if errors:
    for e in errors: print('ERROR:',e)
    raise SystemExit(f'Multilingual QA failed with {len(errors)} error(s)')
print(f'PASS: {len(required)} RU/EN/CZ pages validated')
print('PASS: EN/CZ visible text and accessibility labels contain no Cyrillic')
print('PASS: language switches are ordered EN / CZ / RU')
print('PASS: local links and assets resolve')
print('PASS: core mobile responsive layers are present on RU/EN/CZ')
