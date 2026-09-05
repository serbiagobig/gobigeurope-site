#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
paths = {
    'ru': root / 'berry-harvesting.html',
    'en': root / 'en' / 'berry-harvesting.html',
    'cz': root / 'cz' / 'berry-harvesting.html',
}

section_re = re.compile(r'<section class="section(?: dark)?" id="models">.*?</section>', re.S)
RAW = 'https://raw.githubusercontent.com/serbiagobig/gobigeurope-site/main/'
MODEL_IMAGES = {
    '500L': RAW + '%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0_500_L-removebg-preview.png',
    '500S': RAW + '%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0_500_S-removebg-preview.png',
    '600T': RAW + '%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0_600%D0%A2-removebg-preview.png',
}

copy = {
    'ru': {
        'eyebrow': 'Под масштаб плантации',
        'title': '3 Air harvester models',
        'note': 'Характеристики и стоимость предоставляются по запросу.',
        'items': [
            ('500L', 'Прицепная версия', 'Привод от ВОМ. Для хозяйств с подходящим трактором.'),
            ('500S', 'Автономная прицепная версия', 'Собственный дизельный двигатель. Больше независимости от мощности тягача.'),
            ('600T', 'Самоходная версия', 'Для крупных хозяйств и интенсивной эксплуатации.'),
        ],
    },
    'en': {
        'eyebrow': 'For every plantation scale',
        'title': '3 Air harvester models',
        'note': 'Specifications and pricing are available on request.',
        'items': [
            ('500L', 'Trailed version', 'PTO-driven. Designed for farms with a suitable tractor.'),
            ('500S', 'Autonomous trailed version', 'Own diesel engine for greater independence from tractor power.'),
            ('600T', 'Self-propelled version', 'Designed for large farms and intensive operation.'),
        ],
    },
    'cz': {
        'eyebrow': 'Podle rozsahu plantáže',
        'title': '3 Air harvester models',
        'note': 'Technické parametry a cena jsou k dispozici na vyžádání.',
        'items': [
            ('500L', 'Přívěsná verze', 'Pohon přes PTO. Pro farmy s vhodným traktorem.'),
            ('500S', 'Autonomní přívěsná verze', 'Vlastní dieselový motor. Vyšší nezávislost na výkonu traktoru.'),
            ('600T', 'Samojízdná verze', 'Pro velké farmy a intenzivní provoz.'),
        ],
    },
}

css = r'''
/* White image-led Air Harvester lineup */
#models.models-showcase{background:#fff!important;color:var(--navy)!important;padding:72px 0 78px!important}
#models.models-showcase .eyebrow{color:var(--green)!important;font-size:13px!important;letter-spacing:.16em!important;text-transform:uppercase}
#models.models-showcase h2{color:var(--navy)!important;margin-top:12px!important;font-size:clamp(48px,5vw,72px)!important;line-height:.98!important}
.model-lineup{display:grid;grid-template-columns:repeat(3,1fr);gap:42px;margin-top:38px;align-items:start}
.model-item{min-width:0}
.model-visual{height:250px;display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.model-visual img{display:block;max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}
.model-code{display:block;font:800 clamp(34px,3vw,46px)/1 var(--sans);letter-spacing:-.03em;color:var(--green);margin-bottom:12px}
.model-name{margin:0;font:700 28px/1.08 var(--serif);color:var(--navy)}
.model-copy{margin:12px 0 0;color:#667c91;font-size:15px;line-height:1.55;max-width:360px}
.models-note{margin:30px 0 0;padding-top:18px;border-top:1px solid #dfe6e9;color:#536d82;font-size:15px;font-weight:600}
@media(max-width:900px){
  #models.models-showcase{padding:56px 0 64px!important}
  .model-lineup{grid-template-columns:1fr;gap:34px;margin-top:28px}
  .model-visual{height:220px}
  .model-item{display:grid;grid-template-columns:minmax(150px,.8fr) minmax(0,1.2fr);column-gap:22px;align-items:center}
  .model-visual{grid-row:1/4;margin:0;height:190px}
  .model-code,.model-name,.model-copy{grid-column:2}
}
@media(max-width:560px){
  .model-item{display:block}
  .model-visual{height:190px;margin-bottom:10px}
}
'''

def render(lang):
    c = copy[lang]
    items = []
    for code, name, desc in c['items']:
        items.append(
            '<article class="model-item">'
            f'<div class="model-visual"><img src="{MODEL_IMAGES[code]}" alt="Air Harvester {code}"/></div>'
            f'<b class="model-code">{code}</b>'
            f'<h3 class="model-name">{name}</h3>'
            f'<p class="model-copy">{desc}</p>'
            '</article>'
        )
    return (
        '<section class="section models-showcase" id="models"><div class="wrap">'
        f'<div class="eyebrow">{c["eyebrow"]}</div>'
        f'<h2>{c["title"]}</h2>'
        f'<div class="model-lineup">{"".join(items)}</div>'
        f'<p class="models-note">{c["note"]}</p>'
        '</div></section>'
    )

for lang, p in paths.items():
    if not p.exists():
        raise SystemExit(f'Missing berry page: {p}')
    s = p.read_text(encoding='utf-8')
    s, count = section_re.subn(render(lang), s, count=1)
    if count != 1:
        raise SystemExit(f'Model section not found in {p}')
    if 'White image-led Air Harvester lineup' not in s:
        s = s.replace('</style>', css + '</style>', 1)
    if 'Посмотреть характеристики' in s or 'View specifications' in s:
        raise SystemExit(f'Old specifications CTA remains in {p}')
    p.write_text(s, encoding='utf-8')
    print(f'Rebuilt Air Harvester model lineup: {p}')
