#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path('dist')

NAV_STYLE = r'''
<style id="site-runtime-fixes">
.site-nav-fix-btn{display:none;border:1px solid rgba(11,107,69,.24);background:#fff;color:#0B6B45;border-radius:12px;width:44px;height:44px;align-items:center;justify-content:center;font:800 22px/1 Arial,sans-serif;cursor:pointer;margin-left:auto}
@media(max-width:850px){
  header .head{min-height:72px!important;display:flex!important;flex-direction:row!important;align-items:center!important;flex-wrap:wrap!important;gap:12px!important;padding:10px 0!important}
  header .brand{flex:1 1 auto!important;min-width:0!important}
  .site-nav-fix-btn{display:inline-flex!important}
  header .nav{display:none!important;order:10!important;width:100%!important;max-width:none!important;overflow:visible!important;white-space:normal!important;padding:8px 0 12px!important;margin:0!important;gap:0!important;border-top:1px solid rgba(11,44,99,.09)!important}
  header .nav.site-nav-fix-open{display:flex!important;flex-direction:column!important;align-items:stretch!important}
  header .nav>a{display:block!important;width:100%!important;padding:12px 4px!important;border-bottom:1px solid rgba(11,44,99,.07)!important;font-size:14px!important;line-height:1.25!important;white-space:normal!important}
  header .nav>a:last-child{border-bottom:0!important}
  header .nav .back{border:0!important;border-radius:0!important;padding:12px 4px!important}
}
.flip-card .flip-front{pointer-events:auto}
.flip-card .flip-back{pointer-events:none}
.flip-card.is-flipped .flip-front{pointer-events:none}
.flip-card.is-flipped .flip-back{pointer-events:auto}
.products .product.has-berry-link{cursor:pointer!important}
.products .product.has-berry-link .berry-detail-link{display:inline-flex!important;margin-top:14px!important;padding-bottom:3px!important;border-bottom:1px solid rgba(11,107,69,.38)!important;color:#0B6B45!important;font-size:12px!important;font-weight:800!important;position:relative!important;z-index:3!important}
</style>
'''

RUNTIME_JS = r'''
<script id="site-runtime-fixes-js">
(function(){
  function initMenu(){
    document.querySelectorAll('header').forEach(function(header){
      if(header.querySelector('.site-mobile-toggle')) return;
      const head=header.querySelector('.head');
      const nav=header.querySelector('.nav');
      if(!head||!nav||head.querySelector('.site-nav-fix-btn')) return;
      const btn=document.createElement('button');
      btn.type='button';
      btn.className='site-nav-fix-btn';
      btn.setAttribute('aria-label','Меню');
      btn.setAttribute('aria-expanded','false');
      btn.textContent='☰';
      const brand=head.querySelector('.brand');
      if(brand && brand.nextSibling){ head.insertBefore(btn,brand.nextSibling); } else { head.insertBefore(btn,nav); }
      btn.addEventListener('click',function(e){
        e.preventDefault();
        const open=!nav.classList.contains('site-nav-fix-open');
        nav.classList.toggle('site-nav-fix-open',open);
        btn.setAttribute('aria-expanded',open?'true':'false');
        btn.textContent=open?'×':'☰';
      });
      nav.addEventListener('click',function(e){
        if(e.target.closest('a')){
          nav.classList.remove('site-nav-fix-open');
          btn.setAttribute('aria-expanded','false');
          btn.textContent='☰';
        }
      });
      window.addEventListener('resize',function(){
        if(window.innerWidth>850){
          nav.classList.remove('site-nav-fix-open');
          btn.setAttribute('aria-expanded','false');
          btn.textContent='☰';
        }
      });
    });
  }

  function initFlipCards(){
    document.addEventListener('click',function(e){
      const back=e.target.closest('.flip-back-btn');
      if(back){
        e.preventDefault();e.stopPropagation();
        const card=back.closest('.flip-card');
        if(card){
          card.classList.remove('is-flipped');
          const more=card.querySelector('.flip-more');
          if(more) more.setAttribute('aria-expanded','false');
        }
        return;
      }
      const more=e.target.closest('.flip-more');
      if(more){
        e.preventDefault();e.stopPropagation();
        const card=more.closest('.flip-card');
        if(card){
          card.classList.add('is-flipped');
          more.setAttribute('aria-expanded','true');
        }
      }
    },true);
  }

  function initBerryCard(){
    const berry=document.querySelector('.products .product.has-berry-link');
    if(!berry) return;
    berry.setAttribute('role','link');
    berry.setAttribute('tabindex','0');
    berry.setAttribute('aria-label','Открыть страницу механизированной уборки ягод');
    const open=function(){ window.location.href='berry-harvesting.html'; };
    berry.addEventListener('click',function(e){
      if(e.target.closest('a,button,input,select,textarea')) return;
      open();
    });
    berry.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){ e.preventDefault(); open(); }
    });
  }

  initMenu();
  initFlipCards();
  initBerryCard();
})();
</script>
'''


def inject_runtime(path: Path):
    s = path.read_text(encoding='utf-8')
    if 'site-runtime-fixes' not in s and '</head>' in s:
        s = s.replace('</head>', NAV_STYLE + '\n</head>', 1)
    if 'site-runtime-fixes-js' not in s and '</body>' in s:
        s = s.replace('</body>', RUNTIME_JS + '\n</body>', 1)
    path.write_text(s, encoding='utf-8')


def patch_agro(path: Path):
    s = path.read_text(encoding='utf-8')
    card_re = re.compile(
        r'<article class="product[^\"]*"[^>]*>(?:(?!</article>).)*?(?:class="product-num"[^>]*>05<|<span>05</span>)(?:(?!</article>).)*?</article>',
        re.S,
    )
    m = card_re.search(s)
    if not m:
        raise SystemExit('AGRO TAG product 05 card not found after build')

    card = m.group(0)
    if 'has-berry-link' not in card:
        card = card.replace('<article class="product', '<article class="product has-berry-link', 1)

    if 'berry-detail-link' not in card:
        link = '<a class="berry-detail-link" href="berry-harvesting.html">Подробнее →</a>'
        # Put the link inside the card content, immediately before the final content wrapper closes.
        if '<div class="product-body">' in card:
            pos = card.rfind('</div></article>')
            if pos != -1:
                card = card[:pos] + link + card[pos:]
            else:
                card = card.replace('</article>', link + '</article>', 1)
        else:
            card = card.replace('</article>', link + '</article>', 1)

    s = s[:m.start()] + card + s[m.end():]
    path.write_text(s, encoding='utf-8')


html_files = list(ROOT.glob('*.html')) + list(ROOT.glob('en/*.html')) + list(ROOT.glob('cz/*.html'))
for page in html_files:
    inject_runtime(page)

agro = ROOT / 'agro-tag.html'
if agro.exists():
    patch_agro(agro)

projects = ROOT / 'projects.html'
if projects.exists():
    s = projects.read_text(encoding='utf-8')
    if 'flip-back-btn' not in s or 'flip-more' not in s:
        raise SystemExit('Projects flip controls missing after build')

berry = ROOT / 'berry-harvesting.html'
if not berry.exists():
    raise SystemExit('Berry harvesting page missing from final site artifact')

print('Applied final site fixes to', len(html_files), 'HTML files')
