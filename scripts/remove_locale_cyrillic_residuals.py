#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

EN = {
    'Открыть countriesицу механизированной уборки ягод': 'Open the mechanised berry harvesting page',
    'Открыть страницу механизированной уборки ягод': 'Open the mechanised berry harvesting page',
    'Вывод компании-стартапа of Узбекистана на рынок Сербии. Специализированное ПО для управления BMS-системами зданий. Проведена экспертиза решения, найден локальный партнёр. Проект масштабируется на рынки Балкан.': 'Market entry of a technology startup from Uzbekistan into Serbia. The company develops specialised software for building BMS systems. The solution was assessed, a local partner was identified, and the project is now expanding into the Balkan markets.',
    'Вывод компании-стартапа из Узбекистана на рынок Сербии. Специализированное ПО для управления BMS-системами зданий. Проведена экспертиза решения, найден локальный партнёр. Проект масштабируется на рынки Балкан.': 'Market entry of a technology startup from Uzbekistan into Serbia. The company develops specialised software for building BMS systems. The solution was assessed, a local partner was identified, and the project is now expanding into the Balkan markets.',
    'Поиск инвестора для проекта организации удалённого доступа к лабораторному оборудованию исследовательских организаций. Цель проекта — расширить возможности европейских учёных в проведении научных исследований.': 'Investor search for a project providing remote access to laboratory equipment at research organisations. The goal is to expand the research capabilities available to European scientists.',
    'Организация международного издательского проекта по запросу сербского издательства. Международная команда экспертов и авторов готовит исторические книги для сербских читателей.': 'Organisation of an international publishing project for a Serbian publisher. An international team of experts and authors is preparing history books for Serbian readers.',
    'Комплексная работа с инфраструктурой, переработкой, технологическими партнёрами и развитием агробизнеса.': 'Integrated work with infrastructure, processing, technology partners and agribusiness development.',
    'Growth агропромышленного проекта': 'Growth of an agro-industrial project',
    'Инфраструктура · переработка · партнёрство': 'Infrastructure · processing · partnership',
    'Partners · локализация · продвижение': 'Partners · localisation · promotion',
    'Партнёры · локализация · продвижение': 'Partners · localisation · promotion',
    'Стратегия · локальные партнёры · переговоры': 'Strategy · local partners · negotiations',
    'Экспертиза · партнёр · масштабирование': 'Assessment · partner · scaling',
    'Наука · инфраструктура · удалённый доступ': 'Science · infrastructure · remote access',
    'Инвестиции · наука · инфраструктура · доступ': 'Investment · science · infrastructure · access',
    'Эксперты · авторы · локализация · издание': 'Experts · authors · localisation · publishing',
    'Выход технологического стартапа на рынок Сербии': 'Technology startup entry into the Serbian market',
    'Удалённый доступ к исследовательской инфраструктуре': 'Remote access to research infrastructure',
    'Международный книгоиздательский проект': 'International publishing project',
    'Международные издательские проекты': 'International Publishing Projects',
    'Выход на рынок Сербии': 'Entering the Serbian market',
    'Открытая лаборатория': 'Open Laboratory',
    'Открыть проект →': 'Open project →',
    'Закрыть меню': 'Close menu',
    'Открыть меню': 'Open menu',
    'Подробнее': 'Learn more',
    '← Назад': '← Back',
    'Меню': 'Menu',
}

CZ = {
    'Открыть zemíицу механизированной уборки ягод': 'Otevřít stránku mechanizované sklizně bobulovin',
    'Открыть страницу механизированной уборки ягод': 'Otevřít stránku mechanizované sklizně bobulovin',
    'Вывод компании-стартапа z Узбекистана на рынок Сербии. Специализированное ПО для управления BMS-системами зданий. Проведена экспертиза решения, найден локальный партнёр. Проект масштабируется на рынки Балкан.': 'Vstup technologického startupu z Uzbekistánu na srbský trh. Společnost vyvíjí specializovaný software pro řízení systémů BMS v budovách. Řešení bylo odborně posouzeno, byl nalezen místní partner a projekt se nyní rozšiřuje na balkánské trhy.',
    'Вывод компании-стартапа из Узбекистана на рынок Сербии. Специализированное ПО для управления BMS-системами зданий. Проведена экспертиза решения, найден локальный партнёр. Проект масштабируется на рынки Балкан.': 'Vstup technologického startupu z Uzbekistánu na srbský trh. Společnost vyvíjí specializovaný software pro řízení systémů BMS v budovách. Řešení bylo odborně posouzeno, byl nalezen místní partner a projekt se nyní rozšiřuje na balkánské trhy.',
    'Поиск инвестора для проекта организации удалённого доступа к лабораторному оборудованию исследовательских организаций. Цель проекта — расширить возможности европейских учёных в проведении научных исследований.': 'Hledání investora pro projekt vzdáleného přístupu k laboratornímu vybavení výzkumných organizací. Cílem je rozšířit možnosti evropských vědců při provádění výzkumu.',
    'Организация международного издательского проекта по запросу сербского издательства. Международная команда экспертов и авторов готовит исторические книги для сербских читателей.': 'Organizace mezinárodního vydavatelského projektu na objednávku srbského nakladatelství. Mezinárodní tým expertů a autorů připravuje historické knihy pro srbské čtenáře.',
    'Комплексная работа с инфраструктурой, переработкой, технологическими партнёрами и развитием агробизнеса.': 'Komplexní práce s infrastrukturou, zpracováním, technologickými partnery a rozvojem agropodnikání.',
    'Rozvoj агропромышленного проекта': 'Rozvoj agroprůmyslového projektu',
    'Инфраструктура · переработка · партнёрство': 'Infrastruktura · zpracování · partnerství',
    'Partneři · локализация · продвижение': 'Partneři · lokalizace · propagace',
    'Партнёры · локализация · продвижение': 'Partneři · lokalizace · propagace',
    'Стратегия · локальные партнёры · переговоры': 'Strategie · místní partneři · jednání',
    'Экспертиза · партнёр · масштабирование': 'Posouzení · partner · škálování',
    'Наука · инфраструктура · удалённый доступ': 'Věda · infrastruktura · vzdálený přístup',
    'Инвестиции · наука · инфраструктура · доступ': 'Investice · věda · infrastruktura · přístup',
    'Эксперты · авторы · локализация · издание': 'Experti · autoři · lokalizace · vydání',
    'Выход технологического стартапа на рынок Сербии': 'Vstup technologického startupu na srbský trh',
    'Удалённый доступ к исследовательской инфраструктуре': 'Vzdálený přístup k výzkumné infrastruktuře',
    'Международный книгоиздательский проект': 'Mezinárodní vydavatelský projekt',
    'Международные издательские проекты': 'Mezinárodní vydavatelské projekty',
    'Выход на рынок Сербии': 'Vstup na srbský trh',
    'Открытая лаборатория': 'Otevřená laboratoř',
    'Открыть проект →': 'Otevřít projekt →',
    'Закрыть меню': 'Zavřít menu',
    'Открыть меню': 'Otevřít menu',
    'Подробнее': 'Více informací',
    '← Назад': '← Zpět',
    'Меню': 'Menu',
}

CYR = re.compile(r'[А-Яа-яЁё]')

for lang, mapping in [('en', EN), ('cz', CZ)]:
    folder = ROOT / lang
    if not folder.exists():
        raise SystemExit(f'Missing locale folder: {folder}')
    for path in folder.glob('*.html'):
        text = path.read_text(encoding='utf-8')
        for src in sorted(mapping, key=len, reverse=True):
            text = text.replace(src, mapping[src])
        path.write_text(text, encoding='utf-8')

# The user explicitly requires no Russian text on EN/CZ pages. Validate the complete
# HTML source, including runtime-generated strings in scripts, not only visible DOM text.
failures = []
for lang in ('en', 'cz'):
    for path in sorted((ROOT / lang).glob('*.html')):
        text = path.read_text(encoding='utf-8')
        match = CYR.search(text)
        if match:
            start = max(0, match.start() - 80)
            end = min(len(text), match.start() + 180)
            failures.append(f'{path}: {text[start:end].replace(chr(10), " ")}')

if failures:
    raise SystemExit('Cyrillic remains in localized HTML source:\n' + '\n'.join(failures[:20]))

print('PASS: EN/CZ HTML source contains no Cyrillic, including runtime script strings')
