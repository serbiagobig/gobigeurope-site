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
# Use the existing business-discussion image in the regional markets block.
s = s.replace(
    '<img src="assets/Belgrad1.jpg" alt="Белград — один из региональных контуров GO BIG"/>',
    '<img src="assets/poster_event_12352311.jpg" alt="Деловое обсуждение и международное сотрудничество GO BIG"/>'
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
