#!/bin/sh
set -eu

sh build-base.sh
cp projects.html dist/projects.html
cp berry-harvesting.html dist/berry-harvesting.html
cp berry-harvesting-web.mp4 dist/berry-harvesting-web.mp4
cp blog.html dist/blog.html
cp assets/agro-tag-contact.html dist/agro-tag-contact.html
if [ -f assets/blog-data.json ]; then
  cp assets/blog-data.json dist/assets/blog-data.json
fi
if [ -d catalogs ]; then
  mkdir -p dist/catalogs
  cp -R catalogs/. dist/catalogs/
fi

python scripts/final_site_fixes.py
python scripts/compact_project_cards.py
python scripts/restore_projects_hub.py
python scripts/stabilize_projects_hub.py
python scripts/normalize_main_header.py
python scripts/fix_agro_tag_links.py
python scripts/force_agro_direct_link.py

python scripts/restore_berry_final.py
python scripts/berry_final_lock.py dist

python scripts/mobile_guardrails.py
python scripts/restore_partner_ecosystem.py
python scripts/align_home_stats.py
python scripts/fix_mobile_menu_runtime.py
python scripts/mobile_menu_overlay.py
python scripts/fix_partner_ecosystem_mobile.py
python scripts/final_agro_publish_fixes.py

python scripts/localize_site_v2.py dist
python scripts/localize_cleanup.py dist
python scripts/fix_localized_blog.py dist
python scripts/locale_final_qa.py dist
python scripts/mobile_final_audit.py dist

python scripts/berry_final_lock.py dist
python scripts/localize_berry_final.py dist
python scripts/fix_berry_locales.py dist
python scripts/rebuild_berry_models.py dist
python scripts/match_gentle_reference.py dist

python scripts/localize_berry_final.py dist
python scripts/berry_locale_postfix.py dist
python scripts/match_gentle_reference.py dist

python scripts/berry_final_lock.py dist
python scripts/mobile_final_audit.py dist
python scripts/berry_final_lock.py dist
python scripts/berry_locale_postfix.py dist
python scripts/match_gentle_reference.py dist
python scripts/berry_locale_postfix.py dist

# Final authority for language switches in the generated legacy RU/EN/CZ layout.
python scripts/final_language_switch_fix.py dist

# Final authority for key CTA routes before the language-root promotion.
python scripts/fix_home_cta_links.py dist

# Final repair for berry subnavigation before the language-root promotion.
python scripts/fix_berry_gentle_anchor.py dist

# Add the manufacturer catalog subsection only after every localisation/repair pass.
python scripts/add_manufacturer_catalogs.py dist

# Publish English as the canonical root, preserve Russian under /ru/,
# keep Czech under /cz/, and retain /en/ as a backward-compatible alias.
python scripts/publish_english_root.py dist

# These audits run AFTER the route promotion and validate the actual publish tree.
python scripts/final_anchor_audit.py dist
python scripts/final_site_integrity_audit.py dist
