#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
paths = [
    root / 'berry-harvesting.html',
    root / 'en' / 'berry-harvesting.html',
    root / 'cz' / 'berry-harvesting.html',
]

gentle_re = re.compile(r'<section class="section soft gentle-crops">.*?</section>', re.S)
models_re = re.compile(r'<section class="section dark" id="models">.*?</section>', re.S)

layout_css = r'''
/* Floating berry composition for gentle harvesting module */
.gentle-crops{position:relative!important;overflow:hidden!important;padding:72px 0 86px!important}
.gentle-crops>.wrap{position:relative!important;z-index:1!important;display:flex!important;flex-direction:column!important}
.gentle-crops>.wrap>.eyebrow{order:1}
.gentle-crops>.wrap>h2{order:2}
.gentle-crops>.wrap>.lead{order:3;max-width:900px!important}
.gentle-crops .crop-bridge{order:4;margin:28px 0 0!important;font:700 clamp(30px,3vw,42px)/1.05 var(--serif)!important;color:var(--navy)!important;position:relative;z-index:3}
.gentle-crops .ripeness{order:5;margin-top:28px!important;position:relative!important;z-index:3!important}
.gentle-crops .ripeness article{background:rgba(255,255,255,.96)!important;backdrop-filter:blur(3px)}
.gentle-crops .crop-gallery{display:block!important;position:absolute!important;inset:0!important;margin:0!important;pointer-events:none!important;z-index:2!important}
.gentle-crops .crop-tile{position:absolute!important;min-height:0!important;width:auto!important;height:auto!important;border:0!important;border-radius:0!important;overflow:visible!important;background:transparent!important;box-shadow:none!important}
.gentle-crops .crop-tile:after{display:none!important}
.gentle-crops .crop-tile b{display:none!important}
.gentle-crops .crop-tile img{position:static!important;display:block!important;width:100%!important;height:auto!important;object-fit:contain!important;filter:saturate(1.08) contrast(1.04)}
/* Blueberry — top right */
.gentle-crops .crop-tile:nth-child(1){display:block!important;width:175px!important;right:-8px!important;top:72px!important;left:auto!important;bottom:auto!important}
/* Raspberry — bottom left */
.gentle-crops .crop-tile:nth-child(2){display:block!important;width:215px!important;left:-38px!important;bottom:-18px!important;right:auto!important;top:auto!important}
/* Blackberry hidden: keep the composition light */
.gentle-crops .crop-tile:nth-child(3){display:none!important}
/* Blackcurrant — bottom right */
.gentle-crops .crop-tile:nth-child(4){display:block!important;width:190px!important;right:-22px!important;bottom:-16px!important;left:auto!important;top:auto!important}
@media(max-width:900px){
  .gentle-crops{padding:56px 0 72px!important}
  .gentle-crops .crop-tile:nth-child(1){width:110px!important;right:-38px!important;top:135px!important}
  .gentle-crops .crop-tile:nth-child(2){width:140px!important;left:-48px!important;bottom:-5px!important}
  .gentle-crops .crop-tile:nth-child(4){width:125px!important;right:-42px!important;bottom:10px!important}
  .gentle-crops .ripeness article{background:rgba(255,255,255,.98)!important}
}
'''

for p in paths:
    if not p.exists():
        raise SystemExit(f'Missing berry page: {p}')
    s = p.read_text(encoding='utf-8')

    gentle = gentle_re.search(s)
    models = models_re.search(s)
    if not gentle:
        raise SystemExit(f'Gentle crop module not found in {p}')
    if not models:
        raise SystemExit(f'Models module not found in {p}')

    # Keep the configuration block directly after the gentle/crops module.
    models_html = models.group(0)
    s = s[:models.start()] + s[models.end():]
    gentle = gentle_re.search(s)
    insert_at = gentle.end()
    s = s[:insert_at] + models_html + s[insert_at:]

    # Apply the approved floating-berry composition to the existing crop images.
    if 'Floating berry composition for gentle harvesting module' not in s:
        s = s.replace('</style>', layout_css + '</style>', 1)

    if s.find('gentle-crops') > s.find('id="models"'):
        raise SystemExit(f'Models section order validation failed in {p}')

    p.write_text(s, encoding='utf-8')
    print(f'Applied floating berry composition and model order: {p}')
