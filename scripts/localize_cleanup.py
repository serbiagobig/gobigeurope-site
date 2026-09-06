#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
SCRIPT=Path(__file__).resolve().parent

def run(name):
    subprocess.run([sys.executable,str(SCRIPT/name),str(ROOT)],check=True)

# localize_site_v2.py is expected to have created the standard EN/CZ pages first.
# Apply all content introduced by later project-card/mobile/runtime work, then create
# the Berry page locales, normalize language switches and run strict final QA.
run('localize_current_overrides.py')
run('localize_runtime_residuals.py')
run('localize_berry_final.py')
run('normalize_language_switches.py')
run('locale_final_qa.py')

print('Final localisation cleanup passed for EN/CZ.')
