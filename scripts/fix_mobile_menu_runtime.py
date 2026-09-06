#!/usr/bin/env python3
from pathlib import Path

ROOT = Path('dist')

STYLE = r'''
<style id="mobile-menu-runtime-fix-v3">
header.gobig-unified-header .mobile-menu-toggle{display:none!important}
@media(max-width:850px){
  header.gobig-unified-header .mobile-menu-toggle{display:inline-flex!important}
  header.gobig-unified-header .site-nav-fix-btn,
  header.gobig-unified-header .menu-toggle{display:none!important}
  header.gobig-unified-header .nav{display:none!important}
  header.gobig-unified-header .nav.mobile-open,
  header.gobig-unified-header .nav.site-nav-fix-open{
    display:flex!important;
    flex-direction:column!important;
    align-items:stretch!important;
  }
}
</style>
'''

JS = r'''
<script id="mobile-menu-runtime-fix-v3-js">
(function(){
  function setup(){
    document.querySelectorAll('header.gobig-unified-header').forEach(function(header){
      var head=header.querySelector('.head');
      var nav=header.querySelector('.nav');
      if(!head||!nav)return;

      /* Remove every legacy trigger; only one button may remain. */
      head.querySelectorAll('.site-nav-fix-btn,.menu-toggle').forEach(function(el){el.remove();});
      head.querySelectorAll('.mobile-menu-toggle').forEach(function(el,i){if(i>0)el.remove();});

      var btn=head.querySelector('.mobile-menu-toggle');
      if(!btn){
        btn=document.createElement('button');
        btn.type='button';
        btn.className='mobile-menu-toggle';
        head.insertBefore(btn,nav);
      }

      function setOpen(open){
        nav.classList.toggle('mobile-open',open);
        nav.classList.toggle('site-nav-fix-open',open);
        header.classList.toggle('nav-open',open);
        btn.setAttribute('aria-expanded',open?'true':'false');
        btn.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню');
        btn.textContent=open?'×':'☰';
      }

      /* Reset stale state inherited from older scripts before binding. */
      setOpen(false);

      btn.onclick=function(e){
        e.preventDefault();
        e.stopPropagation();
        setOpen(btn.getAttribute('aria-expanded')!=='true');
      };

      nav.onclick=function(e){
        if(e.target.closest('a')) setOpen(false);
      };

      window.addEventListener('resize',function(){
        if(window.innerWidth>850) setOpen(false);
      });
    });
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',setup,{once:true});
  else setup();
})();
</script>
'''

pages = list(ROOT.glob('*.html')) + list(ROOT.glob('en/*.html')) + list(ROOT.glob('cz/*.html'))
count=0
for p in pages:
    s=p.read_text(encoding='utf-8')
    if 'gobig-unified-header' not in s:
        continue
    if 'mobile-menu-runtime-fix-v3' not in s:
        s=s.replace('</head>',STYLE+'\n</head>',1)
    if 'mobile-menu-runtime-fix-v3-js' not in s:
        s=s.replace('</body>',JS+'\n</body>',1)
    p.write_text(s,encoding='utf-8')
    count+=1

for name in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
    p=ROOT/name
    if not p.exists():
        raise SystemExit(f'Missing core page: {name}')
    s=p.read_text(encoding='utf-8')
    if 'mobile-menu-runtime-fix-v3' not in s or 'site-nav-fix-open' not in s or 'mobile-open' not in s:
        raise SystemExit(f'Mobile menu runtime fix missing in {name}')

print('Installed single synchronized mobile menu runtime on',count,'pages')
