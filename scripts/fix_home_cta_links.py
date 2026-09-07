#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

rules = {
    ROOT / 'index.html': {
        'href': 'international.html#goBigInquiry',
        'labels': ['Обсудить задачу', 'Отправить запрос', 'Назначить встречу'],
    },
    ROOT / 'en' / 'index.html': {
        'href': 'international.html#goBigInquiry',
        'labels': ['Discuss your challenge', 'Send an enquiry', 'Arrange a meeting'],
    },
    ROOT / 'cz' / 'index.html': {
        'href': 'international.html#goBigInquiry',
        'labels': ['Probrat váš záměr', 'Odeslat poptávku', 'Domluvit schůzku'],
    },
    ROOT / 'digital-ai.html': {
        'href': 'international.html#goBigInquiry',
        'labels': ['Обсудить задачу'],
    },
    ROOT / 'en' / 'digital-ai.html': {
        'href': 'international.html#goBigInquiry',
        'labels': ['Discuss your challenge'],
    },
    ROOT / 'cz' / 'digital-ai.html': {
        'href': 'international.html#goBigInquiry',
        'labels': ['Probrat váš záměr'],
    },
}

for page, cfg in rules.items():
    if not page.exists():
        raise SystemExit(f'Missing CTA page: {page}')
    s = page.read_text(encoding='utf-8')
    for label in cfg['labels']:
        pattern = re.compile(
            r'(<a\b[^>]*href=["\'])[^"\']*(["\'][^>]*>\s*' + re.escape(label) + r'\s*</a>)',
            re.I,
        )
        s, n = pattern.subn(r'\1' + cfg['href'] + r'\2', s)
        if n < 1:
            raise SystemExit(f'CTA not found in {page}: {label}')
        print(f'Routed {label} to {cfg["href"]}: {page} ({n} link(s))')
    page.write_text(s, encoding='utf-8')

# Final assertion: every target label on these pages must point to the cooperation application form.
for page, cfg in rules.items():
    s = page.read_text(encoding='utf-8')
    for label in cfg['labels']:
        matches = re.findall(
            r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>\s*' + re.escape(label) + r'\s*</a>',
            s,
            re.I,
        )
        if not matches or any(href != cfg['href'] for href in matches):
            raise SystemExit(f'CTA route validation failed in {page}: {label} -> {matches}')

print('PASS: homepage and Digital & AI CTA buttons route to the cooperation application form')
