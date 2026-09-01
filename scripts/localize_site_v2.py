#!/usr/bin/env python3
from pathlib import Path
import ast
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
SOURCE = Path(__file__).with_name('localize_site.py')
PAGES = [
    'index.html', 'international.html', 'digital-ai.html', 'education-hr.html',
    'projects.html', 'blog.html', 'agro-tag.html', 'agro-tag-contact.html',
    'readiness.html'
]


def load_dictionary(name):
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise RuntimeError(f'Dictionary {name} not found in {SOURCE}')


COMMON_EN = load_dictionary('COMMON_EN')
COMMON_CZ = load_dictionary('COMMON_CZ')
EN = load_dictionary('EN')
CZ = load_dictionary('CZ')


def apply_map(text, mapping):
    # Longest source strings first. This prevents short navigation words such as
    # “Проекты” or “Сервис” from breaking longer, page-specific translations.
    for source in sorted(mapping, key=len, reverse=True):
        text = text.replace(source, mapping[source])
    return text


def fix_paths(text):
    # Localised pages live one directory below the Russian master pages.
    text = text.replace('src="assets/', 'src="../assets/')
    text = text.replace("src='assets/", "src='../assets/")
    text = text.replace('href="assets/', 'href="../assets/')
    text = text.replace("href='assets/", "href='../assets/")
    text = text.replace("url('assets/", "url('../assets/")
    text = text.replace('url("assets/', 'url("../assets/')
    for css in ['home-premium.css', 'international-hero.css', 'partners-ecosystem.css']:
        text = text.replace(f'href="{css}', f'href="../{css}')
    # Root image references that are not already relative/absolute URLs.
    text = re.sub(
        r'(src=["\'])(?!https?://|data:|/|\.\./)([^/"\']+\.(?:png|jpe?g|webp|svg))',
        r'\1../\2', text, flags=re.I
    )
    return text


def root_switch(filename):
    return (
        '<span class="lang-switch" style="font-size:12px;white-space:nowrap;color:#74808d">'
        f'<a href="{filename}" aria-current="page">RU</a>&nbsp;&nbsp;/&nbsp;&nbsp;'
        f'<a href="en/{filename}">EN</a>&nbsp;&nbsp;/&nbsp;&nbsp;'
        f'<a href="cz/{filename}">CZ</a></span>'
    )


def locale_switch(filename, lang):
    if lang == 'en':
        return (
            '<span class="lang-switch" style="font-size:12px;white-space:nowrap;color:#74808d">'
            f'<a href="../{filename}">RU</a>&nbsp;&nbsp;/&nbsp;&nbsp;'
            f'<a href="{filename}" aria-current="page">EN</a>&nbsp;&nbsp;/&nbsp;&nbsp;'
            f'<a href="../cz/{filename}">CZ</a></span>'
        )
    return (
        '<span class="lang-switch" style="font-size:12px;white-space:nowrap;color:#74808d">'
        f'<a href="../{filename}">RU</a>&nbsp;&nbsp;/&nbsp;&nbsp;'
        f'<a href="../en/{filename}">EN</a>&nbsp;&nbsp;/&nbsp;&nbsp;'
        f'<a href="{filename}" aria-current="page">CZ</a></span>'
    )


def install_switch(text, switch):
    if 'class="lang-switch"' in text:
        return re.sub(
            r'<span class="lang-switch"[^>]*>.*?</span>', switch, text,
            count=1, flags=re.S
        )
    if '</nav>' in text:
        return text.replace('</nav>', switch + '</nav>', 1)
    if '</header>' in text:
        return text.replace('</header>', switch + '</header>', 1)
    return text


def patch_locale_links(text, lang):
    # Internal page-to-page links should stay inside the selected language.
    for page in PAGES:
        text = text.replace(f'href="{page}', f'href="{page}')
    if lang == 'en':
        text = text.replace('https://webridge.tech/ru/academy', 'https://webridge.tech/en/academy')
        text = text.replace('https://webridge.tech/ru', 'https://webridge.tech/en')
    elif lang == 'cz':
        # WE BRIDGE currently has no Czech route; use its English international page.
        text = text.replace('https://webridge.tech/ru/academy', 'https://webridge.tech/en/academy')
        text = text.replace('https://webridge.tech/ru', 'https://webridge.tech/en')
    return text


def patch_root_switches():
    for filename in PAGES:
        path = ROOT / filename
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        text = install_switch(text, root_switch(filename))
        path.write_text(text, encoding='utf-8')


def localise(filename, lang, common, page_maps):
    source = ROOT / filename
    if not source.exists():
        print(f'SKIP missing {source}')
        return

    text = source.read_text(encoding='utf-8')
    merged = dict(common)
    merged.update(page_maps.get(filename, {}))
    text = apply_map(text, merged)
    text = re.sub(r'<html lang="[^"]+">', f'<html lang="{lang}">', text, count=1)
    text = fix_paths(text)
    text = install_switch(text, locale_switch(filename, lang))
    text = patch_locale_links(text, lang)

    output = ROOT / lang / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding='utf-8')

    # Report actual Cyrillic fragments so the CI log can be used as a QA pass.
    residual = []
    for match in re.finditer(r'[А-Яа-яЁё][^<>\n]{0,140}', text):
        fragment = match.group(0).strip()
        if fragment and fragment not in residual:
            residual.append(fragment)
    if residual:
        print(f'WARNING {lang}/{filename}: {len(residual)} Cyrillic fragment(s) remain')
        for fragment in residual[:25]:
            print('  CYR:', fragment)
    else:
        print(f'OK {lang}/{filename}: no Cyrillic text remains')


patch_root_switches()
for filename in PAGES:
    localise(filename, 'en', COMMON_EN, EN)
    localise(filename, 'cz', COMMON_CZ, CZ)

print('English (UK) and Czech site versions generated.')
