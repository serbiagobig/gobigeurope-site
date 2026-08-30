#!/bin/sh
set -eu
rm -rf dist
mkdir -p dist
cp index.html international.html digital-ai.html education-hr.html README.txt dist/ 2>/dev/null || true
if [ -d assets ]; then cp -R assets dist/assets; fi
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
s = s.replace('Международное развитие — это не только экспорт.', 'The Advantages of Operating in International Markets in the Modern World')
link = '<link rel="stylesheet" href="international-hero.css"/>'
if 'international-hero.css' not in s:
    s = s.replace('</head>', link + '\n</head>', 1)
p.write_text(s, encoding='utf-8')

for p in Path('dist').glob('*.html'):
    s = p.read_text(encoding='utf-8')
    s = s.replace('href="/assets/', 'href="assets/')
    s = s.replace('src="/assets/', 'src="assets/')
    s = s.replace("url('/assets/", "url('assets/")
    for name in ['index.html','international.html','digital-ai.html','education-hr.html']:
        s = s.replace(f'href="/{name}"', f'href="{name}"')
    p.write_text(s, encoding='utf-8')
PY
cp home-premium.css dist/home-premium.css
cp international-hero.css dist/international-hero.css
sed -i "s#url('/assets/#url('assets/#g" dist/international-hero.css
touch dist/.nojekyll
