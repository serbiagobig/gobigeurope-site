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
        'Инновационная технология': 'Innovative technology',
        'Воздушно-импульсная уборка': 'Air-pulse harvesting',
        'Бесконтактная технология сбора спелой ягоды и фруктов управляемыми импульсами воздуха. Снижение зависимости от сезонных рабочих — при бережном воздействии на растение и урожай.': 'Contactless harvesting of ripe berries and fruit using controlled air pulses. Reduced dependence on seasonal labour while treating plants and crops gently.',
        'Эффективность': 'Efficiency',
        'Мы создаем новую экономику уборки': 'We create a new economics of harvesting',
        'Производительность, которая меняет экономику': 'Productivity that changes the economics',
        'Типичные проблемы ручной уборки': 'Typical challenges of manual harvesting',
        'Когда ручной сбор становится ограничением': 'When manual harvesting becomes the bottleneck',
        'Ручной сбор ограничивает скорость, масштаб хозяйства и стабильность качества ягоды.': 'Manual harvesting limits speed, farm scale and consistency of berry quality.',
        'Операционные ограничения': 'Operational constraints',
        'Люди · сроки · масштаб': 'Labour · timing · scale',
        'Дефицит сезонных рабочих': 'Seasonal labour shortages',
        'Рост стоимости ручного труда': 'Rising manual labour costs',
        'Непредсказуемые сроки уборки': 'Unpredictable harvest timing',
        'Ограничение масштаба хозяйства': 'Limits on farm scale',
        'Риски для качества урожая': 'Risks to crop quality',
        'Ягода · зрелость · хранение': 'Fruit · ripeness · shelf life',
        'Повреждение ягод': 'Berry damage',
        'Потеря защитного воскового налёта': 'Loss of the protective wax bloom',
        'Неоднородная зрелость партии': 'Inconsistent ripeness within the batch',
        'Перегрев и задержка охлаждения': 'Overheating and delayed cooling',
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
        'Инновационная технология': 'Inovativní technologie',
        'Воздушно-импульсная уборка': 'Vzduchově pulzní sklizeň',
        'Бесконтактная технология сбора спелой ягоды и фруктов управляемыми импульсами воздуха. Снижение зависимости от сезонных рабочих — при бережном воздействии на растение и урожай.': 'Bezkontaktní sklizeň zralých bobulí a ovoce pomocí řízených vzduchových impulsů. Nižší závislost na sezónních pracovnících při šetrném působení na rostliny i úrodu.',
        'Эффективность': 'Efektivita',
        'Мы создаем новую экономику уборки': 'Vytváříme novou ekonomiku sklizně',
        'Производительность, которая меняет экономику': 'Produktivita, která mění ekonomiku sklizně',
        'Типичные проблемы ручной уборки': 'Typické problémy ruční sklizně',
        'Когда ручной сбор становится ограничением': 'Když se ruční sklizeň stává omezením',
        'Ручной сбор ограничивает скорость, масштаб хозяйства и стабильность качества ягоды.': 'Ruční sklizeň omezuje rychlost, rozsah hospodářství a stabilitu kvality bobulí.',
        'Операционные ограничения': 'Provozní omezení',
        'Люди · сроки · масштаб': 'Lidé · termíny · rozsah',
        'Дефицит сезонных рабочих': 'Nedostatek sezónních pracovníků',
        'Рост стоимости ручного труда': 'Rostoucí náklady na ruční práci',
        'Непредсказуемые сроки уборки': 'Nepředvídatelné termíny sklizně',
        'Ограничение масштаба хозяйства': 'Omezení rozsahu hospodářství',
        'Риски для качества урожая': 'Rizika pro kvalitu úrody',
        'Ягода · зрелость · хранение': 'Plod · zralost · skladování',
        'Повреждение ягод': 'Poškození bobulí',
        'Потеря защитного воскового налёта': 'Ztráta ochranného voskového povlaku',
        'Неоднородная зрелость партии': 'Nejednotná zralost sklizené partie',
        'Перегрев и задержка охлаждения': 'Přehřívání a opožděné chlazení',
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
