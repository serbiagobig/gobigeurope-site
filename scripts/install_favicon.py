#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path('dist')
SOURCE = Path('go-big-favicon.png')
TARGET = ROOT / 'go-big-favicon.png'

if not SOURCE.exists():
    raise SystemExit('Missing go-big-favicon.png in repository root')
if not ROOT.exists():
    raise SystemExit('Missing dist directory')

shutil.copy2(SOURCE, TARGET)

favicon_tag = '<link rel="icon" type="image/png" href="/go-big-favicon.png?v=20260914"/>'
apple_tag = '<link rel="apple-touch-icon" href="/go-big-favicon.png?v=20260914"/>'

updated = 0
for page in ROOT.rglob('*.html'):
    text = page.read_text(encoding='utf-8')
    if '</head>' not in text:
        continue

    # Remove any older GO BIG favicon tags so the final publish has one authority.
    lines = []
    for line in text.splitlines():
        if 'go-big-favicon.png' in line and ('rel="icon"' in line or 'rel="apple-touch-icon"' in line):
            continue
        lines.append(line)
    text = '\n'.join(lines)

    text = text.replace('</head>', favicon_tag + '\n' + apple_tag + '\n</head>', 1)
    page.write_text(text, encoding='utf-8')
    updated += 1

if updated == 0:
    raise SystemExit('No HTML pages received favicon tags')

print(f'Installed GO BIG favicon on {updated} HTML pages')
print(f'Published favicon: {TARGET}')
