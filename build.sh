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

python scripts/final_site_fixes.py
python scripts/compact_project_cards.py
python scripts/restore_projects_hub.py
python scripts/stabilize_projects_hub.py
python scripts/normalize_main_header.py
python scripts/fix_agro_tag_links.py
python scripts/force_agro_direct_link.py

# Build the approved RU berry page once, immediately normalise it, and treat that output
# as the canonical berry source for the rest of this build.
python scripts/restore_berry_final.py
python scripts/berry_final_lock.py dist

python scripts/mobile_guardrails.py
python scripts/restore_partner_ecosystem.py
python scripts/align_home_stats.py
python scripts/fix_mobile_menu_runtime.py
python scripts/mobile_menu_overlay.py
python scripts/fix_partner_ecosystem_mobile.py
python scripts/final_agro_publish_fixes.py

# Generate EN/CZ from the canonical RU state.
python scripts/localize_site_v2.py dist
python scripts/localize_cleanup.py dist
python scripts/fix_localized_blog.py dist
python scripts/locale_final_qa.py dist

# Final authority for mobile behaviour across the site.
python scripts/mobile_final_audit.py dist

# Re-lock the berry pages after every generic post-build/localisation/mobile pass.
# This step is idempotent and removes the exact legacy fragments that caused repeated regressions.
python scripts/berry_final_lock.py dist
python scripts/localize_berry_final.py dist

# Restore approved berry visual modules.
python scripts/fix_berry_locales.py dist
python scripts/rebuild_berry_models.py dist

# Match the gentle-harvesting module exactly to the approved reference composition.
python scripts/match_gentle_reference.py dist

# Rebuild EN/CZ one final time from the now-complete RU page so late visual rebuilds
# cannot reintroduce stale localized structure.
python scripts/localize_berry_final.py dist
python scripts/berry_locale_postfix.py dist
python scripts/match_gentle_reference.py dist

python scripts/berry_final_lock.py dist
python scripts/mobile_final_audit.py dist
python scripts/berry_final_lock.py dist
python scripts/berry_locale_postfix.py dist

# localize_berry_final rebuilds late berry modules from RU. Reapply the authoritative
# translated technology/crop module after the final lock so no Cyrillic can leak back
# into the EN/CZ production pages. Then restore the approved gentle composition.
python scripts/fix_berry_locales.py dist
python scripts/match_gentle_reference.py dist

# Final integrity audit over every published RU/EN/CZ HTML page and local asset reference.
python scripts/final_site_integrity_audit.py dist
