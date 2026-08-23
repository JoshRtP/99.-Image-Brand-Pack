#!/bin/sh
# Rebuild the character costume turnaround.
set -e
cd "$(dirname "$0")"
python3 build_turnaround.py   # turnaround sheet + five single angles
python3 render_png.py         # PNG exports, with an aspect-ratio check
echo "done"
