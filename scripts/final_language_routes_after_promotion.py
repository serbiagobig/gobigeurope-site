#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')


def expected(locale: str, name: str):
    if locale == 'root':
        return {'EN': name, 'CZ': f'cz/{name}', 'RU': f'ru/{name}'}
    if locale == 'ru':
        return {'EN': f'../{name}', 'CZ': f'../cz/{name}', 'RU': name}
    if locale == 'cz':
        return {'EN': f'../{name}', 'CZ': name, 'RU': f'../ru/{name}'}
    if locale == 'en':
        return {'EN': f'../{name}', 'CZ': f'../cz/{name}', 'RU': f'../ru/{name}'}
    raise ValueError(locale)


def set_href(anchor: str, href: str) -> str:
    if re.search(r'\bhref\s*=\s*["\']', anchor, re.I):
        return re.sub(r'(\bhref\s*=\s*["\'])[^"\']*(["\'])', rf'\g<1>{href}\g<2>', anchor, count=1, flags=re.I)
    return anchor.replace('<a', f'<a href="{href}"', 1)


def patch_labels(region: str, routes: dict, context: str) -> str:
    for label in ('EN', 'CZ', 'RU'):
        pattern = re.compile(r'<a\b[^>]*>\s*' + label + r'\s*</a>', re.I)
        matches = list(pattern.finditer(region))
        if len(matches) != 1:
            raise SystemExit(f'{context}: expected exactly one {label} link in language switch, found {len(matches)}')
        m = matches[0]
        region = region[:m.start()] + set_href(m.group(0), routes[label]) + region[m.end():]
    return region


def patch_page(path: Path, locale: str) -> bool:
    text = path.read_text(encoding='utf-8')
    routes = expected(locale, path.name)
    changed = False

    # Standard GO BIG switch. Most pages place it inside <nav>; a few approved
    # utility pages place the same switch directly in the header. Use </nav>
    # when present, otherwise the enclosing </header> as the safe region end.
    marker = re.search(r'<span\b[^>]*class=["\'][^"\']*\blang-switch\b[^"\']*["\'][^>]*>', text, re.I)
    if marker:
        nav_end = text.find('</nav>', marker.end())
        header_end = text.find('</header>', marker.end())
        ends = [x for x in (nav_end, header_end) if x >= 0]
        if not ends:
            raise SystemExit(f'{path}: lang-switch has no closing nav/header')
        region_end = min(ends)
        region = text[marker.start():region_end]
        patched = patch_labels(region, routes, str(path))
        text = text[:marker.start()] + patched + text[region_end:]
        changed = True

    # Berry page uses its own compact <nav class="langs"> switch.
    nav = re.search(r'<nav\b[^>]*class=["\'][^"\']*\blangs\b[^"\']*["\'][^>]*>.*?</nav>', text, re.S | re.I)
    if nav:
        patched = patch_labels(nav.group(0), routes, str(path))
        text = text[:nav.start()] + patched + text[nav.end():]
        changed = True

    if changed:
        path.write_text(text, encoding='utf-8')
    return changed


locales = [
    ('root', ROOT),
    ('ru', ROOT / 'ru'),
    ('cz', ROOT / 'cz'),
    ('en', ROOT / 'en'),
]
patched = 0
for locale, folder in locales:
    if not folder.exists():
        continue
    for page in sorted(folder.glob('*.html')):
        if patch_page(page, locale):
            patched += 1

# Semantic guardrail for key user-facing routes. Link existence alone is not enough:
# EN must mean the English root, RU must mean /ru/, and CZ must mean /cz/.
KEY = ['index.html','projects.html','international.html','digital-ai.html','blog.html','agro-tag.html','berry-harvesting.html']
for locale, folder in locales:
    if not folder.exists():
        continue
    for name in KEY:
        page = folder / name
        if not page.exists():
            raise SystemExit(f'Missing key locale page: {page}')
        text = page.read_text(encoding='utf-8')
        routes = expected(locale, name)
        for label, href in routes.items():
            if not re.search(r'<a\b[^>]*href=["\']' + re.escape(href) + r'["\'][^>]*>\s*' + label + r'\s*</a>', text, re.I):
                raise SystemExit(f'{page}: wrong final {label} route; expected {href}')

print(f'PASS: canonical EN / CZ / RU routes fixed after root promotion on {patched} pages')
