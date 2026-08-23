"""Full, consistent branding pass over the story set: the Deep Red bag patch
(see apply_to_drafts.py) plus the jacket's approved sleeve mark in every scene
that shows it.

Per Branding/Jacket/README.md, the story set's sewn jacket-sleeve patch is
itself off-brand — patches go on bags only. The jacket's real branding is a
printed heat-transfer mark, 84 mm wide, white wordmark + sand star, no patch
background. That's exactly `Branding/Patch/lockup-stacked.png` (the lockup
traced on its own, without the patch ground/edge), so it drops in directly.

Same method as the bag: the sleeve patch's screen position is read off the
'Input Pictures - Story Based' source (which still carries the old sewn
patch), and that position is used to place the new printed mark onto the
already-clean 'Output Draft Pictures' frame. The old sewn patch is dark
against blue fabric rather than dark against orange, so detection here uses a
lower brightness threshold than the bag patch's; two placements are small or
angled enough that a hand-picked quad is more reliable than the blob detector
and are given directly.

Sizing follows the same real-world-consistency rule as the bag: the mark is a
fixed fraction (SLEEVE_RATIO) of the sleeve's own visible width in each shot,
not a copy of the old placeholder patch's (inconsistent) pixel size.
"""
import os
import numpy as np
from PIL import Image

import compose
import detect_patch as D
import apply_to_drafts as bag

ROOT = bag.ROOT
DRAFT_DIR = bag.DRAFT_DIR
INPUT_DIR = bag.INPUT_DIR

SLEEVE_RATIO = 0.5    # mark width as a fraction of the sleeve's visible width

# FINAL draft filename -> list of sleeve-mark placements in that frame.
# sleeve_w is the jacket sleeve's own visible width at the mark, measured off
# the input frame (px); width_px = sleeve_w * SLEEVE_RATIO.
JACKET_SCENES = {
    '3. Example story trellis - FINAL.png': [
        # hero panel, near the shoulder
        dict(kind='manual', quad=[[405, 262], [458, 258], [462, 298], [409, 302]],
             sleeve_w=150),
        # row 2, col 1 - taking a photo
        dict(kind='manual', quad=[[100, 490], [148, 486], [151, 520], [103, 524]],
             sleeve_w=150),
        # row 2, col 3 - reading the map ('eta 8 hours')
        dict(kind='manual', quad=[[734, 505], [761, 503], [763, 538], [736, 540]],
             sleeve_w=140),
        # row 2, col 4 - reading the map ('alt. route')
        dict(kind='manual', quad=[[1039, 510], [1066, 508], [1068, 540], [1041, 542]],
             sleeve_w=140),
    ],
    '5. Story 2 - FINAL.png': [
        dict(kind='detect', input='5. Story 2.png',
             box=(275, 1130, 365, 1240), thresh=75, sleeve_w=125),
    ],
    '7. Story 4 - FINAL.png': [
        dict(kind='detect', input='7. Story 4.png',
             box=(335, 935, 425, 1050), thresh=75, sleeve_w=120),
    ],
    '8. Story 5 - FINAL.png': [
        dict(kind='detect', input='8. Story 5.png',
             box=(370, 935, 460, 1055), thresh=75, sleeve_w=130),
    ],
    '9. Story 6 - FINAL.png': [
        dict(kind='manual', quad=[[365, 840], [406, 851], [391, 906], [350, 894]],
             sleeve_w=80),
    ],
}


def run(bag_patch_png, mark_png, out_dir, src_dir=DRAFT_DIR, input_dir=INPUT_DIR):
    # start from the bag-patch pass, already consistent-scale + washed out
    report = bag.run(bag_patch_png, out_dir, src_dir, input_dir)

    mark = np.asarray(Image.open(mark_png).convert('RGBA')).astype(np.float64)
    jreport = []
    for name, specs in JACKET_SCENES.items():
        path = os.path.join(out_dir, name)
        out = np.asarray(Image.open(path).convert('RGB')).astype(np.float64)
        notes = []
        for spec in specs:
            width_px = spec['sleeve_w'] * SLEEVE_RATIO
            if spec['kind'] == 'detect':
                input_path = os.path.join(input_dir, spec['input'])
                quad = D.find(input_path, spec['box'], thresh=spec.get('thresh', 110))
            else:
                quad = np.array(spec['quad'], float)
            notes.append(f'sleeve {spec["sleeve_w"]}px -> mark {width_px:.0f}px')
            out, _ = compose.place(out, out, quad, mark, width_px)
        Image.fromarray(out.astype(np.uint8)).save(path)
        jreport.append((name, len(specs), '; '.join(notes)))
    return report, jreport


if __name__ == '__main__':
    import sys
    bag_patch = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), '..', 'patch-embroidered-red-worn.png')
    mark_png = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(__file__), '..', 'lockup-stacked.png')
    out_dir = sys.argv[3] if len(sys.argv) > 3 else os.path.join(
        ROOT, 'Output Pictures - Consistent Branding Set')
    src_dir = sys.argv[4] if len(sys.argv) > 4 else DRAFT_DIR
    input_dir = sys.argv[5] if len(sys.argv) > 5 else INPUT_DIR
    breport, jreport = run(bag_patch, mark_png, out_dir, src_dir, input_dir)
    print('-- bag patch --')
    for name, n, note in breport:
        print(f'  {name:40s} {"patched " + note if n else "unchanged"}')
    print('-- sleeve mark --')
    for name, n, note in jreport:
        print(f'  {name:40s} {note}')
    print(f'wrote {out_dir}')
