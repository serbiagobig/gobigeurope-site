#!/bin/sh
set -eu

sh build-base.sh
cp projects.html dist/projects.html
cp blog.html dist/blog.html
cp assets/agro-tag-contact.html dist/agro-tag-contact.html
if [ -f assets/blog-data.json ]; then
  cp assets/blog-data.json dist/assets/blog-data.json
fi
python scripts/final_site_fixes.py
python scripts/compact_project_cards.py
python scripts/restore_projects_hub.py
python scripts/stabilize_projects_hub.py
python scripts/normalize_main_header.py
python scripts/fix_agro_tag_links.py
python scripts/force_agro_direct_link.py
python scripts/mobile_guardrails.py
python scripts/restore_partner_ecosystem.py
python scripts/align_home_stats.py
python scripts/fix_mobile_menu_runtime.py
python scripts/mobile_menu_overlay.py
python scripts/fix_partner_ecosystem_mobile.py
python scripts/final_agro_publish_fixes.py

# Generate EN/CZ only after the final RU structure is complete, so all three languages
# share the same current layout, links and mobile behaviour.
python scripts/localize_site_v2.py dist
python scripts/localize_cleanup.py dist
python scripts/fix_localized_blog.py dist
python scripts/locale_final_qa.py dist

# Final authority for all mobile behaviour. This runs after localisation and every
# legacy/post-build fixer so earlier responsive rules cannot re-break the published site.
python scripts/mobile_final_audit.py dist

# The berry-equipment route is retired. Remove any stale copies/references and then run
# a full-site audit over every published RU/EN/CZ HTML page and local asset reference.
python scripts/retire_berry_route.py dist
python scripts/final_site_integrity_audit.py dist
