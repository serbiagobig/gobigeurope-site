#!/bin/sh
set -eu

rm -rf dist
mkdir -p dist/assets

cp index.html international.html digital-ai.html education-hr.html readiness.html agro-tag.html README.txt dist/ 2>/dev/null || true

if [ -d assets ]; then
  cp -R assets/. dist/assets/
fi

# Stable public aliases for manually uploaded visual assets.
cp "ChatGPT Image 30 авг. 2026 г., 12_21_44.png" dist/assets/regional-business-white.png
cp "Serbian market.png" dist/assets/projects-serbia.png
cp "Technical project.png" dist/assets/projects-tech.png
cp "book publishing.png" dist/assets/projects-publishing.png
cp "nizkii-ugol-zrenia-ofisnogo-zdania.jpg" dist/assets/digital-transformation-hero.jpg
cp "Plum Sum.png" dist/assets/project-plum-sum.png
cp "сельскохозяйственный_комплекс_на_закате.png" dist/assets/project-agriculture.png
cp "современная_лаборатория_учёные_за_работой.png" dist/assets/project-laboratory.png
cp "Bank.png" dist/assets/project-bank.png

# Turn the AGRO TAG product list into a visual product showcase.
python - <<'PY'
from pathlib import Path
p = Path('dist/agro-tag.html')
s = p.read_text(encoding='utf-8')
old_css = '''.products{position:relative;background:#fff;overflow:hidden}.products:before{display:none}.products .wrap{position:relative;z-index:2}.products .kicker{color:var(--rose)}.products h2{color:var(--deep)}.products-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:13px}.product{position:relative;padding:23px 25px;display:grid;grid-template-columns:52px 1fr;gap:17px;border-radius:18px;background:linear-gradient(180deg,#fafbfb 0%,#f0f3f4 100%);border:1px solid rgba(72,105,133,.12);box-shadow:0 10px 24px rgba(41,62,82,.04);overflow:hidden}.product:before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--blue)}.product:nth-child(3n):before{background:var(--rose)}.product span{color:var(--blue);font-size:24px;font-weight:800;letter-spacing:.06em}.product:nth-child(3n) span{color:var(--rose)}.product h3{color:var(--deep);font-size:24px}.product p{margin-top:8px;color:#667786;font-size:13px;line-height:1.55}'''
new_css = '''.products{position:relative;background:#fff;overflow:hidden}.products:before{display:none}.products .wrap{position:relative;z-index:2}.products .kicker{color:var(--rose)}.products h2{color:var(--deep)}.products .section-head .lead{max-width:560px;font-size:18px;line-height:1.65}.products-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}.product{position:relative;min-height:360px;border-radius:22px;background:#fff;border:1px solid rgba(72,105,133,.12);box-shadow:0 16px 34px rgba(41,62,82,.08);overflow:hidden;display:flex;flex-direction:column;transition:transform .3s ease,box-shadow .3s ease}.product:hover{transform:translateY(-4px);box-shadow:0 22px 44px rgba(41,62,82,.12)}.product-media{height:185px;overflow:hidden;background:#e9eef0}.product-media img{width:100%;height:100%;object-fit:cover;object-position:center;transition:transform .45s ease}.product:hover .product-media img{transform:scale(1.035)}.product-body{position:relative;padding:20px 21px 22px;flex:1}.product-num{display:block;color:var(--green);font-size:30px;font-weight:800;line-height:1;letter-spacing:.04em}.product h3{margin-top:9px;color:var(--deep);font-size:22px;line-height:1.1}.product p{margin-top:10px;color:#667786;font-size:13.5px;line-height:1.52}.product.service-card .product-media img{object-position:center 35%}@media(max-width:980px){.products-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:700px){.products-grid{grid-template-columns:1fr}.product{min-height:auto}.product-media{height:220px}.products .section-head .lead{font-size:16px}}'''
old_section = '''<section class="products" id="products"><div class="wrap"><div class="section-head"><div><div class="kicker">Продуктовые направления</div><h2>Группы продукции и технологий</h2></div><p class="lead">Конкретные модели и комплектации подбираются после анализа культур, хозяйств, тракторного парка и коммерческого потенциала рынка. Будущий портфель Партнёра формируется модульно: начать можно с приоритетных групп и расширять предложение по мере роста рынка.</p></div><div class="products-grid"><article class="product"><span>01</span><div><h3>Обработка почвы</h3><p>Бороны, дисковые орудия, культиваторы, фрезы, ротационные бороны, глубокорыхлители.</p></div></article><article class="product"><span>02</span><div><h3>Посев</h3><p>Механические и пневматические сеялки для зерновых, пропашных и овощных культур.</p></div></article><article class="product"><span>03</span><div><h3>Защита растений</h3><p>Навесные и прицепные опрыскиватели, садовые и виноградниковые атомайзеры.</p></div></article><article class="product"><span>04</span><div><h3>Овощи и корнеплоды</h3><p>Посадка, уход, уборка, транспортировка и послеуборочная обработка.</p></div></article><article class="product"><span>05</span><div><h3>Ягодоводство</h3><p>Подготовка плантаций и механизированная уборка.</p></div></article><article class="product"><span>06</span><div><h3>Транспорт и инфраструктура</h3><p>Прицепы, резервуары, ёмкости, навесы, ограждения и металлоконструкции.</p></div></article><article class="product"><span>07</span><div><h3>Сервисная экосистема</h3><p>Запчасти, расходные материалы, обучение, диагностика и ввод в эксплуатацию.</p></div></article><article class="product"><span>08</span><div><h3>Кошение, кормозаготовка и мульчирование</h3><p>Дисковые и сегментные косилки, грабли и ворошилки для сена, мульчеры для полей, садов и виноградников.</p></div></article></div></div></section>'''
new_section = '''<section class="products" id="products"><div class="wrap"><div class="section-head"><div><div class="kicker">Продуктовые направления</div><h2>Группы продукции и технологий</h2></div><p class="lead">Конкретные модели и комплектации подбираются после анализа культур, хозяйств, тракторного парка и коммерческого потенциала рынка. Будущий портфель Партнёра формируется модульно: начать можно с приоритетных групп и расширять предложение по мере роста рынка.</p></div><div class="products-grid"><article class="product"><div class="product-media"><img src="assets/project-agriculture.png" alt="Почвообрабатывающая сельскохозяйственная техника"/></div><div class="product-body"><span class="product-num">01</span><h3>Обработка почвы</h3><p>Бороны, дисковые орудия, культиваторы, фрезы, ротационные бороны, глубокорыхлители.</p></div></article><article class="product"><div class="product-media"><img src="https://agria.rs/wp-content/uploads/2023/08/zitka-featured-image.webp" alt="Посевная техника"/></div><div class="product-body"><span class="product-num">02</span><h3>Посев</h3><p>Механические и пневматические сеялки для зерновых, пропашных и овощных культур.</p></div></article><article class="product"><div class="product-media"><img src="https://bsk.rs/uploads/ck_editor/images/Rotoprotect-home.jpg" alt="Система защиты растений"/></div><div class="product-body"><span class="product-num">03</span><h3>Защита растений</h3><p>Навесные и прицепные опрыскиватели, садовые и виноградниковые системы защиты.</p></div></article><article class="product"><div class="product-media"><img src="https://agria.rs/wp-content/uploads/2023/08/psp-agria-img.webp" alt="Техника для овощей и корнеплодов"/></div><div class="product-body"><span class="product-num">04</span><h3>Овощи и корнеплоды</h3><p>Посадка, уход, уборка, транспортировка и послеуборочная обработка.</p></div></article><article class="product"><div class="product-media"><img src="https://site.caes.uga.edu/smallfruits/files/2022/07/BBHarvest-Photo1-1024x678.jpg" alt="Механизированная уборка ягод"/></div><div class="product-body"><span class="product-num">05</span><h3>Ягодоводство</h3><p>Подготовка плантаций, защита насаждений и механизированная уборка ягод.</p></div></article><article class="product"><div class="product-media"><img src="https://www.lifam-m.com/wp-content/uploads/2022/04/Nenaslovljeni-dizajn-1.jpg" alt="Сельскохозяйственная инфраструктура и оборудование"/></div><div class="product-body"><span class="product-num">06</span><h3>Транспорт и инфраструктура</h3><p>Прицепы, резервуары, ёмкости, навесы, ограждения и металлоконструкции.</p></div></article><article class="product service-card"><div class="product-media"><img src="https://agria.rs/wp-content/uploads/2023/08/services-agria-image.webp" alt="Сервис сельскохозяйственной техники"/></div><div class="product-body"><span class="product-num">07</span><h3>Сервисная экосистема</h3><p>Запчасти, расходные материалы, обучение, диагностика и ввод в эксплуатацию.</p></div></article><article class="product"><div class="product-media"><img src="https://www.fpm.rs/media/catalogProduct/mulcarZaRatarstvo/Mulcar-za-ratarstvo-1.png" alt="Техника для кошения и мульчирования"/></div><div class="product-body"><span class="product-num">08</span><h3>Кошение, кормозаготовка и мульчирование</h3><p>Косилки, грабли, ворошилки и мульчеры для полей, садов и виноградников.</p></div></article></div></div></section>'''
if old_css not in s:
    raise SystemExit('AGRO TAG product CSS block not found')
if old_section not in s:
    raise SystemExit('AGRO TAG product section not found')
s = s.replace(old_css, new_css, 1).replace(old_section, new_section, 1)
p.write_text(s, encoding='utf-8')
PY

if [ -d en ]; then cp -R en dist/en; fi
if [ -d cz ]; then cp -R cz dist/cz; fi

cp home-premium.css dist/home-premium.css
cp international-hero.css dist/international-hero.css
cp partners-ecosystem.css dist/partners-ecosystem.css

touch dist/.nojekyll
