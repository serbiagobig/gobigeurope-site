#!/usr/bin/env python3
from pathlib import Path

ROOT = Path('dist')

STYLE = r'''
<style id="mobile-guardrails-v1">
@media(max-width:850px){
  html,body{max-width:100%!important;overflow-x:hidden!important}
  body{min-width:0!important}
  img,video,iframe,svg{max-width:100%!important;height:auto}
  .wrap,.container,.section-inner,.content,.inner{max-width:100%!important;min-width:0!important}
  .wrap{width:calc(100% - 28px)!important;margin-left:auto!important;margin-right:auto!important}
  h1,h2,h3,p,a,span,div{overflow-wrap:break-word}

  /* Unified GO BIG header */
  header.gobig-unified-header .head{width:calc(100% - 28px)!important;min-height:72px!important;display:grid!important;grid-template-columns:minmax(0,1fr) 44px!important;align-items:center!important;gap:10px!important;padding:9px 0!important}
  header.gobig-unified-header .brand{min-width:0!important;gap:10px!important}
  header.gobig-unified-header .mark{width:34px!important;height:43px!important}
  header.gobig-unified-header .brand strong{font-size:22px!important;white-space:nowrap!important}
  header.gobig-unified-header .brand small{font-size:9px!important;white-space:nowrap!important}
  header.gobig-unified-header .mobile-menu-toggle{display:inline-flex!important;width:44px!important;height:44px!important;align-items:center!important;justify-content:center!important;border:1px solid rgba(11,107,69,.25)!important;background:#fff!important;color:#0B6B45!important;border-radius:10px!important;font:800 22px/1 Arial,sans-serif!important;cursor:pointer!important}
  header.gobig-unified-header .nav{grid-column:1/-1!important;display:none!important;width:100%!important;max-width:100%!important;margin:0!important;padding:8px 0 4px!important;gap:0!important;white-space:normal!important;border-top:1px solid rgba(11,44,99,.09)!important}
  header.gobig-unified-header .nav.mobile-open{display:flex!important;flex-direction:column!important;align-items:stretch!important}
  header.gobig-unified-header .nav>a{display:block!important;width:100%!important;min-height:0!important;padding:11px 2px!important;font-size:14px!important;line-height:1.25!important;border-bottom:1px solid rgba(11,44,99,.06)!important;box-shadow:none!important;white-space:normal!important}
  header.gobig-unified-header .nav>a.contact{padding:11px 2px!important;border:0!important;border-bottom:1px solid rgba(11,44,99,.06)!important}
  header.gobig-unified-header .lang-switch{display:flex!important;width:100%!important;gap:8px!important;margin:0!important;padding:12px 2px 8px!important}

  /* General hero and section typography */
  main{min-width:0!important}
  .hero{min-width:0!important;overflow:hidden!important}
  .hero h1,.hero-copy h1{font-size:clamp(38px,11vw,56px)!important;line-height:.98!important;max-width:100%!important;word-break:normal!important}
  .hero p,.hero-copy p,.lead{font-size:15px!important;line-height:1.58!important;max-width:100%!important}
  h2{font-size:clamp(34px,9.5vw,48px)!important;line-height:1.02!important;max-width:100%!important}
  h3{max-width:100%!important}
  .section{padding-left:0!important;padding-right:0!important}

  /* Project grids/cards */
  .projects .grid,.projects-grid,.projects-showcase .projects-grid{grid-template-columns:1fr!important;gap:16px!important}
  .projects .card,.projects-showcase .project-card{width:100%!important;max-width:100%!important;min-width:0!important;height:auto!important;min-height:410px!important}
  .projects .copy,.project-copy{left:20px!important;right:20px!important;bottom:20px!important}
  .projects .copy h3,.project-copy h3{font-size:24px!important;line-height:1.06!important;max-width:100%!important}
  .projects .flip-back,.home-project-back{padding:20px!important}
  .projects .flip-back h3,.home-project-back h3{font-size:23px!important;line-height:1.08!important;max-width:100%!important}
  .projects .case-text,.home-project-back p{font-size:12.5px!important;line-height:1.46!important;max-width:100%!important}

  /* AGRO TAG product grids */
  .products,.products-grid,.product-grid{grid-template-columns:1fr!important}
  .product{width:100%!important;max-width:100%!important;min-width:0!important}

  /* Berry harvesting page */
  header.top .head{width:calc(100% - 28px)!important;min-height:0!important;display:grid!important;grid-template-columns:minmax(0,1fr) auto!important;gap:10px!important;padding:10px 0!important}
  header.top .brand{font-size:20px!important;min-width:0!important}
  header.top .mark{width:32px!important;height:40px!important}
  header.top .back{grid-column:1/-1!important;grid-row:2!important;margin:0!important;font-size:11px!important;white-space:normal!important}
  header.top .langs{grid-column:2!important;grid-row:1!important;justify-self:end!important;white-space:nowrap!important}
  .subnav{top:auto!important;position:relative!important}
  .subnav .wrap{width:100%!important;padding:10px 14px!important;gap:18px!important;overflow-x:auto!important;scrollbar-width:none!important}
  .subnav .wrap::-webkit-scrollbar{display:none!important}
  .subnav a{font-size:10px!important;flex:0 0 auto!important}
  .problem,.geometry,.path,.world,.form-wrap,.economy-layout{grid-template-columns:1fr!important}
  .stats,.tech-grid,.plant-grid,.model-grid,.fit-grid,.implementation-grid,.problem-panels{grid-template-columns:1fr!important}
  .culture-grid{grid-template-columns:1fr!important}
  .solution{grid-template-columns:repeat(2,minmax(0,1fr))!important}
  .economy-video{grid-column:1!important;grid-row:auto!important;min-height:0!important;aspect-ratio:16/9!important;margin-top:22px!important}
  .economy-video video{min-height:0!important;width:100%!important;height:100%!important;object-fit:cover!important}
  .economy-stats{grid-column:1!important;grid-row:auto!important}
  .economy-stats .stat{grid-template-columns:1fr!important;gap:8px!important}
  .problem-panel,.implementation-card,.stat,.model,.plant-card,.tech-card{min-width:0!important}
  .panel-head{flex-direction:column!important;align-items:flex-start!important}
  .panel-head small{white-space:normal!important}
  .problem-row{grid-template-columns:44px minmax(0,1fr)!important}
  .problem-row span{font-size:17px!important}
  .form{grid-template-columns:1fr!important}
  .full{grid-column:auto!important}
}

@media(max-width:420px){
  .wrap{width:calc(100% - 22px)!important}
  .hero h1,.hero-copy h1{font-size:clamp(34px,11vw,46px)!important}
  h2{font-size:clamp(31px,9.5vw,42px)!important}
  header.gobig-unified-header .head{width:calc(100% - 22px)!important}
  header.top .head{width:calc(100% - 22px)!important}
}
</style>
'''

JS = r'''
<script id="mobile-guardrails-menu-v1">
(function(){
  function init(){
    document.querySelectorAll('header.gobig-unified-header').forEach(function(header){
      var head=header.querySelector('.head');
      var nav=header.querySelector('.nav');
      if(!head||!nav)return;
      var old=head.querySelector('.site-nav-fix-btn');
      if(old) old.remove();
      var btn=head.querySelector('.mobile-menu-toggle');
      if(!btn){
        btn=document.createElement('button');
        btn.type='button';
        btn.className='mobile-menu-toggle';
        btn.setAttribute('aria-label','Меню');
        btn.setAttribute('aria-expanded','false');
        btn.textContent='☰';
        head.insertBefore(btn,nav);
      }
      btn.onclick=function(e){
        e.preventDefault();
        var open=!nav.classList.contains('mobile-open');
        nav.classList.toggle('mobile-open',open);
        btn.setAttribute('aria-expanded',open?'true':'false');
        btn.textContent=open?'×':'☰';
      };
      nav.addEventListener('click',function(e){
        if(e.target.closest('a')){
          nav.classList.remove('mobile-open');
          btn.setAttribute('aria-expanded','false');
          btn.textContent='☰';
        }
      });
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>
'''

pages = list(ROOT.glob('*.html')) + list(ROOT.glob('en/*.html')) + list(ROOT.glob('cz/*.html'))
for p in pages:
    s=p.read_text(encoding='utf-8')
    if '<meta name="viewport"' not in s:
        s=s.replace('<head>','<head>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>',1)
    if 'mobile-guardrails-v1' not in s:
        s=s.replace('</head>',STYLE+'\n</head>',1)
    if 'gobig-unified-header' in s and 'mobile-guardrails-menu-v1' not in s:
        s=s.replace('</body>',JS+'\n</body>',1)
    p.write_text(s,encoding='utf-8')

# Build-time assertions for core mobile safety.
core=['index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html','agro-tag.html','berry-harvesting.html']
for name in core:
    p=ROOT/name
    if not p.exists():
        raise SystemExit(f'Missing mobile core page: {name}')
    s=p.read_text(encoding='utf-8')
    if '<meta name="viewport"' not in s:
        raise SystemExit(f'Missing viewport meta: {name}')
    if 'mobile-guardrails-v1' not in s:
        raise SystemExit(f'Missing mobile guardrails: {name}')

print('Applied final mobile guardrails to',len(pages),'pages')
