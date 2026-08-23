"""Put the faded (worn) Deep Red patch on the pack in the FINAL draft renders.

The 'Output Draft Pictures' set already has the old non-conforming patch
(mountain graphic, no star) painted OUT — the panel is clean fabric with
nothing to detect. So for most scenes the patch's screen position is measured
instead from the matching 'Input Pictures - Story Based' source, which still
carries the old patch, and that same quad is used to place the new patch onto
the already-clean FINAL frame ('detect' specs below).

Scene 3's hero panel never had a patch to detect in the first place (the only
patch in that frame was on the jacket, not the bag), so its placement there is
given directly as a hand-picked quad ('manual' spec).

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

SCALE = 0.85 * 1.3      # new patch width / old patch width; +30% on top of the
                         # apply_to_scene.py baseline, per feedback that it read undersized

# FINAL draft filename -> list of placements in that frame
SCENES = {
    '1. Opening Scene - FINAL.png': [
        dict(kind='detect', input='1. Opening Scene.png', box=(70, 520, 230, 660)),
    ],
    '2. Transition to trellis - FINAL.png': [
        dict(kind='detect', input='2. Transition to trellis.png',
             box=(48, 345, 140, 438), angle=24),
    ],
    '3. Example story trellis - FINAL.png': [
        # row-2 close-up thumbnail — old patch detectable in the input
        dict(kind='detect', input='3. Example story trellis.png',
             box=(486, 338, 538, 378)),
        # hero panel at the top of the trellis — the bag is visible here too but
        # never carried a bag patch to detect (only a jacket patch, off-brand
        # per Branding/Patch/README.md, sat nearby); placed by hand on the
        # flat panel below the shoulder strap
        dict(kind='manual',
             quad=[[169, 247], [228, 260], [221, 293], [162, 280]],
             width_px=50),
    ],
    '6. Story 3 - FINAL.png': [
        dict(kind='detect', input='6. Story 3.png', box=(520, 460, 720, 610)),
    ],
    '9. Story 6 - FINAL.png': [
        dict(kind='detect', input='9. Story 6.png', box=(58, 890, 152, 975)),
    ],
}


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

        out = np.asarray(Image.open(src).convert('RGB')).astype(np.float64)
        notes = []
        for spec in SCENES[name]:
            if spec['kind'] == 'detect':
                input_path = os.path.join(input_dir, spec['input'])
                quad = D.find(input_path, spec['box'], angle=spec.get('angle'))
                old_w = (np.linalg.norm(quad[1] - quad[0]) + np.linalg.norm(quad[2] - quad[3])) / 2
                width_px = old_w * SCALE
                notes.append(f'{old_w:.0f}px -> {width_px:.0f}px')
            else:
                quad = np.array(spec['quad'], float)
                width_px = spec['width_px']
                notes.append(f'manual -> {width_px:.0f}px')
            out, _ = compose.place(out, out, quad, patch, width_px)
        Image.fromarray(out.astype(np.uint8)).save(dst)
        report.append((name, len(SCENES[name]), '; '.join(notes)))
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
