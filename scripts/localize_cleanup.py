#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

REPLACEMENTS = {
    'en': {
        'Международное сотрудничество': 'International Development',
        'Шаг ${current+1} из ${steps.length}': 'Step ${current+1} of ${steps.length}',
        'Пожалуйста, выберите хотя бы один вариант в обязательном вопросе.': 'Please select at least one option in the required question.',
        'Отправляем…': 'Sending…',
        'Не удалось отправить заявку. Пожалуйста, попробуйте ещё раз чуть позже.': 'We could not submit your enquiry. Please try again a little later.',
    },
    'cz': {
        'Международное сотрудничество': 'Mezinárodní rozvoj',
        'Шаг ${current+1} из ${steps.length}': 'Krok ${current+1} z ${steps.length}',
        'Пожалуйста, выберите хотя бы один вариант в обязательном вопросе.': 'Vyberte prosím alespoň jednu možnost v povinné otázce.',
        'Отправляем…': 'Odesíláme…',
        'Не удалось отправить заявку. Пожалуйста, попробуйте ещё раз чуть позже.': 'Poptávku se nepodařilo odeslat. Zkuste to prosím znovu později.',
    },
}

HOMEPAGE_PSEUDO_HEADING = {
    'en': 'Markets\A Technology\A People',
    'cz': 'Trhy\A Technologie\A Lidé',
}

LEGACY_LANGUAGE_LINK = re.compile(
    r'<a\b[^>]*href=["\'](?:en|cz)\.html["\'][^>]*>\s*(?:EN|CZ)\s*</a>',
    re.IGNORECASE,
)
LEGACY_LANGUAGE_HREF = re.compile(
    r'href=["\'](?:en|cz)\.html["\']',
    re.IGNORECASE,
)


def remove_legacy_language_links(text):
    text = LEGACY_LANGUAGE_LINK.sub('', text)
    text = re.sub(r'(</span>)\s*</span>(\s*</nav>)', r'\1\2', text, flags=re.IGNORECASE)
    return text


def fix_localized_runtime_paths(text):
    """Fix runtime paths inside inline JS that HTML asset rewriting does not catch."""
    text = text.replace("fetch('assets/blog-data.json'", "fetch('../assets/blog-data.json'")
    text = text.replace('fetch("assets/blog-data.json"', 'fetch("../assets/blog-data.json"')
    return text


failed = False

root_home = ROOT / 'index.html'
if root_home.exists():
    root_text = remove_legacy_language_links(root_home.read_text(encoding='utf-8'))
    root_home.write_text(root_text, encoding='utf-8')
    if LEGACY_LANGUAGE_HREF.search(root_text):
        failed = True
        print('ERROR index.html: stale en.html/cz.html language link remains')
    else:
        print('PASS index.html: language switch contains no legacy flat links')

for lang, replacements in REPLACEMENTS.items():
    folder = ROOT / lang
    for path in sorted(folder.glob('*.html')):
        text = path.read_text(encoding='utf-8')
        for source, target in replacements.items():
            text = text.replace(source, target)

        text = remove_legacy_language_links(text)
        text = fix_localized_runtime_paths(text)

        if path.name == 'index.html':
            heading = HOMEPAGE_PSEUDO_HEADING[lang]
            override = (
                '<style id="locale-home-heading">'
                f'.direction-media-copy h3::before{{content:"{heading}" !important;white-space:pre-line !important;}}'
                '</style>'
            )
            if 'id="locale-home-heading"' in text:
                text = re.sub(
                    r'<style id="locale-home-heading">.*?</style>',
                    override,
                    text,
                    count=1,
                    flags=re.S,
                )
            else:
                text = text.replace('</head>', override + '</head>', 1)

        path.write_text(text, encoding='utf-8')

        if LEGACY_LANGUAGE_HREF.search(text):
            failed = True
            print(f'ERROR {lang}/{path.name}: stale en.html/cz.html language link remains')

        if path.name == 'blog.html':
            if '../assets/blog-data.json' not in text:
                failed = True
                print(f'ERROR {lang}/{path.name}: localized blog feed path is incorrect')
            elif 'fetch(\'assets/blog-data.json\'' in text or 'fetch("assets/blog-data.json"' in text:
                failed = True
                print(f'ERROR {lang}/{path.name}: stale localized blog feed path remains')
            else:
                print(f'PASS {lang}/{path.name}: shared blog feed path resolves correctly')

        residuals = []
        for match in re.finditer(r'[А-Яа-яЁё][^<>\n]{0,160}', text):
            fragment = match.group(0).strip()
            if fragment and fragment not in residuals:
                residuals.append(fragment)
        if residuals:
            failed = True
            print(f'ERROR {lang}/{path.name}: Cyrillic remains')
            for fragment in residuals[:30]:
                print('  CYR:', fragment)
        elif not LEGACY_LANGUAGE_HREF.search(text):
            print(f'PASS {lang}/{path.name}')

if failed:
    raise SystemExit('Localisation QA failed: language links, runtime paths or untranslated text remain.')
print('Localisation QA passed: EN/CZ contain no Cyrillic text, legacy language links or broken blog feed paths.')
