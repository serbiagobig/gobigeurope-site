#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
RU = ROOT / 'berry-harvesting.html'
if not RU.exists():
    raise SystemExit('Missing approved berry-harvesting.html')


def strip_section_with(text, marker):
    # Remove the complete section that contains a rejected marker. The tempered
    # pattern prevents crossing a neighbouring <section> boundary.
    rx = re.compile(
        r'<section\b[^>]*>(?:(?!<section\b).)*?' + re.escape(marker) + r'(?:(?!<section\b).)*?</section>',
        re.S | re.I,
    )
    return rx.sub('', text)

s = RU.read_text(encoding='utf-8')

# Make the historical transformer idempotent. It used to turn an already approved
# metric into "до до 500+ кг/час" on a second pass.
while 'до до 500+ кг/час' in s:
    s = s.replace('до до 500+ кг/час', 'до 500+ кг/час')

# These four modules were explicitly removed from the approved page and must never
# re-enter the published source.
for marker in (
    'Проверьте, подходит ли ваша плантация',
    'Механизация — это процесс, а не покупка одной машины',
    'Планируете новую ягодную плантацию?',
    'Когда стоит рассматривать механизированную уборку',
):
    s = strip_section_with(s, marker)

# Remove any stale subnav links to rejected modules.
s = re.sub(r'<a\s+href=["\']#fit["\'][^>]*>.*?</a>', '', s, flags=re.S | re.I)

RU.write_text(s, encoding='utf-8')

# Normalise already-generated locale pages if this script is run after localisation.
for rel, fixes in {
    'en/berry-harvesting.html': {
        'до up to 500+ kg/hour': 'up to 500+ kg/hour',
        'до 500+ kg/hour': 'up to 500+ kg/hour',
    },
    'cz/berry-harvesting.html': {
        'до až 500+ kg/h': 'až 500+ kg/h',
        'до 500+ kg/h': 'až 500+ kg/h',
    },
}.items():
    p = ROOT / rel
    if p.exists():
        t = p.read_text(encoding='utf-8')
        for a, b in fixes.items():
            t = t.replace(a, b)
        p.write_text(t, encoding='utf-8')

# Hard guardrails for the approved RU state.
final = RU.read_text(encoding='utf-8')
required = (
    'Инновационная технология',
    'Воздушно-импульсная уборка',
    'Типичные проблемы ручной уборки',
    'Мы создаем новую экономику уборки',
    'berry-harvesting-web.mp4',
    'Не просто оборудование. Система внедрения.',
    'Анализ хозяйства', 'Подбор технологии', 'Оценка участка', 'Поставка',
    'Запуск', 'Обучение', 'Сервис', 'Запасные части',
)
for marker in required:
    if marker not in final:
        raise SystemExit(f'Approved berry marker missing after lock: {marker}')

for marker in (
    'Проверьте, подходит ли ваша плантация',
    'Механизация — это процесс, а не покупка одной машины',
    'Планируете новую ягодную плантацию?',
    'Когда стоит рассматривать механизированную уборку',
    'до до 500+ кг/час',
):
    if marker in final:
        raise SystemExit(f'Rejected berry content remains after lock: {marker}')

print('PASS: authoritative berry page lock applied')
