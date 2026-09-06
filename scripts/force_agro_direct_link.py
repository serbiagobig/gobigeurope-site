#!/usr/bin/env python3
from pathlib import Path

STYLE = r'''
<style id="agro-tag-link-style-fix">
/* AGRO TAG direct link must look exactly like the other project CTAs. */
.project-card a.project-more,
.projects .card a.more{
  font:inherit!important;
  font-size:12px!important;
  font-weight:800!important;
  line-height:1!important;
  color:#78d3a3!important;
  text-decoration:none!important;
}
.project-card a.project-more:after{content:"→"!important;font-size:20px!important;line-height:1!important}
</style>
'''

JS = r'''
<script id="force-agro-tag-direct-link">
(function(){
  function fix(){
    document.querySelectorAll('.project-card, .projects .card').forEach(function(card){
      const h=card.querySelector('h3');
      if(!h || h.textContent.trim()!=='AGRO TAG') return;
      const btn=card.querySelector('.flip-more, button.project-more, button.more');
      const existing=card.querySelector('a.project-more, a.more');
      if(existing){
        existing.setAttribute('href','agro-tag.html');
        existing.classList.remove('flip-more');
        existing.textContent='Подробнее';
      }
      if(btn){
        const a=document.createElement('a');
        a.href='agro-tag.html';
        a.className=btn.classList.contains('project-more')?'project-more':'more';
        a.textContent='Подробнее';
        btn.replaceWith(a);
      }
      card.classList.remove('is-flipped');
    });
  }
  fix();
  document.addEventListener('DOMContentLoaded',fix,{once:true});
})();
</script>
'''

for name in ('international.html','projects.html'):
    p=Path('dist')/name
    if not p.exists():
        raise SystemExit(f'Missing {name}')
    s=p.read_text(encoding='utf-8')
    if 'agro-tag-link-style-fix' not in s:
        if '</head>' not in s:
            raise SystemExit(f'No </head> in {name}')
        s=s.replace('</head>',STYLE+'\n</head>',1)
    if 'force-agro-tag-direct-link' not in s:
        if '</body>' not in s:
            raise SystemExit(f'No </body> in {name}')
        s=s.replace('</body>',JS+'\n</body>',1)
    p.write_text(s,encoding='utf-8')

print('Forced AGRO TAG direct links with unified CTA styling')
