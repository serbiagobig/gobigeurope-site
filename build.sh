#!/bin/sh
set -eu
rm -rf dist
mkdir -p dist
cp index.html international.html digital-ai.html education-hr.html readiness.html README.txt dist/ 2>/dev/null || true
if [ -d assets ]; then cp -R assets dist/assets; fi
if [ -d en ]; then cp -R en dist/en; fi
if [ -d cz ]; then cp -R cz dist/cz; fi
python3 - <<'PY'
from pathlib import Path
import base64
import shutil

# Prefer the direct binary hero asset. Only use legacy text chunks as fallback.
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
    if all(p.exists() for p in new_parts):
        parts = new_parts
    else:
        parts = sorted(chunks.glob('part*'))
    encoded = ''.join(p.read_text(encoding='utf-8').strip() for p in parts)
    encoded = encoded.replace('=', '')
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
s = s.replace(
    'Международное развитие — это не только экспорт.',
    'Преимущества работы на международных рынках в современном мире'
)
# Language switcher foundation for the current Russian master page.
s = s.replace(
    '<a href="#">RU&nbsp;&nbsp;/&nbsp;&nbsp;EN</a>',
    '<span class="lang-switch"><a href="international.html" aria-current="page">RU</a>&nbsp;&nbsp;/&nbsp;&nbsp;<a href="en/index.html">EN</a>&nbsp;&nbsp;/&nbsp;&nbsp;<a href="cz/index.html">CZ</a></span>'
)
# Add a conversion-oriented action after the services cards.
needle = '</div></div></section>\n<section><div class="wrap regions-grid">'
cta = '</div><div style="margin-top:28px;padding:28px 30px;background:#fff;border:1px solid var(--line);border-radius:24px;display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;box-shadow:var(--shadow-soft)"><div style="max-width:650px"><h3 style="font-size:30px">Готовы к выходу на новый рынок?</h3><p style="margin-top:10px;color:var(--muted);line-height:1.65">Проверьте готовность компании к международному масштабированию и получите оценку по четырём ключевым направлениям.</p></div><div class="btns" style="margin:0"><a class="btn btn-primary" href="readiness.html" target="_blank" rel="noopener">Оценить готовность</a><a class="btn btn-secondary" href="#contact" style="color:var(--navy);border-color:var(--line);background:#fff">Обсудить задачу</a></div></div></div></section>\n<section><div class="wrap regions-grid">'
if needle in s and 'readiness.html' not in s:
    s = s.replace(needle, cta, 1)

# Rebuild the regional markets module into a cleaner editorial layout.
old_regions = '''<section><div class="wrap regions-grid"><div class="regions-copy"><h2>Работаем на нескольких региональных контурах</h2><p>GO BIG соединяет компании с рынками, партнёрами и инфраструктурой роста там, где у нас есть собственная сеть и рабочие связи.</p><div class="chips"><span>Европа</span><span>Балканы</span><span>Сербия</span><span>Центральная Азия</span><span>GCC</span><span>MENA</span></div><div class="note-box">Сильная сторона подхода — сочетание локального присутствия, международной кооперации и компетенций в технологиях, автоматизации и развитии команд.</div></div><div class="regions-media"><img src="assets/Belgrad1.jpg" alt="Белград — один из региональных контуров GO BIG"/><div class="regions-panel"><div class="regions-stat"><strong>01</strong><span>от идеи — к конкретной географии</span></div><div class="regions-stat"><strong>02</strong><span>через сеть локальных партнёров</span></div><div class="regions-stat"><strong>03</strong><span>в прямом диалоге с рынком</span></div><div class="regions-stat"><strong>04</strong><span>без хаотичного набора активностей</span></div></div></div></div></section>'''
new_regions = '''<section class="regions-modern"><div class="wrap"><div class="regions-modern-shell"><div class="regions-modern-copy"><div class="regions-modern-kicker">География работы</div><h2>Работаем на нескольких региональных контурах</h2><p>GO BIG соединяет компании с рынками, партнёрами и инфраструктурой роста там, где у нас есть собственная сеть и рабочие связи.</p><div class="market-chips"><span>Европа</span><span>Балканы</span><span>Сербия</span><span>Центральная Азия</span><span>GCC</span><span>MENA</span></div></div><div class="regions-modern-media"><img src="assets/poster_event_12352311.jpg" alt="Деловое обсуждение и международное сотрудничество GO BIG"/><div class="regions-modern-shade"></div><div class="approach-overlay"><span>Сильная сторона подхода</span><p>Локальное присутствие, международная кооперация и компетенции в технологиях, автоматизации и развитии команд.</p></div></div></div><div class="regions-flow"><div class="flow-item"><b>01</b><span>От идеи — к конкретной географии</span></div><div class="flow-item"><b>02</b><span>Через сеть локальных партнёров</span></div><div class="flow-item"><b>03</b><span>В прямом диалоге с рынком</span></div><div class="flow-item"><b>04</b><span>Без хаотичного набора активностей</span></div></div></div></section>'''
if old_regions in s:
    s = s.replace(old_regions, new_regions, 1)

regions_css = '''<style>
.regions-modern{padding:92px 0;background:#fff}
.regions-modern-shell{display:grid;grid-template-columns:minmax(0,.82fr) minmax(0,1.18fr);gap:28px;align-items:stretch}
.regions-modern-copy{padding:22px 26px 18px 4px;display:flex;flex-direction:column;justify-content:center}
.regions-modern-kicker{font-size:12px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--green);margin-bottom:18px}
.regions-modern-copy h2{max-width:10.5ch;font-size:clamp(38px,4.2vw,58px);line-height:.99}
.regions-modern-copy>p{margin-top:24px;max-width:590px;color:var(--muted);font-size:17px;line-height:1.72}
.market-chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:30px}
.market-chips span{padding:11px 16px;border-radius:999px;background:#f1f3f5;border:1px solid rgba(11,44,99,.04);color:var(--navy);font-size:13px;font-weight:800}
.regions-modern-media{position:relative;min-height:585px;overflow:hidden;border-radius:30px;background:#1b2229;box-shadow:var(--shadow)}
.regions-modern-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 46%;filter:saturate(.70) contrast(1.04) brightness(.82) grayscale(.10)}
.regions-modern-shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,23,32,.06) 0%,rgba(22,28,34,.12) 44%,rgba(22,27,32,.72) 100%)}
.approach-overlay{position:absolute;left:30px;right:30px;bottom:28px;z-index:2;max-width:650px;padding:22px 24px;border:1px solid rgba(255,255,255,.14);border-radius:22px;background:rgba(35,41,47,.78);backdrop-filter:blur(10px);color:#fff}
.approach-overlay span{display:block;margin-bottom:9px;font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.68)}
.approach-overlay p{font-size:16px;line-height:1.58;color:#fff}
.regions-flow{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px}
.flow-item{min-height:112px;padding:20px 20px 18px;border:1px solid var(--line);border-radius:20px;background:#fff;box-shadow:0 10px 26px rgba(17,29,47,.04)}
.flow-item b{display:block;font:700 25px/1 var(--font-heading);color:var(--green);margin-bottom:12px}
.flow-item span{font-size:14px;font-weight:700;line-height:1.45;color:#314057}
@media(max-width:980px){.regions-modern-shell{grid-template-columns:1fr}.regions-modern-copy{padding:0 0 8px}.regions-modern-copy h2{max-width:15ch}.regions-modern-media{min-height:520px}.regions-flow{grid-template-columns:repeat(2,1fr)}}
@media(max-width:620px){.regions-modern{padding:72px 0}.regions-modern-media{min-height:500px}.regions-modern-media img{object-position:52% center}.approach-overlay{left:18px;right:18px;bottom:18px;padding:18px}.approach-overlay p{font-size:14px}.regions-flow{grid-template-columns:1fr}.flow-item{min-height:auto}.market-chips span{padding:10px 13px;font-size:12px}}
</style>'''
if 'regions-modern-shell' in s and '.regions-modern-shell{' not in s:
    s = s.replace('</head>', regions_css + '\n</head>', 1)

link = '<link rel="stylesheet" href="international-hero.css"/>'
if 'international-hero.css' not in s:
    s = s.replace('</head>', link + '\n</head>', 1)
p.write_text(s, encoding='utf-8')

for p in Path('dist').glob('*.html'):
    s = p.read_text(encoding='utf-8')
    s = s.replace('href="/assets/', 'href="assets/')
    s = s.replace('src="/assets/', 'src="assets/')
    s = s.replace("url('/assets/", "url('assets/")
    for name in ['index.html','international.html','digital-ai.html','education-hr.html','readiness.html']:
        s = s.replace(f'href="/{name}"', f'href="{name}"')
    p.write_text(s, encoding='utf-8')
PY
cp home-premium.css dist/home-premium.css
cp international-hero.css dist/international-hero.css
sed -i "s#url('/assets/#url('assets/#g" dist/international-hero.css
touch dist/.nojekyll
