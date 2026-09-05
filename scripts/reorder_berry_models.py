#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
paths = [
    root / 'berry-harvesting.html',
    root / 'en' / 'berry-harvesting.html',
    root / 'cz' / 'berry-harvesting.html',
]

gentle_re = re.compile(r'<section class="section soft gentle-crops">.*?</section>', re.S)
models_re = re.compile(r'<section class="section dark" id="models">.*?</section>', re.S)

for p in paths:
    if not p.exists():
        raise SystemExit(f'Missing berry page: {p}')
    s = p.read_text(encoding='utf-8')
    gentle = gentle_re.search(s)
    models = models_re.search(s)
    if not gentle:
        raise SystemExit(f'Gentle crop module not found in {p}')
    if not models:
        raise SystemExit(f'Models module not found in {p}')

    models_html = models.group(0)
    s = s[:models.start()] + s[models.end():]
    gentle = gentle_re.search(s)
    insert_at = gentle.end()
    s = s[:insert_at] + models_html + s[insert_at:]

    if s.find('gentle-crops') > s.find('id="models"'):
        raise SystemExit(f'Models section order validation failed in {p}')
    p.write_text(s, encoding='utf-8')
    print(f'Moved models section after gentle crop module: {p}')
