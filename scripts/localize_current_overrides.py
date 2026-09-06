#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')

EN={
'Показать другие проекты':'View more projects',
'Открыть меню':'Open menu','Закрыть меню':'Close menu','Меню':'Menu','← Назад':'← Back','Назад':'Back',
'Выход технологического стартапа на рынок Сербии':'Technology startup entry into the Serbian market',
'Вывод компании-стартапа из Узбекистана на рынок Сербии. Специализированное ПО для управления BMS-системами зданий. Проведена экспертиза решения, найден локальный партнёр. Проект масштабируется на рынки Балкан.':'Market entry of a technology startup from Uzbekistan into Serbia. The company develops specialised software for building BMS systems. The solution was assessed, a local partner was identified, and the project is now expanding into the Balkan markets.',
'Экспертиза · партнёр · масштабирование':'Assessment · partner · scaling',
'Удалённый доступ к исследовательской инфраструктуре':'Remote access to research infrastructure',
'Поиск инвестора для проекта организации удалённого доступа к лабораторному оборудованию исследовательских организаций. Цель проекта — расширить возможности европейских учёных в проведении научных исследований.':'Investor search for a project providing remote access to laboratory equipment at research organisations. The goal is to expand the research capabilities available to European scientists.',
'Инвестиции · наука · инфраструктура · доступ':'Investment · science · infrastructure · access',
'Международный книгоиздательский проект':'International publishing project',
'Организация международного издательского проекта по запросу сербского издательства. Международная команда экспертов и авторов готовит исторические книги для сербских читателей.':'Organisation of an international publishing project for a Serbian publisher. An international team of experts and authors is preparing history books for Serbian readers.',
'Эксперты · авторы · локализация · издание':'Experts · authors · localisation · publishing',
'Оптимизация работы ИИ-агентов':'Optimising AI-agent operations',
'Применение решения сербского разработчика ПО в крупной биотехнологической исследовательской компании. Платформа позволяет анализировать и управлять работой ИИ-агентов, а также снижать затраты на использование токенов при их работе.':'Deployment of a Serbian software developer’s solution in a major biotechnology research company. The platform analyses and manages AI-agent operations and helps reduce token-usage costs.',
'ИИ-агенты · контроль · аналитика · экономия':'AI agents · control · analytics · savings',
'Цифровая трансформация банков Казахстана':'Digital transformation of banks in Kazakhstan',
'Вывод цифровой платформы сербского разработчика на рынок Центральной Азии. Внедрение решения на базе process mining и искусственного интеллекта в банках Казахстана для анализа и оптимизации бизнес-процессов.':'Market entry of a Serbian developer’s digital platform into Central Asia. A process-mining and AI solution is being introduced in banks in Kazakhstan to analyse and optimise business processes.',
'Process mining · AI · банки · Казахстан':'Process mining · AI · banking · Kazakhstan',
'Стратегия · локальные партнёры · переговоры':'Strategy · local partners · negotiations',
'Наука · инфраструктура · удалённый доступ':'Science · infrastructure · remote access',
'Партнёры · локализация · продвижение':'Partners · localisation · promotion',
'ИИ-агенты · аналитика · оптимизация затрат':'AI agents · analytics · cost optimisation',
'Стратегия · партнёрство · трансфер технологий':'Strategy · partnership · technology transfer',
'Инфраструктура, переработка и развитие агробизнеса.':'Infrastructure, processing and agribusiness development.',
'Инновационная технология':'Innovative technology',
}

CZ={
'Показать другие проекты':'Zobrazit další projekty',
'Открыть меню':'Otevřít menu','Закрыть меню':'Zavřít menu','Меню':'Menu','← Назад':'← Zpět','Назад':'Zpět',
'Выход технологического стартапа на рынок Сербии':'Vstup technologického startupu na srbský trh',
'Вывод компании-стартапа из Узбекистана на рынок Сербии. Специализированное ПО для управления BMS-системами зданий. Проведена экспертиза решения, найден локальный партнёр. Проект масштабируется на рынки Балкан.':'Vstup technologického startupu z Uzbekistánu na srbský trh. Společnost vyvíjí specializovaný software pro řízení systémů BMS v budovách. Řešení bylo odborně posouzeno, byl nalezen místní partner a projekt se nyní rozšiřuje na balkánské trhy.',
'Экспертиза · партнёр · масштабирование':'Posouzení · partner · škálování',
'Удалённый доступ к исследовательской инфраструктуре':'Vzdálený přístup k výzkumné infrastruktuře',
'Поиск инвестора для проекта организации удалённого доступа к лабораторному оборудованию исследовательских организаций. Цель проекта — расширить возможности европейских учёных в проведении научных исследований.':'Hledání investora pro projekt vzdáleného přístupu k laboratornímu vybavení výzkumných organizací. Cílem je rozšířit možnosti evropských vědců při provádění výzkumu.',
'Инвестиции · наука · инфраструктура · доступ':'Investice · věda · infrastruktura · přístup',
'Международный книгоиздательский проект':'Mezinárodní vydavatelský projekt',
'Организация международного издательского проекта по запросу сербского издательства. Международная команда экспертов и авторов готовит исторические книги для сербских читателей.':'Organizace mezinárodního vydavatelského projektu na objednávku srbského nakladatelství. Mezinárodní tým expertů a autorů připravuje historické knihy pro srbské čtenáře.',
'Эксперты · авторы · локализация · издание':'Experti · autoři · lokalizace · vydání',
'Оптимизация работы ИИ-агентов':'Optimalizace provozu AI agentů',
'Применение решения сербского разработчика ПО в крупной биотехнологической исследовательской компании. Платформа позволяет анализировать и управлять работой ИИ-агентов, а также снижать затраты на использование токенов при их работе.':'Nasazení řešení srbského softwarového vývojáře ve velké biotechnologické výzkumné společnosti. Platforma umožňuje analyzovat a řídit práci AI agentů a snižovat náklady na spotřebu tokenů.',
'ИИ-агенты · контроль · аналитика · экономия':'AI agenti · řízení · analytika · úspory',
'Цифровая трансформация банков Казахстана':'Digitální transformace bank v Kazachstánu',
'Вывод цифровой платформы сербского разработчика на рынок Центральной Азии. Внедрение решения на базе process mining и искусственного интеллекта в банках Казахстана для анализа и оптимизации бизнес-процессов.':'Vstup digitální platformy srbského vývojáře na trh Střední Asie. V bankách v Kazachstánu se zavádí řešení založené na process miningu a umělé inteligenci pro analýzu a optimalizaci podnikových procesů.',
'Process mining · AI · банки · Казахстан':'Process mining · AI · bankovnictví · Kazachstán',
'Стратегия · локальные партнёры · переговоры':'Strategie · místní partneři · jednání',
'Наука · инфраструктура · удалённый доступ':'Věda · infrastruktura · vzdálený přístup',
'Партнёры · локализация · продвижение':'Partneři · lokalizace · propagace',
'ИИ-агенты · аналитика · оптимизация затрат':'AI agenti · analytika · optimalizace nákladů',
'Стратегия · партнёрство · трансфер технологий':'Strategie · partnerství · transfer technologií',
'Инфраструктура, переработка и развитие агробизнеса.':'Infrastruktura, zpracování a rozvoj agropodnikání.',
'Инновационная технология':'Inovativní technologie',
}

for lang,mapping in [('en',EN),('cz',CZ)]:
    folder=ROOT/lang
    if not folder.exists():
        raise SystemExit(f'Missing locale folder: {folder}')
    for p in folder.glob('*.html'):
        s=p.read_text(encoding='utf-8')
        for src in sorted(mapping,key=len,reverse=True):
            s=s.replace(src,mapping[src])
        p.write_text(s,encoding='utf-8')

print('Applied current-project localisation overrides for EN/CZ')
