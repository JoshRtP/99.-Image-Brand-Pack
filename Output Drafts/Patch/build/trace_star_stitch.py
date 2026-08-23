"""Stitch-safe star: the approved star grown by ~0.19mm per side so its minor
rays clear the 0.9mm minimum satin width at the 63mm patch size."""
import json
import numpy as np
import trace as T

DILATE = 4  # source px per side

red, gold = T.masks()
m = gold[:, 858:1084]
d = m.copy()
for _ in range(DILATE):
    p = np.pad(d, 1)
    d = (p[1:-1,1:-1] | p[:-2,1:-1] | p[2:,1:-1] | p[1:-1,:-2] | p[1:-1,2:])
full = np.zeros_like(gold)
full[:, 858:1084] = d
path = T.trace_region(full, 858 - DILATE, 1083 + DILATE, 'STAR_STITCH')
g = json.load(open(T.OUT))
g['glyphs']['STAR_STITCH'] = path
g['x']['STAR_STITCH'] = 858 - DILATE
json.dump(g, open(T.OUT, 'w'))
print('added STAR_STITCH')
