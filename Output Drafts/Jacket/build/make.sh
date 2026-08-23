#!/bin/sh
# Rebuild every jacket asset.
set -e
cd "$(dirname "$0")"
python3 build_jacket.py             # technical flats, all colourways
python3 build_jacket_spec.py        # dimensioned spec sheet
python3 build_jacket_colourways.py  # colourway comparison sheet
python3 render_png.py               # PNG exports, with an aspect-ratio check
echo "done"
