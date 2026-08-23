#!/bin/sh
# Rebuild the direct-stitch assets.
set -e
cd "$(dirname "$0")"
python3 build_stitch.py    # production artwork, fabric panels, transparent plates
python3 build_sheets.py    # thread comparison sheet
python3 build_spec.py      # specification sheet
python3 build_threads_json.py   # machine-readable entry point for agents
python3 render_png.py      # PNG exports
python3 - <<'PY'
import os, build_sheets as B, build_stitch as S
for key in ('deep-red', 'warm-charcoal', 'olive'):
    B.on_bag(key, os.path.join(S.OUT, f'stitch-on-bag-{key}.png'),
             os.path.join(S.OUT, f'stitch-{key}-alpha.png'))
PY
echo "done"
