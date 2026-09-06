#!/usr/bin/env python3
from pathlib import Path

p=Path('dist/index.html')
if not p.exists():
    raise SystemExit('Missing dist/index.html')
s=p.read_text(encoding='utf-8')

STYLE=r'''
<style id="home-stats-mobile-align">
@media(max-width:850px){
  .home-stat-mobile-wrap{display:grid!important;grid-template-columns:1fr!important;width:100%!important;max-width:100%!important;gap:0!important}
  .home-stat-mobile-card{width:100%!important;max-width:100%!important;min-width:0!important;margin:0!important;padding:20px 14px!important;text-align:left!important;justify-self:stretch!important;align-self:stretch!important;border-left:0!important;border-right:0!important}
  .home-stat-mobile-card>*{margin-left:0!important;margin-right:0!important;text-align:left!important;justify-content:flex-start!important}
  .home-stat-mobile-card strong,.home-stat-mobile-card b,.home-stat-mobile-card .num,.home-stat-mobile-card .number{display:block!important;margin:0!important;text-align:left!important}
  .home-stat-mobile-card small,.home-stat-mobile-card span,.home-stat-mobile-card p{display:block!important;margin-left:0!important;text-align:left!important}
}
</style>
'''

JS=r'''
<script id="home-stats-mobile-align-runtime">
(function(){
  function textOf(el){return (el.textContent||'').replace(/\s+/g,' ').trim();}
  function init(){
    var wanted=['13+','10+','300+','100+'];
    var found=[];
    document.querySelectorAll('body *').forEach(function(el){
      var t=textOf(el);
      if(wanted.indexOf(t)!==-1 && el.children.length===0) found.push(el);
    });
    var unique=[];
    wanted.forEach(function(w){
      var hit=found.find(function(el){return textOf(el)===w;});
      if(hit) unique.push(hit);
    });
    if(unique.length!==4) return;

    function cardFor(el){
      var n=el;
      for(var i=0;i<5 && n && n.parentElement;i++,n=n.parentElement){
        var txt=textOf(n);
        var count=wanted.filter(function(w){return txt.indexOf(w)!==-1;}).length;
        if(count===1 && n.children.length>1) return n;
      }
      return el.parentElement;
    }
    var cards=unique.map(cardFor);
    var wrap=cards[0].parentElement;
    while(wrap && !cards.every(function(c){return wrap.contains(c);})){wrap=wrap.parentElement;}
    if(!wrap) return;
    wrap.classList.add('home-stat-mobile-wrap');
    cards.forEach(function(c){c.classList.add('home-stat-mobile-card');});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>
'''

if 'home-stats-mobile-align' not in s:
    s=s.replace('</head>',STYLE+'\n</head>',1)
if 'home-stats-mobile-align-runtime' not in s:
    s=s.replace('</body>',JS+'\n</body>',1)

for marker in ('13+','10+','300+','100+'):
    if marker not in s:
        raise SystemExit(f'Homepage stat missing: {marker}')

p.write_text(s,encoding='utf-8')
print('Aligned homepage mobile statistics')
