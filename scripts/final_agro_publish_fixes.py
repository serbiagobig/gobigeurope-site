#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT=Path('dist')
ASSETS=ROOT/'assets'
ASSETS.mkdir(parents=True,exist_ok=True)

# These aliases used to be created by the Pages workflow after localisation.
# Create them inside the build so RU/EN/CZ are generated from the same final source.
asset_aliases={
    'AGRO TAG CENTR.png':'agro-tag-center.png',
    'карточка_1-removebg-preview.png':'agro-card-01.png',
    'Карточка 2.png':'agro-card-02.png',
    'Карточка 3.png':'agro-card-03.png',
    'Карточка 4.png':'agro-card-04.png',
    'Карточка 5.png':'agro-card-05.png',
    'Карточка 6.png':'agro-card-06.png',
    'Карточка 7.png':'agro-card-07.png',
    'Карточка 8.png':'agro-card-08.png',
    'Центральная Азия.png':'central-asia.png',
}
for src_name,dst_name in asset_aliases.items():
    src=Path(src_name)
    if not src.exists():
        raise SystemExit(f'Missing AGRO TAG visual asset: {src_name}')
    shutil.copy2(src,ASSETS/dst_name)

for css_name in ('agro-benefits-final.css','agro-asia-final.css'):
    src=Path('assets')/css_name
    if not src.exists():
        raise SystemExit(f'Missing AGRO TAG CSS: {css_name}')
    shutil.copy2(src,ASSETS/css_name)

p=ROOT/'agro-tag.html'
if not p.exists():
    raise SystemExit('Missing dist/agro-tag.html')
s=p.read_text(encoding='utf-8')

replacements={
    'https://shop.fpm.rs/media/catalogProduct/teskaFrezaRotas2606/FPM-ROTAS.png':'assets/agro-card-01.png',
    'https://agria.rs/wp-content/uploads/2023/08/zitka-featured-image.webp':'assets/agro-card-02.png',
    'https://bsk.rs/uploads/ck_editor/images/Rotoprotect-home.jpg':'assets/agro-card-03.png',
    'https://agria.rs/wp-content/uploads/2023/08/psp-agria-img.webp':'assets/agro-card-04.png',
    'https://site.caes.uga.edu/smallfruits/files/2022/07/BBHarvest-Photo1-1024x678.jpg':'assets/agro-card-05.png',
    'https://www.lifam-m.com/wp-content/uploads/2022/04/Nenaslovljeni-dizajn-1.jpg':'assets/agro-card-06.png',
    'https://agria.rs/wp-content/uploads/2023/08/services-agria-image.webp':'assets/agro-card-07.png',
    'https://www.fpm.rs/media/catalogProduct/mulcarZaRatarstvo/Mulcar-za-ratarstvo-1.png':'assets/agro-card-08.png',
}
for old,new in replacements.items():
    s=s.replace(old,new)

s=s.replace('Создадим новый центр агротехнологий','Станьте национальным или региональным партнёром AGRO TAG')
placeholder='<div class="partner-image-placeholder" role="img" aria-label="Место для изображения сельхозугодий в горной местности Центральной Азии"></div>'
image='<div class="partner-image-placeholder"><img src="assets/central-asia.png" alt="Сельхозугодья в горной местности Центральной Азии"/></div>'
s=s.replace(placeholder,image)

old_center='<div class="center-visual"><img src="assets/agro-tag-center.png" alt="AGRO TAG CENTR"/></div>'
new_center='''<div class="center-left-stack"><div class="center-visual"><img src="assets/agro-tag-center.png" alt="AGRO TAG CENTR"/></div><div class="partnership-roles"><div class="role-line"><span class="role-label partner-label">ПАРТНЁР</span><span class="role-text">рынок · клиенты · продажи · логистика · сервис</span></div><div class="role-line"><span class="role-label tag-label">AGRO TAG</span><span class="role-text">продукция · технологии · координация · обучение</span></div><div class="role-line"><span class="role-label joint-label">СОВМЕСТНО</span><span class="role-text">запуск · склад · развитие · локализация</span></div><div class="role-key"><small>Ключевой критерий</small><strong>AGRO TAG — долгосрочное направление, а не разовая сделка.</strong></div></div></div>'''
if 'class="center-left-stack"' not in s:
    if old_center not in s:
        raise SystemExit('AGRO TAG center visual block not found')
    s=s.replace(old_center,new_center,1)

for link in (
    '<link rel="stylesheet" href="assets/agro-benefits-final.css?v=20260901-4">',
    '<link rel="stylesheet" href="assets/agro-asia-final.css?v=20260901-2">',
):
    if link not in s:
        s=s.replace('</head>',link+'\n</head>',1)

old_asia='''<section class="asia"><div class="wrap asia-shell"><div><div class="kicker">Центральная Азия</div><h2>Преференции сегодня. Локализация завтра.</h2><p class="lead" style="margin-top:24px">Казахстан и Кыргызстан входят в ЕАЭС. Соглашение о свободной торговле между Сербией и ЕАЭС действует с 10 июля 2021 года.</p><p class="legal-note">Для отдельных товаров сербского происхождения возможен преференциальный или беспошлинный режим. Применимость проверяется по коду ТН ВЭД, правилам происхождения, исключениям и документам конкретной поставки.</p></div><div><div class="ladder"><article class="rung"><b>01</b><h3>Импорт</h3><p>Готовая техника.</p></article><article class="rung"><b>02</b><h3>Сервис</h3><p>Склад и ремонт.</p></article><article class="rung"><b>03</b><h3>Сборка</h3><p>Узлы и комплектация.</p></article><article class="rung"><b>04</b><h3>Кооперация</h3><p>Компоненты и производство.</p></article></div><p class="legal-note">Преференции и локализация оцениваются отдельно для конкретной страны, товара и проекта.</p></div></div></section>'''
new_asia='''<section class="asia"><div class="wrap asia-shell"><div class="asia-copy"><div class="kicker">Центральная Азия</div><h2>Преференции сегодня. Локализация завтра.</h2><p class="asia-main-note">Для отдельных товаров сербского происхождения возможен преференциальный или беспошлинный режим. Применимость проверяется по коду ТН ВЭД, правилам происхождения, исключениям и документам конкретной поставки.</p></div><div class="asia-path"><div class="ladder-kicker">Лестница развития</div><div class="ladder"><article class="rung"><b>01</b><h3>Импорт</h3><p>Готовая техника.</p></article><article class="rung"><b>02</b><h3>Сервис</h3><p>Склад и ремонт.</p></article><article class="rung"><b>03</b><h3>Сборка</h3><p>Узлы и комплектация.</p></article><article class="rung"><b>04</b><h3>Кооперация</h3><p>Компоненты и производство.</p></article></div><p class="legal-note">Преференции и локализация оцениваются отдельно для конкретной страны, товара и проекта.</p></div></div></section>'''
if old_asia in s:
    s=s.replace(old_asia,new_asia,1)
elif 'class="asia-copy"' not in s:
    raise SystemExit('AGRO TAG Central Asia final section not found')

s=s.replace('<p><strong>TESLA Alliance (Сербия)</strong></p>','<p><strong>TESLA Alliance (Сербия)</strong> — международная бизнес-экосистема и координатор развития AGRO TAG на зарубежных рынках.</p>')
s=s.replace('<p><strong>Go Big (Чешская Республика)</strong> — международный консалтинг, трансфер технологий и международные образовательные инициативы.</p>','<p><strong>Go Big (Чешская Республика)</strong> — международный консалтинг, трансфер технологий и развитие бизнеса на зарубежных рынках.</p>')
s=s.replace('<a class="btn primary" href="mailto:info@atesla.rs?subject=AGRO%20TAG%20partnership">Связаться с нами</a>','<a class="btn primary" href="agro-tag-contact.html" target="_blank" rel="noopener">Связаться с нами</a>')
p.write_text(s,encoding='utf-8')

# The homepage typography/card finishing step also belongs before localisation.
home=ROOT/'index.html'
h=home.read_text(encoding='utf-8')
link='<link rel="stylesheet" href="home-premium.css?v=20260901-7">'
if 'home-premium.css' not in h:
    h=h.replace('</head>',link+'\n</head>',1)
new_card='''<article class="project-card agro-tag-card"><img src="сельскохозяйственный_комплекс_на_закате.png" alt="AGRO TAG"/><div class="project-shade"></div><div class="project-top"><span class="project-type">Agro / Technology Transfer</span><span class="project-no">01</span></div><div class="project-copy"><h3>AGRO TAG</h3><p>Стратегия · партнёрство · трансфер технологий</p><a class="project-more" href="agro-tag.html">Подробнее</a></div></article>'''
candidates=[
    '<article class="project-card"><img src="сельскохозяйственный_комплекс_на_закате.png" alt="Проект в сельском хозяйстве"/></article>',
    '<article class="project-card"><img src="assets/project-agriculture.png" alt="Проект в сельском хозяйстве"/></article>',
    '<article class="project-card"><img src="сельскохозяйственный_комплекс_на_закате.png" alt="Умное сельское хозяйство"/></article>',
]
if 'agro-tag-card' not in h:
    for old in candidates:
        if old in h:
            h=h.replace(old,new_card,1)
            break
home.write_text(h,encoding='utf-8')

print('Applied final AGRO TAG/Home publish fixes before localisation')
