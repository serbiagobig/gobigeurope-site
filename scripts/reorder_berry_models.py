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
models_re = re.compile(r'<section class="section dark" id="models">.*?</section>', re.S)
gallery_re = re.compile(r'<div class="crop-gallery">.*?</div>', re.S)

RAW = 'https://raw.githubusercontent.com/serbiagobig/gobigeurope-site/main/'
IMAGES = {
    'raspberry': RAW + '%D0%9C%D0%B0%D0%BB%D0%B8%D0%BD%D0%B0-removebg-preview.png',
    'blueberry': RAW + '%D0%93%D0%BE%D0%BB%D1%83%D0%B1%D0%B8%D0%BA%D0%B0-removebg-preview.png',
    'currant': RAW + '%D0%A1%D0%BC%D0%BE%D1%80%D0%BE%D0%B4%D0%B8%D0%BD%D0%B0-removebg-preview.png',
    'blackberry': RAW + '%D0%95%D0%B6%D0%B5%D0%B2%D0%B8%D0%BA%D0%B0-removebg-preview.png',
}
LABELS = {
    'ru': ('Малина', 'Голубика', 'Смородина', 'Ежевика'),
    'en': ('Raspberry', 'Blueberry', 'Blackcurrant', 'Blackberry'),
    'cz': ('Malina', 'Borůvka', 'Černý rybíz', 'Ostružina'),
}

layout_css = r'''
/* Exact floating berry composition from repository removebg PNGs */
.gentle-crops{position:relative!important;overflow:hidden!important;padding:58px 0 74px!important}
.gentle-crops>.wrap{position:relative!important;z-index:1!important;display:flex!important;flex-direction:column!important;min-height:560px}
.gentle-crops>.wrap>.eyebrow{order:1}
.gentle-crops>.wrap>h2{order:2;max-width:980px!important}
.gentle-crops>.wrap>.lead{order:3;max-width:880px!important}
.gentle-crops .crop-bridge{order:4;margin:28px 0 0!important;font:700 clamp(30px,3vw,42px)/1.05 var(--serif)!important;color:var(--navy)!important;position:relative;z-index:4;max-width:760px}
.gentle-crops .ripeness{order:5;margin-top:26px!important;position:relative!important;z-index:4!important;max-width:100%!important}
.gentle-crops .ripeness article{background:rgba(255,255,255,.96)!important;backdrop-filter:blur(2px)}
.gentle-crops .crop-gallery{display:block!important;position:absolute!important;inset:0!important;margin:0!important;pointer-events:none!important;z-index:2!important}
.gentle-crops .crop-tile{position:absolute!important;display:block!important;min-height:0!important;width:auto!important;height:auto!important;border:0!important;border-radius:0!important;overflow:visible!important;background:transparent!important;box-shadow:none!important}
.gentle-crops .crop-tile:after{display:none!important}
.gentle-crops .crop-tile b{display:none!important}
.gentle-crops .crop-tile img{position:static!important;display:block!important;width:100%!important;height:auto!important;object-fit:contain!important;filter:none!important}
/* 1 Raspberry: upper-right */
.gentle-crops .crop-tile:nth-child(1){width:138px!important;right:38px!important;top:38px!important;left:auto!important;bottom:auto!important}
/* 2 Blueberry: center-right, between intro and cards */
.gentle-crops .crop-tile:nth-child(2){width:118px!important;right:238px!important;top:205px!important;left:auto!important;bottom:auto!important}
/* 3 Blackcurrant: right-middle */
.gentle-crops .crop-tile:nth-child(3){width:150px!important;right:38px!important;top:195px!important;left:auto!important;bottom:auto!important}
/* 4 Blackberry: pushed farther right, close to module edge */
.gentle-crops .crop-tile:nth-child(4){width:124px!important;right:-96px!important;bottom:2px!important;left:auto!important;top:auto!important}
@media(max-width:1180px){
  .gentle-crops>.wrap{min-height:600px}
  .gentle-crops .crop-tile:nth-child(1){width:118px!important;right:10px!important;top:48px!important}
  .gentle-crops .crop-tile:nth-child(2){width:100px!important;right:175px!important;top:225px!important}
  .gentle-crops .crop-tile:nth-child(3){width:128px!important;right:8px!important;top:218px!important}
  .gentle-crops .crop-tile:nth-child(4){width:108px!important;right:-72px!important;bottom:6px!important}
}
@media(max-width:900px){
  .gentle-crops{padding:52px 0 64px!important}
  .gentle-crops>.wrap{min-height:0}
  .gentle-crops .crop-gallery{position:relative!important;inset:auto!important;order:5!important;display:grid!important;grid-template-columns:repeat(4,1fr)!important;gap:12px!important;margin:22px 0 8px!important;z-index:2!important}
  .gentle-crops .crop-tile,.gentle-crops .crop-tile:nth-child(n){position:relative!important;inset:auto!important;width:auto!important;height:110px!important;display:flex!important;align-items:center!important;justify-content:center!important}
  .gentle-crops .crop-tile img{max-width:100%!important;max-height:100%!important;width:auto!important;height:auto!important}
  .gentle-crops .ripeness{order:6!important;margin-top:18px!important}
}
@media(max-width:560px){
  .gentle-crops .crop-gallery{grid-template-columns:repeat(2,1fr)!important}
  .gentle-crops .crop-tile,.gentle-crops .crop-tile:nth-child(n){height:96px!important}
}
'''

def gallery_html(lang):
    raspberry, blueberry, currant, blackberry = LABELS[lang]
    return (
        '<div class="crop-gallery">'
        f'<article class="crop-tile"><img src="{IMAGES["raspberry"]}" alt="{raspberry}"/></article>'
        f'<article class="crop-tile"><img src="{IMAGES["blueberry"]}" alt="{blueberry}"/></article>'
        f'<article class="crop-tile"><img src="{IMAGES["currant"]}" alt="{currant}"/></article>'
        f'<article class="crop-tile"><img src="{IMAGES["blackberry"]}" alt="{blackberry}"/></article>'
        '</div>'
    )

for lang, p in paths.items():
    if not p.exists():
        raise SystemExit(f'Missing berry page: {p}')
    s = p.read_text(encoding='utf-8')

    gentle = gentle_re.search(s)
    models = models_re.search(s)
    if not gentle:
        raise SystemExit(f'Gentle crop module not found in {p}')
    if not models:
        raise SystemExit(f'Models module not found in {p}')

    models_html = models.group(0)
    s = s[:models.start()] + s[models.end():]
    gentle = gentle_re.search(s)
    insert_at = gentle.end()
    s = s[:insert_at] + models_html + s[insert_at:]

    s, count = gallery_re.subn(gallery_html(lang), s, count=1)
    if count != 1:
        raise SystemExit(f'Crop gallery not found in {p}')

    s = s.replace('</style>', layout_css + '</style>', 1)

    if s.find('gentle-crops') > s.find('id="models"'):
        raise SystemExit(f'Models section order validation failed in {p}')
    for url in IMAGES.values():
        if url not in s:
            raise SystemExit(f'Expected repository berry image missing in {p}')

    p.write_text(s, encoding='utf-8')
    print(f'Applied exact repository berry PNG composition: {p}')
