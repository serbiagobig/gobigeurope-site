#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
MAPS={
'en':{
'≈ 7–8 м':'≈ 7–8 m','до 2,3 м':'up to 2.3 m','от 2,5 м':'from 2.5 m','≈ 2,6 м':'≈ 2.6 m','2,6 м':'2.6 m','Другое':'Other',
'Создадим новый центр агротехнологий':'Let’s create a new agri-technology centre',
'Казахстан и Кыргызстан входят в ЕАЭС. Agreement о свободной торговле между Сербией и ЕАЭС действует с 10 июля 2021 года.':'Kazakhstan and Kyrgyzstan are members of the EAEU. The free trade agreement between Serbia and the EAEU has been in force since 10 July 2021.',
'Казахстан и Кыргызстан входят в ЕАЭС. Соглашение о свободной торговле между Сербией и ЕАЭС действует с 10 июля 2021 года.':'Kazakhstan and Kyrgyzstan are members of the EAEU. The free trade agreement between Serbia and the EAEU has been in force since 10 July 2021.',
'международный консалтинг, трансфер технологий и международные образовательные инициативы.':'international consulting, technology transfer and international education initiatives.',
'Место для изображения сельхозугодий в горной местности Центральной Азии':'Agricultural landscape in the mountainous areas of Central Asia',
},
'cz':{
'≈ 7–8 м':'≈ 7–8 m','до 2,3 м':'do 2,3 m','от 2,5 м':'od 2,5 m','≈ 2,6 м':'≈ 2,6 m','2,6 м':'2,6 m','Другое':'Jiné',
'Создадим новый центр агротехнологий':'Vybudujme nové centrum agrotechnologií',
'Казахстан и Кыргызстан входят в ЕАЭС. Dohoda о свободной торговле между Сербией и ЕАЭС действует с 10 июля 2021 года.':'Kazachstán a Kyrgyzstán jsou členy EAEU. Dohoda o volném obchodu mezi Srbskem a EAEU je účinná od 10. července 2021.',
'Казахстан и Кыргызстан входят в ЕАЭС. Соглашение о свободной торговле между Сербией и ЕАЭС действует с 10 июля 2021 года.':'Kazachstán a Kyrgyzstán jsou členy EAEU. Dohoda o volném obchodu mezi Srbskem a EAEU je účinná od 10. července 2021.',
'международный консалтинг, трансфер технологий и международные образовательные инициативы.':'mezinárodní poradenství, transfer technologií a mezinárodní vzdělávací iniciativy.',
'Место для изображения сельхозугодий в горной местности Центральной Азии':'Zemědělská krajina v horských oblastech Střední Asie',
}}
for lang,mapping in MAPS.items():
    folder=ROOT/lang
    if not folder.exists(): continue
    for p in folder.glob('*.html'):
        s=p.read_text(encoding='utf-8')
        for src in sorted(mapping,key=len,reverse=True): s=s.replace(src,mapping[src])
        p.write_text(s,encoding='utf-8')
print('Finalised locale measurements and late-injected copy')
