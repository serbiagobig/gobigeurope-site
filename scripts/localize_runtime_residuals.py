#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
EN={
'Открыть страницу механизированной уборки ягод':'Open the mechanised berry harvesting page',
'Закрыть меню':'Close menu','Открыть меню':'Open menu','Меню':'Menu',
'Научно-технологический парк Нови-Сад':'Science and Technology Park Novi Sad',
'Научно-технологический парк Чачак':'Science and Technology Park Čačak',
'Научно-технологический парк Республики Сербской':'Science and Technology Park of Republika Srpska',
'Ассоциация фермеров Казахстана':'Association of Farmers of Kazakhstan',
'Национальный инфраструктурный проект «Туран», Кыргызстан':'National Infrastructure Project “Turan”, Kyrgyz Republic',
'ОБФ «Кыргыз ТехноВумен»':'Kyrgyz TechnoWomen Public Charitable Foundation',
'Торгово-промышленная палата Воеводины':'Chamber of Commerce and Industry of Vojvodina',
'Торгово-промышленная палата Республики Сербской':'Chamber of Commerce and Industry of Republika Srpska',
'Профильные ассоциации, институты развития и деловые объединения':'Specialist associations, development institutions and business organisations',
'← Назад':'← Back','Подробнее':'Learn more',
}
CZ={
'Открыть страницу механизированной уборки ягод':'Otevřít stránku mechanizované sklizně bobulovin',
'Закрыть меню':'Zavřít menu','Открыть меню':'Otevřít menu','Меню':'Menu',
'Научно-технологический парк Нови-Сад':'Vědeckotechnologický park Novi Sad',
'Научно-технологический парк Чачак':'Vědeckotechnologický park Čačak',
'Научно-технологический парк Республики Сербской':'Vědeckotechnologický park Republiky srbské',
'Ассоциация фермеров Казахстана':'Asociace farmářů Kazachstánu',
'Национальный инфраструктурный проект «Туран», Кыргызстан':'Národní infrastrukturní projekt „Turan“, Kyrgyzská republika',
'ОБФ «Кыргыз ТехноВумен»':'Veřejná charitativní nadace Kyrgyz TechnoWomen',
'Торгово-промышленная палата Воеводины':'Obchodní a průmyslová komora Vojvodiny',
'Торгово-промышленная палата Республики Сербской':'Obchodní a průmyslová komora Republiky srbské',
'Профильные ассоциации, институты развития и деловые объединения':'Oborové asociace, rozvojové instituce a podnikatelská sdružení',
'← Назад':'← Zpět','Подробнее':'Více informací',
}
for lang,mapping in [('en',EN),('cz',CZ)]:
    folder=ROOT/lang
    if not folder.exists(): continue
    for p in folder.glob('*.html'):
        s=p.read_text(encoding='utf-8')
        for src in sorted(mapping,key=len,reverse=True): s=s.replace(src,mapping[src])
        p.write_text(s,encoding='utf-8')
print('Translated runtime-only locale strings')
