#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

FIXES = {
    'en': {
        'Открыть countriesицу механизированной уборки ягод': 'Open the mechanised berry harvesting page',
        'Открыть страницу механизированной уборки ягод': 'Open the mechanised berry harvesting page',
        'Growth агропромышленного проекта': 'Growth of an agro-industrial project',
        'Комплексная работа с инфраструктурой, переработкой, технологическими партнёрами и развитием агробизнеса.': 'Integrated work with infrastructure, processing, technology partners and agribusiness development.',
        'Инфраструктура · переработка · партнёрство': 'Infrastructure · processing · partnership',
        'Partners · локализация · продвижение': 'Partners · localisation · promotion',
        'Меню': 'Menu',
    },
    'cz': {
        'Открыть zemíицу механизированной уборки ягод': 'Otevřít stránku mechanizované sklizně bobulovin',
        'Открыть страницу механизированной уборки ягод': 'Otevřít stránku mechanizované sklizně bobulovin',
        'Rozvoj агропромышленного проекта': 'Rozvoj agroprůmyslového projektu',
        'Комплексная работа с инфраструктурой, переработкой, технологическими партнёрами и развитием агробизнеса.': 'Komplexní práce s infrastrukturou, zpracováním, technologickými partnery a rozvojem agropodnikání.',
        'Инфраструктура · переработка · партнёрство': 'Infrastruktura · zpracování · partnerství',
        'Partneři · локализация · продвижение': 'Partneři · lokalizace · propagace',
        'Меню': 'Menu',
    },
}

for lang, fixes in FIXES.items():
    for path in (ROOT / lang).glob('*.html'):
        text = path.read_text(encoding='utf-8')
        for src, dst in fixes.items():
            text = text.replace(src, dst)
        path.write_text(text, encoding='utf-8')

print('Fixed known EN/CZ runtime language contamination.')
