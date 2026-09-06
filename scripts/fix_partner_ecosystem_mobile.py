#!/usr/bin/env python3
from pathlib import Path

ROOT=Path('dist')
CSS=r'''
<style id="partner-ecosystem-mobile-final">
@media(max-width:850px){
  .partners{padding:56px 0!important;overflow:hidden!important}
  .partners .wrap{width:calc(100% - 28px)!important;min-height:0!important}
  .partners h2{position:relative!important;width:100%!important;min-height:0!important;margin:0 0 28px!important;font-size:11px!important;line-height:1.4!important;color:#55b77e!important;letter-spacing:.16em!important}
  .partners h2::before,.partners h2::after{position:static!important;display:block!important;width:auto!important;max-width:100%!important;left:auto!important;top:auto!important}
  .partners h2::before{margin-top:12px!important;font-size:clamp(34px,10vw,44px)!important;line-height:1.02!important;letter-spacing:-.03em!important}
  .partners h2::after{margin-top:18px!important;font-size:14px!important;line-height:1.65!important;color:rgba(255,255,255,.68)!important}

  .partners .partner-grid{position:relative!important;inset:auto!important;width:100%!important;height:auto!important;margin:0!important;display:grid!important;grid-template-columns:1fr!important;gap:14px!important;background:none!important}
  .partners .partner-grid::before{position:relative!important;left:auto!important;top:auto!important;transform:none!important;width:132px!important;height:132px!important;margin:0 auto 8px!important;font-size:30px!important;grid-column:auto!important}
  .partners .partner-grid::after{position:relative!important;left:auto!important;top:auto!important;width:100%!important;min-height:0!important;margin:0!important;padding:18px!important;border-radius:18px!important;font-size:12px!important;line-height:1.6!important;grid-column:auto!important;white-space:normal!important}

  .partners .partner-card,
  .partners .partner-card:nth-child(1),
  .partners .partner-card:nth-child(2),
  .partners .partner-card:nth-child(3){
    position:relative!important;inset:auto!important;width:100%!important;max-width:100%!important;min-height:0!important;margin:0!important;padding:22px 18px!important;display:block!important;border-radius:22px!important;overflow:hidden!important;transform:none!important;box-shadow:none!important;cursor:default!important
  }
  .partners .partner-card h3{width:100%!important;margin:0!important;text-align:left!important}
  .partners .partner-card h3::before{margin:0!important;font-size:18px!important;line-height:1.25!important;text-align:left!important}
  .partners .partner-card h3::after{margin-top:8px!important;font-size:12px!important;line-height:1.5!important;text-align:left!important}

  /* Kill desktop hover tooltips on mobile. */
  .partners .partner-card::before,
  .partners .partner-card>ul::after{display:none!important;content:none!important}

  /* Business partners. */
  .partners .partner-card:nth-child(1){padding-bottom:22px!important}
  .partners .partner-card:nth-child(1)::after{content:"TESLA Alijansa HQ · Winno"!important;position:static!important;display:block!important;margin-top:16px!important;color:#72c99b!important;font-size:11px!important;line-height:1.5!important;text-align:left!important}

  /* University / experts and development institutions become normal stacked subcards. */
  .partners .partner-card:nth-child(2)>ul,
  .partners .partner-card:nth-child(3)>ul{
    position:relative!important;inset:auto!important;width:100%!important;min-height:0!important;margin:18px 0 0!important;padding:18px!important;display:block!important;border:1px solid rgba(139,196,164,.25)!important;border-radius:16px!important;background:rgba(7,20,26,.35)!important;box-shadow:none!important;overflow:hidden!important
  }
  .partners .partner-card:nth-child(2)>ul::before,
  .partners .partner-card:nth-child(3)>ul::before{display:block!important;white-space:normal!important;text-align:left!important;font-size:15px!important;line-height:1.45!important;color:#fff!important}

  /* Full institution lists: readable body text, never pseudo-tooltip overlays. */
  .partners .partner-card:nth-child(2)::after,
  .partners .partner-card:nth-child(3)::after{
    display:block!important;position:static!important;margin-top:16px!important;padding-top:14px!important;border-top:1px solid rgba(116,207,156,.16)!important;color:#72c99b!important;font-size:10.5px!important;line-height:1.55!important;white-space:pre-line!important;text-align:left!important
  }
  html[lang="ru"] .partners .partner-card:nth-child(2)::after{content:"Научно-технологический парк Нови-Сад\A Научно-технологический парк Чачак\A Научно-технологический парк Республики Сербской\A Ассоциация фермеров Казахстана\A Национальный инфраструктурный проект «Туран», Кыргызстан\A ОБФ «Кыргыз ТехноВумен»"!important}
  html[lang="ru"] .partners .partner-card:nth-child(3)::after{content:"Торгово-промышленная палата Воеводины\A Торгово-промышленная палата Республики Сербской\A Профильные ассоциации, институты развития и деловые объединения"!important}

  /* Hide legacy institution pseudo-content from locale CSS, which caused overlap. */
  html[lang="ru"] .partners .partner-card:nth-child(2)::before,
  html[lang="en"] .partners .partner-card:nth-child(2)::before,
  html[lang="cs"] .partners .partner-card:nth-child(2)::before,
  html[lang="cz"] .partners .partner-card:nth-child(2)::before{display:none!important;content:none!important}
}
</style>
'''

for rel in ('international.html','en/international.html','cz/international.html'):
    p=ROOT/rel
    if not p.exists():
        continue
    s=p.read_text(encoding='utf-8')
    if '<section class="partners"' not in s:
        raise SystemExit(f'Partners section missing: {rel}')
    if 'partner-ecosystem-mobile-final' not in s:
        s=s.replace('</head>',CSS+'\n</head>',1)
    p.write_text(s,encoding='utf-8')

print('Applied final mobile layout for partner ecosystem')
