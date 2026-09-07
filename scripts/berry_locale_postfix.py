#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

replacements = {
    'en': {
        'Регулируемые импульсы воздуха отделяют зрелую ягоду и фрукты без жёсткого механического воздействия на растение. Затем урожай мягко принимается и направляется в систему сбора.': 'Controlled air pulses detach ripe berries and fruit without harsh mechanical impact on the plant. The crop is then received gently and guided into the collection system.',
        'Воздушно-импульсное воздействие': 'Air-pulse action',
        'Управляемые импульсы воздуха отделяют зрелые плоды от растения. Скорость и частота воздействия регулируются под культуру и условия уборки.': 'Controlled air pulses detach ripe fruit from the plant. Air speed and pulse frequency are adjusted to the crop and harvesting conditions.',
        '>Другое<': '>Other<',
        'value="Другое"': 'value="Other"',
    },
    'cz': {
        'Регулируемые импульсы воздуха отделяют зрелую ягоду и фрукты без жёсткого механического воздействия на растение. Затем урожай мягко принимается и направляется в систему сбора.': 'Řízené vzduchové impulsy oddělují zralé bobule a ovoce bez tvrdého mechanického působení na rostlinu. Úroda je poté šetrně zachycena a vedena do sběrného systému.',
        'Воздушно-импульсное воздействие': 'Působení vzduchových impulzů',
        'Управляемые импульсы воздуха отделяют зрелые плоды от растения. Скорость и частота воздействия регулируются под культуру и условия уборки.': 'Řízené vzduchové impulsy oddělují zralé plody od rostliny. Rychlost vzduchu a frekvence impulsů se nastavují podle plodiny a podmínek sklizně.',
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
