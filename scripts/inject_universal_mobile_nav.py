#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
PAGES = [
    'index.html', 'international.html', 'digital-ai.html', 'education-hr.html',
    'projects.html', 'blog.html', 'agro-tag.html', 'agro-tag-contact.html',
    'readiness.html'
]

LABELS = {
    'ru': {
        'international.html': 'Международное сотрудничество',
        'digital-ai.html': 'Цифровизация и ИИ',
        'education-hr.html': 'Образование и HR',
        'projects.html': 'Проекты',
        'blog.html': 'Блог',
        'cta': 'Обсудить задачу',
        'open': 'Открыть меню',
    },
    'en': {
        'international.html': 'International Development',
        'digital-ai.html': 'Digital & AI',
        'education-hr.html': 'Education & HR',
        'projects.html': 'Projects',
        'blog.html': 'Blog',
        'cta': 'Discuss your project',
        'open': 'Open menu',
    },
    'cz': {
        'international.html': 'Mezinárodní rozvoj',
        'digital-ai.html': 'Digitalizace a AI',
        'education-hr.html': 'Vzdělávání a HR',
        'projects.html': 'Projekty',
        'blog.html': 'Blog',
        'cta': 'Probrat váš záměr',
        'open': 'Otevřít menu',
    },
}

NAV_PAGES = ['international.html', 'digital-ai.html', 'education-hr.html', 'projects.html', 'blog.html']


def current_nav_page(page):
    if page in NAV_PAGES:
        return page
    if page in {'agro-tag.html', 'agro-tag-contact.html', 'readiness.html'}:
        return 'international.html'
    return None


def mobile_markup(lang, page):
    labels = LABELS[lang]
    active = current_nav_page(page)
    links = []
    for target in NAV_PAGES:
        current = ' aria-current="page"' if target == active else ''
        links.append(f'<a href="{target}"{current}>{labels[target]}</a>')

    lang_links = []
    for code, folder, text in [('ru', '..' if lang != 'ru' else '', 'RU'), ('en', '../en' if lang != 'en' else '', 'EN'), ('cz', '../cz' if lang != 'cz' else '', 'CZ')]:
        if lang == 'ru':
            href = page if code == 'ru' else f'{code}/{page}'
        elif lang == 'en':
            href = f'../{page}' if code == 'ru' else (page if code == 'en' else f'../cz/{page}')
        else:
            href = f'../{page}' if code == 'ru' else (f'../en/{page}' if code == 'en' else page)
        current = ' aria-current="page"' if code == lang else ''
        lang_links.append(f'<a href="{href}"{current}>{text}</a>')

    return (
        f'<button class="site-mobile-toggle" type="button" aria-expanded="false" aria-controls="site-mobile-nav" aria-label="{labels["open"]}">'
        '<span class="site-mobile-toggle-box"><span></span></span>'
        '</button>'
        '<div class="site-mobile-nav" id="site-mobile-nav">'
        '<div class="site-mobile-links">' + ''.join(links) + '</div>'
        f'<a class="site-mobile-cta" href="international.html#application">{labels["cta"]}</a>'
        '<div class="site-mobile-langs">' + ''.join(lang_links) + '</div>'
        '</div>'
    )


def inject_file(path, lang, page):
    text = path.read_text(encoding='utf-8')

    css_href = 'assets/universal-mobile-nav.css?v=20260902-1' if lang == 'ru' else '../assets/universal-mobile-nav.css?v=20260902-1'
    js_src = 'assets/universal-mobile-nav.js?v=20260902-1' if lang == 'ru' else '../assets/universal-mobile-nav.js?v=20260902-1'

    css_tag = f'<link id="universal-mobile-nav-css" rel="stylesheet" href="{css_href}"/>'
    js_tag = f'<script id="universal-mobile-nav-js" src="{js_src}" defer></script>'

    if 'id="universal-mobile-nav-css"' not in text:
        text = text.replace('</head>', css_tag + '\n' + js_tag + '\n</head>', 1)

    # Remove an older injected version if the script is re-run.
    text = re.sub(r'<button class="site-mobile-toggle".*?</div>\s*</div>', '', text, flags=re.S)

    markup = mobile_markup(lang, page)

    # Insert into the header's .head container immediately after the brand.
    brand_match = re.search(r'(<header\b.*?<div\b[^>]*class=["\'][^"\']*\bhead\b[^"\']*["\'][^>]*>.*?</a>)', text, flags=re.S | re.I)
    if not brand_match:
        raise SystemExit(f'Cannot locate header brand in {path}')
    insert_at = brand_match.end(1)
    text = text[:insert_at] + markup + text[insert_at:]

    path.write_text(text, encoding='utf-8')


for lang, folder in [('ru', ROOT), ('en', ROOT / 'en'), ('cz', ROOT / 'cz')]:
    for page in PAGES:
        path = folder / page
        if not path.exists():
            raise SystemExit(f'Missing page for mobile nav injection: {path}')
        inject_file(path, lang, page)
        print(f'Injected universal mobile nav: {lang}/{page}')
