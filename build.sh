#!/bin/sh
set -eu
rm -rf dist
mkdir -p dist
cp index.html international.html digital-ai.html education-hr.html readiness.html README.txt dist/ 2>/dev/null || true
if [ -d assets ]; then cp -R assets dist/assets; fi
mkdir -p dist/assets
cp "ChatGPT Image 30 авг. 2026 г., 12_21_44.png" dist/assets/regional-business-white.png
cp "Serbian market.png" dist/assets/projects-serbia.png
cp "Technical project.png" dist/assets/projects-tech.png
cp "book publishing.png" dist/assets/projects-publishing.png
if [ -d en ]; then cp -R en dist/en; fi
if [ -d cz ]; then cp -R cz dist/cz; fi
python3 - <<'PY'
from pathlib import Path
import base64
import shutil

direct = Path('assets/international-city-hero.webp')
if direct.exists():
    raw = direct.read_bytes()
    if len(raw) < 12 or raw[:4] != b'RIFF' or raw[8:12] != b'WEBP':
        raise SystemExit('Direct International hero image is not a valid WebP container')
else:
    chunks = Path('assets/.city-hero')
    if not chunks.is_dir():
        raise SystemExit('International hero image asset is missing')
    new_parts = [chunks / f'new0{i}' for i in range(4)]
    parts = new_parts if all(p.exists() for p in new_parts) else sorted(chunks.glob('part*'))
    encoded = ''.join(p.read_text(encoding='utf-8').strip() for p in parts).replace('=', '')
    encoded += '=' * (-len(encoded) % 4)
    raw = base64.b64decode(encoded, validate=True)
    if len(raw) < 12 or raw[:4] != b'RIFF' or raw[8:12] != b'WEBP':
        raise SystemExit('International hero image is not a valid WebP container')
    out = Path('dist/assets/international-city-hero.webp')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)

shutil.rmtree(Path('dist/assets/.city-hero'), ignore_errors=True)

p = Path('dist/index.html')
s = p.read_text(encoding='utf-8')
link = '<link rel="stylesheet" href="home-premium.css"/>'
if 'home-premium.css' not in s:
    s = s.replace('</head>', link + '\n</head>', 1)
p.write_text(s, encoding='utf-8')

p = Path('dist/international.html')
s = p.read_text(encoding='utf-8')
s = s.replace('Международное развитие — это не только экспорт.','Преимущества работы на международных рынках в современном мире')
s = s.replace('<a href="#">RU&nbsp;&nbsp;/&nbsp;&nbsp;EN</a>','<span class="lang-switch"><a href="international.html" aria-current="page">RU</a>&nbsp;&nbsp;/&nbsp;&nbsp;<a href="en/index.html">EN</a>&nbsp;&nbsp;/&nbsp;&nbsp;<a href="cz/index.html">CZ</a></span>')
needle = '</div></div></section>\n<section><div class="wrap regions-grid">'
cta = '</div><div style="margin-top:28px;padding:28px 30px;background:#fff;border:1px solid var(--line);border-radius:24px;display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;box-shadow:var(--shadow-soft)"><div style="max-width:650px"><h3 style="font-size:30px">Готовы к выходу на новый рынок?</h3><p style="margin-top:10px;color:var(--muted);line-height:1.65">Проверьте готовность компании к международному масштабированию и получите оценку по четырём ключевым направлениям.</p></div><div class="btns" style="margin:0"><a class="btn btn-primary" href="readiness.html" target="_blank" rel="noopener">Оценить готовность</a><a class="btn btn-secondary" href="#contact" style="color:var(--navy);border-color:var(--line);background:#fff">Обсудить задачу</a></div></div></div></section>\n<section><div class="wrap regions-grid">'
if needle in s and 'readiness.html' not in s:
    s = s.replace(needle, cta, 1)

old_regions = '''<section><div class="wrap regions-grid"><div class="regions-copy"><h2>Работаем на нескольких региональных контурах</h2><p>GO BIG соединяет компании с рынками, партнёрами и инфраструктурой роста там, где у нас есть собственная сеть и рабочие связи.</p><div class="chips"><span>Европа</span><span>Балканы</span><span>Сербия</span><span>Центральная Азия</span><span>GCC</span><span>MENA</span></div><div class="note-box">Сильная сторона подхода — сочетание локального присутствия, международной кооперации и компетенций в технологиях, автоматизации и развитии команд.</div></div><div class="regions-media"><img src="assets/Belgrad1.jpg" alt="Белград — один из региональных контуров GO BIG"/><div class="regions-panel"><div class="regions-stat"><strong>01</strong><span>от идеи — к конкретной географии</span></div><div class="regions-stat"><strong>02</strong><span>через сеть локальных партнёров</span></div><div class="regions-stat"><strong>03</strong><span>в прямом диалоге с рынком</span></div><div class="regions-stat"><strong>04</strong><span>без хаотичного набора активностей</span></div></div></div></div></section>'''
new_regions = '''<section class="regions-modern"><div class="wrap"><div class="regions-modern-shell"><div class="regions-modern-copy"><div class="regions-modern-kicker">География работы</div><h2>Работаем на нескольких региональных контурах</h2><p>GO BIG соединяет компании с рынками, партнёрами и инфраструктурой роста там, где у нас есть собственная сеть и рабочие связи.</p><div class="market-chips"><span>Европа</span><span>Балканы</span><span>Сербия</span><span>Центральная Азия</span><span>GCC</span><span>MENA</span></div></div><div class="regions-modern-media"><img src="assets/regional-business-white.png" alt="Деловое обсуждение и международное сотрудничество GO BIG"/><div class="regions-modern-shade"></div><div class="approach-overlay"><span>Сильная сторона подхода</span><p>Локальное присутствие, международная кооперация и компетенции в технологиях, автоматизации и развитии команд.</p></div><div class="regions-cards"><div class="regions-card"><b>01</b><i></i><span>От идеи — к конкретной географии</span></div><div class="regions-card"><b>02</b><i></i><span>Через сеть локальных партнёров</span></div><div class="regions-card"><b>03</b><i></i><span>В прямом диалоге с рынком</span></div><div class="regions-card"><b>04</b><i></i><span>Без хаотичного набора активностей</span></div></div></div></div></div></section>'''
if old_regions in s:
    s = s.replace(old_regions,new_regions,1)

regions_css = '''<style>
.regions-modern{padding:92px 0;background:#fff}.regions-modern-shell{display:grid;grid-template-columns:minmax(0,.82fr) minmax(0,1.18fr);gap:28px;align-items:stretch}.regions-modern-copy{padding:24px 28px 24px 4px;display:flex;flex-direction:column;justify-content:center}.regions-modern-kicker{font-size:12px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--green);margin-bottom:18px}.regions-modern-copy h2{max-width:10.5ch;font-size:clamp(38px,4.2vw,58px);line-height:.99}.regions-modern-copy>p{margin-top:24px;max-width:590px;color:var(--muted);font-size:17px;line-height:1.72}.market-chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}.market-chips span{padding:11px 16px;border-radius:999px;background:#f1f3f5;border:1px solid rgba(11,44,99,.04);color:var(--navy);font-size:13px;font-weight:800}.regions-modern-media{position:relative;min-height:650px;overflow:hidden;border-radius:30px;background:#eef1f3;box-shadow:var(--shadow)}.regions-modern-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 48%;filter:saturate(.92) contrast(1.03) brightness(.98)}.regions-modern-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,20,29,.02) 0%,rgba(22,27,33,.03) 42%,rgba(18,23,29,.34) 100%)}.approach-overlay{position:absolute;top:28px;right:28px;z-index:3;width:min(45%,360px);padding:20px 22px;border:1px solid rgba(255,255,255,.22);border-radius:20px;background:rgba(42,47,53,.66);backdrop-filter:blur(10px);color:#fff}.approach-overlay span{display:block;margin-bottom:9px;font-size:10px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:#78c5a0}.approach-overlay p{font-size:14px;line-height:1.55;color:rgba(255,255,255,.96)}.regions-cards{position:absolute;left:28px;right:28px;bottom:28px;z-index:3;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.regions-card{min-height:126px;padding:20px 21px;border:1px solid rgba(255,255,255,.20);border-radius:20px;background:rgba(23,31,41,.78);backdrop-filter:blur(9px);color:#fff}.regions-card b{display:block;font:700 30px/1 var(--font-heading);color:#fff}.regions-card i{display:block;width:38px;height:2px;background:var(--green);margin:12px 0 13px}.regions-card span{display:block;font-size:15px;font-weight:650;line-height:1.38;color:rgba(255,255,255,.98)}
@media(max-width:900px){.regions-modern-shell{grid-template-columns:1fr}.regions-modern-copy{padding:0}.regions-modern-copy h2{max-width:none;font-size:clamp(34px,8vw,46px);line-height:1.02}.regions-modern-copy>p{font-size:16px}.regions-modern-media{min-height:0;height:auto;overflow:visible;background:transparent;box-shadow:none;display:flex;flex-direction:column;gap:12px}.regions-modern-media img{position:relative;inset:auto;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;object-position:center center;border-radius:24px;filter:saturate(.96) contrast(1.02) brightness(1)}.regions-modern-shade{display:none}.approach-overlay{position:relative;inset:auto;top:auto;right:auto;width:100%;max-width:none;background:#2d3339;border-radius:18px;padding:18px 20px;box-shadow:none}.regions-cards{position:relative;inset:auto;left:auto;right:auto;bottom:auto;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.regions-card{min-height:112px;padding:17px;background:#242c35}.market-chips{margin-top:22px}}
@media(max-width:620px){.regions-modern{padding:64px 0}.regions-modern-shell{gap:24px}.regions-modern-copy h2{font-size:36px}.regions-modern-media img{aspect-ratio:1/1;object-position:52% center}.regions-cards{grid-template-columns:1fr}.regions-card{min-height:auto}.regions-card b{font-size:25px}.regions-card i{margin:8px 0 9px}.regions-card span{font-size:14px}.market-chips span{padding:9px 12px;font-size:12px}}
</style>'''
if 'regions-modern-shell' in s and '.regions-modern-shell{' not in s:
    s = s.replace('</head>',regions_css+'\n</head>',1)

mobile_css='''<style>
html,body{max-width:100%;overflow-x:hidden}
@media(max-width:760px){
  .wrap{width:calc(100% - 28px)!important}
  header{position:relative!important}
  .head{padding:14px 0!important;gap:12px!important;align-items:flex-start!important}
  .brand{flex-shrink:0}.mark{width:34px!important;height:42px!important}.brand strong{font-size:24px!important}
  nav{width:100%!important;display:flex!important;flex-wrap:nowrap!important;overflow-x:auto!important;gap:14px!important;padding:2px 0 8px!important;scrollbar-width:none}nav::-webkit-scrollbar{display:none}nav a,.lang-switch{white-space:nowrap!important;font-size:12px!important}
  .hero{min-height:560px!important}.hero-copy{padding:50px 0 48px!important;max-width:100%!important}.hero h1{font-size:40px!important;line-height:1.02!important;max-width:9ch!important}.lead{font-size:15px!important;line-height:1.5!important;max-width:95%!important}.btns{gap:10px!important}.btn{min-height:50px!important;padding:0 18px!important;font-size:14px!important}
  section{padding:64px 0}.intro-grid,.service-grid,.process-grid,.case-shell,.regions-grid{grid-template-columns:1fr!important}.adv-grid{grid-template-columns:1fr!important}.section-head{display:block!important}.section-head p{margin-top:14px!important}.service-summary h3{font-size:22px!important}.service-summary{padding:22px 62px 20px 22px!important}.service-toggle{right:20px!important;top:23px!important}
  .cta-box{padding:28px 22px!important}.cta-box h2{font-size:34px!important}.foot{flex-direction:column!important}
}
@media(max-width:420px){.hero h1{font-size:36px!important}.lead{font-size:14px!important}.btns .btn{width:100%!important}.section-head h2,h2{font-size:34px!important}}
</style>'''
s=s.replace('</head>',mobile_css+'\n</head>',1)
link='<link rel="stylesheet" href="international-hero.css"/>'
if 'international-hero.css' not in s:s=s.replace('</head>',link+'\n</head>',1)
p.write_text(s,encoding='utf-8')

for p in Path('dist').glob('*.html'):
    s=p.read_text(encoding='utf-8')
    s=s.replace('href="/assets/','href="assets/').replace('src="/assets/','src="assets/').replace("url('/assets/","url('assets/")
    for name in ['index.html','international.html','digital-ai.html','education-hr.html','readiness.html']:
        s=s.replace(f'href="/{name}"',f'href="{name}"')
    p.write_text(s,encoding='utf-8')
PY
cp home-premium.css dist/home-premium.css
cp international-hero.css dist/international-hero.css
sed -i "s#url('/assets/#url('assets/#g" dist/international-hero.css
touch dist/.nojekyll
