#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
CORE = ['index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html']


def switch_html(locale: str, name: str) -> str:
    if locale == 'ru':
        links = [('EN', f'en/{name}', False), ('CZ', f'cz/{name}', False), ('RU', name, True)]
    elif locale == 'en':
        links = [('EN', name, True), ('CZ', f'../cz/{name}', False), ('RU', f'../{name}', False)]
    else:
        links = [('EN', f'../en/{name}', False), ('CZ', name, True), ('RU', f'../{name}', False)]
    out = ['<span class="lang-switch">']
    for i, (label, href, current) in enumerate(links):
        if i:
            out.append('<span class="lang-sep">/</span>')
        cls = ' class="current" aria-current="page"' if current else ''
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    out.append('</span>')
    return ''.join(out)

count = 0
for locale in ('ru','en','cz'):
    folder = ROOT if locale == 'ru' else ROOT / locale
    for name in CORE:
        p = folder / name
        if not p.exists():
            continue
        s = p.read_text(encoding='utf-8')
        header = re.search(r'(<header\b[^>]*class="[^"]*gobig-unified-header[^"]*"[^>]*>.*?</header>)', s, re.S | re.I)
        if not header:
            continue
        h = header.group(1)
        nav = re.search(r'(<nav\b[^>]*class="[^"]*nav[^"]*"[^>]*>)(.*?)(</nav>)', h, re.S | re.I)
        if not nav:
            raise SystemExit(f'Missing unified nav in {p}')
        body = nav.group(2)
        marker = re.search(r'<span\b[^>]*class="[^"]*lang-switch[^"]*"[^>]*>', body, re.I)
        if not marker:
            raise SystemExit(f'Missing language switch in {p}')
        clean_body = body[:marker.start()] + switch_html(locale, name)
        new_nav = nav.group(1) + clean_body + nav.group(3)
        new_h = h[:nav.start()] + new_nav + h[nav.end():]
        s = s[:header.start()] + new_h + s[header.end():]
        p.write_text(s, encoding='utf-8')
        count += 1

# Hard assertion: each unified core header must expose exactly EN / CZ / RU once.
for locale in ('ru','en','cz'):
    folder = ROOT if locale == 'ru' else ROOT / locale
    for name in CORE:
        p = folder / name
        if not p.exists():
            continue
        s = p.read_text(encoding='utf-8')
        m = re.search(r'<header\b[^>]*gobig-unified-header[^>]*>.*?<nav\b[^>]*class="[^"]*nav[^"]*"[^>]*>(.*?)</nav>.*?</header>', s, re.S | re.I)
        if not m:
            raise SystemExit(f'Cannot validate unified header in {p}')
        labels = re.findall(r'>\s*(EN|CZ|RU)\s*</a>', m.group(1), re.I)
        if [x.upper() for x in labels] != ['EN','CZ','RU']:
            raise SystemExit(f'Duplicate or invalid language switch in {p}: {labels}')

print(f'PASS: deduplicated final EN / CZ / RU switch on {count} core pages')
