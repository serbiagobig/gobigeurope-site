#!/bin/sh
set -eu

sh build-base.sh
cp projects.html dist/projects.html
python scripts/final_site_fixes.py
