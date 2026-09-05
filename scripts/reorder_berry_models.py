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

gentle_re = re.compile(r'<section class="section soft gentle-crops">.*?</section>', re.S)
models_re = re.compile(r'<section class="section(?: dark)?(?: models-showcase)?" id="models">.*?</section>', re.S)
gallery_re = re.compile(r'<div class="crop-gallery">.*?</div>', re.S)
preassessment_re = re.compile(r'<section class="section[^"]*"[^>]*>(?:(?!<section ).)*?<div class="geometry">.*?</section>', re.S)
transition_re = re.compile(r'<section class="section[^"]*"[^>]*>(?:(?!<section ).)*?<div class="path">.*?</section>', re.S)

RAW = 'https://raw.githubusercontent.com/serbiagobig/gobigeurope-site/main/'
IMAGES = {
    'raspberry': RAW + '%D0%9C%D0%B0%D0%BB%D0%B8%D0%BD%D0%B0-removebg-preview.png',
    'blueberry': RAW + '%D0%93%D0%BE%D0%BB%D1%83%D0%B1%D0%B8%D0%BA%D0%B0-removebg-preview.png',
    'currant': RAW + '%D0%A1%D0%BC%D0%BE%D1%80%D0%BE%D0%B4%D0%B8%D0%BD%D0%B0-removebg-preview.png',
    'blackberry': RAW + '%D0%95%D0%B6%D0%B5%D0%B2%D0%B8%D0%BA%D0%B0-removebg-preview.png',
    '500L': RAW + '%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0_500_L-removebg-preview.png',
    '500S': RAW + '%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0_500_S-removebg-preview.png',
    '600T': RAW + '%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0_600%D0%A2-removebg-preview.png',
}

BERRY_LABELS = {
    'ru': ('Малина', 'Голубика', 'Смородина', 'Ежевика'),
    'en': ('Raspberry', 'Blueberry', 'Blackcurrant', 'Blackberry'),
    'cz': ('Malina', 'Borůvka', 'Černý rybíz', 'Ostružina'),
}

MODEL_COPY = {
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
/* Exact floating berry composition from repository removebg PNGs */
.gentle-crops{position:relative!important;overflow:hidden!important;padding:58px 0 74px!important}
.gentle-crops>.wrap{position:relative!important;z-index:1!important;display:flex!important;flex-direction:column!important;min-height:560px}
.gentle-crops>.wrap>.eyebrow{order:1}.gentle-crops>.wrap>h2{order:2;max-width:980px!important}.gentle-crops>.wrap>.lead{order:3;max-width:880px!important}
.gentle-crops .crop-bridge{order:4;margin:28px 0 0!important;font:700 clamp(30px,3vw,42px)/1.05 var(--serif)!important;color:var(--navy)!important;position:relative;z-index:4;max-width:760px}
.gentle-crops .ripeness{order:5;margin-top:26px!important;position:relative!important;z-index:4!important}.gentle-crops .ripeness article{background:rgba(255,255,255,.96)!important}
.gentle-crops .crop-gallery{display:block!important;position:absolute!important;inset:0!important;margin:0!important;pointer-events:none!important;z-index:2!important}
.gentle-crops .crop-tile{position:absolute!important;display:block!important;min-height:0!important;border:0!important;background:transparent!important;box-shadow:none!important}.gentle-crops .crop-tile:after,.gentle-crops .crop-tile b{display:none!important}.gentle-crops .crop-tile img{display:block!important;width:100%!important;height:auto!important;object-fit:contain!important}
.gentle-crops .crop-tile:nth-child(1){width:138px!important;right:38px!important;top:38px!important}.gentle-crops .crop-tile:nth-child(2){width:118px!important;right:238px!important;top:205px!important}.gentle-crops .crop-tile:nth-child(3){width:150px!important;right:38px!important;top:195px!important}.gentle-crops .crop-tile:nth-child(4){width:124px!important;right:-96px!important;bottom:2px!important}
/* White image-led Air Harvester lineup */
#models.models-showcase{background:#fff!important;color:var(--navy)!important;padding:72px 0 78px!important}
#models.models-showcase .eyebrow{color:var(--green)!important;font-size:13px!important;letter-spacing:.16em!important;text-transform:uppercase}
#models.models-showcase h2{color:var(--navy)!important;margin-top:12px!important;font-size:clamp(48px,5vw,72px)!important;line-height:.98!important}
.model-lineup{display:grid;grid-template-columns:repeat(3,1fr);gap:44px;margin-top:36px;align-items:start}.model-item{min-width:0}.model-visual{height:250px;display:flex;align-items:center;justify-content:center;margin-bottom:10px}.model-visual img{display:block;max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain}.model-code{display:block;font:800 clamp(36px,3vw,48px)/1 var(--sans);letter-spacing:-.03em;color:var(--green);margin-bottom:12px}.model-name{margin:0;font:700 28px/1.08 var(--serif);color:var(--navy)}.model-copy{margin:12px 0 0;color:#667c91;font-size:15px;line-height:1.55;max-width:360px}.models-note{margin:30px 0 0;padding-top:18px;border-top:1px solid #dfe6e9;color:#536d82;font-size:15px;font-weight:600}
@media(max-width:900px){.gentle-crops>.wrap{min-height:0}.gentle-crops .crop-gallery{position:relative!important;inset:auto!important;order:5!important;display:grid!important;grid-template-columns:repeat(4,1fr)!important;gap:12px!important;margin:22px 0 8px!important}.gentle-crops .crop-tile,.gentle-crops .crop-tile:nth-child(n){position:relative!important;inset:auto!important;width:auto!important;height:110px!important;display:flex!important;align-items:center!important;justify-content:center!important}.gentle-crops .crop-tile img{max-width:100%!important;max-height:100%!important;width:auto!important;height:auto!important}.gentle-crops .ripeness{order:6!important}.model-lineup{grid-template-columns:1fr;gap:34px}.model-item{display:grid;grid-template-columns:minmax(150px,.8fr) minmax(0,1.2fr);column-gap:22px;align-items:center}.model-visual{grid-row:1/4;margin:0;height:190px}.model-code,.model-name,.model-copy{grid-column:2}}
@media(max-width:560px){.gentle-crops .crop-gallery{grid-template-columns:repeat(2,1fr)!important}.model-item{display:block}.model-visual{height:190px;margin-bottom:10px}}
'''

def gallery_html(lang):
    raspberry, blueberry, currant, blackberry = BERRY_LABELS[lang]
    return '<div class="crop-gallery">' + ''.join([
        f'<article class="crop-tile"><img src="{IMAGES["raspberry"]}" alt="{raspberry}"/></article>',
        f'<article class="crop-tile"><img src="{IMAGES["blueberry"]}" alt="{blueberry}"/></article>',
        f'<article class="crop-tile"><img src="{IMAGES["currant"]}" alt="{currant}"/></article>',
        f'<article class="crop-tile"><img src="{IMAGES["blackberry"]}" alt="{blackberry}"/></article>',
    ]) + '</div>'

def models_html(lang):
    c = MODEL_COPY[lang]
    items = ''.join(
        f'<article class="model-item"><div class="model-visual"><img src="{IMAGES[code]}" alt="Air Harvester {code}"/></div><b class="model-code">{code}</b><h3 class="model-name">{name}</h3><p class="model-copy">{desc}</p></article>'
        for code, name, desc in c['items']
    )
    return f'<section class="section models-showcase" id="models"><div class="wrap"><div class="eyebrow">{c["eyebrow"]}</div><h2>{c["title"]}</h2><div class="model-lineup">{items}</div><p class="models-note">{c["note"]}</p></div></section>'

for lang, p in paths.items():
    if not p.exists():
        raise SystemExit(f'Missing berry page: {p}')
    s = p.read_text(encoding='utf-8')

    gentle = gentle_re.search(s)
    models = models_re.search(s)
    if not gentle or not models:
        raise SystemExit(f'Required module missing in {p}')

    s, count = gallery_re.subn(gallery_html(lang), s, count=1)
    if count != 1:
        raise SystemExit(f'Crop gallery not found in {p}')

    s, count = models_re.subn(models_html(lang), s, count=1)
    if count != 1:
        raise SystemExit(f'Model section not found in {p}')

    models = models_re.search(s)
    models_block = models.group(0)
    s = s[:models.start()] + s[models.end():]
    gentle = gentle_re.search(s)
    s = s[:gentle.end()] + models_block + s[gentle.end():]

    s, removed = preassessment_re.subn('', s, count=1)
    if removed != 1:
        raise SystemExit(f'Plantation pre-assessment geometry module not found in {p}')

    s, removed_transition = transition_re.subn('', s, count=1)
    if removed_transition != 1:
        raise SystemExit(f'Mechanization transition module not found in {p}')

    s = s.replace('</style>', css + '</style>', 1)
    if 'Посмотреть характеристики' in s or 'View specifications' in s:
        raise SystemExit(f'Old model CTA remains in {p}')
    if 'class="geometry"' in s:
        raise SystemExit(f'Plantation pre-assessment geometry remains in {p}')
    if 'class="path"' in s:
        raise SystemExit(f'Mechanization transition module remains in {p}')
    p.write_text(s, encoding='utf-8')
    print(f'Rebuilt berry modules and removed geometry/transition sections: {p}')
