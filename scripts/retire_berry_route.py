#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')

# The separate berry-equipment landing page is retired. Remove every published locale copy.
for rel in ('berry-harvesting.html','en/berry-harvesting.html','cz/berry-harvesting.html'):
    p=ROOT/rel
    if p.exists():
        p.unlink()
        print('Removed retired route:',rel)

# No published page may still navigate to the retired route. Redirect any stale links
# back to the corresponding AGRO TAG page in the same locale.
for p in list(ROOT.glob('*.html'))+list(ROOT.glob('en/*.html'))+list(ROOT.glob('cz/*.html')):
    s=p.read_text(encoding='utf-8')
    original=s
    s=re.sub(r'href=["\'](?:\.\./)?berry-harvesting\.html(?:#[^"\']*)?["\']', 'href="agro-tag.html"', s, flags=re.I)
    s=s.replace("window.location.href = 'berry-harvesting.html';", "window.location.href = 'agro-tag.html';")
    s=s.replace('window.location.href = "berry-harvesting.html";', 'window.location.href = "agro-tag.html";')
    s=s.replace("window.location.href='berry-harvesting.html';", "window.location.href='agro-tag.html';")
    s=s.replace('window.location.href="berry-harvesting.html";', 'window.location.href="agro-tag.html";')
    if s!=original:
        p.write_text(s,encoding='utf-8')
        print('Removed stale berry navigation from',p.relative_to(ROOT))

# Hard guardrail: fail instead of silently re-publishing the retired page or a link to it.
errors=[]
for rel in ('berry-harvesting.html','en/berry-harvesting.html','cz/berry-harvesting.html'):
    if (ROOT/rel).exists(): errors.append('retired route still exists: '+rel)
for p in list(ROOT.glob('*.html'))+list(ROOT.glob('en/*.html'))+list(ROOT.glob('cz/*.html')):
    s=p.read_text(encoding='utf-8')
    if re.search(r'berry-harvesting\.html',s,re.I):
        errors.append('retired route referenced by '+str(p.relative_to(ROOT)))
if errors:
    for e in errors: print('ERROR:',e)
    raise SystemExit('Berry route retirement guard failed')
print('PASS: retired berry route and all published links to it are absent')
