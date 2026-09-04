#!/usr/bin/env python3
from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else 'dist')
fixes = {
    'en': {
        'Механизированная уборка ягод': 'Mechanized berry harvesting',
        'до 500+ кг/час': 'up to 500+ kg/hour',
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
        'Бесконтактная технология сбора спелой ягоды и фруктов управляемыми импульсами воздуха. ': 'Contactless harvesting of ripe berries and fruit using controlled air pulses. ',
        'Снижение зависимости от сезонных рабочих': 'Reduced dependence on seasonal labour',
        'при бережном воздействии на растение и урожай.': 'while treating plants and crops gently.',
        'Эффективность': 'Efficiency',
        'Мы создаем новую экономику уборки': 'We create a new economics of harvesting',
        'Производительность, которая меняет экономику': 'Productivity that changes the economics',
        'Для ягодных плантаций в подходящих условиях.': 'For berry plantations under suitable conditions.',
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
        'до 500+ кг/час': 'až 500+ kg/h',
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
        'Бесконтактная технология сбора спелой ягоды и фруктов управляемыми импульсами воздуха. ': 'Bezkontaktní sklizeň zralých bobulí a ovoce pomocí řízených vzduchových impulsů. ',
        'Снижение зависимости от сезонных рабочих': 'Nižší závislost na sezónních pracovnících',
        'при бережном воздействии на растение и урожай.': 'při šetrném působení na rostliny i úrodu.',
        'Эффективность': 'Efektivita',
        'Мы создаем новую экономику уборки': 'Vytváříme novou ekonomiku sklizně',
        'Производительность, которая меняет экономику': 'Produktivita, která mění ekonomiku sklizně',
        'Для ягодных плантаций в подходящих условиях.': 'Pro plantáže bobulovin ve vhodných podmínkách.',
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

tech_content = {
    'ru': {
        'eyebrow': 'Технология',
        'title': 'Сила природы — под контролем',
        'lead': 'Регулируемые импульсы воздуха отделяют зрелую ягоду и фрукты без жёсткого механического воздействия на растение. Затем урожай мягко принимается и направляется в систему сбора.',
        'flow': ('Отделить', 'Принять', 'Адаптировать к культуре'),
        'cards': [
            ('01', '/%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%92%D0%BE%D0%B7%D0%B4%D1%83%D1%88%D0%BD%D0%B0%D1%8F%20%D1%83%D0%B1%D0%BE%D1%80%D0%BA%D0%B0.png', 'Воздушно-импульсное воздействие', 'Управляемые импульсы воздуха отделяют зрелые плоды от растения. Скорость и частота воздействия регулируются под культуру и условия уборки.'),
            ('02', '/%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%9F%D0%BD%D0%B5%D0%B2%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BF%D0%BE%D0%B4%D1%83%D1%88%D0%BA%D0%B8.png', 'Мягкая система приёма', 'Эластичные пневматические элементы принимают отделившийся урожай, поглощают энергию падения и помогают снизить риск повреждения.'),
            ('03', '/%D0%BA%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%9C%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BF%D0%B0%D0%BB%D1%8C%D1%86%D1%8B.png', 'Адаптация к культуре', 'Направляющие элементы помогают работать с различной формой куста и ветвей. При необходимости механическое воздействие дополняет воздушный импульс и остаётся под контролем оператора.'),
        ],
    },
    'en': {
        'eyebrow': 'Technology',
        'title': 'The power of nature — under control',
        'lead': 'Controlled air pulses detach ripe berries and fruit without harsh mechanical impact on the plant. The crop is then received gently and guided into the collection system.',
        'flow': ('Detach', 'Receive', 'Adapt to the crop'),
        'cards': [
            ('01', '/%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%92%D0%BE%D0%B7%D0%B4%D1%83%D1%88%D0%BD%D0%B0%D1%8F%20%D1%83%D0%B1%D0%BE%D1%80%D0%BA%D0%B0.png', 'Air-pulse action', 'Controlled air pulses detach ripe fruit from the plant. Air speed and pulse frequency are adjusted to the crop and harvesting conditions.'),
            ('02', '/%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%9F%D0%BD%D0%B5%D0%B2%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BF%D0%BE%D0%B4%D1%83%D1%88%D0%BA%D0%B8.png', 'Gentle receiving system', 'Elastic pneumatic elements receive the detached crop, absorb impact energy and help reduce the risk of damage.'),
            ('03', '/%D0%BA%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%9C%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BF%D0%B0%D0%BB%D1%8C%D1%86%D1%8B.png', 'Adaptation to the crop', 'Guiding elements help the machine work with different bush shapes and branch structures. When needed, controlled mechanical action complements the air pulse.'),
        ],
    },
    'cz': {
        'eyebrow': 'Technologie',
        'title': 'Síla přírody — pod kontrolou',
        'lead': 'Řízené vzduchové impulsy oddělují zralé bobule a ovoce bez tvrdého mechanického působení na rostlinu. Úroda je poté šetrně zachycena a vedena do sběrného systému.',
        'flow': ('Oddělit', 'Zachytit', 'Přizpůsobit plodině'),
        'cards': [
            ('01', '/%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%92%D0%BE%D0%B7%D0%B4%D1%83%D1%88%D0%BD%D0%B0%D1%8F%20%D1%83%D0%B1%D0%BE%D1%80%D0%BA%D0%B0.png', 'Vzduchově pulzní působení', 'Řízené vzduchové impulsy oddělují zralé plody od rostliny. Rychlost vzduchu a frekvence impulsů se nastavují podle plodiny a podmínek sklizně.'),
            ('02', '/%D0%9A%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%9F%D0%BD%D0%B5%D0%B2%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BF%D0%BE%D0%B4%D1%83%D1%88%D0%BA%D0%B8.png', 'Šetrný systém zachycení', 'Elastické pneumatické prvky zachycují oddělenou úrodu, absorbují energii pádu a pomáhají snižovat riziko poškození.'),
            ('03', '/%D0%BA%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%BA%D0%B0%20%D0%9C%D0%B5%D1%85%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5%20%D0%BF%D0%B0%D0%BB%D1%8C%D1%86%D1%8B.png', 'Přizpůsobení plodině', 'Vodicí prvky pomáhají pracovat s různým tvarem keřů a větví. V případě potřeby řízené mechanické působení doplňuje vzduchový impuls.'),
        ],
    },
}

tech_css = '''
.technology-visual{padding:72px 0 76px}
.technology-visual .lead{max-width:900px}
.tech-flow{display:flex;align-items:center;gap:10px;margin-top:28px;color:#8ce9b5;font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}
.tech-flow i{display:block;width:36px;height:1px;background:rgba(140,233,181,.55)}
.tech-visual-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:24px}
.tech-visual-card{overflow:hidden;border:1px solid rgba(255,255,255,.14);border-radius:24px;background:#1c2d3b}
.tech-visual-media{height:200px;overflow:hidden;background:#0e1c28}
.tech-visual-media img{display:block;width:100%;height:100%;object-fit:cover;object-position:center}
.tech-visual-body{padding:22px 24px 25px}
.tech-visual-num{display:block;color:#78d9a5;font-size:27px;font-weight:800;line-height:1}
.tech-visual-card h3{margin:15px 0 0;font:700 27px/1.07 var(--serif);color:#fff}
.tech-visual-card p{margin:12px 0 0;color:rgba(255,255,255,.72);font-size:14px;line-height:1.58}
@media(max-width:900px){.technology-visual{padding:56px 0}.tech-flow{flex-wrap:wrap}.tech-visual-grid{grid-template-columns:1fr}.tech-visual-media{height:230px}}
'''


def render_tech(lang):
    t = tech_content[lang]
    cards = ''.join(
        f'<article class="tech-visual-card"><div class="tech-visual-media"><img src="{img}" alt="{title}"/></div><div class="tech-visual-body"><b class="tech-visual-num">{num}</b><h3>{title}</h3><p>{body}</p></div></article>'
        for num, img, title, body in t['cards']
    )
    a, b, c = t['flow']
    return (
        '<section class="section dark technology-visual" id="technology"><div class="wrap">'
        f'<div class="eyebrow">{t["eyebrow"]}</div><h2>{t["title"]}</h2><p class="lead">{t["lead"]}</p>'
        f'<div class="tech-flow"><span>{a}</span><i></i><span>{b}</span><i></i><span>{c}</span></div>'
        f'<div class="tech-visual-grid">{cards}</div></div></section>'
    )

for lang, mapping in fixes.items():
    p = root / lang / 'berry-harvesting.html'
    if not p.exists():
        raise SystemExit(f'Missing localized berry page: {p}')
    s = p.read_text(encoding='utf-8')
    for old in sorted(mapping, key=len, reverse=True):
        s = s.replace(old, mapping[old])
    p.write_text(s, encoding='utf-8')
    print(f'Cleaned residual berry locale strings: {lang}')

paths = {
    'ru': root / 'berry-harvesting.html',
    'en': root / 'en' / 'berry-harvesting.html',
    'cz': root / 'cz' / 'berry-harvesting.html',
}
pattern = re.compile(r'<section class="section dark" id="technology">.*?</section>', re.S)
for lang, p in paths.items():
    if not p.exists():
        raise SystemExit(f'Missing berry page for technology replacement: {p}')
    s = p.read_text(encoding='utf-8')
    s2, count = pattern.subn(render_tech(lang), s, count=1)
    if count != 1:
        raise SystemExit(f'Could not replace technology section in {p}')
    if tech_css not in s2:
        s2 = s2.replace('</style>', tech_css + '</style>', 1)
    p.write_text(s2, encoding='utf-8')
    print(f'Rebuilt visual berry technology module: {lang}')
