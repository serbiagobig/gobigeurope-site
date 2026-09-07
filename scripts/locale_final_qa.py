#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist').resolve()
PAGES=['index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html','agro-tag.html','agro-tag-contact.html','readiness.html']
CYR=re.compile(r'[А-Яа-яЁё]')
LATE_GENERATED_ASSETS={'assets/agro-tag-center.png','../assets/agro-tag-center.png','assets/agro-card-05.png','../assets/agro-card-05.png'}
RETIRED='berry-harvesting.html'

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

def get_switch_labels(text):
    m=re.search(r'<span class="lang-switch"[^>]*>(.*?)<a\b[^>]*>\s*RU\s*</a>\s*</span>',text,re.S|re.I)
    if m:
        return [x.upper() for x in re.findall(r'>\s*(EN|CZ|RU)\s*</a>',m.group(0),re.I)]
    m=re.search(r'<nav class="langs">(.*?)</nav>',text,re.S|re.I)
    if m:
        return [x.upper() for x in re.findall(r'>\s*(EN|CZ|RU)\s*</a>',m.group(0),re.I)]
    return []

errors=[]
required=[]
for locale in ('ru','en','cz'):
    folder=ROOT if locale=='ru' else ROOT/locale
    for page in PAGES:
        required.append((locale,folder/page))

# Removed route must stay removed in every locale.
for rel in (RETIRED,'en/'+RETIRED,'cz/'+RETIRED):
    if (ROOT/rel).exists(): errors.append(f'retired route was republished: {rel}')

for locale,path in required:
    if not path.exists():
        errors.append(f'{locale}: missing page {path.relative_to(ROOT)}')
        continue
    text=path.read_text(encoding='utf-8')
    parser=Parser(); parser.feed(text)

    if RETIRED.lower() in text.lower():
        errors.append(f'{path.relative_to(ROOT)}: retired berry route reference remains')

    expected='ru' if locale=='ru' else ('en' if locale=='en' else 'cs')
    if not re.search(rf'<html\b[^>]*\blang=["\']{expected}["\']',text,re.I):
        errors.append(f'{path.relative_to(ROOT)}: incorrect html lang')

    if locale in ('en','cz'):
        leftovers=[x for x in parser.visible+parser.attrs_text if CYR.search(x)]
        if leftovers:
            uniq=[]
            for x in leftovers:
                if x not in uniq: uniq.append(x)
            errors.append(f'{path.relative_to(ROOT)}: visible Cyrillic remains: '+' | '.join(uniq[:12]))

    labels=get_switch_labels(text)
    if labels and labels[:3] != ['EN','CZ','RU']:
        errors.append(f'{path.relative_to(ROOT)}: language order is not EN / CZ / RU ({labels[:3]})')

    if path.name in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
        for marker in ('responsive-final.css','mobile-guardrails-v2','mobile-menu-overlay-v4'):
            if marker not in text:
                errors.append(f'{path.relative_to(ROOT)}: missing mobile marker {marker}')

    for ref in parser.refs:
        if ref.startswith(('#','mailto:','tel:','javascript:','data:','http://','https://','//')): continue
        local=ref.split('#',1)[0].split('?',1)[0]
        if not local or local in LATE_GENERATED_ASSETS: continue
        target=(path.parent/unquote(local)).resolve()
        try: target.relative_to(ROOT)
        except ValueError: continue
        if not target.exists(): errors.append(f'{path.relative_to(ROOT)}: broken local reference {ref}')

    if locale in ('en','cz') and path.name in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
        nav_match=re.search(r'<nav class="nav">(.*?)</nav>',text,re.S|re.I)
        if not nav_match:
            errors.append(f'{path.relative_to(ROOT)}: localized main navigation missing')
        else:
            nav=nav_match.group(1)
            for page in ('international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
                if f'href="{page}"' not in nav and f"href='{page}'" not in nav:
                    errors.append(f'{path.relative_to(ROOT)}: localized navigation missing {page}')

if errors:
    for e in errors: print('ERROR:',e)
    raise SystemExit(f'Multilingual QA failed with {len(errors)} error(s)')
print(f'PASS: {len(required)} RU/EN/CZ pages validated')
print('PASS: retired berry harvesting route is absent in RU/EN/CZ and unreferenced')
print('PASS: EN/CZ visible text and accessibility labels contain no Cyrillic')
print('PASS: language switches are ordered EN / CZ / RU')
print('PASS: local links/assets resolve at build stage')
print('PASS: core mobile responsive layers are present on RU/EN/CZ')
