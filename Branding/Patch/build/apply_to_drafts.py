"""Put the faded (worn) Deep Red patch on the pack in the FINAL draft renders.

The 'Output Draft Pictures' set already has the old non-conforming patch
(mountain graphic, no star) painted OUT — the panel is clean fabric with
nothing to detect. So the patch's screen position for each scene is measured
instead from the matching 'Input Pictures - Story Based' source, which still
carries the old patch, and that same quad is used to place the new patch onto
the already-clean FINAL frame.

Scenes with no visible pack patch are copied through unchanged so the
delivered package keeps the same file list.
"""
import os, shutil, sys
import numpy as np
from PIL import Image

import compose
import detect_patch as D

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DRAFT_DIR = os.path.join(ROOT, 'Output Draft Pictures')
INPUT_DIR = os.path.join(ROOT, 'Input Pictures - Story Based')

# FINAL draft filename -> matching input filename (for quad detection) + search box
SCENES = {
    '1. Opening Scene - FINAL.png':         ('1. Opening Scene.png',
                                              dict(box=(70, 520, 230, 660))),
    '2. Transition to trellis - FINAL.png': ('2. Transition to trellis.png',
                                              dict(box=(48, 345, 140, 438), angle=24)),
    '3. Example story trellis - FINAL.png': ('3. Example story trellis.png',
                                              dict(box=(486, 338, 538, 378))),
    '6. Story 3 - FINAL.png':               ('6. Story 3.png',
                                              dict(box=(520, 460, 720, 610))),
    '9. Story 6 - FINAL.png':               ('9. Story 6.png',
                                              dict(box=(58, 890, 152, 975))),
}
SCALE = 0.85            # new patch width / old patch width, matched to apply_to_scene.py


def run(patch_png, out_dir, src_dir=DRAFT_DIR, input_dir=INPUT_DIR, only=None):
    os.makedirs(out_dir, exist_ok=True)
    patch = np.asarray(Image.open(patch_png).convert('RGBA')).astype(np.float64)
    report = []
    for name in sorted(os.listdir(src_dir)):
        src = os.path.join(src_dir, name)
        dst = os.path.join(out_dir, name)
        if not name.lower().endswith('.png'):
            shutil.copy2(src, dst)
            continue
        if name not in SCENES or (only and name not in only):
            shutil.copy2(src, dst)
            report.append((name, 0, ''))
            continue
        input_name, spec = SCENES[name]
        input_path = os.path.join(input_dir, input_name)
        quad = D.find(input_path, spec['box'], angle=spec.get('angle'))
        old_w = (np.linalg.norm(quad[1] - quad[0]) + np.linalg.norm(quad[2] - quad[3])) / 2

        clean = np.asarray(Image.open(src).convert('RGB')).astype(np.float64)
        out, _ = compose.place(clean, clean, quad, patch, old_w * SCALE)
        Image.fromarray(out.astype(np.uint8)).save(dst)
        report.append((name, 1, f'{old_w:.0f}px -> {old_w * SCALE:.0f}px'))
    return report


if __name__ == '__main__':
    patch_png = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), '..', 'patch-embroidered-red-worn.png')
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        ROOT, 'Ouput Pictures - Updated Images')
    src_dir = sys.argv[3] if len(sys.argv) > 3 else DRAFT_DIR
    for name, n, note in run(patch_png, out_dir, src_dir):
        print(f'  {name:40s} {"patched " + note if n else "unchanged"}')
    print(f'wrote {out_dir}')
