"""Put the approved patch on the pack in every scene of the story set.

The scenes ship with a non-conforming patch - a mountain graphic above the
wordmark, no star. This finds it, takes it out, and lays the approved patch back
in its place at 0.85x the old patch's width, which is what puts the 63 mm patch
at true physical scale on the pack in scene 6 (measured against the front panel).

Scenes with no visible pack patch are copied through unchanged so the delivered
package keeps the same numbering and the same file list.
"""
import os, shutil, sys
import numpy as np
from PIL import Image

import compose
import detect_patch as D

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SRC = os.path.join(ROOT, 'Input Pictures - Story Based')

# where the existing pack patch sits in each scene, and any roll the automatic
# fit cannot resolve on its own (a near-square blob has no unique fit)
SCENES = {
    '1. Opening Scene.png':         [dict(box=(70, 520, 230, 660))],
    '2. Transition to trellis.png': [dict(box=(48, 345, 140, 438), angle=24)],
    '3. Example story trellis.png': [dict(box=(486, 338, 538, 378))],
    '6. Story 3.png':               [dict(box=(520, 460, 720, 610))],
    '9. Story 6.png':               [dict(box=(58, 890, 152, 975))],
}
SCALE = 0.85            # new patch width / old patch width


def run(patch_png, out_dir, only=None):
    os.makedirs(out_dir, exist_ok=True)
    patch = np.asarray(Image.open(patch_png).convert('RGBA')).astype(np.float64)
    report = []
    for name in sorted(os.listdir(SRC)):
        src = os.path.join(SRC, name)
        dst = os.path.join(out_dir, name)
        if not name.lower().endswith('.png'):
            shutil.copy2(src, dst)
            continue
        if name not in SCENES or (only and name not in only):
            shutil.copy2(src, dst)
            report.append((name, 0, ''))
            continue
        im = Image.open(src).convert('RGB')
        base = np.asarray(im).astype(np.float64)
        out = base
        notes = []
        for spec in SCENES[name]:
            quad = D.find(src, spec['box'], angle=spec.get('angle'))
            old_w = (np.linalg.norm(quad[1] - quad[0]) + np.linalg.norm(quad[2] - quad[3])) / 2
            clean, _ = compose.remove(out, quad)
            out, dstq = compose.place(out if out is base else out, clean, quad, patch,
                                      old_w * SCALE)
            notes.append(f'{old_w:.0f}px -> {old_w * SCALE:.0f}px')
        Image.fromarray(out.astype(np.uint8)).save(dst)
        report.append((name, len(SCENES[name]), '; '.join(notes)))
    return report


if __name__ == '__main__':
    patch_png = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(__file__), '..', 'patch-embroidered-red.png')
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        ROOT, 'Story Set - Deep Red Patch')
    for name, n, note in run(patch_png, out_dir):
        print(f'  {name:32s} {"patched " + note if n else "unchanged"}')
    print(f'wrote {out_dir}')
