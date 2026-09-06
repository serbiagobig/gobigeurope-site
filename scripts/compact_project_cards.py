#!/usr/bin/env python3
from pathlib import Path

STYLE = r'''
<style id="compact-project-card-standard">
/* One compact visual standard for project cards across International, Digital & AI and Projects. */
.projects-showcase .projects-grid{gap:18px!important;align-items:stretch!important}
.projects-showcase .project-card{min-height:440px!important;border-radius:26px!important}
.projects-showcase .project-copy{left:22px!important;right:22px!important;bottom:22px!important}
.projects-showcase .project-copy h3{font-size:clamp(22px,1.45vw,27px)!important;line-height:1.06!important;max-width:15ch!important;color:#fff!important;text-shadow:0 2px 12px rgba(0,0,0,.26)!important}
.projects-showcase .project-copy p{margin-top:10px!important;font-size:12.5px!important;line-height:1.48!important;color:rgba(255,255,255,.9)!important;display:-webkit-box!important;-webkit-line-clamp:3!important;-webkit-box-orient:vertical!important;overflow:hidden!important}
.projects-showcase .project-more{margin-top:15px!important;font-size:12px!important;color:#78d3a3!important;position:relative!important;z-index:5!important}

/* Critical fix: the original project-card pseudo overlay sat ABOVE the injected flip faces. */
.project-card.home-project-flip:after{display:none!important;content:none!important}
.project-card.home-project-flip{overflow:visible!important;background:transparent!important;box-shadow:none!important;isolation:isolate!important}
.project-card.home-project-flip .home-project-inner{overflow:visible!important;border-radius:26px!important}
.project-card.home-project-flip .home-project-face{border-radius:26px!important;overflow:hidden!important}
.project-card.home-project-flip .home-project-front:after{content:""!important;position:absolute!important;inset:0!important;z-index:1!important;background:linear-gradient(180deg,rgba(7,27,53,.02) 18%,rgba(7,27,53,.28) 53%,rgba(7,27,53,.91) 100%)!important;pointer-events:none!important}
.project-card.home-project-flip .home-project-front .project-shade{display:none!important}
.project-card.home-project-flip .home-project-front .project-top,
.project-card.home-project-flip .home-project-front .project-copy{z-index:3!important}
.project-card.home-project-flip .home-project-front .project-type,
.project-card.home-project-flip .home-project-front .project-no{color:#fff!important}

/* Flipped project cards used on International and Digital & AI. */
.project-card.home-project-flip .home-project-back{padding:24px!important}
.project-card.home-project-flip .home-project-back h3{margin-top:14px!important;font-size:26px!important;line-height:1.05!important;max-width:14ch!important;color:#fff!important}
.project-card.home-project-flip .home-project-back p{margin-top:16px!important;font-size:12.8px!important;line-height:1.5!important;color:rgba(255,255,255,.9)!important}
.project-card.home-project-flip .home-project-status{margin-top:15px!important;padding-top:13px!important;font-size:9.5px!important;line-height:1.4!important}
.project-card.home-project-flip .home-back{margin-top:13px!important;font-size:12px!important;color:#fff!important;position:relative!important;z-index:5!important}

/* Main Projects page. */
.projects .grid{gap:20px!important;align-items:stretch!important}
.projects .card{border-radius:26px!important}
.projects .card .copy{left:22px!important;right:22px!important;bottom:22px!important}
.projects .card .copy h3{font-size:27px!important;line-height:1.04!important;max-width:15ch!important;color:#fff!important}
.projects .card .copy p{margin-top:10px!important;font-size:12.5px!important;line-height:1.48!important;color:rgba(255,255,255,.9)!important;display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;overflow:hidden!important}
.projects .card .more{margin-top:15px!important}
.projects .flip-back{padding:24px!important}
.projects .flip-back h3{margin-top:14px!important;font-size:26px!important;line-height:1.05!important;max-width:14ch!important;color:#fff!important}
.projects .case-text{margin-top:16px!important;font-size:12.8px!important;line-height:1.5!important;color:rgba(255,255,255,.9)!important}
.projects .case-status{margin-top:15px!important;padding-top:13px!important;font-size:9.5px!important;line-height:1.4!important}
.projects .flip-back .more{margin-top:13px!important;color:#fff!important}

@media(max-width:980px){
  .projects-showcase .projects-grid{grid-template-columns:repeat(2,minmax(0,1fr))!important}
}
@media(max-width:760px){
  .projects-showcase .projects-grid{grid-template-columns:1fr!important;gap:16px!important}
  .projects-showcase .project-card{min-height:390px!important;aspect-ratio:auto!important}
  .projects-showcase .project-copy h3{font-size:24px!important}
  .project-card.home-project-flip .home-project-back{padding:21px!important}
  .project-card.home-project-flip .home-project-back h3{font-size:24px!important}
  .project-card.home-project-flip .home-project-back p{font-size:12.5px!important;line-height:1.46!important}
  .projects .card{min-height:430px!important}
  .projects .card .copy h3{font-size:25px!important}
  .projects .flip-back{padding:21px!important}
  .projects .flip-back h3{font-size:24px!important}
  .projects .case-text{font-size:12.5px!important;line-height:1.46!important}
}
</style>
'''

for name in ('international.html', 'digital-ai.html', 'projects.html'):
    path = Path('dist') / name
    if not path.exists():
        raise SystemExit(f'Missing {name} in dist')
    s = path.read_text(encoding='utf-8')
    if 'compact-project-card-standard' not in s:
        if '</head>' not in s:
            raise SystemExit(f'No </head> in {name}')
        s = s.replace('</head>', STYLE + '\n</head>', 1)
        path.write_text(s, encoding='utf-8')

print('Applied compact project-card standard to International, Digital & AI and Projects')
