#!/bin/sh
# Rebuild every patch asset from the brand master PNG.
set -e
cd "$(dirname "$0")"
python3 trace.py                 # vectorise the wordmark and star
python3 trace_star_stitch.py     # stitch-safe star variant
python3 build_patch.py           # lockup + flat/embroidered/worn, all colourways
python3 build_spec.py            # dimensioned spec sheet
python3 build_colourways.py      # colourway comparison sheet
python3 render_png.py            # PNG exports, with an aspect-ratio check
python3 place_on_bag.py ../patch-embroidered.png ../patch-placement-reference.png
python3 build_onbag.py           # every colourway composited onto the pack
echo "done"
