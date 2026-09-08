#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

COPY = {
    'ru': {
        'title': 'Каталоги производителей',
        'lead': 'Каталоги производителей сельскохозяйственной техники и оборудования, представленных в экосистеме AGRO TAG.',
        'manufacturer': 'Производитель',
        'open': 'Открыть каталог ↗',
        'soon': 'Скоро',
    },
    'en': {
        'title': 'Manufacturer catalogues',
        'lead': 'Manufacturer catalogues for agricultural machinery and equipment represented in the AGRO TAG ecosystem.',
        'manufacturer': 'Manufacturer',
        'open': 'Open catalogue ↗',
        'soon': 'Coming soon',
    },
    'cz': {
        'title': 'Katalogy výrobců',
        'lead': 'Katalogy výrobců zemědělské techniky a zařízení zastoupených v ekosystému AGRO TAG.',
        'manufacturer': 'Výrobce',
        'open': 'Otevřít katalog ↗',
        'soon': 'Připravujeme',
    },
}

STYLE = r'''
<style id="manufacturer-catalogs-style-v1">
.manufacturer-catalogs{padding:58px 0 66px;background:#fff;border-top:1px solid rgba(72,105,133,.10)}
.manufacturer-catalogs .catalog-head{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:46px;align-items:end;margin-bottom:24px}
.manufacturer-catalogs h2{margin:0;color:var(--deep);font:700 clamp(34px,3.6vw,50px)/1 var(--serif);letter-spacing:-.03em}
.manufacturer-catalogs .catalog-lead{margin:0;max-width:650px;color:#667786;font-size:15px;line-height:1.65}
.manufacturer-catalogs .catalog-list{border-top:1px solid rgba(72,105,133,.16)}
.manufacturer-catalogs .catalog-row{min-height:66px;display:grid;grid-template-columns:58px minmax(0,1fr) auto;gap:18px;align-items:center;border-bottom:1px solid rgba(72,105,133,.14)}
.manufacturer-catalogs .catalog-no{color:var(--blue);font-size:15px;font-weight:800;letter-spacing:.12em}
.manufacturer-catalogs .catalog-name{color:var(--deep);font-size:16px;font-weight:750}
.manufacturer-catalogs .catalog-state{justify-self:end;font-size:13px;font-weight:800;white-space:nowrap}
.manufacturer-catalogs .catalog-state.active{color:var(--green)}
.manufacturer-catalogs .catalog-state.soon{color:#9aa5af;font-weight:700}
@media(max-width:700px){
 .manufacturer-catalogs{padding:46px 0 52px}
 .manufacturer-catalogs .catalog-head{grid-template-columns:1fr;gap:14px;margin-bottom:18px}
 .manufacturer-catalogs .catalog-row{grid-template-columns:42px minmax(0,1fr);gap:12px;padding:14px 0}
 .manufacturer-catalogs .catalog-state{grid-column:2;justify-self:start;margin-top:-4px;white-space:normal}
}
</style>
'''

def section(lang):
    t = COPY[lang]
    rows = []
    for i in range(1, 6):
        state_class = 'active' if i <= 2 else 'soon'
        state_text = t['open'] if i <= 2 else t['soon']
        rows.append(
            f'<div class="catalog-row" data-manufacturer="{i}" data-catalog-ready="{"true" if i <= 2 else "false"}">'
            f'<span class="catalog-no">{i:02d}</span>'
            f'<span class="catalog-name">{t["manufacturer"]} {i}</span>'
            f'<span class="catalog-state {state_class}">{state_text}</span>'
            '</div>'
        )
    return (
        '<section class="manufacturer-catalogs" id="manufacturer-catalogs">'
        '<div class="wrap">'
        '<div class="catalog-head">'
        f'<h2>{t["title"]}</h2>'
        f'<p class="catalog-lead">{t["lead"]}</p>'
        '</div>'
        '<div class="catalog-list">' + ''.join(rows) + '</div>'
        '</div></section>'
    )

pages = [
    ('ru', ROOT / 'agro-tag.html'),
    ('en', ROOT / 'en' / 'agro-tag.html'),
    ('cz', ROOT / 'cz' / 'agro-tag.html'),
]

for lang, page in pages:
    if not page.exists():
        raise SystemExit(f'Missing AGRO TAG page: {page}')
    s = page.read_text(encoding='utf-8')

    # Remove an older generated copy if this script runs more than once.
    s = re.sub(r'<section class="manufacturer-catalogs".*?</section>', '', s, count=1, flags=re.S)
    s = re.sub(r'<style id="manufacturer-catalogs-style-v1">.*?</style>', '', s, count=1, flags=re.S)

    marker = re.search(r'(<section class="products"\b.*?</section>)', s, re.S)
    if not marker:
        raise SystemExit(f'Products section not found in {page}')

    block = marker.group(1) + '\n' + section(lang)
    s = s[:marker.start()] + block + s[marker.end():]
    s = s.replace('</head>', STYLE + '\n</head>', 1)

    # Guardrails: exactly one catalog subsection, five rows, first two open, last three future.
    if s.count('class="manufacturer-catalogs"') != 1:
        raise SystemExit(f'Catalog subsection duplication in {page}')
    if s.count('class="catalog-row"') != 5:
        raise SystemExit(f'Catalog row count is not five in {page}')
    if s.count('data-catalog-ready="true"') != 2 or s.count('data-catalog-ready="false"') != 3:
        raise SystemExit(f'Catalog readiness state invalid in {page}')

    page.write_text(s, encoding='utf-8')
    print(f'Added manufacturer catalog subsection: {page}')

print('PASS: manufacturer catalog subsection added without changing product cards')
