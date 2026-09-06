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

/* Homepage project cards: restore the approved flip-card behaviour. */
.project-card.home-project-flip{position:relative!important;overflow:visible!important;background:transparent!important;perspective:1400px!important;isolation:auto!important}
.project-card.home-project-flip .home-project-inner{position:absolute!important;inset:0!important;border-radius:inherit!important;transform-style:preserve-3d!important;transition:transform .68s cubic-bezier(.2,.72,.2,1)!important;box-shadow:0 18px 42px rgba(17,29,47,.10)!important}
.project-card.home-project-flip.is-flipped .home-project-inner{transform:rotateY(180deg)!important}
.project-card.home-project-flip .home-project-face{position:absolute!important;inset:0!important;overflow:hidden!important;border-radius:inherit!important;backface-visibility:hidden!important;-webkit-backface-visibility:hidden!important;background:#1d2630!important}
.project-card.home-project-flip .home-project-front>img{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;object-fit:cover!important;z-index:0!important}
.project-card.home-project-flip .home-project-back{transform:rotateY(180deg)!important;display:flex!important;flex-direction:column!important;justify-content:space-between!important;padding:26px!important;background:linear-gradient(145deg,#0b2c63 0%,#10253d 58%,#0b6b45 145%)!important;color:#fff!important}
.project-card.home-project-flip .home-project-back .home-back-kicker{font-size:10px!important;font-weight:800!important;letter-spacing:.12em!important;text-transform:uppercase!important;color:#78d3a3!important}
.project-card.home-project-flip .home-project-back h3{margin:18px 0 0!important;color:#fff!important;font-family:var(--font-heading,Georgia,serif)!important;font-size:clamp(25px,1.85vw,32px)!important;line-height:1.03!important;letter-spacing:-.025em!important}
.project-card.home-project-flip .home-project-back p{margin:20px 0 0!important;color:rgba(255,255,255,.90)!important;font-size:13px!important;line-height:1.62!important}
.project-card.home-project-flip .home-project-status{margin-top:20px!important;padding-top:16px!important;border-top:1px solid rgba(255,255,255,.16)!important;color:#78d3a3!important;font-size:10px!important;font-weight:800!important;letter-spacing:.08em!important;text-transform:uppercase!important}
.project-card.home-project-flip button.project-more{border-left:0!important;border-right:0!important;border-top:0!important;background:none!important;cursor:pointer!important;font:inherit!important}
.project-card.home-project-flip .home-back{align-self:flex-start!important;margin-top:18px!important;padding:0 0 5px!important;border:0!important;border-bottom:1px solid rgba(255,255,255,.38)!important;background:none!important;color:#fff!important;font-size:12px!important;font-weight:800!important;cursor:pointer!important}
.project-card.home-project-flip .home-project-front{pointer-events:auto!important}
.project-card.home-project-flip .home-project-back{pointer-events:none!important}
.project-card.home-project-flip.is-flipped .home-project-front{pointer-events:none!important}
.project-card.home-project-flip.is-flipped .home-project-back{pointer-events:auto!important}
@media(prefers-reduced-motion:reduce){.project-card.home-project-flip .home-project-inner{transition:none!important}}
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

  function homeFront(image,alt,type,no,title,teaser){
    return '<div class="home-project-face home-project-front flip-front">'+
      '<img src="'+image+'" alt="'+alt+'"/>'+ 
      '<div class="project-shade"></div>'+ 
      '<div class="project-top"><span class="project-type">'+type+'</span><span class="project-no">'+no+'</span></div>'+ 
      '<div class="project-copy"><h3>'+title+'</h3><p>'+teaser+'</p><button class="project-more flip-more" type="button" aria-expanded="false">Подробнее</button></div>'+ 
      '</div>';
  }

  function homeBack(kicker,title,text,status){
    return '<div class="home-project-face home-project-back flip-back"><div>'+ 
      '<div class="home-back-kicker">'+kicker+'</div><h3>'+title+'</h3><p>'+text+'</p><div class="home-project-status">'+status+'</div>'+ 
      '</div><button class="home-back flip-back-btn" type="button">← Назад</button></div>';
  }

  function initHomeProjectCards(){
    const cards=Array.from(document.querySelectorAll('.project-card'));
    if(cards.length<4) return;
    const defs=[
      {
        index:1,
        image:'assets/projects-serbia.png', alt:'Выход на рынок Сербии', type:'MARKET ENTRY', no:'02', title:'Выход на рынок Сербии', teaser:'Стратегия · локальные партнёры · переговоры',
        kicker:'ENTERING THE SERBIAN MARKET', backTitle:'Выход технологического стартапа на рынок Сербии',
        text:'Вывод компании-стартапа из Узбекистана на рынок Сербии. Специализированное ПО для управления BMS-системами зданий. Проведена экспертиза решения, найден локальный партнёр. Проект масштабируется на рынки Балкан.',
        status:'Экспертиза · партнёр · масштабирование'
      },
      {
        index:2,
        image:'assets/projects-tech.png', alt:'Открытая лаборатория', type:'RESEARCH INFRASTRUCTURE', no:'03', title:'Открытая лаборатория', teaser:'Наука · инфраструктура · удалённый доступ',
        kicker:'OPEN LABORATORY', backTitle:'Удалённый доступ к исследовательской инфраструктуре',
        text:'Поиск инвестора для проекта организации удалённого доступа к лабораторному оборудованию исследовательских организаций. Цель проекта — расширить возможности европейских учёных в проведении научных исследований.',
        status:'Инвестиции · наука · инфраструктура · доступ'
      },
      {
        index:3,
        image:'assets/projects-publishing.png', alt:'Международные издательские проекты', type:'CULTURE / PUBLISHING', no:'04', title:'Международные издательские проекты', teaser:'Партнёры · локализация · продвижение',
        kicker:'INTERNATIONAL PUBLISHING PROJECT', backTitle:'Международный книгоиздательский проект',
        text:'Организация международного издательского проекта по запросу сербского издательства. Международная команда экспертов и авторов готовит исторические книги для сербских читателей.',
        status:'Эксперты · авторы · локализация · издание'
      }
    ];
    defs.forEach(function(d){
      const card=cards[d.index];
      if(!card) return;
      card.classList.add('flip-card','home-project-flip');
      card.innerHTML='<div class="home-project-inner">'+homeFront(d.image,d.alt,d.type,d.no,d.title,d.teaser)+homeBack(d.kicker,d.backTitle,d.text,d.status)+'</div>';
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
  initHomeProjectCards();
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
    required_projects = [
        'Открытая лаборатория',
        'Международные издательские проекты',
        'Applied Research',
        'Banking Transformation',
        'Оптимизация работы ИИ-агентов',
        'Цифровая трансформация банков Казахстана',
        'flip-back-btn',
        'flip-more',
    ]
    missing = [marker for marker in required_projects if marker not in s]
    if missing:
        raise SystemExit('Latest Projects page was not published; missing markers: ' + ', '.join(missing))

berry = ROOT / 'berry-harvesting.html'
if not berry.exists():
    raise SystemExit('Berry harvesting page missing from final site artifact')

print('Applied final site fixes to', len(html_files), 'HTML files')
