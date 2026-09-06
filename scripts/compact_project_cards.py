#!/usr/bin/env python3
from pathlib import Path

STYLE = r'''
<style id="compact-project-card-standard">
/* One compact visual standard for project cards across International, Digital & AI and Projects. */
.projects-showcase .project-card{min-height:440px!important}
.projects-showcase .project-copy{left:22px!important;right:22px!important;bottom:22px!important}
.projects-showcase .project-copy h3{font-size:clamp(23px,1.55vw,28px)!important;line-height:1.06!important;max-width:13ch!important}
.projects-showcase .project-copy p{margin-top:10px!important;font-size:12.5px!important;line-height:1.48!important;display:-webkit-box!important;-webkit-line-clamp:3!important;-webkit-box-orient:vertical!important;overflow:hidden!important}
.projects-showcase .project-more{margin-top:15px!important;font-size:12px!important}

/* Flipped project cards used on International and Digital & AI. */
.project-card.home-project-flip .home-project-back{padding:24px!important}
.project-card.home-project-flip .home-project-back h3{margin-top:14px!important;font-size:27px!important;line-height:1.05!important;max-width:12ch!important}
.project-card.home-project-flip .home-project-back p{margin-top:16px!important;font-size:13px!important;line-height:1.5!important}
.project-card.home-project-flip .home-project-status{margin-top:15px!important;padding-top:13px!important;font-size:9.5px!important;line-height:1.4!important}
.project-card.home-project-flip .home-back{margin-top:13px!important;font-size:12px!important}

/* Main Projects page. */
.projects .card .copy{left:22px!important;right:22px!important;bottom:22px!important}
.projects .card .copy h3{font-size:28px!important;line-height:1.04!important;max-width:13ch!important}
.projects .card .copy p{margin-top:10px!important;font-size:12.5px!important;line-height:1.48!important;display:-webkit-box!important;-webkit-line-clamp:2!important;-webkit-box-orient:vertical!important;overflow:hidden!important}
.projects .card .more{margin-top:15px!important}
.projects .flip-back{padding:24px!important}
.projects .flip-back h3{margin-top:14px!important;font-size:27px!important;line-height:1.05!important;max-width:12ch!important}
.projects .case-text{margin-top:16px!important;font-size:13px!important;line-height:1.5!important}
.projects .case-status{margin-top:15px!important;padding-top:13px!important;font-size:9.5px!important;line-height:1.4!important}
.projects .flip-back .more{margin-top:13px!important}

@media(max-width:760px){
  .projects-showcase .project-card{min-height:380px!important;aspect-ratio:auto!important}
  .projects-showcase .project-copy h3{font-size:25px!important}
  .project-card.home-project-flip .home-project-back{padding:21px!important}
  .project-card.home-project-flip .home-project-back h3{font-size:25px!important}
  .project-card.home-project-flip .home-project-back p{font-size:12.5px!important;line-height:1.46!important}
  .projects .card{min-height:430px!important}
  .projects .card .copy h3{font-size:26px!important}
  .projects .flip-back{padding:21px!important}
  .projects .flip-back h3{font-size:25px!important}
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
