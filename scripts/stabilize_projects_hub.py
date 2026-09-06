#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path('dist')

STYLE=r'''
<style id="projects-hub-stable-style">
/* Stable shared project-card system */
.projects-grid,.projects .grid{align-items:stretch!important}
.projects .grid{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:20px!important}
.projects .card{height:480px!important;min-height:480px!important;border-radius:26px!important}
.projects .flip-card{overflow:visible!important;background:transparent!important;box-shadow:none!important;perspective:1400px!important}
.projects .flip-card .flip-inner{position:absolute!important;inset:0!important;height:100%!important;border-radius:26px!important;transform-style:preserve-3d!important;transition:transform .62s cubic-bezier(.2,.72,.2,1)!important}
.projects .flip-card.is-flipped .flip-inner{transform:rotateY(180deg)!important}
.projects .flip-face{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;overflow:hidden!important;border-radius:26px!important;backface-visibility:hidden!important;-webkit-backface-visibility:hidden!important}
.projects .flip-front{transform:rotateY(0deg)!important;pointer-events:auto!important}
.projects .flip-back{transform:rotateY(180deg)!important;pointer-events:none!important;display:flex!important;flex-direction:column!important;justify-content:space-between!important;padding:24px!important;background:linear-gradient(145deg,#0b2c63 0%,#10253d 58%,#0b6b45 145%)!important;color:#fff!important}
.projects .flip-card.is-flipped .flip-front{pointer-events:none!important}
.projects .flip-card.is-flipped .flip-back{pointer-events:auto!important}
.projects .copy{left:22px!important;right:22px!important;bottom:22px!important}
.projects .copy h3{font-size:27px!important;line-height:1.05!important;max-width:13ch!important}
.projects .copy p{margin-top:10px!important;font-size:12.5px!important;line-height:1.46!important;display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;overflow:hidden!important}
.projects .flip-back h3{margin:13px 0 0!important;font-size:25px!important;line-height:1.06!important;max-width:13ch!important}
.projects .case-text{margin:15px 0 0!important;font-size:12.7px!important;line-height:1.48!important}
.projects .case-status{margin-top:14px!important;padding-top:12px!important;font-size:9.5px!important;line-height:1.35!important}
.projects .flip-back .more{margin-top:12px!important;font-size:12px!important}

/* Same proportions for project showcases on International / Digital / homepage */
.projects-showcase .project-card{height:460px!important;min-height:460px!important;aspect-ratio:auto!important;border-radius:26px!important}
.projects-showcase .project-card.home-project-flip{overflow:visible!important;background:transparent!important;perspective:1400px!important}
.project-card.home-project-flip .home-project-inner{position:absolute!important;inset:0!important;height:100%!important;transform-style:preserve-3d!important;transition:transform .62s cubic-bezier(.2,.72,.2,1)!important;border-radius:26px!important}
.project-card.home-project-flip.is-flipped .home-project-inner{transform:rotateY(180deg)!important}
.project-card.home-project-flip .home-project-face{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;overflow:hidden!important;border-radius:26px!important;backface-visibility:hidden!important;-webkit-backface-visibility:hidden!important}
.project-card.home-project-flip .home-project-front{transform:rotateY(0deg)!important;pointer-events:auto!important}
.project-card.home-project-flip .home-project-back{transform:rotateY(180deg)!important;pointer-events:none!important;display:flex!important;flex-direction:column!important;justify-content:space-between!important;padding:23px!important;background:linear-gradient(145deg,#0b2c63 0%,#10253d 58%,#0b6b45 145%)!important;color:#fff!important}
.project-card.home-project-flip.is-flipped .home-project-front{pointer-events:none!important}
.project-card.home-project-flip.is-flipped .home-project-back{pointer-events:auto!important}
.project-card.home-project-flip .project-copy h3{font-size:26px!important;line-height:1.05!important;max-width:13ch!important}
.project-card.home-project-flip .project-copy p{font-size:12.5px!important;line-height:1.46!important}
.project-card.home-project-flip .home-project-back h3{font-size:24px!important;line-height:1.06!important;max-width:13ch!important;margin:13px 0 0!important}
.project-card.home-project-flip .home-project-back p{font-size:12.5px!important;line-height:1.48!important;margin-top:14px!important}
.project-card.home-project-flip .home-project-status{font-size:9.5px!important;line-height:1.35!important;margin-top:13px!important;padding-top:11px!important}
@media(max-width:980px){.projects .grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@media(max-width:700px){.projects .grid{grid-template-columns:1fr!important}.projects .card{height:440px!important;min-height:440px!important}.projects-showcase .project-card{height:420px!important;min-height:420px!important}.projects .flip-back,.project-card.home-project-flip .home-project-back{padding:21px!important}}
@media(prefers-reduced-motion:reduce){.projects .flip-card .flip-inner,.project-card.home-project-flip .home-project-inner{transition:none!important}}
</style>
'''

JS=r'''
<script id="projects-hub-stable-js">
(function(){
  const defs={
    'AGRO TAG':{k:'AGRO / TECHNOLOGY TRANSFER',t:'AGRO TAG',d:'Международный проект по подбору, локализации и трансферу агротехнологий и оборудования с комплексным сопровождением выхода на новые рынки.',s:'Стратегия · партнёрство · трансфер технологий',u:'agro-tag.html'},
    'Выход на рынок Сербии':{k:'ENTERING THE SERBIAN MARKET',t:'Выход технологического стартапа на рынок Сербии',d:'Вывод компании-стартапа из Узбекистана на рынок Сербии. Специализированное ПО для управления BMS-системами зданий. Проведена экспертиза решения, найден локальный партнёр. Проект масштабируется на рынки Балкан.',s:'Экспертиза · партнёр · масштабирование'},
    'Открытая лаборатория':{k:'OPEN LABORATORY',t:'Удалённый доступ к исследовательской инфраструктуре',d:'Поиск инвестора для проекта организации удалённого доступа к лабораторному оборудованию исследовательских организаций. Цель проекта — расширить возможности европейских учёных в проведении научных исследований.',s:'Инвестиции · наука · инфраструктура · доступ'},
    'Международная технологическая кооперация':{k:'OPEN LABORATORY',t:'Удалённый доступ к исследовательской инфраструктуре',d:'Поиск инвестора для проекта организации удалённого доступа к лабораторному оборудованию исследовательских организаций. Цель проекта — расширить возможности европейских учёных в проведении научных исследований.',s:'Инвестиции · наука · инфраструктура · доступ'},
    'Международные издательские проекты':{k:'INTERNATIONAL PUBLISHING PROJECT',t:'Международный книгоиздательский проект',d:'Организация международного издательского проекта по запросу сербского издательства. Международная команда экспертов и авторов готовит исторические книги для сербских читателей.',s:'Эксперты · авторы · локализация · издание'},
    'AGRO HOLDING':{k:'AGRO / INDUSTRIAL PARTNERSHIP',t:'Развитие агропромышленного проекта',d:'Комплексная работа с инфраструктурой, переработкой, технологическими партнёрами и развитием агробизнеса.',s:'Инфраструктура · переработка · партнёрство'},
    'Applied Research':{k:'APPLIED AI / BIOTECH',t:'Оптимизация работы ИИ-агентов',d:'Применение решения сербского разработчика ПО в крупной биотехнологической исследовательской компании. Платформа позволяет анализировать и управлять работой ИИ-агентов, а также снижать затраты на использование токенов при их работе.',s:'ИИ-агенты · контроль · аналитика · экономия'},
    'Banking Transformation':{k:'BANKING / MARKET ENTRY',t:'Цифровая трансформация банков Казахстана',d:'Вывод цифровой платформы сербского разработчика на рынок Центральной Азии. Внедрение решения на базе process mining и искусственного интеллекта в банках Казахстана для анализа и оптимизации бизнес-процессов.',s:'Process mining · AI · банки · Казахстан'}
  };

  function esc(s){return String(s||'').replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}

  function bind(card){
    if(card.dataset.flipBound==='1')return;
    card.dataset.flipBound='1';
    card.addEventListener('click',function(e){
      const more=e.target.closest('.flip-more');
      const back=e.target.closest('.flip-back-btn');
      if(more){e.preventDefault();e.stopPropagation();card.classList.add('is-flipped');more.setAttribute('aria-expanded','true')}
      if(back){e.preventDefault();e.stopPropagation();card.classList.remove('is-flipped');const m=card.querySelector('.flip-more');if(m)m.setAttribute('aria-expanded','false')}
    },true);
    card.addEventListener('keydown',function(e){if(e.key==='Escape'){card.classList.remove('is-flipped')}});
  }

  function normalizeMainProjects(){
    document.querySelectorAll('.projects .card').forEach(function(card){
      let title=(card.querySelector('.copy h3')||card.querySelector('.flip-front h3'));
      title=title?title.textContent.trim():'';
      const d=defs[title];
      if(!d){return}
      if(title==='Международная технологическая кооперация'){
        const h=card.querySelector('.copy h3'); if(h)h.textContent='Открытая лаборатория';
      }
      if(!card.classList.contains('flip-card')){
        const img=card.querySelector('img');
        const src=img?img.getAttribute('src'):'';
        const alt=img?img.getAttribute('alt'):title;
        const source=(card.querySelector('.source')||{}).outerHTML||'';
        const label=(card.querySelector('.label')||{}).outerHTML||'';
        const teaser=(card.querySelector('.copy p')||{}).textContent||'';
        const action=d.u?'<a class="more" href="'+esc(d.u)+'">Открыть проект →</a>':'<button class="more flip-back-btn" type="button">← Назад</button>';
        card.classList.add('flip-card');
        card.innerHTML='<div class="flip-inner"><div class="flip-face flip-front"><img src="'+esc(src)+'" alt="'+esc(alt)+'"/><div class="shade"></div>'+source+'<div class="copy">'+label+'<h3>'+esc(title)+'</h3><p>'+esc(teaser)+'</p><button class="more flip-more" type="button" aria-expanded="false">Подробнее →</button></div></div><div class="flip-face flip-back"><div><div class="label">'+esc(d.k)+'</div><h3>'+esc(d.t)+'</h3><p class="case-text">'+esc(d.d)+'</p><div class="case-status">'+esc(d.s)+'</div></div>'+action+'</div></div>';
        if(d.u){
          const link=card.querySelector('.flip-back a.more');
          if(link){link.insertAdjacentHTML('beforebegin','<button class="more flip-back-btn" type="button">← Назад</button> ')}
        }
      }
      bind(card);
    });
  }

  function normalizeShowcases(){
    document.querySelectorAll('.projects-showcase .project-card').forEach(function(card){
      const h=card.querySelector('.project-copy h3, h3');
      if(!h)return;
      let title=h.textContent.trim();
      const d=defs[title];
      if(!d)return;
      if(title==='Международная технологическая кооперация')title='Открытая лаборатория';
      if(card.classList.contains('home-project-flip')){bind(card);return}
      const img=card.querySelector('img'); const src=img?img.getAttribute('src'):''; const alt=img?img.getAttribute('alt'):title;
      const type=(card.querySelector('.project-type')||{}).textContent||d.k;
      const no=(card.querySelector('.project-no')||{}).textContent||'';
      const teaser=(card.querySelector('.project-copy p')||{}).textContent||d.s;
      card.classList.add('flip-card','home-project-flip');
      card.innerHTML='<div class="home-project-inner"><div class="home-project-face home-project-front"><img src="'+esc(src)+'" alt="'+esc(alt)+'"/><div class="project-shade"></div><div class="project-top"><span class="project-type">'+esc(type)+'</span><span class="project-no">'+esc(no)+'</span></div><div class="project-copy"><h3>'+esc(title)+'</h3><p>'+esc(teaser)+'</p><button class="project-more flip-more" type="button" aria-expanded="false">Подробнее</button></div></div><div class="home-project-face home-project-back"><div><div class="home-back-kicker">'+esc(d.k)+'</div><h3>'+esc(d.t)+'</h3><p>'+esc(d.d)+'</p><div class="home-project-status">'+esc(d.s)+'</div></div><button class="home-back flip-back-btn" type="button">← Назад</button></div></div>';
      bind(card);
    });
  }

  normalizeMainProjects();
  normalizeShowcases();
})();
</script>
'''

# Force all root-page menu links named Projects to the shared hub.
for p in ROOT.glob('*.html'):
    s=p.read_text(encoding='utf-8')
    s=re.sub(r'href="[^"]*#projects"([^>]*)>Проекты</a>',r'href="projects.html"\1>Проекты</a>',s)
    s=re.sub(r'href="#projects"([^>]*)>Проекты</a>',r'href="projects.html"\1>Проекты</a>',s)
    if p.name in ('index.html','international.html','digital-ai.html','projects.html'):
        if 'projects-hub-stable-style' not in s and '</head>' in s:
            s=s.replace('</head>',STYLE+'\n</head>',1)
        if 'projects-hub-stable-js' not in s and '</body>' in s:
            s=s.replace('</body>',JS+'\n</body>',1)
    p.write_text(s,encoding='utf-8')

projects=ROOT/'projects.html'
if not projects.exists():
    raise SystemExit('projects.html is missing from final Pages artifact')
s=projects.read_text(encoding='utf-8')
for marker in ('Выход на рынок Сербии','Открытая лаборатория','Международные издательские проекты','Applied Research','Banking Transformation'):
    if marker not in s:
        raise SystemExit('projects.html missing project: '+marker)
print('Projects hub route, card sizing and flip behaviour stabilized')
