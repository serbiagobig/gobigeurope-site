#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

targets = {
    ROOT / 'index.html': ('Обсудить задачу', 'international.html#goBigInquiry'),
    ROOT / 'en' / 'index.html': ('Discuss your challenge', 'international.html#goBigInquiry'),
    ROOT / 'cz' / 'index.html': ('Probrat váš záměr', 'international.html#goBigInquiry'),
}

for page, (label, href) in targets.items():
    if not page.exists():
        raise SystemExit(f'Missing homepage: {page}')
    s = page.read_text(encoding='utf-8')
    pattern = re.compile(r'(<a\b[^>]*href=["\'])[^"\']*(["\'][^>]*>\s*' + re.escape(label) + r'\s*</a>)', re.I)
    s, n = pattern.subn(r'\1' + href + r'\2', s)
    if n < 1:
        raise SystemExit(f'Homepage CTA not found in {page}: {label}')
    page.write_text(s, encoding='utf-8')
    print(f'Routed {label} to {href}: {page}')

# Final assertion: the primary CTA must no longer point to the old local #contact anchor.
for page, (label, href) in targets.items():
    s = page.read_text(encoding='utf-8')
    m = re.search(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>\s*' + re.escape(label) + r'\s*</a>', s, re.I)
    if not m or m.group(1) != href:
        raise SystemExit(f'Homepage CTA route validation failed in {page}')

print('PASS: homepage primary CTAs route to the international inquiry form')
