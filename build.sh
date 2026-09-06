#!/bin/sh
set -eu

sh build-base.sh
cp projects.html dist/projects.html
cp berry-harvesting.html dist/berry-harvesting.html
python scripts/final_site_fixes.py
python scripts/compact_project_cards.py
python scripts/restore_projects_hub.py
