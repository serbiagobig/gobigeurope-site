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


def language_page_href(lang, code, page):
    if lang == 'ru':
        return page if code == 'ru' else f'{code}/{page}'
    if lang == 'en':
        return f'../{page}' if code == 'ru' else (page if code == 'en' else f'../cz/{page}')
    return f'../{page}' if code == 'ru' else (f'../en/{page}' if code == 'en' else page)


def mobile_markup(lang, page):
    labels = LABELS[lang]
    active = current_nav_page(page)
    links = []
    for target in NAV_PAGES:
        current = ' aria-current="page"' if target == active else ''
        links.append(f'<a href="{target}"{current}>{labels[target]}</a>')

    lang_links = []
    for code, text in [('en', 'EN'), ('cz', 'CZ'), ('ru', 'RU')]:
        href = language_page_href(lang, code, page)
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


def fallback_header(lang, page, markup):
    home_href = 'index.html' if lang == 'ru' else 'index.html'
    return (
        '<header class="site-mobile-shell">'
        '<div class="site-mobile-shell-head">'
        f'<a class="site-mobile-shell-brand" href="{home_href}">'
        '<span class="site-mobile-shell-mark"></span>'
        '<span><strong>GO BIG</strong><small>žádné omezení</small></span>'
        '</a>'
        + markup +
        '</div>'
        '</header>'
    )


def inject_file(path, lang, page):
    text = path.read_text(encoding='utf-8')

    css_href = 'assets/universal-mobile-nav.css?v=20260902-2' if lang == 'ru' else '../assets/universal-mobile-nav.css?v=20260902-2'
    js_src = 'assets/universal-mobile-nav.js?v=20260902-2' if lang == 'ru' else '../assets/universal-mobile-nav.js?v=20260902-2'

    css_tag = f'<link id="universal-mobile-nav-css" rel="stylesheet" href="{css_href}"/>'
    js_tag = f'<script id="universal-mobile-nav-js" src="{js_src}" defer></script>'

    if 'id="universal-mobile-nav-css"' not in text:
        if '</head>' not in text:
            raise SystemExit(f'Cannot inject mobile-nav assets: {path} has no </head>')
        text = text.replace('</head>', css_tag + '\n' + js_tag + '\n</head>', 1)

    markup = mobile_markup(lang, page)

    brand_match = re.search(
        r'(<header\b.*?<div\b[^>]*class=["\'][^"\']*\bhead\b[^"\']*["\'][^>]*>.*?</a>)',
        text,
        flags=re.S | re.I,
    )
    if brand_match:
        insert_at = brand_match.end(1)
        text = text[:insert_at] + markup + text[insert_at:]
    else:
        shell = fallback_header(lang, page, markup)
        if re.search(r'<body\b[^>]*>', text, flags=re.I):
            text = re.sub(r'(<body\b[^>]*>)', r'\1' + shell, text, count=1, flags=re.I)
        else:
            raise SystemExit(f'Cannot locate <body> in {path}')

    path.write_text(text, encoding='utf-8')


for lang, folder in [('ru', ROOT), ('en', ROOT / 'en'), ('cz', ROOT / 'cz')]:
    for page in PAGES:
        path = folder / page
        if not path.exists():
            raise SystemExit(f'Missing page for mobile nav injection: {path}')
        inject_file(path, lang, page)
        print(f'Injected universal mobile nav: {lang}/{page}')
