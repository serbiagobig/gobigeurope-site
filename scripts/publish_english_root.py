#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
EN = ROOT / 'en'
CZ = ROOT / 'cz'
RU = ROOT / 'ru'

if not EN.exists() or not CZ.exists():
    raise SystemExit('Expected generated en/ and cz/ locales before root-language promotion')

root_pages = sorted(p.name for p in ROOT.glob('*.html'))
if not root_pages:
    raise SystemExit('No root HTML pages found')
missing_en = [name for name in root_pages if not (EN / name).exists()]
missing_cz = [name for name in root_pages if not (CZ / name).exists()]
if missing_en or missing_cz:
    raise SystemExit(f'Locale parity failed before promotion. Missing EN={missing_en}; CZ={missing_cz}')

RU.mkdir(exist_ok=True)

# Snapshot the approved Russian root pages before replacing the root with English.
ru_source = {name: (ROOT / name).read_text(encoding='utf-8') for name in root_pages}
en_source = {name: (EN / name).read_text(encoding='utf-8') for name in root_pages}

ROOT_FILES = {
    'home-premium.css', 'international-hero.css', 'partners-ecosystem.css',
    'berry-harvesting-web.mp4', 'CNAME', 'robots.txt', 'sitemap.xml'
}


def shift_root_assets_for_nested(text: str) -> str:
    # Pages moved from / to /ru need one extra parent level for shared site assets.
    for prefix in ('assets/', 'catalogs/'):
        text = text.replace(f'src="{prefix}', f'src="../{prefix}')
        text = text.replace(f"src='{prefix}", f"src='../{prefix}")
        text = text.replace(f'href="{prefix}', f'href="../{prefix}')
        text = text.replace(f"href='{prefix}", f"href='../{prefix}")
        text = text.replace(f'url("{prefix}', f'url("../{prefix}')
        text = text.replace(f"url('{prefix}", f"url('../{prefix}")
    for filename in ROOT_FILES:
        text = text.replace(f'href="{filename}', f'href="../{filename}')
        text = text.replace(f"href='{filename}", f"href='../{filename}")
        text = text.replace(f'src="{filename}', f'src="../{filename}')
        text = text.replace(f"src='{filename}", f"src='../{filename}")
    # Existing language links from the old Russian root are normalized later,
    # but these rewrites also keep any non-header cross-locale links valid.
    text = re.sub(r'(["\'])en/([^"\']+\.html(?:#[^"\']*)?)', r'\1../\2', text)
    text = re.sub(r'(["\'])cz/([^"\']+\.html(?:#[^"\']*)?)', r'\1../cz/\2', text)
    return text


def shift_nested_en_to_root(text: str) -> str:
    # Generated English pages currently live one level down. Promote them to /.
    for prefix in ('assets/', 'catalogs/'):
        text = text.replace(f'src="../{prefix}', f'src="{prefix}')
        text = text.replace(f"src='../{prefix}", f"src='{prefix}")
        text = text.replace(f'href="../{prefix}', f'href="{prefix}')
        text = text.replace(f"href='../{prefix}", f"href='{prefix}")
        text = text.replace(f'url("../{prefix}', f'url("{prefix}')
        text = text.replace(f"url('../{prefix}", f"url('{prefix}")
    for filename in ROOT_FILES:
        text = text.replace(f'href="../{filename}', f'href="{filename}')
        text = text.replace(f"href='../{filename}", f"href='{filename}")
        text = text.replace(f'src="../{filename}', f'src="{filename}')
        text = text.replace(f"src='../{filename}", f"src='{filename}")
    # Old EN language links to CZ remain one level too high after promotion.
    text = re.sub(r'(["\'])\.\./cz/([^"\']+\.html(?:#[^"\']*)?)', r'\1cz/\2', text)
    # Old EN language links to the former Russian root now belong under /ru/.
    text = re.sub(r'(["\'])\.\./([^/"\']+\.html(?:#[^"\']*)?)', r'\1ru/\2', text)
    return text


def switch_html(locale: str, name: str) -> str:
    if locale == 'root':
        links = [('EN', name, True), ('CZ', f'cz/{name}', False), ('RU', f'ru/{name}', False)]
    elif locale == 'ru':
        links = [('EN', f'../{name}', False), ('CZ', f'../cz/{name}', False), ('RU', name, True)]
    elif locale == 'cz':
        links = [('EN', f'../{name}', False), ('CZ', name, True), ('RU', f'../ru/{name}', False)]
    else:  # legacy /en/ alias
        links = [('EN', f'../{name}', True), ('CZ', f'../cz/{name}', False), ('RU', f'../ru/{name}', False)]
    out = ['<span class="lang-switch">']
    for i, (label, href, current) in enumerate(links):
        if i:
            out.append('<span class="lang-sep">/</span>')
        cls = ' class="current" aria-current="page"' if current else ''
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    out.append('</span>')
    return ''.join(out)


def normalize_unified_switch(text: str, locale: str, name: str) -> str:
    header = re.search(r'(<header\b[^>]*class="[^"]*gobig-unified-header[^"]*"[^>]*>.*?</header>)', text, re.S | re.I)
    if not header:
        return text
    h = header.group(1)
    nav = re.search(r'(<nav\b[^>]*class="[^"]*nav[^"]*"[^>]*>)(.*?)(</nav>)', h, re.S | re.I)
    if not nav:
        raise SystemExit(f'Missing unified nav while publishing {locale}/{name}')
    body = nav.group(2)
    marker = re.search(r'<span\b[^>]*class="[^"]*lang-switch[^"]*"[^>]*>', body, re.I)
    if not marker:
        return text
    clean_body = body[:marker.start()] + switch_html(locale, name)
    new_nav = nav.group(1) + clean_body + nav.group(3)
    new_h = h[:nav.start()] + new_nav + h[nav.end():]
    return text[:header.start()] + new_h + text[header.end():]

# 1) Move approved Russian pages under /ru/.
for name, text in ru_source.items():
    text = shift_root_assets_for_nested(text)
    text = normalize_unified_switch(text, 'ru', name)
    (RU / name).write_text(text, encoding='utf-8')

# 2) Promote generated English pages to the site root.
for name, text in en_source.items():
    text = shift_nested_en_to_root(text)
    text = normalize_unified_switch(text, 'root', name)
    (ROOT / name).write_text(text, encoding='utf-8')

# 3) Keep /en/ as a backward-compatible alias, but point its language switch
# to the new canonical root/CZ/RU locations.
for name in root_pages:
    p = EN / name
    text = p.read_text(encoding='utf-8')
    text = normalize_unified_switch(text, 'en-alias', name)
    p.write_text(text, encoding='utf-8')

# 4) Update Czech language switches to the new English-root/Russian-/ru layout.
for name in root_pages:
    p = CZ / name
    text = p.read_text(encoding='utf-8')
    text = normalize_unified_switch(text, 'cz', name)
    p.write_text(text, encoding='utf-8')

# Hard route assertions for every published page name.
for name in root_pages:
    if not (ROOT / name).exists() or not (RU / name).exists() or not (CZ / name).exists() or not (EN / name).exists():
        raise SystemExit(f'Language route missing after promotion: {name}')

# Home pages must now clearly identify their languages.
root_home = (ROOT / 'index.html').read_text(encoding='utf-8')
ru_home = (RU / 'index.html').read_text(encoding='utf-8')
if re.search(r'<html\b[^>]*lang=["\']ru', root_home, re.I):
    raise SystemExit('Root homepage is still marked Russian after English promotion')
if not re.search(r'<html\b[^>]*lang=["\'](?:en|en-GB)', root_home, re.I):
    raise SystemExit('Root homepage is not marked English')
if not re.search(r'<html\b[^>]*lang=["\']ru', ru_home, re.I):
    raise SystemExit('/ru homepage is not marked Russian')

print(f'PASS: English promoted to root for {len(root_pages)} pages')
print(f'PASS: Russian preserved under /ru/ for {len(root_pages)} pages')
print('PASS: Czech remains under /cz/ and /en/ remains as backward-compatible English alias')
