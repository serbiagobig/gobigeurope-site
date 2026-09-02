#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')

REPLACEMENTS = {
    'en': {
        'Международное сотрудничество': 'International Development',
        'Шаг ${current+1} из ${steps.length}': 'Step ${current+1} of ${steps.length}',
        'Пожалуйста, выберите хотя бы один вариант в обязательном вопросе.': 'Please select at least one option in the required question.',
        'Отправляем…': 'Sending…',
        'Не удалось отправить заявку. Пожалуйста, попробуйте ещё раз чуть позже.': 'We could not submit your enquiry. Please try again a little later.',
    },
    'cz': {
        'Международное сотрудничество': 'Mezinárodní rozvoj',
        'Шаг ${current+1} из ${steps.length}': 'Krok ${current+1} z ${steps.length}',
        'Пожалуйста, выберите хотя бы один вариант в обязательном вопросе.': 'Vyberte prosím alespoň jednu možnost v povinné otázce.',
        'Отправляем…': 'Odesíláme…',
        'Не удалось отправить заявку. Пожалуйста, попробуйте ещё раз чуть позже.': 'Poptávku se nepodařilo odeslat. Zkuste to prosím znovu později.',
    },
}

HOMEPAGE_PSEUDO_HEADING = {
    'en': 'Markets. Technology. People.',
    'cz': 'Trhy. Technologie. Lidé.',
}

failed = False
for lang, replacements in REPLACEMENTS.items():
    folder = ROOT / lang
    for path in sorted(folder.glob('*.html')):
        text = path.read_text(encoding='utf-8')
        for source, target in replacements.items():
            text = text.replace(source, target)

        # The homepage visual heading is rendered by a ::before pseudo-element
        # in the shared Russian CSS. Override it inside each localised homepage.
        if path.name == 'index.html':
            heading = HOMEPAGE_PSEUDO_HEADING[lang]
            override = (
                '<style id="locale-home-heading">'
                f'.direction-media-copy h3::before{{content:"{heading}" !important;}}'
                '</style>'
            )
            if 'id="locale-home-heading"' in text:
                text = re.sub(
                    r'<style id="locale-home-heading">.*?</style>',
                    override,
                    text,
                    count=1,
                    flags=re.S,
                )
            else:
                text = text.replace('</head>', override + '</head>', 1)

        path.write_text(text, encoding='utf-8')

        residuals = []
        for match in re.finditer(r'[А-Яа-яЁё][^<>\n]{0,160}', text):
            fragment = match.group(0).strip()
            if fragment and fragment not in residuals:
                residuals.append(fragment)
        if residuals:
            failed = True
            print(f'ERROR {lang}/{path.name}: Cyrillic remains')
            for fragment in residuals[:30]:
                print('  CYR:', fragment)
        else:
            print(f'PASS {lang}/{path.name}')

if failed:
    raise SystemExit('Localisation QA failed: untranslated Cyrillic remains.')
print('Localisation QA passed: EN and CZ contain no Cyrillic text.')
