"""Put the worn Deep Red patch on the pack in the FINAL draft renders.

The 'Output Draft Pictures' set already has the old non-conforming patch
(mountain graphic, no star) painted OUT — the panel is clean fabric with
nothing to detect. So the new patch's position, roll and size are all taken
from hand measurements of the OLD patch in the matching 'Input Pictures -
Story Based' source (which still carries it), rather than from any automatic
detection.

That's a deliberate change from two earlier passes that both got this wrong
in different ways:

- Pass 1 scaled off the old patch's own pixel width via an automatic
  minimum-area-rectangle fit. The old patch is an irregular blob (a mountain
  icon plus two lines of text, not a filled rectangle), so that fit locked
  onto the irregular outline instead of the patch's true edges - wrong width,
  wrong rotation, sometimes by a lot (one scene came back nearly square).
  That's what made the patch look crooked and randomly sized.
- Pass 2 tried to fix sizing by scaling to a fraction of the pack's own
  front-panel width instead, measured by eye. But "panel width" turned out to
  be a much harder, less repeatable thing to eyeball consistently than the
  patch itself - scene to scene the estimates drifted enough that the sizing
  was still visibly inconsistent side by side.

This pass instead hand-measures the OLD patch's centre, bounding width and
roll directly off a pixel grid overlaid on the source photo (see the numbers
inline below) - the one thing that's both stable across the two prior
attempts' failure modes and directly checkable against the image. Width scales
by SCALE, same idea as the original apply_to_scene.py's 0.85 (the rendered
patch carries a couple mm of bleed the finished patch doesn't), with the
previously-requested +30% still applied on top since that hasn't been walked
back.

Scene 3's hero panel never had an old patch to measure (the only patch in that
frame was on the jacket, not the bag), so its placement is a hand-picked
centre/angle in the same units.

Colour is the plain 'worn' render (patch-embroidered-red-worn.png), no extra
grading on top.

Scenes with no visible pack patch are copied through unchanged so the
delivered package keeps the same file list.
"""
import os, shutil, sys
import numpy as np
from PIL import Image

import compose

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
DRAFT_DIR = os.path.join(ROOT, 'Output Draft Pictures')

SCALE = 0.85 * 1.3   # new patch width / old patch's own measured width

# FINAL draft filename -> list of placements. center/angle/old_w are read
# straight off a pixel grid on the OLD patch in the matching input photo
# (bounding width - left edge to right edge - not a fitted rectangle).
SCENES = {
    '1. Opening Scene - FINAL.png': [
        dict(center=(129, 600), angle=0, old_w=65),
    ],
    '2. Transition to trellis - FINAL.png': [
        # the only scene where the pack itself is genuinely rolled in frame
        dict(center=(98, 386), angle=13, old_w=81),
    ],
    '3. Example story trellis - FINAL.png': [
        # row-2 close-up thumbnail — old patch measurable in the input
        # (previous measurement of 23px was wrong - re-read off a fresh grid,
        # the old patch here is actually ~45px, which is why the first pass
        # rendered a tiny, illegible patch on this thumbnail)
        dict(center=(516, 364), angle=0, old_w=45),
        # hero panel at the top of the trellis — bag visible but never carried
        # a bag patch (only a jacket patch, off-brand); hand-picked to match
        # the apparent scale of the other close scenes at this camera distance
        dict(center=(198, 268), angle=0, old_w=68),
    ],
    '6. Story 3 - FINAL.png': [
        dict(center=(614, 530), angle=0, old_w=92),
    ],
    '9. Story 6 - FINAL.png': [
        dict(center=(72, 919), angle=0, old_w=73),
    ],
}


def quad_at(center, angle_deg, w=40, h=25):
    """A small rectangle at `center`, rolled by `angle_deg`. Only its centre
    and roll are used downstream (compose.place re-derives the actual placed
    size from width_px) so w/h here are arbitrary placeholders.
    """
    cx, cy = center
    a = np.radians(angle_deg)
    u = np.array([np.cos(a), np.sin(a)])
    v = np.array([-np.sin(a), np.cos(a)])
    return np.array([
        [cx, cy] - u * w / 2 - v * h / 2,
        [cx, cy] + u * w / 2 - v * h / 2,
        [cx, cy] + u * w / 2 + v * h / 2,
        [cx, cy] - u * w / 2 + v * h / 2,
    ])


def run(patch_png, out_dir, src_dir=DRAFT_DIR, only=None):
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
            width_px = spec['old_w'] * SCALE
            quad = quad_at(spec['center'], spec['angle'])
            notes.append(f'old {spec["old_w"]}px -> patch {width_px:.0f}px @ {spec["angle"]}deg')
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
