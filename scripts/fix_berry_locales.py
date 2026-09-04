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
        'Эффективность': 'Efficiency',
        'Мы создаем новую экономику уборки': 'We create a new economics of harvesting',
        'Производительность, которая меняет экономику': 'Productivity that changes the economics',
        'Типичные проблемы ручной уборки': 'Typical challenges of manual harvesting',
        'Когда урожай есть, а ручной сбор становится ограничением': 'When the crop is ready but manual harvesting becomes the bottleneck',
        'Ручная уборка влияет не только на затраты. Она определяет скорость сбора, качество партии, возможность масштабировать площадь и срок хранения ягоды.': 'Manual harvesting affects more than cost. It determines harvest speed, batch quality, the ability to scale plantation area and berry shelf life.',
        'Операционные ограничения': 'Operational constraints',
        'Люди · сроки · масштаб': 'Labour · timing · scale',
        'Дефицит сезонных рабочих': 'Seasonal labour shortages',
        'Нужное количество сборщиков трудно найти именно в короткий период пикового созревания.': 'It is difficult to find enough pickers during the short period of peak ripening.',
        'Рост стоимости ручного труда': 'Rising manual labour costs',
        'Увеличение стоимости рабочей силы напрямую повышает себестоимость уборки урожая.': 'Higher labour costs directly increase the cost of harvesting.',
        'Непредсказуемые сроки уборки': 'Unpredictable harvest timing',
        'Производительность зависит от количества людей, их опыта, погоды и ежедневной доступности персонала.': 'Productivity depends on crew size, experience, weather and day-to-day labour availability.',
        'Ограничение масштаба хозяйства': 'Limits on farm scale',
        'Чем больше площадь плантации, тем сложнее обеспечить достаточное количество сборщиков одновременно.': 'The larger the plantation, the harder it becomes to provide enough pickers at the same time.',
        'Риски для качества урожая': 'Risks to crop quality',
        'Ягода · зрелость · хранение': 'Fruit · ripeness · shelf life',
        'Повреждение ягод': 'Berry damage',
        'Сдавливание пальцами, падение и давление ягод друг на друга вызывают вмятины и микроповреждения.': 'Finger pressure, drops and berries pressing against each other can cause bruising and micro-damage.',
        'Удаление защитного воскового налёта': 'Loss of the protective wax bloom',
        'Частые прикосновения ухудшают внешний вид ягоды и снижают её естественную защиту.': 'Frequent handling can worsen appearance and reduce the berry’s natural protection.',
        'Неоднородная зрелость партии': 'Inconsistent ripeness within the batch',
        'Из-за усталости или недостаточного опыта сборщики могут снимать недозрелые и перезрелые ягоды.': 'Fatigue or limited experience can lead pickers to harvest both underripe and overripe berries.',
        'Перегрев и задержка охлаждения': 'Overheating and delayed cooling',
        'Низкая скорость сбора увеличивает время нахождения ягод на плантации, что сокращает срок хранения.': 'Slow harvesting increases the time berries remain in the field, which can shorten shelf life.',
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
        'Эффективность': 'Efektivita',
        'Мы создаем новую экономику уборки': 'Vytváříme novou ekonomiku sklizně',
        'Производительность, которая меняет экономику': 'Produktivita, která mění ekonomiku sklizně',
        'Типичные проблемы ручной уборки': 'Typické problémy ruční sklizně',
        'Когда урожай есть, а ручной сбор становится ограничением': 'Když je úroda připravena, ale ruční sklizeň se stává omezením',
        'Ручная уборка влияет не только на затраты. Она определяет скорость сбора, качество партии, возможность масштабировать площадь и срок хранения ягоды.': 'Ruční sklizeň neovlivňuje jen náklady. Určuje rychlost sklizně, kvalitu partie, možnost rozšiřovat plochu i dobu skladovatelnosti bobulí.',
        'Операционные ограничения': 'Provozní omezení',
        'Люди · сроки · масштаб': 'Lidé · termíny · rozsah',
        'Дефицит сезонных рабочих': 'Nedostatek sezónních pracovníků',
        'Нужное количество сборщиков трудно найти именно в короткий период пикового созревания.': 'Dostatečný počet sběračů je obtížné zajistit právě v krátkém období vrcholného dozrávání.',
        'Рост стоимости ручного труда': 'Rostoucí náklady na ruční práci',
        'Увеличение стоимости рабочей силы напрямую повышает себестоимость уборки урожая.': 'Vyšší cena pracovní síly přímo zvyšuje náklady na sklizeň.',
        'Непредсказуемые сроки уборки': 'Nepředvídatelné termíny sklizně',
        'Производительность зависит от количества людей, их опыта, погоды и ежедневной доступности персонала.': 'Výkonnost závisí na počtu pracovníků, jejich zkušenostech, počasí a každodenní dostupnosti personálu.',
        'Ограничение масштаба хозяйства': 'Omezení rozsahu hospodářství',
        'Чем больше площадь плантации, тем сложнее обеспечить достаточное количество сборщиков одновременно.': 'Čím větší je plocha plantáže, tím obtížnější je zajistit dostatečný počet sběračů současně.',
        'Риски для качества урожая': 'Rizika pro kvalitu úrody',
        'Ягода · зрелость · хранение': 'Plod · zralost · skladování',
        'Повреждение ягод': 'Poškození bobulí',
        'Сдавливание пальцами, падение и давление ягод друг на друга вызывают вмятины и микроповреждения.': 'Stlačení prsty, pády a tlak bobulí na sebe mohou způsobovat otlaky a mikro-poškození.',
        'Удаление защитного воскового налёта': 'Odstranění ochranného voskového povlaku',
        'Частые прикосновения ухудшают внешний вид ягоды и снижают её естественную защиту.': 'Častý kontakt zhoršuje vzhled bobulí a snižuje jejich přirozenou ochranu.',
        'Неоднородная зрелость партии': 'Nejednotná zralost sklizené partie',
        'Из-за усталости или недостаточного опыта сборщики могут снимать недозрелые и перезрелые ягоды.': 'Kvůli únavě nebo nedostatku zkušeností mohou pracovníci sklízet nedozrálé i přezrálé bobule.',
        'Перегрев и задержка охлаждения': 'Přehřívání a opožděné chlazení',
        'Низкая скорость сбора увеличивает время нахождения ягод на плантации, что сокращает срок хранения.': 'Nízká rychlost sklizně prodlužuje dobu, po kterou bobule zůstávají na plantáži, a tím může zkracovat jejich trvanlivost.',
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
