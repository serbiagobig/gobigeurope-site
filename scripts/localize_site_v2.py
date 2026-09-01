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

# Technical and metadata strings identified by the first localisation QA pass.
EXTRA_EN = {
    'index.html': {
        'GO BIG помогает компаниям выходить на новые рынки, внедрять цифровые решения и развивать людей и команды.': 'GO BIG helps companies enter new markets, implement digital solutions and develop people and teams.',
    },
    'international.html': {
        'GO BIG помогает компаниям выходить на рынки Европы, Балкан, Центральной Азии и GCC: стратегия, партнёры, сопровождение и развитие международных связей.': 'GO BIG helps companies enter markets across Europe, the Balkans, Central Asia and the GCC through strategy, partnerships, hands-on support and international business development.',
        'Рынки и международный опыт': 'Markets and international experience',
        'Международный опыт': 'International experience',
        'Целевые рынки': 'Target markets',
        'Опыт на целевом рынке': 'Target-market experience',
        'Задача компании': 'Company objective',
        'Описание задачи': 'Objective description',
        'Готовность и ожидания': 'Readiness and expectations',
        'Стадия': 'Stage',
        'Бюджет': 'Budget',
        'Срок старта': 'Preferred start date',
        'Ожидаемая поддержка': 'Expected support',
        'Критерий успеха': 'Success criterion',
        'Документы / интеллектуальные права': 'Documents / intellectual property',
        'Готовность предоставить дополнительную информацию': 'Willingness to provide additional information',
    },
    'digital-ai.html': {
        'GO BIG соединяет задачи бизнеса и государства с цифровыми технологиями, помогает запускать пилоты, внедрять решения и масштабировать технологии на международных рынках.': 'GO BIG connects business and public-sector challenges with digital technologies, helping to launch pilots, implement solutions and scale technology internationally.',
        'Что мы делаем': 'What we do',
        'Как строится работа': 'How we work',
        'Проекты и кейсы': 'Projects and case studies',
        'цифровая%20трансформация': 'digital%20transformation',
    },
    'education-hr.html': {
        'GO BIG развивает руководителей и команды, создаёт корпоративные программы обучения, собственные методологии развития и Academy GO BIG для международного роста.': 'GO BIG develops leaders and teams, designs corporate learning programmes, proprietary development methodologies and Academy GO BIG programmes for international growth.',
        'Что мы делаем': 'What we do',
        'Имя': 'Name',
        'Интерес': 'Area of interest',
        'Задача': 'Objective',
        'Сроки': 'Timing',
    },
    'projects.html': {
        'Проекты GO BIG в международном развитии, технологической кооперации, цифровизации, AI и агротехнологиях.': 'GO BIG projects in international development, technology cooperation, digital transformation, AI and agri-technology.',
    },
    'blog.html': {
        'Новости, международные проекты, технологии и партнёрства GO BIG и TESLA Alliance.': 'News, international projects, technology and partnerships from GO BIG and TESLA Alliance.',
    },
    'agro-tag.html': {
        'AGRO TAG — международная экспортно-сервисная платформа для развития техники, технологий, сервиса и дилерской инфраструктуры на рынках Центральной Азии.': 'AGRO TAG is an international export and service platform for machinery, technology, service and dealer-network development in Central Asian markets.',
    },
    'agro-tag-contact.html': {
        'Короткая форма заявки на партнёрство с AGRO TAG для дилеров, дистрибьюторов и производителей.': 'A short AGRO TAG partnership enquiry form for dealers, distributors and manufacturers.',
        'запрос на партнёрство — ': 'partnership enquiry — ',
        'Новая заявка AGRO TAG': 'New AGRO TAG enquiry',
        'Кого представляет: ': 'Represents: ',
        'Страна / рынок: ': 'Country / market: ',
        'Интерес: ': 'Interest: ',
        'Источник: ': 'Source: ',
    },
    'readiness.html': {
        'Мы понимаем регуляторные ограничения.': 'We understand the regulatory constraints.',
    },
}

EXTRA_CZ = {
    'index.html': {
        'GO BIG помогает компаниям выходить на новые рынки, внедрять цифровые решения и развивать людей и команды.': 'GO BIG pomáhá firmám vstupovat na nové trhy, zavádět digitální řešení a rozvíjet lidi i týmy.',
    },
    'international.html': {
        'GO BIG помогает компаниям выходить на рынки Европы, Балкан, Центральной Азии и GCC: стратегия, партнёры, сопровождение и развитие международных связей.': 'GO BIG pomáhá firmám vstupovat na trhy Evropy, Balkánu, Střední Asie a zemí GCC prostřednictvím strategie, partnerství, praktické podpory a rozvoje mezinárodních obchodních vztahů.',
        'Рынки и международный опыт': 'Trhy a mezinárodní zkušenosti',
        'Международный опыт': 'Mezinárodní zkušenosti',
        'Целевые рынки': 'Cílové trhy',
        'Опыт на целевом рынке': 'Zkušenosti na cílovém trhu',
        'Задача компании': 'Záměr společnosti',
        'Описание задачи': 'Popis záměru',
        'Готовность и ожидания': 'Připravenost a očekávání',
        'Стадия': 'Fáze',
        'Бюджет': 'Rozpočet',
        'Срок старта': 'Požadovaný termín zahájení',
        'Ожидаемая поддержка': 'Očekávaná podpora',
        'Критерий успеха': 'Kritérium úspěchu',
        'Документы / интеллектуальные права': 'Dokumenty / duševní vlastnictví',
        'Готовность предоставить дополнительную информацию': 'Ochota poskytnout doplňující informace',
    },
    'digital-ai.html': {
        'GO BIG соединяет задачи бизнеса и государства с цифровыми технологиями, помогает запускать пилоты, внедрять решения и масштабировать технологии на международных рынках.': 'GO BIG propojuje potřeby firem a veřejného sektoru s digitálními technologiemi a pomáhá spouštět piloty, zavádět řešení a škálovat technologie na mezinárodních trzích.',
        'Что мы делаем': 'Co děláme',
        'Как строится работа': 'Jak pracujeme',
        'Проекты и кейсы': 'Projekty a případové studie',
        'цифровая%20трансформация': 'digitalni%20transformace',
    },
    'education-hr.html': {
        'GO BIG развивает руководителей и команды, создаёт корпоративные программы обучения, собственные методологии развития и Academy GO BIG для международного роста.': 'GO BIG rozvíjí manažery a týmy, vytváří firemní vzdělávací programy, vlastní rozvojové metodiky a programy Academy GO BIG pro mezinárodní růst.',
        'Что мы делаем': 'Co děláme',
        'Имя': 'Jméno',
        'Интерес': 'Oblast zájmu',
        'Задача': 'Záměr',
        'Сроки': 'Termín',
    },
    'projects.html': {
        'Проекты GO BIG в международном развитии, технологической кооперации, цифровизации, AI и агротехнологиях.': 'Projekty GO BIG v mezinárodním rozvoji, technologické spolupráci, digitalizaci, AI a agrotechnologiích.',
    },
    'blog.html': {
        'Новости, международные проекты, технологии и партнёрства GO BIG и TESLA Alliance.': 'Novinky, mezinárodní projekty, technologie a partnerství GO BIG a TESLA Alliance.',
    },
    'agro-tag.html': {
        'AGRO TAG — международная экспортно-сервисная платформа для развития техники, технологий, сервиса и дилерской инфраструктуры на рынках Центральной Азии.': 'AGRO TAG je mezinárodní exportní a servisní platforma pro rozvoj techniky, technologií, servisu a dealerské infrastruktury na trzích Střední Asie.',
    },
    'agro-tag-contact.html': {
        'Короткая форма заявки на партнёрство с AGRO TAG для дилеров, дистрибьюторов и производителей.': 'Krátký formulář partnerské poptávky AGRO TAG pro dealery, distributory a výrobce.',
        'запрос на партнёрство — ': 'partnerská poptávka — ',
        'Новая заявка AGRO TAG': 'Nová poptávka AGRO TAG',
        'Кого представляет: ': 'Zastupuje: ',
        'Страна / рынок: ': 'Země / trh: ',
        'Интерес: ': 'Zájem: ',
        'Источник: ': 'Zdroj: ',
    },
    'readiness.html': {
        'Мы понимаем регуляторные ограничения.': 'Rozumíme regulatorním omezením.',
    },
}


def apply_map(text, mapping):
    for source in sorted(mapping, key=len, reverse=True):
        text = text.replace(source, mapping[source])
    return text


def fix_paths(text):
    text = text.replace('src="assets/', 'src="../assets/')
    text = text.replace("src='assets/", "src='../assets/")
    text = text.replace('href="assets/', 'href="../assets/')
    text = text.replace("href='assets/", "href='../assets/")
    text = text.replace("url('assets/", "url('../assets/")
    text = text.replace('url("assets/', 'url("../assets/')
    for css in ['home-premium.css', 'international-hero.css', 'partners-ecosystem.css']:
        text = text.replace(f'href="{css}', f'href="../{css}')
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
    if lang == 'en':
        text = text.replace('https://webridge.tech/ru/academy', 'https://webridge.tech/en/academy')
        text = text.replace('https://webridge.tech/ru', 'https://webridge.tech/en')
    elif lang == 'cz':
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


def localise(filename, lang, common, page_maps, extras):
    source = ROOT / filename
    if not source.exists():
        print(f'SKIP missing {source}')
        return

    text = source.read_text(encoding='utf-8')
    merged = dict(common)
    merged.update(page_maps.get(filename, {}))
    merged.update(extras.get(filename, {}))
    text = apply_map(text, merged)
    text = re.sub(r'<html lang="[^"]+">', f'<html lang="{lang}">', text, count=1)
    text = fix_paths(text)
    text = install_switch(text, locale_switch(filename, lang))
    text = patch_locale_links(text, lang)
    # A second pass also covers strings introduced by final build/patch operations.
    text = apply_map(text, merged)

    output = ROOT / lang / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding='utf-8')

    residual = []
    for match in re.finditer(r'[А-Яа-яЁё][^<>\n]{0,140}', text):
        fragment = match.group(0).strip()
        if fragment and fragment not in residual:
            residual.append(fragment)
    if residual:
        print(f'WARNING {lang}/{filename}: {len(residual)} Cyrillic fragment(s) remain')
        for fragment in residual[:30]:
            print('  CYR:', fragment)
    else:
        print(f'OK {lang}/{filename}: no Cyrillic text remains')


patch_root_switches()
for filename in PAGES:
    localise(filename, 'en', COMMON_EN, EN, EXTRA_EN)
    localise(filename, 'cz', COMMON_CZ, CZ, EXTRA_CZ)

print('English (UK) and Czech site versions generated.')
