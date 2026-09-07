#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

replacements = {
    'en': {
        'Регулируемые импульсы воздуха отделяют зрелую ягоду и фрукты без жёсткого механического воздействия на растение. Затем урожай мягко принимается и направляется в систему сбора.': 'Controlled air pulses detach ripe berries and fruit without harsh mechanical impact on the plant. The crop is then received gently and guided into the collection system.',
        'Воздушно-импульсное воздействие': 'Air-pulse action',
        'Управляемые импульсы воздуха отделяют зрелые плоды от растения. Скорость и частота воздействия регулируются под культуру и условия уборки.': 'Controlled air pulses detach ripe fruit from the plant. Air speed and pulse frequency are adjusted to the crop and harvesting conditions.',
        'Мягкая система приёма': 'Gentle receiving system',
        'Эластичные пневматические элементы принимают отделившийся урожай, поглощают энергию падения и помогают снизить риск повреждения.': 'Elastic pneumatic elements receive the detached crop, absorb impact energy and help reduce the risk of damage.',
        'Адаптация к культуре': 'Adaptation to the crop',
        'Направляющие элементы помогают работать с различной формой куста и ветвей. При необходимости механическое воздействие дополняет воздушный импульс и остаётся под контролем оператора.': 'Guiding elements help the machine work with different bush shapes and branch structures. When needed, controlled mechanical action complements the air pulse and remains under operator control.',
        'Guiding elements помогают работать с различной формой куста и ветвей. При необходимости механическое воздействие дополняет воздушный импульс и остаётся под контролем оператора.': 'Guiding elements help the machine work with different bush shapes and branch structures. When needed, controlled mechanical action complements the air pulse and remains under operator control.',
        'Под масштаб плантации': 'For every plantation scale',
        'Характеристики и стоимость предоставляются по запросу.': 'Specifications and pricing are available on request.',
        'Прицепная версия': 'Trailed version',
        'Привод от ВОМ. Для хозяйств с подходящим трактором.': 'PTO-driven. Designed for farms with a suitable tractor.',
        'Автономная прицепная версия': 'Autonomous trailed version',
        'Собственный дизельный двигатель. Больше независимости от мощности тягача.': 'Own diesel engine for greater independence from tractor power.',
        'Самоходная версия': 'Self-propelled version',
        'Для крупных хозяйств и интенсивной эксплуатации.': 'Designed for large farms and intensive operation.',
        '>Другое<': '>Other<',
        'value="Другое"': 'value="Other"',
    },
    'cz': {
        'Регулируемые импульсы воздуха отделяют зрелую ягоду и фрукты без жёсткого механического воздействия на растение. Затем урожай мягко принимается и направляется в систему сбора.': 'Řízené vzduchové impulsy oddělují zralé bobule a ovoce bez tvrdého mechanického působení na rostlinu. Úroda je poté šetrně zachycena a vedena do sběrného systému.',
        'Воздушно-импульсное воздействие': 'Vzduchově pulzní působení',
        'Управляемые импульсы воздуха отделяют зрелые плоды от растения. Скорость и частота воздействия регулируются под культуру и условия уборки.': 'Řízené vzduchové impulsy oddělují zralé plody od rostliny. Rychlost vzduchu a frekvence impulsů se nastavují podle plodiny a podmínek sklizně.',
        'Мягкая система приёма': 'Šetrný systém zachycení',
        'Эластичные пневматические элементы принимают отделившийся урожай, поглощают энергию падения и помогают снизить риск повреждения.': 'Elastické pneumatické prvky zachycují oddělenou úrodu, absorbují energii pádu a pomáhají snižovat riziko poškození.',
        'Адаптация к культуре': 'Přizpůsobení plodině',
        'Направляющие элементы помогают работать с различной формой куста и ветвей. При необходимости механическое воздействие дополняет воздушный импульс и остаётся под контролем оператора.': 'Vodicí prvky pomáhají pracovat s různým tvarem keřů a větví. V případě potřeby řízené mechanické působení doplňuje vzduchový impuls a zůstává pod kontrolou obsluhy.',
        'Vodicí prvky помогают работать с различной формой куста и ветвей. При необходимости механическое воздействие дополняет воздушный импульс и остаётся под контролем оператора.': 'Vodicí prvky pomáhají pracovat s různým tvarem keřů a větví. V případě potřeby řízené mechanické působení doplňuje vzduchový impuls a zůstává pod kontrolou obsluhy.',
        'Под масштаб плантации': 'Podle rozsahu plantáže',
        'Характеристики и стоимость предоставляются по запросу.': 'Technické parametry a cena jsou k dispozici na vyžádání.',
        'Прицепная версия': 'Přívěsná verze',
        'Привод от ВОМ. Для хозяйств с подходящим трактором.': 'Pohon přes PTO. Pro farmy s vhodným traktorem.',
        'Автономная прицепная версия': 'Autonomní přívěsná verze',
        'Собственный дизельный двигатель. Больше независимости от мощности тягача.': 'Vlastní dieselový motor. Vyšší nezávislost na výkonu traktoru.',
        'Самоходная версия': 'Samojízdná verze',
        'Для крупных хозяйств и интенсивной эксплуатации.': 'Pro velké farmy a intenzivní provoz.',
        '>Другое<': '>Jiné<',
        'value="Другое"': 'value="Jiné"',
    },
}

for locale, repls in replacements.items():
    page = root / locale / 'berry-harvesting.html'
    if not page.exists():
        raise SystemExit(f'Missing localized berry page: {page}')
    s = page.read_text(encoding='utf-8')
    for old, new in repls.items():
        s = s.replace(old, new)
    page.write_text(s, encoding='utf-8')
    print(f'Applied final berry locale postfix: {locale}')
