#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')

LOCALES={
    'en':{
        'state_loading':'Updating feed…',
        'empty_loading':'Loading TESLA Alliance updates…',
        'more':'Read on atesla.rs →',
        'fallback':'The feed is temporarily unavailable. Original posts are available at',
        'source':'Source: atesla.rs',
        'updated':'Feed updated: ',
        'auto':'TESLA Alliance automatic feed',
        'locale':'en-GB',
    },
    'cz':{
        'state_loading':'Aktualizujeme přehled…',
        'empty_loading':'Načítáme novinky TESLA Alliance…',
        'more':'Číst na atesla.rs →',
        'fallback':'Přehled je dočasně nedostupný. Původní příspěvky najdete na',
        'source':'Zdroj: atesla.rs',
        'updated':'Přehled aktualizován: ',
        'auto':'Automatický přehled TESLA Alliance',
        'locale':'cs-CZ',
    }
}

CSS=r'''
<style id="localized-blog-mobile-fix-v1">
@media(max-width:850px){
  body{overflow-x:hidden!important}
  header.gobig-unified-header{display:block!important;position:sticky!important;top:0!important;z-index:3000!important;background:#fff!important;min-height:72px!important}
  header.gobig-unified-header .head{display:grid!important;visibility:visible!important;opacity:1!important}
  header.gobig-unified-header .brand{display:flex!important;visibility:visible!important;opacity:1!important}
  header.gobig-unified-header .mobile-menu-toggle{display:inline-flex!important;visibility:visible!important;opacity:1!important}
  .hero{padding-top:56px!important}
  .blog{padding-top:54px!important;padding-bottom:72px!important}
  .blog .grid{grid-template-columns:1fr!important;gap:18px!important}
  .blog .card{min-height:0!important;width:100%!important}
  .blog .media{height:210px!important}
  .blog .body{padding:22px!important}
  .blog .body h3{font-size:23px!important;line-height:1.12!important}
  .blog-top{display:block!important;margin-bottom:24px!important}
  .blog-top h2{font-size:clamp(34px,10vw,44px)!important}
  .sync-state{display:block!important;margin-top:8px!important}
  .empty{padding:24px!important;border-radius:18px!important}
}
</style>
'''

for lang,cfg in LOCALES.items():
    p=ROOT/lang/'blog.html'
    if not p.exists():
        raise SystemExit(f'Missing localized blog page: {p}')
    s=p.read_text(encoding='utf-8')

    # Localized pages live one directory below the shared feed.
    s=s.replace("fetch('assets/blog-data.json'", "fetch('../assets/blog-data.json'")
    s=s.replace('fetch("assets/blog-data.json"', 'fetch("../assets/blog-data.json"')

    # Normalize runtime copy regardless of how older translators transformed it.
    s=re.sub(r"state\.textContent='[^']*';", f"state.textContent='{cfg['source']}';", s, count=1)
    s=re.sub(r"state\.textContent='[^']*'\+d\.toLocaleString\('[^']+'", f"state.textContent='{cfg['updated']}'+d.toLocaleString('{cfg['locale']}'", s, count=1)
    s=re.sub(r"else state\.textContent='[^']*';", f"else state.textContent='{cfg['auto']}';", s, count=1)

    # Replace known UI strings left from RU or produced by prior passes.
    replacements={
        'Обновляем ленту…':cfg['state_loading'],
        'Загружаем публикации TESLA Alliance…':cfg['empty_loading'],
        'Читать на atesla.rs →':cfg['more'],
        'Лента временно недоступна. Оригинальные публикации можно посмотреть на':cfg['fallback'],
        'Источник: atesla.rs':cfg['source'],
        'Лента обновлена: ':cfg['updated'],
        'Автоматическая лента TESLA Alliance':cfg['auto'],
        'The feed is temporarily unavailable. Original posts are available at':cfg['fallback'],
        'Read on atesla.rs →':cfg['more'],
        'Source: atesla.rs':cfg['source'],
        'Feed updated: ':cfg['updated'],
        'TESLA Alliance automatic feed':cfg['auto'],
        'Přehled je dočasně nedostupný. Původní příspěvky najdete na':cfg['fallback'],
        'Číst na atesla.rs →':cfg['more'],
        'Zdroj: atesla.rs':cfg['source'],
        'Přehled aktualizován: ':cfg['updated'],
        'Automatický přehled TESLA Alliance':cfg['auto'],
    }
    for old,new in replacements.items():
        s=s.replace(old,new)

    # Ensure the card CTA itself is localized inside the JS template.
    s=re.sub(r'<div class="more">.*?atesla\.rs\s*→</div>', f'<div class="more">{cfg["more"]}</div>', s)

    # Ensure fallback remains compact and never replaces the visual hierarchy.
    fallback=f'''<div class="empty">{cfg['fallback']} <a href="https://www.atesla.rs/blog" target="_blank" rel="noopener" style="color:#0B6B45;font-weight:800">atesla.rs →</a></div>'''
    s=re.sub(r"grid\.innerHTML='<div class=\"empty\">.*?</div>';state\.textContent='[^']*';", lambda m: "grid.innerHTML='"+fallback+"';state.textContent='"+cfg['source']+"';", s, count=1)

    if 'localized-blog-mobile-fix-v1' not in s:
        s=s.replace('</head>',CSS+'\n</head>',1)

    p.write_text(s,encoding='utf-8')

    final=p.read_text(encoding='utf-8')
    if "../assets/blog-data.json" not in final:
        raise SystemExit(f'Localized blog feed path not fixed: {p}')
    if 'gobig-unified-header' not in final:
        raise SystemExit(f'Unified header missing on localized blog: {p}')
    if 'localized-blog-mobile-fix-v1' not in final:
        raise SystemExit(f'Blog mobile safety CSS missing: {p}')

print('Fixed EN/CZ blog feed paths, runtime copy and mobile header')
