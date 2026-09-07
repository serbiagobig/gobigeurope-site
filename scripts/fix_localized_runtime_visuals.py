#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')

TEXT={
'en':{
 'Рынки':'Markets','Технологии':'Technology','Люди':'People',
 'Подробнее':'Learn more','Открыть проект':'Open project','← Назад':'← Back',
},
'cz':{
 'Рынки':'Trhy','Технологии':'Technologie','Люди':'Lidé',
 'Подробнее':'Více informací','Открыть проект':'Otevřít projekt','← Назад':'← Zpět',
}}

RUNTIME=r'''
<script id="localized-runtime-visual-fix-v2">
(function(){
  const assets={
    'ENTERING THE SERBIAN MARKET':'../assets/projects-serbia.png',
    'OPEN LABORATORY':'../assets/projects-tech.png',
    'INTERNATIONAL PUBLISHING PROJECT':'../assets/projects-publishing.png',
    'APPLIED AI / BIOTECH':'../assets/project-laboratory.png',
    'BANKING / MARKET ENTRY':'../assets/project-bank.png',
    'AGRO / INDUSTRIAL PARTNERSHIP':'../assets/project-plum-sum.png',
    'AGRO / TECHNOLOGY TRANSFER':'../assets/project-agriculture.png'
  };

  function repairProjectImages(){
    document.querySelectorAll('.project-card.home-project-flip').forEach(function(card){
      const front=card.querySelector('.home-project-front');
      if(!front)return;
      let img=front.querySelector('img');
      const key=(card.querySelector('.home-back-kicker')||card.querySelector('.project-type')||{}).textContent||'';
      const fallback=assets[key.trim()];
      if(!img && fallback){
        img=document.createElement('img');
        img.src=fallback;
        img.alt=(card.querySelector('.project-copy h3')||{}).textContent||'';
        front.insertBefore(img,front.firstChild);
      }else if(img){
        let src=(img.getAttribute('src')||'').trim();
        if(src.startsWith('assets/')){
          src='../'+src;
          img.setAttribute('src',src);
        }
        if((!src || src==='#' || src.endsWith('/en/') || src.endsWith('/cz/')) && fallback) img.src=fallback;
        img.addEventListener('error',function(){if(fallback && img.getAttribute('src')!==fallback)img.src=fallback;},{once:true});
      }
      if(img){
        img.style.position='absolute';img.style.inset='0';img.style.width='100%';img.style.height='100%';img.style.objectFit='cover';img.style.display='block';
      }
    });
  }

  function bindFlips(){
    document.querySelectorAll('.flip-card,.home-project-flip').forEach(function(card){
      if(card.dataset.localeFlipBound==='1')return;
      card.dataset.localeFlipBound='1';
      card.addEventListener('click',function(e){
        const open=e.target.closest('.flip-more');
        const close=e.target.closest('.flip-back-btn');
        if(open){e.preventDefault();e.stopPropagation();card.classList.add('is-flipped');open.setAttribute('aria-expanded','true');}
        if(close){e.preventDefault();e.stopPropagation();card.classList.remove('is-flipped');const m=card.querySelector('.flip-more');if(m)m.setAttribute('aria-expanded','false');}
      },true);
    });
  }

  function run(){repairProjectImages();bindFlips();}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});else run();
  setTimeout(run,0);
  setTimeout(run,250);
})();
</script>
'''

CSS=r'''
<style id="localized-runtime-visual-fix-v2-css">
@media(max-width:850px){
  .projects-showcase .project-card.home-project-flip .home-project-front>img{display:block!important;position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;opacity:1!important;visibility:visible!important}
  .projects-showcase .project-card.home-project-flip .home-project-front{background:#182430!important}
  .projects-showcase .project-card.home-project-flip:not(.is-flipped) .home-project-inner{transform:rotateY(0deg)!important}
  .projects-showcase .project-card.home-project-flip.is-flipped .home-project-inner{transform:rotateY(180deg)!important}
}
</style>
'''

for lang,mapping in TEXT.items():
    folder=ROOT/lang
    if not folder.exists():
        raise SystemExit(f'Missing locale folder {folder}')
    for p in folder.glob('*.html'):
        s=p.read_text(encoding='utf-8')
        for old,new in mapping.items():
            s=s.replace(old,new)
        # Fix relative asset paths in localized HTML itself, not only at runtime.
        s=re.sub(r'(?P<attr>src|poster)="assets/',lambda m:m.group('attr')+'="../assets/',s)
        if p.name in ('index.html','international.html','digital-ai.html','projects.html'):
            if 'localized-runtime-visual-fix-v2-css' not in s:
                s=s.replace('</head>',CSS+'\n</head>',1)
            if 'localized-runtime-visual-fix-v2' not in s:
                s=s.replace('</body>',RUNTIME+'\n</body>',1)
        p.write_text(s,encoding='utf-8')

print('Fixed EN/CZ homepage overlay text and localized project-card asset/runtime behaviour')
