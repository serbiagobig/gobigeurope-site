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
        'international.html': 'Международное развитие',
        'digital-ai.html': 'Цифровизация и ИИ',
        'education-hr.html': 'Обучение и HR',
        'projects.html': 'Проекты',
        'blog.html': 'Блог',
        'contact': 'Контакты',
        'back': 'Назад',
        'open': 'Открыть меню',
        'close': 'Закрыть меню',
        'nav': 'Основная навигация',
    },
    'en': {
        'international.html': 'International Development',
        'digital-ai.html': 'Digital & AI',
        'education-hr.html': 'Learning & HR',
        'projects.html': 'Projects',
        'blog.html': 'Insights',
        'contact': 'Contacts',
        'back': 'Back',
        'open': 'Open menu',
        'close': 'Close menu',
        'nav': 'Main navigation',
    },
    'cz': {
        'international.html': 'Mezinárodní rozvoj',
        'digital-ai.html': 'Digitalizace a AI',
        'education-hr.html': 'Vzdělávání a HR',
        'projects.html': 'Projekty',
        'blog.html': 'Novinky',
        'contact': 'Kontakty',
        'back': 'Zpět',
        'open': 'Otevřít menu',
        'close': 'Zavřít menu',
        'nav': 'Hlavní navigace',
    },
}

NAV_PAGES = ['international.html', 'digital-ai.html', 'education-hr.html', 'projects.html', 'blog.html']
BACK_PAGES = {
    'projects.html': 'index.html',
    'agro-tag.html': 'projects.html',
    'agro-tag-contact.html': 'agro-tag.html',
}


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


def nav_links(lang, page, css_class):
    labels = LABELS[lang]
    active = current_nav_page(page)
    links = []
    for target in NAV_PAGES:
        current = ' aria-current="page"' if target == active else ''
        links.append(f'<a class="{css_class}" href="{target}"{current}>{labels[target]}</a>')
    links.append(f'<a class="{css_class} site-contact-link" href="international.html#application">{labels["contact"]}</a>')
    return ''.join(links)


def language_links(lang, page, css_class):
    links = []
    for code, text in [('en', 'EN'), ('cz', 'CZ'), ('ru', 'RU')]:
        href = language_page_href(lang, code, page)
        current = ' aria-current="page"' if code == lang else ''
        links.append(f'<a class="{css_class}" href="{href}"{current}>{text}</a>')
    return ''.join(links)


def universal_markup(lang, page):
    labels = LABELS[lang]
    desktop = (
        f'<nav class="site-universal-nav" aria-label="{labels["nav"]}">'
        f'<div class="site-universal-links">{nav_links(lang, page, "site-universal-link")}</div>'
        f'<div class="site-universal-langs">{language_links(lang, page, "site-universal-lang")}</div>'
        '</nav>'
    )
    mobile = (
        f'<button class="site-mobile-toggle" type="button" aria-expanded="false" aria-controls="site-mobile-nav" '
        f'aria-label="{labels["open"]}" data-open-label="{labels["open"]}" data-close-label="{labels["close"]}">'
        '<span class="site-mobile-toggle-box"><span></span></span>'
        '</button>'
        '<div class="site-mobile-nav" id="site-mobile-nav">'
        f'<div class="site-mobile-links">{nav_links(lang, page, "site-mobile-link")}</div>'
        f'<div class="site-mobile-langs">{language_links(lang, page, "site-mobile-lang")}</div>'
        '</div>'
    )
    return desktop + mobile


def back_markup(lang, page):
    if page not in BACK_PAGES:
        return ''
    label = LABELS[lang]['back']
    fallback = BACK_PAGES[page]
    return (
        '<div class="site-context-back-wrap">'
        f'<a class="site-context-back" href="{fallback}" data-site-back="true">← {label}</a>'
        '</div>'
    )


def fallback_header(markup):
    return (
        '<header class="site-universal-shell">'
        '<div class="site-universal-shell-head">'
        '<a class="site-universal-shell-brand" href="index.html">'
        '<span class="site-universal-shell-mark"></span>'
        '<span><strong>GO BIG</strong><small>žádné omezení</small></span>'
        '</a>'
        + markup +
        '</div>'
        '</header>'
    )


def inject_file(path, lang, page):
    text = path.read_text(encoding='utf-8')

    css_href = 'assets/universal-mobile-nav.css?v=20260902-4' if lang == 'ru' else '../assets/universal-mobile-nav.css?v=20260902-4'
    js_src = 'assets/universal-mobile-nav.js?v=20260902-4' if lang == 'ru' else '../assets/universal-mobile-nav.js?v=20260902-4'
    css_tag = f'<link id="universal-mobile-nav-css" rel="stylesheet" href="{css_href}"/>'
    js_tag = f'<script id="universal-mobile-nav-js" src="{js_src}" defer></script>'

    if 'id="universal-mobile-nav-css"' not in text:
        if '</head>' not in text:
            raise SystemExit(f'Cannot inject universal navigation assets: {path} has no </head>')
        text = text.replace('</head>', css_tag + '\n' + js_tag + '\n</head>', 1)

    markup = universal_markup(lang, page)
    brand_match = re.search(
        r'(<header\b.*?<div\b[^>]*class=["\'][^"\']*\bhead\b[^"\']*["\'][^>]*>.*?</a>)',
        text,
        flags=re.S | re.I,
    )
    if brand_match:
        insert_at = brand_match.end(1)
        text = text[:insert_at] + markup + text[insert_at:]
    else:
        shell = fallback_header(markup)
        if re.search(r'<body\b[^>]*>', text, flags=re.I):
            text = re.sub(r'(<body\b[^>]*>)', r'\1' + shell, text, count=1, flags=re.I)
        else:
            raise SystemExit(f'Cannot locate <body> in {path}')

    back = back_markup(lang, page)
    if back:
        # Insert immediately after the first header so the return path is obvious on desktop and mobile.
        text = re.sub(r'(</header>)', r'\1' + back, text, count=1, flags=re.I)

    path.write_text(text, encoding='utf-8')


for lang, folder in [('ru', ROOT), ('en', ROOT / 'en'), ('cz', ROOT / 'cz')]:
    for page in PAGES:
        path = folder / page
        if not path.exists():
            raise SystemExit(f'Missing page for universal nav injection: {path}')
        inject_file(path, lang, page)
        print(f'Injected universal desktop/mobile nav: {lang}/{page}')
