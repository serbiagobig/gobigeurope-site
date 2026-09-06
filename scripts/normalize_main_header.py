#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path('dist')
CORE = ['index.html','international.html','digital-ai.html','education-hr.html','projects.html','blog.html']

STYLE = r'''
<style id="gobig-unified-header-style">
header.gobig-unified-header{position:sticky!important;top:0!important;z-index:100!important;background:rgba(255,255,255,.97)!important;border-bottom:1px solid rgba(11,44,99,.10)!important;backdrop-filter:blur(10px)!important}
header.gobig-unified-header .head{width:min(1200px,calc(100% - 48px))!important;min-height:100px!important;margin:0 auto!important;display:flex!important;align-items:center!important;justify-content:space-between!important;gap:26px!important;padding:0!important}
header.gobig-unified-header .brand{display:flex!important;align-items:center!important;gap:16px!important;flex:0 0 auto!important;text-decoration:none!important}
header.gobig-unified-header .mark{width:56px!important;height:70px!important;background:#0B6B45!important;display:block!important;flex:0 0 auto!important}
header.gobig-unified-header .brand strong{display:block!important;margin:0!important;color:#0B6B45!important;font:700 31px/1 "Source Serif 4",Georgia,serif!important;letter-spacing:.02em!important}
header.gobig-unified-header .brand small{display:block!important;margin-top:5px!important;color:#0B6B45!important;font:400 11px/1.2 Manrope,Arial,sans-serif!important}
header.gobig-unified-header .nav{margin-left:auto!important;display:flex!important;align-items:center!important;justify-content:flex-end!important;gap:25px!important;flex-wrap:nowrap!important;width:auto!important;overflow:visible!important;white-space:nowrap!important;padding:0!important}
header.gobig-unified-header .nav>a{display:inline-flex!important;align-items:center!important;min-height:48px!important;padding:0!important;border:0!important;color:#243045!important;font:600 15px/1.2 Manrope,Arial,sans-serif!important;text-decoration:none!important}
header.gobig-unified-header .nav>a:hover,header.gobig-unified-header .nav>a.active{color:#0B6B45!important}
header.gobig-unified-header .nav>a.active{box-shadow:inset 0 -2px 0 #0B6B45!important}
header.gobig-unified-header .nav>a.contact{min-height:50px!important;padding:0 20px!important;border:1px solid #0B6B45!important;color:#0B6B45!important;box-shadow:none!important}
header.gobig-unified-header .lang-switch{display:flex!important;align-items:center!important;gap:8px!important;margin-left:4px!important;color:#9aa3ad!important;font:700 13px/1 Manrope,Arial,sans-serif!important}
header.gobig-unified-header .lang-switch a{padding:0!important;border:0!important;color:#7c8795!important;text-decoration:none!important;font:700 13px/1 Manrope,Arial,sans-serif!important}
header.gobig-unified-header .lang-switch a.current{color:#0B6B45!important}
header.gobig-unified-header .lang-sep{color:#b7bec6!important;font-weight:500!important}
@media(max-width:1080px){header.gobig-unified-header .head{gap:18px!important}header.gobig-unified-header .nav{gap:16px!important}header.gobig-unified-header .nav>a{font-size:13px!important}header.gobig-unified-header .mark{width:48px!important;height:60px!important}header.gobig-unified-header .brand strong{font-size:28px!important}}
@media(max-width:850px){
 header.gobig-unified-header .head{width:calc(100% - 28px)!important;min-height:78px!important;display:flex!important;flex-direction:row!important;align-items:center!important;flex-wrap:wrap!important;gap:12px!important;padding:10px 0!important}
 header.gobig-unified-header .mark{width:38px!important;height:48px!important}header.gobig-unified-header .brand strong{font-size:24px!important}
 header.gobig-unified-header .site-nav-fix-btn{display:inline-flex!important}
 header.gobig-unified-header .nav{display:none!important;order:10!important;width:100%!important;margin:0!important;padding:10px 0 8px!important;gap:0!important;border-top:1px solid rgba(11,44,99,.09)!important;white-space:normal!important}
 header.gobig-unified-header .nav.site-nav-fix-open{display:flex!important;flex-direction:column!important;align-items:stretch!important}
 header.gobig-unified-header .nav>a{width:100%!important;min-height:0!important;padding:11px 4px!important;font-size:14px!important;border-bottom:1px solid rgba(11,44,99,.06)!important;box-shadow:none!important}
 header.gobig-unified-header .nav>a.contact{border:0!important;border-bottom:1px solid rgba(11,44,99,.06)!important;padding:11px 4px!important}
 header.gobig-unified-header .lang-switch{padding:13px 4px 5px!important;margin:0!important}
}
</style>
'''


def nav(active):
    def a(href, label, key, cls=''):
        classes=[]
        if cls: classes.append(cls)
        if active==key: classes.append('active')
        c=f' class="{" ".join(classes)}"' if classes else ''
        return f'<a{c} href="{href}">{label}</a>'
    return (
        a('international.html','Международное сотрудничество','international')+
        a('digital-ai.html','Цифровизация и ИИ','digital')+
        a('education-hr.html','Образование и HR','education')+
        a('projects.html','Проекты','projects')+
        a('blog.html','Блог','blog')+
        a('index.html#contact','Контакты','contact','contact')+
        '<span class="lang-switch">'
        '<a href="en/index.html">EN</a><span class="lang-sep">/</span>'
        '<a href="cz/index.html">CZ</a><span class="lang-sep">/</span>'
        '<a class="current" href="index.html">RU</a>'
        '</span>'
    )

ACTIVE = {
    'index.html': None,
    'international.html': 'international',
    'digital-ai.html': 'digital',
    'education-hr.html': 'education',
    'projects.html': 'projects',
    'blog.html': 'blog',
}

for name in CORE:
    p=ROOT/name
    if not p.exists():
        raise SystemExit(f'Missing core page: {name}')
    s=p.read_text(encoding='utf-8')
    header=(
        '<header class="gobig-unified-header"><div class="head">'
        '<a class="brand" href="index.html"><span class="mark"></span><span><strong>GO BIG</strong><small>žádné omezení</small></span></a>'
        f'<nav class="nav">{nav(ACTIVE[name])}</nav>'
        '</div></header>'
    )
    s,n=re.subn(r'<header\b[^>]*>.*?</header>',header,s,count=1,flags=re.S|re.I)
    if n!=1:
        raise SystemExit(f'Could not replace header in {name}')
    if 'gobig-unified-header-style' not in s:
        if '</head>' not in s:
            raise SystemExit(f'No </head> in {name}')
        s=s.replace('</head>',STYLE+'\n</head>',1)
    p.write_text(s,encoding='utf-8')

print('Unified GO BIG header across core pages; language order EN / CZ / RU')
