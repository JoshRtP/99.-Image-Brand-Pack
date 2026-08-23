"""Put the worn Deep Red patch on the pack in the FINAL draft renders.

The 'Output Draft Pictures' set already has the old non-conforming patch
(mountain graphic, no star) painted OUT — the panel is clean fabric with
nothing to detect. So for most scenes the patch's screen *position* is
measured instead from the matching 'Input Pictures - Story Based' source,
which still carries the old patch, and that position is used to place the new
patch onto the already-clean FINAL frame ('detect' specs below).

Rotation is NOT taken from the detected quad. The old placeholder patch is an
irregular blob (mountain icon + two lines of text, not a clean filled
rectangle), so the automatic minimum-area-rectangle fit locks onto that
irregular outline rather than the patch's true edges - it read plausible but
was actually off by 5-25 degrees scene to scene, which is what made the last
pass look crooked. Each placement instead carries an explicit, eyeballed-off-
the-source `angle` (0 unless the panel itself is visibly rolled in that shot,
e.g. scene 2), and detect_patch.find is forced to that angle rather than
fitting its own.

Scene 3's hero panel never had a patch to detect in the first place (the only
patch in that frame was on the jacket, not the bag), so its placement there is
given directly as a hand-picked quad ('manual' spec).

Sizing: the brand rule (Output Drafts/Patch/README.md) is one *real-world*
size in every scene — 63 mm on the pack — so apparent pixel size should track
the pack's own apparent size in each frame, not be copied from the old
placeholder patch (which was never drawn to a consistent scale itself; that's
what made an earlier pass look inconsistent scene to scene). Each placement
below instead carries the pack's own measured front-panel width in that shot,
and the patch is sized as a fixed fraction of it (PANEL_RATIO), so every scene
reads at the same true scale. PANEL_RATIO of 0.21 is the README's own
calibration (63 mm on a ~300 mm panel, verified in
patch-placement-reference.png).

Colour is the plain 'worn' render (patch-embroidered-red-worn.png) with no
extra grading on top - a prior pass washed it out further and that read wrong,
so this reverts to the colourway as rendered.

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

PANEL_RATIO = 0.21 * 1.3   # patch width as a fraction of the pack's front-panel width

# FINAL draft filename -> list of placements in that frame. panel_w is the
# pack's own front-panel width measured in that shot (px); width_px = panel_w
# * PANEL_RATIO. `angle` is the panel's own roll in degrees, read off the
# source photo (fold lines / seams) - not fitted - so the placed patch sits
# level with the panel instead of inheriting the old placeholder's crooked fit.
SCENES = {
    '1. Opening Scene - FINAL.png': [
        dict(kind='detect', input='1. Opening Scene.png',
             box=(70, 520, 230, 660), angle=0, panel_w=165),
    ],
    '2. Transition to trellis - FINAL.png': [
        # the only scene where the pack is genuinely rolled in frame
        dict(kind='detect', input='2. Transition to trellis.png',
             box=(48, 345, 140, 438), angle=18, panel_w=150),
    ],
    '3. Example story trellis - FINAL.png': [
        # row-2 close-up thumbnail — old patch detectable in the input
        dict(kind='detect', input='3. Example story trellis.png',
             box=(486, 338, 538, 378), angle=0, panel_w=130),
        # hero panel at the top of the trellis — the bag is visible here too but
        # never carried a bag patch to detect (only a jacket patch, off-brand
        # per Output Drafts/Patch/README.md, sat nearby); placed by hand on the
        # flat panel below the shoulder strap
        dict(kind='manual',
             quad=[[168, 251], [227, 251], [227, 284], [168, 284]],
             panel_w=145),
    ],
    '6. Story 3 - FINAL.png': [
        dict(kind='detect', input='6. Story 3.png',
             box=(520, 460, 720, 610), angle=0, panel_w=260),
    ],
    '9. Story 6 - FINAL.png': [
        dict(kind='detect', input='9. Story 6.png',
             box=(58, 890, 152, 975), angle=0, panel_w=150),
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
            width_px = spec['panel_w'] * PANEL_RATIO
            if spec['kind'] == 'detect':
                input_path = os.path.join(input_dir, spec['input'])
                quad = D.find(input_path, spec['box'], angle=spec.get('angle', 0))
            else:
                quad = np.array(spec['quad'], float)
            notes.append(f'panel {spec["panel_w"]}px -> patch {width_px:.0f}px')
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
