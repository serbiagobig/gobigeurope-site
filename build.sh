#!/bin/sh
set -eu
rm -rf dist
mkdir -p dist
cp index.html international.html digital-ai.html education-hr.html README.txt dist/ 2>/dev/null || true
if [ -d assets ]; then cp -R assets dist/assets; fi
python3 - <<'PY'
from pathlib import Path
p = Path('dist/index.html')
s = p.read_text(encoding='utf-8')
link = '<link rel="stylesheet" href="/home-premium.css"/>'
if link not in s:
    s = s.replace('</head>', link + '\n</head>', 1)
p.write_text(s, encoding='utf-8')
PY
cp home-premium.css dist/home-premium.css
