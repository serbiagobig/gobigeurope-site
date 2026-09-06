#!/usr/bin/env python3
from pathlib import Path

ROOT=Path('dist')
STYLE=r'''
<style id="mobile-menu-overlay-v4">
@media(max-width:850px){
  body.gobig-menu-open{overflow:hidden!important;touch-action:none}
  header.gobig-unified-header{height:78px!important;min-height:78px!important;overflow:visible!important}
  header.gobig-unified-header .head{height:78px!important;min-height:78px!important;max-height:78px!important;display:grid!important;grid-template-columns:minmax(0,1fr) 44px!important;align-items:center!important;gap:10px!important;padding:0!important}
  header.gobig-unified-header .nav,
  header.gobig-unified-header .nav.site-nav-fix-open,
  header.gobig-unified-header .nav.mobile-open{
    position:fixed!important;
    z-index:9999!important;
    inset:78px 0 0 0!important;
    width:100vw!important;
    max-width:none!important;
    height:calc(100dvh - 78px)!important;
    margin:0!important;
    padding:18px 18px 26px!important;
    background:#fff!important;
    border-top:1px solid rgba(11,44,99,.08)!important;
    overflow-y:auto!important;
    overflow-x:hidden!important;
    display:none!important;
    flex-direction:column!important;
    align-items:stretch!important;
    justify-content:flex-start!important;
    gap:0!important;
    transform:none!important;
    box-shadow:0 18px 36px rgba(11,44,99,.08)!important;
  }
  header.gobig-unified-header .nav.mobile-open,
  header.gobig-unified-header .nav.site-nav-fix-open{display:flex!important}
  header.gobig-unified-header .nav>a{flex:0 0 auto!important;width:100%!important;min-height:52px!important;padding:14px 2px!important;display:flex!important;align-items:center!important;border-bottom:1px solid rgba(11,44,99,.08)!important;font-size:16px!important;line-height:1.25!important;white-space:normal!important}
  header.gobig-unified-header .nav>a.contact{margin-top:8px!important;min-height:52px!important;padding:0 18px!important;justify-content:center!important;border:1px solid #0B6B45!important;border-radius:12px!important;background:#0B6B45!important;color:#fff!important}
  header.gobig-unified-header .lang-switch{flex:0 0 auto!important;width:100%!important;margin-top:14px!important;padding:16px 2px 4px!important;display:flex!important;gap:10px!important;border-top:1px solid rgba(11,44,99,.08)!important}
}
</style>
'''
JS=r'''
<script id="mobile-menu-overlay-v4-js">
(function(){
  function init(){
    document.querySelectorAll('header.gobig-unified-header').forEach(function(header){
      var head=header.querySelector('.head');
      var nav=header.querySelector('.nav');
      if(!head||!nav)return;
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
        document.body.classList.toggle('gobig-menu-open',open);
        btn.setAttribute('aria-expanded',open?'true':'false');
        btn.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню');
        btn.textContent=open?'×':'☰';
      }
      setOpen(false);
      btn.onclick=function(e){
        e.preventDefault();e.stopPropagation();
        setOpen(btn.getAttribute('aria-expanded')!=='true');
      };
      nav.onclick=function(e){if(e.target.closest('a'))setOpen(false);};
      window.addEventListener('resize',function(){if(window.innerWidth>850)setOpen(false);});
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
</script>
'''

pages=list(ROOT.glob('*.html'))+list(ROOT.glob('en/*.html'))+list(ROOT.glob('cz/*.html'))
count=0
for p in pages:
    s=p.read_text(encoding='utf-8')
    if 'gobig-unified-header' not in s: continue
    if 'mobile-menu-overlay-v4' not in s:
        s=s.replace('</head>',STYLE+'\n</head>',1)
    if 'mobile-menu-overlay-v4-js' not in s:
        s=s.replace('</body>',JS+'\n</body>',1)
    p.write_text(s,encoding='utf-8')
    count+=1

for name in ('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html'):
    p=ROOT/name
    if not p.exists(): raise SystemExit(f'Missing core page: {name}')
    s=p.read_text(encoding='utf-8')
    if 'mobile-menu-overlay-v4' not in s or 'gobig-menu-open' not in s:
        raise SystemExit(f'Overlay mobile menu missing in {name}')
print('Installed fixed mobile menu overlay on',count,'pages')
