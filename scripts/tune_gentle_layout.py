#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
paths = [
    root / 'berry-harvesting.html',
    root / 'en' / 'berry-harvesting.html',
    root / 'cz' / 'berry-harvesting.html',
]

css = r'''
/* Final gentle-harvesting composition: statement above cards, floating crop imagery */
.gentle-crops{position:relative!important;overflow:hidden!important;padding:72px 0 86px!important}
.gentle-crops>.wrap{position:relative!important;z-index:1!important;display:flex!important;flex-direction:column!important}
.gentle-crops>.wrap>.eyebrow{order:1}
.gentle-crops>.wrap>h2{order:2}
.gentle-crops>.wrap>.lead{order:3;max-width:900px!important}
.gentle-crops .crop-bridge{order:4;margin:28px 0 0!important;font-size:clamp(30px,3vw,42px)!important;position:relative;z-index:3}
.gentle-crops .ripeness{order:5;margin-top:28px!important;position:relative;z-index:3}
.gentle-crops .ripeness article{background:rgba(255,255,255,.94)!important;backdrop-filter:blur(3px)}
.gentle-crops .crop-gallery{order:6!important;position:absolute!important;inset:0!important;display:block!important;margin:0!important;pointer-events:none!important;z-index:1!important}
.gentle-crops .crop-tile{position:absolute!important;min-height:0!important;width:auto!important;height:auto!important;border:0!important;border-radius:0!important;overflow:visible!important;background:transparent!important;box-shadow:none!important}
.gentle-crops .crop-tile:after{display:none!important}
.gentle-crops .crop-tile b{display:none!important}
.gentle-crops .crop-tile img{position:static!important;display:block!important;width:100%!important;height:auto!important;object-fit:contain!important;mix-blend-mode:multiply!important;filter:saturate(1.06) contrast(1.03)}
/* Blueberry */
.gentle-crops .crop-tile:nth-child(1){width:190px!important;right:-12px!important;top:90px!important;left:auto!important;bottom:auto!important}
/* Raspberry */
.gentle-crops .crop-tile:nth-child(2){width:235px!important;left:-56px!important;bottom:-22px!important;right:auto!important;top:auto!important}
/* Blackberry hidden to keep the module visually lighter */
.gentle-crops .crop-tile:nth-child(3){display:none!important}
/* Blackcurrant */
.gentle-crops .crop-tile:nth-child(4){width:210px!important;right:-35px!important;bottom:-18px!important;left:auto!important;top:auto!important}
@media(max-width:900px){
  .gentle-crops{padding:56px 0 72px!important}
  .gentle-crops .crop-tile:nth-child(1){width:125px!important;right:-38px!important;top:125px!important}
  .gentle-crops .crop-tile:nth-child(2){width:150px!important;left:-54px!important;bottom:-12px!important}
  .gentle-crops .crop-tile:nth-child(4){width:135px!important;right:-42px!important;bottom:12px!important}
  .gentle-crops .ripeness article{background:rgba(255,255,255,.97)!important}
}
'''

for p in paths:
    if not p.exists():
        raise SystemExit(f'Missing berry page: {p}')
    s = p.read_text(encoding='utf-8')
    if 'Final gentle-harvesting composition' not in s:
        s = s.replace('</style>', css + '</style>', 1)
    p.write_text(s, encoding='utf-8')
    print(f'Tuned gentle harvesting layout: {p}')
