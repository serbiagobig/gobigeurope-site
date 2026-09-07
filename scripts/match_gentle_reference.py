#!/usr/bin/env python3
from pathlib import Path
import re
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

css = r'''
/* Approved gentle-harvesting reference module */
.gentle-reference{padding:78px 0 84px;background:#f1f5f5}
.gentle-reference .wrap{max-width:1180px}
.gentle-reference .eyebrow{margin:0 0 22px;color:#188452;font-size:13px;font-weight:800;letter-spacing:.17em;text-transform:uppercase}
.gentle-reference h2{max-width:1040px;margin:0;color:var(--navy);font:700 clamp(46px,5.2vw,72px)/.98 var(--serif);letter-spacing:-.035em}
.gentle-reference .gentle-lead{max-width:900px;margin:26px 0 0;color:#7b8996;font-size:18px;line-height:1.58}
.gentle-reference .gentle-bridge{margin:54px 0 28px;color:var(--navy);font:700 clamp(34px,3.6vw,48px)/1 var(--serif);letter-spacing:-.025em}
.gentle-reference .ripeness{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:0}
.gentle-reference .ripeness article{min-height:214px;padding:34px 32px 32px;border:1px solid #d7e1e3;border-radius:24px;background:#fff;box-shadow:none}
.gentle-reference .ripeness strong{display:block;color:#1f2935;font-size:25px;font-weight:800;line-height:1.18}
.gentle-reference .ripeness .ripe strong{color:#13854f}
.gentle-reference .ripeness p{max-width:470px;margin:28px 0 0;color:#8794a1;font-size:17px;line-height:1.55}
@media(max-width:900px){
  .gentle-reference{padding:58px 0 62px}
  .gentle-reference h2{font-size:clamp(40px,9vw,58px)}
  .gentle-reference .gentle-bridge{margin-top:42px}
  .gentle-reference .ripeness{grid-template-columns:1fr}
  .gentle-reference .ripeness article{min-height:0;padding:28px 24px}
}
@media(max-width:560px){
  .gentle-reference h2{font-size:40px}
  .gentle-reference .gentle-lead{font-size:16px}
  .gentle-reference .gentle-bridge{font-size:32px}
  .gentle-reference .ripeness strong{font-size:22px}
  .gentle-reference .ripeness p{margin-top:20px;font-size:16px}
}
'''

def render(lang):
    t = copy[lang]
    return (
        '<section class="section soft gentle-reference">'
        '<div class="wrap">'
        f'<div class="eyebrow">{t["eyebrow"]}</div>'
        f'<h2>{t["title"]}</h2>'
        f'<p class="gentle-lead">{t["lead"]}</p>'
        f'<h3 class="gentle-bridge">{t["bridge"]}</h3>'
        '<div class="ripeness">'
        f'<article class="ripe"><strong>{t["ripe"]}</strong><p>{t["ripe_text"]}</p></article>'
        f'<article><strong>{t["unripe"]}</strong><p>{t["unripe_text"]}</p></article>'
        '</div>'
        '</div></section>'
    )

pages = {
    'ru': root / 'berry-harvesting.html',
    'en': root / 'en' / 'berry-harvesting.html',
    'cz': root / 'cz' / 'berry-harvesting.html',
}

pattern = re.compile(r'<section class="section soft (?:gentle-crops|gentle-reference)">.*?</section>', re.S)
for lang, path in pages.items():
    if not path.exists():
        raise SystemExit(f'Missing berry page: {path}')
    s = path.read_text(encoding='utf-8')
    s, count = pattern.subn(render(lang), s, count=1)
    if count != 1:
        raise SystemExit(f'Could not replace gentle harvesting module in {path}')
    if '/* Approved gentle-harvesting reference module */' not in s:
        s = s.replace('</style>', css + '</style>', 1)
    path.write_text(s, encoding='utf-8')
    print(f'Matched gentle harvesting reference module: {lang}')
