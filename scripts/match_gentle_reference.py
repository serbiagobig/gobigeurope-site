#!/usr/bin/env python3
from pathlib import Path
import re
import shutil
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

copy = {
    'ru': {
        'eyebrow': 'БЕРЕЖНЫЙ ПРИНЦИП',
        'title': 'Механизированная уборка без жёсткого контакта',
        'lead': 'Созревшая ягода удерживается растением слабее, чем незрелая. Правильно настроенное воздушное воздействие использует это различие.',
        'bridge': 'Один принцип. Разные культуры.',
        'ripe': 'Спелая ягода → отделяется',
        'ripe_text': 'Настройки подбираются под культуру, зрелость и состояние насаждений.',
        'unripe': 'Незрелая ягода → остаётся',
        'unripe_text': 'Цель — сохранить незрелые плоды на растении и снизить нежелательное воздействие.',
    },
    'en': {
        'eyebrow': 'GENTLE HARVESTING PRINCIPLE',
        'title': 'Mechanized harvesting without hard contact',
        'lead': 'Ripe fruit is held less firmly by the plant than unripe fruit. Properly tuned air action uses this difference.',
        'bridge': 'One principle. Different crops.',
        'ripe': 'Ripe berry → detaches',
        'ripe_text': 'Settings are adapted to crop, ripeness and plantation condition.',
        'unripe': 'Unripe berry → remains',
        'unripe_text': 'The objective is to keep unripe fruit on the plant and minimize unwanted impact.',
    },
    'cz': {
        'eyebrow': 'ŠETRNÝ PRINCIP',
        'title': 'Mechanizovaná sklizeň bez tvrdého kontaktu',
        'lead': 'Zralé plody drží na rostlině slaběji než nezralé. Správně nastavené působení vzduchu tento rozdíl využívá.',
        'bridge': 'Jeden princip. Různé plodiny.',
        'ripe': 'Zralá bobule → oddělí se',
        'ripe_text': 'Nastavení se přizpůsobuje plodině, zralosti a stavu porostu.',
        'unripe': 'Nezralá bobule → zůstává',
        'unripe_text': 'Cílem je ponechat nezralé plody na rostlině a omezit nežádoucí působení.',
    },
}

# Use the approved transparent berry artwork already stored in the repository.
assets = {
    'raspberry': ('Малина-removebg-preview.png', 'gentle-raspberry.png'),
    'blueberry': ('Голубика-removebg-preview.png', 'gentle-blueberry.png'),
    'currant': ('Смородина-removebg-preview.png', 'gentle-currant.png'),
    'blackberry': ('Ежевика-removebg-preview.png', 'gentle-blackberry.png'),
}
asset_dir = root / 'assets'
asset_dir.mkdir(parents=True, exist_ok=True)
for _, (src_name, dst_name) in assets.items():
    src = Path(src_name)
    if not src.exists():
        raise SystemExit(f'Missing approved berry artwork: {src_name}')
    shutil.copyfile(src, asset_dir / dst_name)

css = r'''
/* Approved gentle-harvesting reference module */
.gentle-reference{padding:78px 0 84px;background:#f1f5f5;overflow:hidden}
.gentle-reference .wrap{max-width:1180px;position:relative}
.gentle-reference .eyebrow{margin:0 0 22px;color:#188452;font-size:13px;font-weight:800;letter-spacing:.17em;text-transform:uppercase}
.gentle-reference h2{position:relative;z-index:2;max-width:710px;margin:0;color:var(--navy);font:700 clamp(46px,5.2vw,72px)/.98 var(--serif);letter-spacing:-.035em}
.gentle-reference .gentle-lead{position:relative;z-index:2;max-width:700px;margin:26px 0 0;color:#7b8996;font-size:18px;line-height:1.58}
.gentle-reference .gentle-berries{position:absolute;z-index:1;top:18px;right:-6px;width:430px;height:360px;pointer-events:none}
.gentle-reference .gentle-berries img{position:absolute!important;display:block!important;width:auto!important;height:auto!important;max-width:none!important;object-fit:contain!important;filter:drop-shadow(0 18px 24px rgba(16,37,61,.12))}
.gentle-reference .gentle-berries .raspberry{width:170px!important;top:0;right:16px;transform:rotate(7deg)}
.gentle-reference .gentle-berries .blueberry{width:158px!important;top:108px;left:24px;transform:rotate(-7deg)}
.gentle-reference .gentle-berries .currant{width:168px!important;top:132px;right:-8px;transform:rotate(5deg)}
.gentle-reference .gentle-berries .blackberry{width:178px!important;right:58px;bottom:-2px;transform:rotate(-8deg)}
.gentle-reference .gentle-bridge{position:relative;z-index:2;margin:72px 0 28px;color:var(--navy);font:700 clamp(34px,3.6vw,48px)/1 var(--serif);letter-spacing:-.025em}
.gentle-reference .ripeness{position:relative;z-index:3;display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:0}
.gentle-reference .ripeness article{min-height:214px;padding:34px 32px 32px;border:1px solid #d7e1e3;border-radius:24px;background:#fff;box-shadow:none}
.gentle-reference .ripeness strong{display:block;color:#1f2935;font-size:25px;font-weight:800;line-height:1.18}
.gentle-reference .ripeness .ripe strong{color:#13854f}
.gentle-reference .ripeness p{max-width:470px;margin:28px 0 0;color:#8794a1;font-size:17px;line-height:1.55}
@media(max-width:1000px){
  .gentle-reference h2,.gentle-reference .gentle-lead{max-width:62%}
  .gentle-reference .gentle-berries{right:-36px;width:390px;transform:scale(.92);transform-origin:top right}
}
@media(max-width:900px){
  .gentle-reference{padding:58px 0 62px}
  .gentle-reference h2{max-width:100%;font-size:clamp(40px,9vw,58px)}
  .gentle-reference .gentle-lead{max-width:100%}
  .gentle-reference .gentle-berries{position:relative;top:auto;right:auto;width:100%;height:300px;margin:18px 0 6px;transform:none}
  .gentle-reference .gentle-berries .raspberry{width:142px!important;top:0;right:8%}
  .gentle-reference .gentle-berries .blueberry{width:128px!important;top:74px;left:8%}
  .gentle-reference .gentle-berries .currant{width:138px!important;top:102px;right:2%}
  .gentle-reference .gentle-berries .blackberry{width:146px!important;right:31%;bottom:0}
  .gentle-reference .gentle-bridge{margin-top:28px}
  .gentle-reference .ripeness{grid-template-columns:1fr}
  .gentle-reference .ripeness article{min-height:0;padding:28px 24px}
}
@media(max-width:560px){
  .gentle-reference h2{font-size:40px}
  .gentle-reference .gentle-lead{font-size:16px}
  .gentle-reference .gentle-berries{height:250px;margin-top:14px}
  .gentle-reference .gentle-berries .raspberry{width:118px!important;right:4%}
  .gentle-reference .gentle-berries .blueberry{width:108px!important;top:72px;left:0}
  .gentle-reference .gentle-berries .currant{width:112px!important;top:86px;right:-3%}
  .gentle-reference .gentle-berries .blackberry{width:120px!important;right:28%}
  .gentle-reference .gentle-bridge{font-size:32px}
  .gentle-reference .ripeness strong{font-size:22px}
  .gentle-reference .ripeness p{margin-top:20px;font-size:16px}
}
'''

def render(lang, prefix=''):
    t = copy[lang]
    berry_html = (
        '<div class="gentle-berries" aria-hidden="true">'
        f'<img class="raspberry" src="{prefix}assets/gentle-raspberry.png" alt="">'
        f'<img class="blueberry" src="{prefix}assets/gentle-blueberry.png" alt="">'
        f'<img class="currant" src="{prefix}assets/gentle-currant.png" alt="">'
        f'<img class="blackberry" src="{prefix}assets/gentle-blackberry.png" alt="">'
        '</div>'
    )
    return (
        '<section class="section soft gentle-reference">'
        '<div class="wrap">'
        f'<div class="eyebrow">{t["eyebrow"]}</div>'
        f'<h2>{t["title"]}</h2>'
        f'<p class="gentle-lead">{t["lead"]}</p>'
        + berry_html +
        f'<h3 class="gentle-bridge">{t["bridge"]}</h3>'
        '<div class="ripeness">'
        f'<article class="ripe"><strong>{t["ripe"]}</strong><p>{t["ripe_text"]}</p></article>'
        f'<article><strong>{t["unripe"]}</strong><p>{t["unripe_text"]}</p></article>'
        '</div>'
        '</div></section>'
    )

pages = {
    'ru': (root / 'berry-harvesting.html', ''),
    'en': (root / 'en' / 'berry-harvesting.html', '../'),
    'cz': (root / 'cz' / 'berry-harvesting.html', '../'),
}

pattern = re.compile(r'<section class="section soft (?:gentle-crops|gentle-reference)">.*?</section>', re.S)
for lang, (path, prefix) in pages.items():
    if not path.exists():
        raise SystemExit(f'Missing berry page: {path}')
    s = path.read_text(encoding='utf-8')
    s, count = pattern.subn(render(lang, prefix), s, count=1)
    if count != 1:
        raise SystemExit(f'Could not replace gentle harvesting module in {path}')
    # Replace any older version of this module CSS so the approved composition is authoritative.
    s = re.sub(r'/\* Approved gentle-harvesting reference module \*/.*?(?=</style>)', css, s, count=1, flags=re.S)
    if '/* Approved gentle-harvesting reference module */' not in s:
        s = s.replace('</style>', css + '</style>', 1)
    for marker in ('gentle-raspberry.png','gentle-blueberry.png','gentle-currant.png','gentle-blackberry.png'):
        if marker not in s:
            raise SystemExit(f'Missing berry decoration in {path}: {marker}')
    path.write_text(s, encoding='utf-8')
    print(f'Matched gentle harvesting reference module with berry artwork: {lang}')
