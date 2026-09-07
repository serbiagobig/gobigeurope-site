#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist').resolve()
CYR=re.compile(r'[А-Яа-яЁё]')

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

    if p.name in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
        if 'gobig-mobile-master-v5' not in text:
            errors.append(f'{rel}: final mobile master layer missing')
        if 'gobig-unified-header' not in text:
            errors.append(f'{rel}: unified header missing')

# Berry route is intentional and must exist in all three languages.
berry_pages={
    'berry-harvesting.html':{
        'must':['Инновационная технология','Воздушно-импульсная уборка','Типичные проблемы ручной уборки','Когда ручной сбор становится ограничением','Мы создаем новую экономику уборки','до 500+ кг/час','до 4 га/день','Не просто оборудование. Система внедрения.','Анализ хозяйства','Запасные части','berry-harvesting-web.mp4'],
        'forbid':['Проверьте, подходит ли ваша плантация','Механизация — это процесс, а не покупка одной машины.','Планируете новую ягодную плантацию?','id="fit"']
    },
    'en/berry-harvesting.html':{
        'must':['Innovative technology','Air-pulse harvesting','Typical challenges of manual harvesting','Creating new harvesting economics','up to 500+ kg/hour','More than equipment. An implementation system.'],
        'forbid':['Проверьте, подходит ли ваша плантация','Механизация — это процесс, а не покупка одной машины.','Планируете новую ягодную плантацию?','id="fit"']
    },
    'cz/berry-harvesting.html':{
        'must':['Inovativní technologie','Sklizeň vzduchovými impulsy'],
        'forbid':['Проверьте, подходит ли ваша плантация','Механизация — это процесс, а не покупка одной машины.','Планируете новую ягодную плантацию?','id="fit"']
    }
}
for rel,cfg in berry_pages.items():
    p=ROOT/rel
    if not p.exists():
        errors.append(f'Approved berry page missing: {rel}')
        continue
    text=p.read_text(encoding='utf-8')
    for marker in cfg['must']:
        if marker not in text: errors.append(f'{rel}: approved berry marker missing: {marker}')
    for marker in cfg['forbid']:
        if marker in text: errors.append(f'{rel}: rejected berry block returned: {marker}')

# AGRO TAG must retain a path to the berry case without putting it in the main menu.
for rel in ('agro-tag.html','en/agro-tag.html','cz/agro-tag.html'):
    p=ROOT/rel
    if not p.exists(): continue
    text=p.read_text(encoding='utf-8')
    if 'berry-harvesting.html' not in text:
        errors.append(f'{rel}: berry-case entry point missing')
    nav_match=re.search(r'<nav class="nav">(.*?)</nav>',text,re.S|re.I)
    if nav_match and 'berry-harvesting.html' in nav_match.group(1):
        errors.append(f'{rel}: berry page was incorrectly added to main navigation')

if errors:
    for e in errors[:100]: print('ERROR:',e)
    raise SystemExit(f'FINAL SITE INTEGRITY AUDIT FAILED: {len(errors)} error(s)')

print(f'PASS: full-site integrity audit validated {len(pages)} published HTML pages')
print('PASS: exact approved berry state exists in RU/EN/CZ and rejected blocks are absent')
print('PASS: AGRO TAG links to berry case without adding it to main navigation')
print('PASS: all local page/assets references resolve')
print('PASS: EN/CZ visible text contains no Cyrillic')
print('PASS: final mobile/header layer present on all core RU/EN/CZ pages')
