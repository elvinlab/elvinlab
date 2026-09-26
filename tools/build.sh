#!/usr/bin/env bash
# Regenerate every profile SVG in ../assets and embed the fonts.
set -euo pipefail
cd "$(dirname "$0")"
[ -d .venv ] || { python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt; }
[ -d fonts ] || ./fetch_fonts.sh
.venv/bin/python banner.py
.venv/bin/python sections.py
.venv/bin/python embed_fonts.py ../assets/banner-*.svg ../assets/cards-*.svg ../assets/timeline-*.svg ../assets/strip-*.svg
