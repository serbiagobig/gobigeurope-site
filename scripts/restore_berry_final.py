#!/usr/bin/env python3
from pathlib import Path
import re

p = Path('dist/berry-harvesting.html')
if not p.exists():
    raise SystemExit('Missing dist/berry-harvesting.html')
s = p.read_text(encoding='utf-8')

# 1) Approved hero.
s = s.replace(
    '<div class="hero-copy"><div class="kicker">AGRO TAG SELECTED TECHNOLOGY</div><h1>Механизированная уборка ягод для свежего рынка</h1>',
    '<div class="hero-copy"><div class="kicker">Инновационная технология</div><h1>Воздушно-импульсная уборка</h1>',
    1,
)
s = s.replace(
    'Бесконтактная технология сбора спелой ягоды управляемыми импульсами воздуха. Снижение зависимости от сезонных рабочих — при бережном воздействии на растение и урожай.',
    'Бесконтактная технология сбора спелой ягоды и фруктов управляемыми импульсами воздуха. Снижение зависимости от сезонных рабочих — при бережном воздействии на растение и урожай.',
    1,
)

# 2) Approved compact manual-harvest problem block.
old_problem_re = re.compile(r'<section class="section"><div class="wrap problem">.*?</section>', re.S)
new_problem = '''<section class="section manual-problems"><div class="wrap"><div class="eyebrow">Типичные проблемы ручной уборки</div><h2>Когда ручной сбор становится ограничением</h2><p class="lead manual-intro">Ручной сбор ограничивает скорость, масштаб хозяйства и стабильность качества ягоды.</p>
<div class="problem-panels">
<article class="problem-panel"><div class="panel-head"><span>Операционные ограничения</span><small>Люди · сроки · масштаб</small></div><div class="problem-list">
<div class="problem-row"><b>01</b><span>Дефицит сезонных рабочих</span></div>
<div class="problem-row"><b>02</b><span>Рост стоимости ручного труда</span></div>
<div class="problem-row"><b>03</b><span>Непредсказуемые сроки уборки</span></div>
<div class="problem-row"><b>04</b><span>Ограничение масштаба хозяйства</span></div>
</div></article>
<article class="problem-panel quality-panel"><div class="panel-head"><span>Риски для качества урожая</span><small>Ягода · зрелость · хранение</small></div><div class="problem-list">
<div class="problem-row"><b>05</b><span>Повреждение ягод</span></div>
<div class="problem-row"><b>06</b><span>Потеря защитного воскового налёта</span></div>
<div class="problem-row"><b>07</b><span>Неоднородная зрелость партии</span></div>
<div class="problem-row"><b>08</b><span>Перегрев и задержка охлаждения</span></div>
</div></article>
</div></div></section>'''
s, count = old_problem_re.subn(new_problem, s, count=1)
if count != 1 and 'manual-problems' not in s:
    raise SystemExit('Could not restore approved manual-harvest block')

# 3) Approved economics block with video.
old_benefits = '<section class="section soft" id="benefits"><div class="wrap"><div class="eyebrow">Экономика уборки</div><h2>Производительность, которая меняет экономику</h2><div class="stats">'
new_benefits = '''<section class="section soft" id="benefits"><div class="wrap economy-layout"><div class="eyebrow">Эффективность</div><h2>Мы создаем новую экономику уборки</h2><p class="economy-subtitle">Производительность, которая меняет экономику</p><div class="economy-video"><video autoplay muted loop playsinline preload="metadata" poster="/assets/agro-card-05.png" aria-label="Механизированная уборка ягод"><source src="/berry-harvesting-web.mp4" type="video/mp4"></video></div><div class="stats economy-stats">'''
if old_benefits in s:
    s = s.replace(old_benefits, new_benefits, 1)
s = s.replace('500+ кг/час', 'до 500+ кг/час', 1)
s = s.replace('Для голубичных плантаций в подходящих условиях.', 'Для ягодных плантаций в подходящих условиях.', 1)

# 4) Remove modules explicitly rejected in the approved version.
patterns = [
    re.compile(r'<section class="section[^\"]*"[^>]*id="fit"[^>]*>.*?</section>', re.S | re.I),
    re.compile(r'<section class="section[^\"]*"[^>]*>(?:(?!<section ).)*?(?:НОВЫЕ ПРОЕКТЫ|Планируете новую ягодную плантацию\?).*?</section>', re.S | re.I),
    re.compile(r'<section class="section[^\"]*"[^>]*>(?:(?!<section ).)*?Механизация — это процесс, а не покупка одной машины.*?</section>', re.S | re.I),
]
for rx in patterns:
    s = rx.sub('', s, count=1)

# 5) Replace legacy implementation solution with the approved system block.
impl_re = re.compile(r'<section class="section soft"><div class="wrap"><div class="eyebrow">(?:AGRO TAG SOLUTION|[^<]+)</div><h2>[^<]*(?:Система внедрения)[^<]*</h2>.*?</section>', re.S | re.I)
legacy_impl_re = re.compile(r'<section class="section soft"><div class="wrap">(?:(?!</section>).)*?<div class="solution">.*?</section>', re.S)
items = ['Анализ хозяйства','Подбор технологии','Оценка участка','Поставка','Запуск','Обучение','Сервис','Запасные части']
cards = ''.join(f'<article class="implementation-card"><b>{i:02d}</b><span>{label}</span></article>' for i,label in enumerate(items,1))
replacement = '<section class="section implementation-system" id="implementation"><div class="wrap"><div class="eyebrow">Система внедрения</div><h2>Не просто оборудование. Система внедрения.</h2><p class="implementation-lead">Поставщик сопровождает внедрение технологии от первичной оценки хозяйства до запуска оборудования и последующей сервисной поддержки.</p><div class="implementation-grid">'+cards+'</div></div></section>'
s2, n = impl_re.subn(replacement, s, count=1)
if n == 0:
    s2, n = legacy_impl_re.subn(replacement, s, count=1)
if n == 1:
    s = s2

# 6) Approved subnavigation.
s = s.replace('<section class="section soft gentle-crops">','<section class="section soft gentle-crops" id="gentle">',1)
nav_re = re.compile(r'<nav class="subnav"><div class="wrap">.*?</div></nav>', re.S)
nav = '<nav class="subnav"><div class="wrap"><a href="#benefits">Эффективность</a><a href="#technology">Технология</a><a href="#gentle">Бережный принцип</a><a href="#models">Модели</a><a href="#plantation">Подготовка плантации</a><a href="#implementation">Система внедрения</a><a href="#contact">Консультация</a></div></nav>'
s, nav_count = nav_re.subn(nav, s, count=1)
if nav_count != 1:
    raise SystemExit('Berry subnavigation not found')

# 7) Approved visual system.
css = r'''
/* APPROVED BERRY PAGE — authoritative post-build design */
.hero-copy{max-width:930px!important}.hero .kicker{font-size:13px!important;letter-spacing:.16em!important;color:#71d0a0!important;margin-bottom:14px}.hero h1{margin:0!important;font-size:clamp(54px,5.8vw,82px)!important;line-height:.95!important;text-transform:uppercase}
.manual-problems{background:#fff;padding:66px 0 72px}.manual-problems h2{max-width:980px;font-size:clamp(42px,4.2vw,62px)}.manual-problems .manual-intro{max-width:850px;margin-top:14px;font-size:16px}.problem-panels{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:30px}.problem-panel{padding:24px 26px 20px;border:1px solid var(--line);border-radius:24px;background:#f7f9f9}.quality-panel{background:#f1f6f3;border-color:#d6e5dd}.panel-head{display:flex;align-items:baseline;justify-content:space-between;gap:14px;padding-bottom:13px;border-bottom:1px solid #d9e1e4}.panel-head span{font:700 23px/1.1 var(--serif);color:var(--navy)}.panel-head small{font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--green);white-space:nowrap}.problem-list{display:grid;margin-top:4px}.problem-row{display:grid;grid-template-columns:54px 1fr;gap:12px;align-items:center;min-height:60px;border-bottom:1px solid #e1e7e9}.problem-row:last-child{border-bottom:0}.problem-row b{color:var(--green);font-size:23px;font-weight:800;line-height:1}.problem-row span{font:700 19px/1.18 var(--serif);color:var(--navy)}
#benefits{padding:62px 0}.economy-layout{display:grid;grid-template-columns:minmax(0,.86fr) minmax(0,1.14fr);grid-template-rows:auto auto auto 1fr;column-gap:34px;align-items:start}.economy-layout>.eyebrow,.economy-layout>h2,.economy-layout>.economy-subtitle,.economy-layout>.economy-stats{grid-column:1}.economy-layout>.eyebrow{grid-row:1}.economy-layout>h2{grid-row:2;margin-top:10px;font-size:clamp(40px,4vw,58px)}.economy-subtitle{grid-row:3;margin:12px 0 0;font:600 clamp(20px,2vw,27px)/1.2 var(--serif);color:#486985}.economy-stats{grid-row:4;grid-template-columns:1fr;gap:10px;margin-top:22px}.economy-stats .stat{padding:17px 20px;border-radius:18px;display:grid;grid-template-columns:minmax(220px,1fr) minmax(0,1.15fr);gap:28px;align-items:center}.economy-stats .stat strong{font-size:34px;white-space:nowrap}.economy-stats .stat span{margin-top:0;font-size:15px;line-height:1.5}.economy-video{grid-column:2;grid-row:1/5;align-self:stretch;min-height:470px;border-radius:28px;overflow:hidden;background:#101f2b;box-shadow:0 18px 38px rgba(16,37,61,.12)}.economy-video video{display:block;width:100%;height:100%;min-height:470px;object-fit:cover;object-position:center}
.gentle-crops .crop-gallery{overflow:visible!important}.gentle-crops .crop-tile{overflow:visible!important;border-radius:0!important;height:auto!important}.gentle-crops .crop-tile img{position:static!important;inset:auto!important;width:100%!important;height:auto!important;max-width:none!important;max-height:none!important;object-fit:contain!important;display:block!important}
.implementation-system{background:#fff!important;min-height:0!important;display:block!important;padding:78px 0!important}.implementation-system .wrap{width:min(1200px,calc(100% - 48px))!important}.implementation-system .eyebrow{font-size:11px!important;letter-spacing:.14em!important;margin-bottom:0!important}.implementation-system h2{max-width:980px!important;font-size:clamp(38px,4.4vw,60px)!important;line-height:1!important;margin-top:12px!important}.implementation-system .implementation-lead{max-width:760px!important;margin:20px 0 0!important;font-size:17px!important;line-height:1.7!important;color:var(--muted)!important}.implementation-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:30px}.implementation-card{min-height:148px;padding:20px 20px 21px;border:1px solid #e0e7e7;border-radius:18px;background:#fbfcfc;box-shadow:0 8px 20px rgba(16,37,61,.035);display:flex;flex-direction:column;justify-content:space-between}.implementation-card b{font:800 36px/1 var(--sans);color:#0b6b45;letter-spacing:-.045em}.implementation-card span{display:block;margin-top:20px;font:700 clamp(19px,1.45vw,23px)/1.1 var(--serif);color:#10253d}
@media(max-width:1000px){.implementation-grid{grid-template-columns:repeat(2,1fr)}.implementation-card{min-height:138px}.implementation-system .wrap{width:calc(100% - 36px)!important}}@media(max-width:900px){.hero h1{font-size:clamp(42px,11vw,62px)!important}.manual-problems{padding:54px 0}.problem-panels{grid-template-columns:1fr}.panel-head{align-items:flex-start;flex-direction:column}.problem-panel{padding:20px}.problem-row{grid-template-columns:48px 1fr}.problem-row span{font-size:18px}#benefits{padding:54px 0}.economy-layout{grid-template-columns:1fr;grid-template-rows:auto}.economy-layout>.eyebrow,.economy-layout>h2,.economy-layout>.economy-subtitle,.economy-layout>.economy-video,.economy-layout>.economy-stats{grid-column:1;grid-row:auto}.economy-video{margin-top:24px;min-height:0;aspect-ratio:16/9;border-radius:22px}.economy-video video{min-height:0}.economy-stats{margin-top:18px}.economy-stats .stat{grid-template-columns:1fr;gap:8px}.gentle-crops .crop-tile img{width:auto!important;height:auto!important;max-width:100%!important;max-height:100%!important}}@media(max-width:560px){.implementation-system{padding:56px 0!important}.implementation-grid{grid-template-columns:1fr;gap:10px;margin-top:26px}.implementation-card{min-height:108px;padding:18px}.implementation-card b{font-size:32px}.implementation-card span{margin-top:15px;font-size:20px}.implementation-system h2{font-size:clamp(38px,11vw,52px)!important}}
'''
if 'APPROVED BERRY PAGE' not in s:
    s = s.replace('</style>', css + '</style>', 1)

# 8) Guardrails: fail the build if rejected legacy modules return.
for marker in ('id="fit"','href="#fit"','Планируете новую ягодную плантацию?','Механизация — это процесс, а не покупка одной машины'):
    if marker in s:
        raise SystemExit(f'Rejected legacy berry module returned: {marker}')
for marker in ('Воздушно-импульсная уборка','manual-problems','economy-layout','id="implementation"','Поставщик сопровождает внедрение технологии'):
    if marker not in s:
        raise SystemExit(f'Approved berry marker missing: {marker}')

p.write_text(s, encoding='utf-8')
print('Restored approved berry-harvesting page as final build source')
