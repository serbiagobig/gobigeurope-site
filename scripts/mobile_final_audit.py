#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
CORE=('index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html')
PROJECT_ASSETS=('project-agriculture.png','projects-serbia.png','projects-tech.png','projects-publishing.png','project-plum-sum.png','project-laboratory.png','project-bank.png')

CSS=r'''
<style id="gobig-mobile-master-v5">
/* One final mobile authority. Older responsive layers may remain for desktop/source
   compatibility, but nothing below 850px is allowed to override these rules. */
html{max-width:100%!important;overflow-x:hidden!important;-webkit-text-size-adjust:100%!important;text-size-adjust:100%!important}
body{max-width:100%!important;overflow-x:hidden!important}
*,*::before,*::after{box-sizing:border-box!important}
img,svg,video,canvas,iframe{max-width:100%!important}

/* The old universal-nav system is disabled on pages that use the approved unified header. */
body:has(header.gobig-unified-header) .site-universal-shell,
body:has(header.gobig-unified-header) .site-universal-nav,
body:has(header.gobig-unified-header) .site-mobile-nav,
body:has(header.gobig-unified-header) .site-mobile-toggle,
body:has(header.gobig-unified-header) .site-context-back-wrap{display:none!important}
header.gobig-unified-header .site-nav-fix-btn,
header.gobig-unified-header .menu-toggle{display:none!important}
header.gobig-unified-header .mobile-menu-toggle{display:none!important}

@media(max-width:850px){
  body.gobig-menu-open{overflow:hidden!important;touch-action:none!important}
  .wrap,.container,.section-inner,.content,.inner{width:auto!important;max-width:calc(100% - 28px)!important;min-width:0!important;margin-left:auto!important;margin-right:auto!important}
  main,section,article,aside,div{min-width:0}
  h1,h2,h3,h4{max-width:100%!important;overflow-wrap:normal!important;word-break:normal!important;hyphens:none!important}
  p,li,label,a,span{overflow-wrap:break-word}
  img,svg,video,canvas,iframe{max-width:100%!important}

  /* Single mobile header/menu implementation. */
  header.gobig-unified-header{position:sticky!important;top:0!important;z-index:5000!important;height:78px!important;min-height:78px!important;background:#fff!important;overflow:visible!important;border-bottom:1px solid rgba(11,44,99,.09)!important}
  header.gobig-unified-header .head{width:calc(100% - 28px)!important;height:78px!important;min-height:78px!important;max-height:78px!important;margin:0 auto!important;padding:0!important;display:grid!important;grid-template-columns:minmax(0,1fr) 44px!important;align-items:center!important;gap:10px!important}
  header.gobig-unified-header .brand{min-width:0!important;display:flex!important;align-items:center!important;gap:10px!important}
  header.gobig-unified-header .mark{width:34px!important;height:43px!important;flex:0 0 34px!important}
  header.gobig-unified-header .brand strong{font-size:22px!important;white-space:nowrap!important}
  header.gobig-unified-header .brand small{font-size:9px!important;white-space:nowrap!important}
  header.gobig-unified-header .mobile-menu-toggle{grid-column:2!important;display:inline-flex!important;width:44px!important;height:44px!important;align-items:center!important;justify-content:center!important;margin:0!important;padding:0!important;border:1px solid rgba(11,107,69,.22)!important;border-radius:11px!important;background:#fff!important;color:#0B6B45!important;font:800 22px/1 Arial,sans-serif!important;cursor:pointer!important}
  header.gobig-unified-header .nav,
  header.gobig-unified-header .nav.site-nav-fix-open,
  header.gobig-unified-header .nav.mobile-open{position:fixed!important;z-index:4999!important;inset:78px 0 0 0!important;width:100vw!important;max-width:none!important;height:calc(100dvh - 78px)!important;margin:0!important;padding:18px 18px 26px!important;display:none!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;gap:0!important;overflow-y:auto!important;overflow-x:hidden!important;background:#fff!important;border:0!important;border-top:1px solid rgba(11,44,99,.08)!important;box-shadow:none!important;transform:none!important;white-space:normal!important}
  header.gobig-unified-header .nav.mobile-open,
  header.gobig-unified-header .nav.site-nav-fix-open{display:flex!important}
  header.gobig-unified-header .nav>a{flex:0 0 auto!important;width:100%!important;min-height:52px!important;padding:14px 2px!important;display:flex!important;align-items:center!important;border:0!important;border-bottom:1px solid rgba(11,44,99,.08)!important;box-shadow:none!important;font-size:16px!important;line-height:1.25!important;white-space:normal!important}
  header.gobig-unified-header .nav>a.contact{margin-top:10px!important;min-height:52px!important;padding:0 18px!important;justify-content:center!important;border:1px solid #0B6B45!important;border-radius:12px!important;background:#0B6B45!important;color:#fff!important}
  header.gobig-unified-header .lang-switch{width:100%!important;margin:14px 0 0!important;padding:16px 2px 4px!important;display:flex!important;align-items:center!important;gap:10px!important;border-top:1px solid rgba(11,44,99,.08)!important}

  /* Global mobile typography and grids recovered from the approved responsive history. */
  .hero{min-width:0!important;overflow:hidden!important}
  .hero h1,.hero-copy h1{max-width:100%!important;font-size:clamp(31px,9.2vw,42px)!important;line-height:1.02!important;letter-spacing:-.025em!important}
  .hero p,.hero-copy p,.lead{max-width:100%!important;font-size:15px!important;line-height:1.58!important}
  section h2,h2{max-width:100%!important;font-size:clamp(29px,8.8vw,40px)!important;line-height:1.04!important;letter-spacing:-.025em!important}
  .intro-grid,.adv-grid,.service-grid,.process-grid,.value-grid,.hero-lead-grid,.cta-box,.application-shell,.application-box,.form-wrap,.choice-grid,.choice-grid.three,.radio-row,.choices,.role-group{grid-template-columns:minmax(0,1fr)!important;width:100%!important;max-width:100%!important}
  .section-head,.projects-head{display:block!important;max-width:100%!important}

  /* Homepage: directions must never become three narrow columns again. */
  .direction-grid{display:grid!important;grid-template-columns:minmax(0,1fr)!important;width:100%!important;max-width:100%!important}
  .direction-item{width:100%!important;max-width:100%!important;min-width:0!important;min-height:0!important;padding:28px 22px 26px!important;border-right:0!important;border-bottom:1px solid rgba(10,37,88,.12)!important}
  .direction-item:last-child{border-bottom:0!important}
  .direction-item h3{width:100%!important;max-width:none!important;font-size:clamp(27px,8.5vw,34px)!important;line-height:1.05!important;overflow-wrap:normal!important;word-break:normal!important;hyphens:none!important}
  .direction-item p{width:100%!important;max-width:42rem!important;font-size:15px!important;line-height:1.6!important}

  /* Homepage media statement. */
  .direction-media{height:470px!important;min-height:470px!important;position:relative!important;overflow:hidden!important}
  .direction-media img{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;object-position:center center!important}
  .direction-media-copy{left:50%!important;right:auto!important;top:50%!important;bottom:auto!important;width:calc(100% - 28px)!important;transform:translate(-50%,-50%)!important;padding:14px 0!important;text-align:center!important}
  .direction-media-copy h3{max-width:100%!important;font-size:0!important;line-height:1.06!important}
  .direction-media-copy h3::before{font-size:clamp(26px,8vw,36px)!important;line-height:1.06!important}
  .direction-media-copy p{max-width:540px!important;margin:11px auto 0!important;font-size:11px!important;line-height:1.46!important}

  /* Homepage statistics: one vertical baseline and identical padding. */
  .home-stat-mobile-wrap{display:grid!important;grid-template-columns:1fr!important;width:100%!important;max-width:100%!important;gap:0!important}
  .home-stat-mobile-card{width:100%!important;max-width:100%!important;min-width:0!important;margin:0!important;padding:20px 14px!important;text-align:left!important;border-left:0!important;border-right:0!important}
  .home-stat-mobile-card>*{margin-left:0!important;margin-right:0!important;text-align:left!important;justify-content:flex-start!important}

  /* Geography block: no desktop min-content width survives. */
  .geo,.geo .wrap,.geopanel,.geocopy,.map{width:100%!important;max-width:100%!important;min-width:0!important}
  .geopanel{grid-template-columns:minmax(0,1fr)!important;height:auto!important;min-height:0!important;overflow:hidden!important}
  .geocopy{padding:32px 20px 18px!important}
  .geocopy h2{width:100%!important;max-width:100%!important;margin:0!important;font-size:clamp(29px,9vw,37px)!important;line-height:1.04!important}
  .regions{display:grid!important;grid-template-columns:1fr!important;gap:8px!important;width:100%!important;max-width:100%!important;margin-top:22px!important}
  .regions span{display:block!important;width:100%!important;padding:10px 12px!important;white-space:normal!important;line-height:1.3!important}
  .map{padding:8px 16px 26px!important;overflow:hidden!important}.map img{display:block!important;width:100%!important;height:auto!important;object-fit:contain!important}

  /* International regional composition. */
  .regions-modern-shell{grid-template-columns:minmax(0,1fr)!important;width:100%!important;max-width:100%!important}
  .regions-modern-media{min-height:620px!important;max-width:100%!important}
  .approach-overlay{left:16px!important;right:16px!important;top:16px!important;width:auto!important}
  .regions-cards{left:16px!important;right:16px!important;bottom:16px!important;grid-template-columns:1fr!important}

  /* Project showcases and the shared project hub. */
  .projects .grid,.projects-grid,.projects-showcase .projects-grid{display:grid!important;grid-template-columns:minmax(0,1fr)!important;gap:16px!important;width:100%!important}
  .projects .card,.projects-showcase .project-card{width:100%!important;max-width:100%!important;min-width:0!important;height:430px!important;min-height:430px!important;border-radius:24px!important}
  .project-card.home-project-flip,.projects .flip-card{position:relative!important;overflow:visible!important;background:transparent!important}
  .project-card.home-project-flip .home-project-inner,.projects .flip-card .flip-inner{position:absolute!important;inset:0!important;width:100%!important;height:100%!important}
  .project-card.home-project-flip .home-project-face,.projects .flip-face{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;overflow:hidden!important}
  .project-card.home-project-flip .home-project-front>img,.projects .flip-front>img,.projects-showcase .project-card>img,.projects .card>img{display:block!important;position:absolute!important;inset:0!important;width:100%!important;height:100%!important;max-width:none!important;object-fit:cover!important;opacity:1!important;visibility:visible!important}
  .projects .copy,.project-copy{left:20px!important;right:20px!important;bottom:20px!important;max-width:calc(100% - 40px)!important}
  .projects .copy h3,.project-copy h3{font-size:24px!important;line-height:1.06!important;max-width:100%!important}
  .projects .flip-back,.home-project-back{padding:20px!important}.projects .flip-back h3,.home-project-back h3{font-size:23px!important;line-height:1.08!important;max-width:100%!important}.projects .case-text,.home-project-back p{font-size:12.5px!important;line-height:1.46!important;max-width:100%!important}

  /* Partner ecosystem: desktop absolute geometry is forbidden on mobile. */
  .partners{overflow:visible!important}.partners .wrap{min-height:0!important}
  .partners .partner-grid{position:relative!important;inset:auto!important;width:100%!important;height:auto!important;margin:0!important;display:grid!important;grid-template-columns:1fr!important;gap:14px!important;background:none!important}
  .partners .partner-card,.partners .partner-card:nth-child(1),.partners .partner-card:nth-child(2),.partners .partner-card:nth-child(3){position:relative!important;inset:auto!important;width:100%!important;max-width:100%!important;min-width:0!important;min-height:0!important;margin:0!important;padding:22px 18px!important;display:block!important;transform:none!important;overflow:hidden!important}
  .partners .partner-card:nth-child(2)>ul,.partners .partner-card:nth-child(3)>ul{position:relative!important;inset:auto!important;width:100%!important;max-width:100%!important;margin:18px 0 0!important;padding:18px!important;display:block!important}

  /* Products, forms and Berry. */
  .products,.products-grid,.product-grid{grid-template-columns:minmax(0,1fr)!important}.product{width:100%!important;max-width:100%!important;min-width:0!important}
  .form{grid-template-columns:1fr!important}.full{grid-column:auto!important}.btns,.actions,.form-actions,.form-actions-right,.services-cta{max-width:100%!important;flex-wrap:wrap!important}
  .problem,.geometry,.path,.world,.economy-layout,.stats,.tech-grid,.plant-grid,.model-grid,.fit-grid,.implementation-grid,.problem-panels,.culture-grid{grid-template-columns:1fr!important}
  .economy-video{grid-column:1!important;grid-row:auto!important;min-height:0!important;aspect-ratio:16/9!important;margin-top:22px!important}.economy-video video{width:100%!important;height:100%!important;object-fit:cover!important}
}

@media(max-width:420px){
  .wrap,.container,.section-inner,.content,.inner{max-width:calc(100% - 22px)!important}
  header.gobig-unified-header .head{width:calc(100% - 22px)!important}
  .hero h1,.hero-copy h1{font-size:clamp(29px,9vw,38px)!important}
  section h2,h2{font-size:clamp(28px,8.7vw,36px)!important}
  .projects .card,.projects-showcase .project-card{height:420px!important;min-height:420px!important}
}
</style>
'''

JS=r'''
<script id="gobig-mobile-master-v5-js">
(function(){
  function labels(){var l=(document.documentElement.lang||'ru').toLowerCase();if(l.indexOf('en')===0)return['Open menu','Close menu'];if(l.indexOf('cs')===0||l.indexOf('cz')===0)return['Otevřít menu','Zavřít menu'];return['Открыть меню','Закрыть меню'];}
  function initHeader(){
    document.querySelectorAll('header.gobig-unified-header').forEach(function(header){
      var head=header.querySelector('.head'),nav=header.querySelector('.nav');if(!head||!nav)return;
      head.querySelectorAll('.site-nav-fix-btn,.menu-toggle,.site-mobile-toggle').forEach(function(x){x.remove();});
      head.querySelectorAll('.mobile-menu-toggle').forEach(function(x,i){if(i)x.remove();});
      var btn=head.querySelector('.mobile-menu-toggle');if(!btn){btn=document.createElement('button');btn.type='button';btn.className='mobile-menu-toggle';head.insertBefore(btn,nav);}
      var lab=labels();
      function setOpen(open){nav.classList.toggle('mobile-open',open);nav.classList.toggle('site-nav-fix-open',open);header.classList.toggle('nav-open',open);document.body.classList.toggle('gobig-menu-open',open);btn.setAttribute('aria-expanded',open?'true':'false');btn.setAttribute('aria-label',open?lab[1]:lab[0]);btn.textContent=open?'×':'☰';}
      setOpen(false);btn.onclick=function(e){e.preventDefault();e.stopPropagation();setOpen(btn.getAttribute('aria-expanded')!=='true');};nav.onclick=function(e){if(e.target.closest('a'))setOpen(false);};window.addEventListener('resize',function(){if(window.innerWidth>850)setOpen(false);});
    });
  }
  function fixStats(){var wanted=['13+','10+','300+','100+'],hits=[];document.querySelectorAll('body *').forEach(function(el){var t=(el.textContent||'').replace(/\s+/g,' ').trim();if(wanted.indexOf(t)>=0&&!el.children.length)hits.push(el);});var cards=[];wanted.forEach(function(w){var el=hits.find(function(x){return (x.textContent||'').trim()===w;});if(!el)return;var n=el;for(var i=0;i<5&&n.parentElement;i++,n=n.parentElement){var tx=(n.textContent||'');if(wanted.filter(function(v){return tx.indexOf(v)>=0;}).length===1&&n.children.length>1){cards.push(n);break;}}});if(cards.length===4){var wrap=cards[0].parentElement;while(wrap&&!cards.every(function(c){return wrap.contains(c);})){wrap=wrap.parentElement;}if(wrap){wrap.classList.add('home-stat-mobile-wrap');cards.forEach(function(c){c.classList.add('home-stat-mobile-card');});}}}
  function init(){initHeader();fixStats();}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
</script>
'''

pages=list(ROOT.glob('*.html'))+list(ROOT.glob('en/*.html'))+list(ROOT.glob('cz/*.html'))
for p in pages:
    s=p.read_text(encoding='utf-8')
    if '<meta name="viewport"' not in s:
        s=s.replace('<head>','<head>\n<meta name="viewport" content="width=device-width,initial-scale=1"/>',1)
    if 'gobig-mobile-master-v5' not in s:
        s=s.replace('</head>',CSS+'\n</head>',1)
    if 'gobig-unified-header' in s and 'gobig-mobile-master-v5-js' not in s:
        s=s.replace('</body>',JS+'\n</body>',1)

    # Localized routes always use shared root assets.
    if p.parent.name in ('en','cz'):
        for asset in PROJECT_ASSETS:
            s=s.replace(f'src="assets/{asset}"',f'src="../assets/{asset}"')
            s=s.replace(f"src='assets/{asset}'",f"src='../assets/{asset}'")
            s=s.replace(f'"assets/{asset}"',f'"../assets/{asset}"')
            s=s.replace(f"'assets/{asset}'",f"'../assets/{asset}'")
        s=s.replace("fetch('assets/blog-data.json'","fetch('../assets/blog-data.json'")
        s=s.replace('fetch("assets/blog-data.json"','fetch("../assets/blog-data.json"')
    p.write_text(s,encoding='utf-8')

# Static build guardrails for the exact regressions already seen in production.
errors=[]
for locale in ('ru','en','cz'):
    folder=ROOT if locale=='ru' else ROOT/locale
    for name in CORE:
        p=folder/name
        if not p.exists(): errors.append(f'missing {locale}/{name}');continue
        s=p.read_text(encoding='utf-8')
        for marker in ('gobig-mobile-master-v5','<meta name="viewport"'):
            if marker not in s: errors.append(f'{p}: missing {marker}')
        if 'gobig-unified-header' not in s: errors.append(f'{p}: unified header missing')
        if 'gobig-mobile-master-v5-js' not in s: errors.append(f'{p}: single mobile menu runtime missing')

for locale in ('en','cz'):
    for name in ('index.html','international.html','digital-ai.html','projects.html'):
        p=ROOT/locale/name
        if not p.exists(): continue
        s=p.read_text(encoding='utf-8')
        for asset in PROJECT_ASSETS:
            if f'src="assets/{asset}"' in s or f"src='assets/{asset}'" in s:
                errors.append(f'{p}: bad project asset path {asset}')

# External homepage pseudo-heading must have explicit locale overrides.
home_css=Path('home-premium.css')
if not home_css.exists(): errors.append('home-premium.css missing')
else:
    hs=home_css.read_text(encoding='utf-8')
    if 'Markets\\ATechnology\\APeople' not in hs: errors.append('EN direction pseudo-heading override missing')
    if 'Trhy\\ATechnologie\\ALidé' not in hs: errors.append('CZ direction pseudo-heading override missing')

if errors:
    for e in errors: print('ERROR:',e)
    raise SystemExit(f'Final mobile audit failed with {len(errors)} error(s)')
print('PASS: consolidated final mobile system applied to',len(pages),'pages')
print('PASS: core RU/EN/CZ headers, project asset paths, historic mobile fixes and locale pseudo-headings validated')
