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

# Rebuild the International hero image from text chunks committed to GitHub.
chunks = Path('assets/.city-hero')
if chunks.is_dir():
    encoded = ''.join(p.read_text(encoding='utf-8').strip() for p in sorted(chunks.glob('part*')))
    out = Path('dist/assets/international-city-hero.webp')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(encoded))
    shutil.rmtree(Path('dist/assets/.city-hero'), ignore_errors=True)

p = Path('dist/index.html')
s = p.read_text(encoding='utf-8')
link = '<link rel="stylesheet" href="/home-premium.css"/>'
if link not in s:
    s = s.replace('</head>', link + '\n</head>', 1)
p.write_text(s, encoding='utf-8')

p = Path('dist/international.html')
s = p.read_text(encoding='utf-8')
link = '<link rel="stylesheet" href="/international-hero.css"/>'
if link not in s:
    s = s.replace('</head>', link + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
PY
cp home-premium.css dist/home-premium.css
cp international-hero.css dist/international-hero.css
