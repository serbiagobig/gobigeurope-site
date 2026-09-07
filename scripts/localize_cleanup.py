#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT=Path(sys.argv[1] if len(sys.argv)>1 else 'dist')
SCRIPT=Path(__file__).resolve().parent

def run(name):
    subprocess.run([sys.executable,str(SCRIPT/name),str(ROOT)],check=True)

# localize_site_v2.py creates the standard EN/CZ pages from the final RU build.
# These post-passes deliberately run afterwards to repair late runtime/project content,
# generate the Berry routes, rebuild locale navigation, repair known runtime language
# contamination, and only then run strict QA.
run('localize_current_overrides.py')
run('localize_runtime_residuals.py')
run('localize_berry_final.py')
run('finalize_locale_details.py')
run('normalize_localized_headers.py')
run('normalize_language_switches.py')
run('fix_locale_runtime_contamination.py')
run('locale_final_qa.py')

print('Final localisation cleanup passed for EN/CZ.')
