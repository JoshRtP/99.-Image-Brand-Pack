"""Add the jacket's Rev B cuff wordmarks (TERRA left wrist, NEXUS right wrist)
to the scenes where a wrist is actually visible.

Per Output Drafts/Jacket/README.md, Rev B moves branding off the shoulder
entirely onto the two cuffs - heat-transfer prints, letters only (no star).
There's no standalone cuff-mark render to drop in (the build only draws it as
part of the full flat garment illustration), so `cuff-terra.png` /
`cuff-nexus.png` are lifted straight out of the patch's own
`lockup-stacked.png` lockup by colour (keep near-white pixels, drop the gold
star and its background) - same traced letterforms the spec calls for.

Only two scenes show a wrist at all: '4. Story 1' (one hand, holding a
compass) and '5a. Story 2-alt' (both hands, holding a GPS device). Everywhere
else the sleeves are rolled down past the wrist or the arm isn't in frame, so
nothing else changes.

This is deliberately a *branding* fix, not a silhouette fix: it prints the
correct wordmark onto the cuff of the jacket as it exists in these photos,
which is still the older, looser Rev A cut. Per the README, matching Rev B's
actual slim fit needs new renders, not compositing.

Which wrist is which hand is a judgment call from the framing, not a
certainty - flag it if it reads backwards once composited.
"""
import os
import numpy as np
from PIL import Image

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'Patch', 'build'))
import compose

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
IMG_DIR = os.path.join(ROOT, 'Ouput Pictures - Updated Images')
JACKET_DIR = os.path.join(os.path.dirname(__file__), '..')

# filename -> list of (mark_file, center, angle_deg, width_px), hand-measured
# off the source photo's cuff band.
SCENES = {
    '4. Story 1 - FINAL.png': [
        # one wrist in frame, reading as the right hand from the grip
        ('cuff-nexus.png', (475, 1218), -8, 85),
    ],
    '5a. Story 2-alt - FINAL.png': [
        ('cuff-terra.png', (90, 1165), -5, 130),
        ('cuff-nexus.png', (810, 1145), 8, 140),
    ],
}


def quad_at(center, angle_deg, w=40, h=25):
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


def run(img_dir=IMG_DIR, jacket_dir=JACKET_DIR):
    marks = {}
    report = []
    for name, specs in SCENES.items():
        path = os.path.join(img_dir, name)
        out = np.asarray(Image.open(path).convert('RGB')).astype(np.float64)
        notes = []
        for mark_file, center, angle, width_px in specs:
            if mark_file not in marks:
                marks[mark_file] = np.asarray(
                    Image.open(os.path.join(jacket_dir, mark_file)).convert('RGBA')
                ).astype(np.float64)
            quad = quad_at(center, angle)
            out, _ = compose.place(out, out, quad, marks[mark_file], width_px)
            notes.append(f'{mark_file} @ {center} {angle}deg -> {width_px}px')
        Image.fromarray(out.astype(np.uint8)).save(path)
        report.append((name, '; '.join(notes)))
    return report


if __name__ == '__main__':
    for name, note in run():
        print(f'  {name:40s} {note}')
