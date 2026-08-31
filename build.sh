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

if [ -d en ]; then cp -R en dist/en; fi
if [ -d cz ]; then cp -R cz dist/cz; fi

cp home-premium.css dist/home-premium.css
cp international-hero.css dist/international-hero.css
cp partners-ecosystem.css dist/partners-ecosystem.css

touch dist/.nojekyll
