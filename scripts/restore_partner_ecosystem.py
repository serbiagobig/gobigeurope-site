#!/usr/bin/env python3
from pathlib import Path

ROOT = Path('dist')

# The approved ecosystem consists of three CSS layers:
# 1) layout/interaction, 2) full institution lists, 3) technology ecosystem lists.
base_css = Path('partners-ecosystem.css')
if not base_css.exists():
    raise SystemExit('Missing authoritative partners-ecosystem.css')
(ROOT / 'partners-ecosystem.css').write_text(base_css.read_text(encoding='utf-8'), encoding='utf-8')

required_assets = [
    ROOT / 'assets' / 'partners-ecosystem-locales.css',
    ROOT / 'assets' / 'technology-ecosystem-locales.css',
]
for asset in required_assets:
    if not asset.exists() or asset.stat().st_size < 1000:
        raise SystemExit(f'Missing ecosystem data layer: {asset}')

# RU is always present. EN/CZ are patched too whenever the full localized routes exist.
targets = [
    (ROOT / 'international.html', '', 'assets'),
    (ROOT / 'en' / 'international.html', '../', '../assets'),
    (ROOT / 'cz' / 'international.html', '../', '../assets'),
]

for page, base_prefix, asset_prefix in targets:
    if not page.exists():
        continue
    s = page.read_text(encoding='utf-8')
    if '<section class="partners"' not in s:
        raise SystemExit(f'Partner ecosystem section missing in {page}')

    tags = [
        f'<link id="partners-ecosystem-layout" rel="stylesheet" href="{base_prefix}partners-ecosystem.css?v=20260906-restore"/>',
        f'<link id="partners-ecosystem-locales" rel="stylesheet" href="{asset_prefix}/partners-ecosystem-locales.css?v=20260906-restore"/>',
        f'<link id="technology-ecosystem-locales" rel="stylesheet" href="{asset_prefix}/technology-ecosystem-locales.css?v=20260906-restore"/>',
    ]
    for tag in tags:
        tag_id = tag.split('id="',1)[1].split('"',1)[0]
        if f'id="{tag_id}"' not in s:
            if '</head>' not in s:
                raise SystemExit(f'No </head> in {page}')
            s = s.replace('</head>', tag + '\n</head>', 1)

    # Hard validation: all three layers must remain linked after every build.
    for marker in ('partners-ecosystem.css','partners-ecosystem-locales.css','technology-ecosystem-locales.css'):
        if marker not in s:
            raise SystemExit(f'Ecosystem stylesheet link missing in {page}: {marker}')

    page.write_text(s, encoding='utf-8')
    print(f'Restored complete partner ecosystem layers: {page}')

# Validate the approved RU content source itself, so truncated institution lists cannot silently ship.
partner_data = (ROOT/'assets/partners-ecosystem-locales.css').read_text(encoding='utf-8')
tech_data = (ROOT/'assets/technology-ecosystem-locales.css').read_text(encoding='utf-8')
required_ru = [
    'Факультет технических наук Университета Нови-Сада',
    'Факультет сельскохозяйственных наук Университета Нови-Сада',
    'Казахский национальный университет имени аль-Фараби',
    'Торгово-промышленная палата Воеводины',
    'Торгово-промышленная палата Республики Сербской',
    'Наманганское региональное управление',
]
required_tech = [
    'Научно-технологический парк Нови-Сад',
    'Научно-технологический парк Чачак',
    'Научно-технологический парк Республики Сербской',
    'Ассоциация фермеров Казахстана',
    'Национальный инфраструктурный проект «Туран»',
    'Кыргыз ТехноВумен',
]
for item in required_ru:
    if item not in partner_data:
        raise SystemExit(f'Approved ecosystem institution missing: {item}')
for item in required_tech:
    if item not in tech_data:
        raise SystemExit(f'Approved technology ecosystem institution missing: {item}')

print('Partner ecosystem content guardrails passed')
