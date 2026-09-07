#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
PAGES=('international.html','digital-ai.html','projects.html','index.html')
PROJECT_ASSETS=(
    'project-agriculture.png','projects-serbia.png','projects-tech.png','projects-publishing.png',
    'project-plum-sum.png','project-laboratory.png','project-bank.png'
)

for lang in ('en','cz'):
    for name in PAGES:
        p=ROOT/lang/name
        if not p.exists():
            continue
        s=p.read_text(encoding='utf-8')

        # Project images live in the shared root /assets directory. Any localized page
        # path starting with assets/... incorrectly resolves to /en/assets or /cz/assets.
        for asset in PROJECT_ASSETS:
            s=s.replace(f'src="assets/{asset}"', f'src="../assets/{asset}"')
            s=s.replace(f"src='assets/{asset}'", f"src='../assets/{asset}'")
            s=s.replace(f'"assets/{asset}"', f'"../assets/{asset}"')
            s=s.replace(f"'assets/{asset}'", f"'../assets/{asset}'")
            s=s.replace(f'url(assets/{asset})', f'url(../assets/{asset})')
            s=s.replace(f'url("assets/{asset}")', f'url("../assets/{asset}")')
            s=s.replace(f"url('assets/{asset}')", f"url('../assets/{asset}')")

        p.write_text(s,encoding='utf-8')

        final=p.read_text(encoding='utf-8')
        for asset in PROJECT_ASSETS:
            bad=[f'src="assets/{asset}"',f"src='assets/{asset}'",f'"assets/{asset}"',f"'assets/{asset}'"]
            if any(x in final for x in bad):
                raise SystemExit(f'Bad localized project asset path remains in {p}: {asset}')

print('Fixed final EN/CZ project-card asset paths')
