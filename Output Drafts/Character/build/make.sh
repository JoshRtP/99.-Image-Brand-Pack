#!/bin/sh
# Rebuild the character costume turnaround.
set -e
cd "$(dirname "$0")"
python3 shots.py --check      # every reference the brief names must exist
python3 shots.py --json       # machine-readable shot list
python3 build_sheet.py        # character sheet - photographic plates, plus any generated ones
python3 build_turnaround.py   # garment turnaround + five single angles
python3 render_png.py         # PNG exports, with an aspect-ratio check
echo "done"
