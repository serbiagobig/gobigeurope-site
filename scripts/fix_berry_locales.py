#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
fixes = {
    'en': {
        'Механизированная уборка ягод': 'Mechanized berry harvesting',
        '500+ кг/час': '500+ kg/hour',
        'до 4 га/день': 'up to 4 ha/day',
        '20+ лет': '20+ years',
        '≈ 7–8 м': '≈ 7–8 m',
        'до 2,3 м': 'up to 2.3 m',
        'от 2,5 м': 'from 2.5 m',
        '≈ 2,6 м': '≈ 2.6 m',
        '2,6 м': '2.6 m',
    },
    'cz': {
        'Механизированная уборка ягод': 'Mechanizovaná sklizeň bobulovin',
        '500+ кг/час': '500+ kg/h',
        'до 4 га/день': 'až 4 ha/den',
        '20+ лет': '20+ let',
        '≈ 7–8 м': '≈ 7–8 m',
        'до 2,3 м': 'do 2,3 m',
        'от 2,5 м': 'od 2,5 m',
        '≈ 2,6 м': '≈ 2,6 m',
        '2,6 м': '2,6 m',
    },
}

for lang, mapping in fixes.items():
    p = root / lang / 'berry-harvesting.html'
    if not p.exists():
        raise SystemExit(f'Missing localized berry page: {p}')
    s = p.read_text(encoding='utf-8')
    for old in sorted(mapping, key=len, reverse=True):
        s = s.replace(old, mapping[old])
    p.write_text(s, encoding='utf-8')
    print(f'Cleaned residual berry locale strings: {lang}')
