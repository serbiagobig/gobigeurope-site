#!/bin/sh
set -eu

sh build-base.sh
cp projects.html dist/projects.html
cp berry-harvesting.html dist/berry-harvesting.html
cp blog.html dist/blog.html
if [ -f assets/blog-data.json ]; then
  cp assets/blog-data.json dist/assets/blog-data.json
fi
python scripts/final_site_fixes.py
python scripts/compact_project_cards.py
python scripts/restore_projects_hub.py
python scripts/stabilize_projects_hub.py
python scripts/normalize_main_header.py
python scripts/fix_agro_tag_links.py
