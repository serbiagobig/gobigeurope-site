#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
PAGES = [ROOT / 'berry-harvesting.html', ROOT / 'en' / 'berry-harvesting.html', ROOT / 'cz' / 'berry-harvesting.html']

for path in PAGES:
    if not path.exists():
        raise SystemExit(f'Missing berry page: {path}')
    text = path.read_text(encoding='utf-8')
    pattern = re.compile(r'<section class="section soft gentle-reference"(?![^>]*\bid=)[^>]*>', re.I)
    text, count = pattern.subn('<section id="gentle" class="section soft gentle-reference">', text, count=1)
    if count == 0 and not re.search(r'<section\b[^>]*\bid=["\']gentle["\'][^>]*class=["\'][^"\']*gentle-reference', text, re.I):
        raise SystemExit(f'Could not install #gentle anchor in {path}')
    path.write_text(text, encoding='utf-8')
    print(f'PASS: #gentle anchor present in {path}')
