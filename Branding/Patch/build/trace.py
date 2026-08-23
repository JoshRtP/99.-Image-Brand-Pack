"""Vectorise the approved Terra Nexus wordmark + star from the master PNG.

Source: Branding/Trasnparent-StdLogo.png (1960x343, letters #E63D2F, star #E8D77E).
Contours are lifted with sub-pixel marching squares off a lightly blurred
super-sampled field, so raster stair-steps do not survive into the vector.

Output: Branding/Patch/build/glyphs.json - one SVG path per glyph in source
        pixel coordinates (cap height 219, cap top y=35, baseline y=254).
"""
import json, math, os
from PIL import Image
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SRC = os.path.join(ROOT, 'Branding', 'Trasnparent-StdLogo.png')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'glyphs.json')
UP = 4            # super-sample factor
SIGMA = 1.3       # blur in super-sampled px (~0.33 source px) - kills stair-steps
TOL = 0.55        # RDP tolerance in super-sampled px (~0.14 source px)
SMOOTH_ANGLE = 28.0


def masks():
    a = np.asarray(Image.open(SRC).convert('RGBA')).astype(int)
    op = a[..., 3] > 128
    rgb = a[..., :3]
    red = op & (np.abs(rgb - np.array([230, 61, 47])).sum(axis=2) < 140)
    gold = op & (np.abs(rgb - np.array([232, 215, 126])).sum(axis=2) < 140)
    return red, gold


def blur(f, sigma):
    r = int(math.ceil(sigma * 3))
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    pad = np.pad(f, ((r, r), (r, r)), mode='edge')
    tmp = np.apply_along_axis(lambda m: np.convolve(m, k, 'valid'), 1, pad)
    return np.apply_along_axis(lambda m: np.convolve(m, k, 'valid'), 0, tmp)


def field(mask):
    """Binary mask -> smooth float field at UP resolution, padded with empty."""
    im = Image.fromarray((mask * 255).astype(np.uint8), 'L')
    im = im.resize((im.width * UP, im.height * UP), Image.BILINEAR)
    f = np.asarray(im).astype(float) / 255.0
    f = np.pad(f, ((2, 2), (2, 2)))
    return blur(f, SIGMA)


# ---------------- marching squares with linear interpolation ----------------
def marching_squares(f, level=0.5):
    h, w = f.shape
    segs = []

    def ip(p, q, vp, vq):                    # interpolate crossing point
        t = (level - vp) / (vq - vp) if vq != vp else 0.5
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)

    for y in range(h - 1):
        row0, row1 = f[y], f[y + 1]
        for x in range(w - 1):
            a, b, c, d = row0[x], row0[x + 1], row1[x + 1], row1[x]   # TL TR BR BL
            idx = (a > level) | ((b > level) << 1) | ((c > level) << 2) | ((d > level) << 3)
            if idx == 0 or idx == 15:
                continue
            top    = ip((x, y), (x + 1, y), a, b)
            right  = ip((x + 1, y), (x + 1, y + 1), b, c)
            bottom = ip((x + 1, y + 1), (x, y + 1), c, d)
            left   = ip((x, y + 1), (x, y), d, a)
            # each segment is emitted so that the filled region lies to its left
            if idx in (1, 14):   segs.append((left, top) if idx == 1 else (top, left))
            elif idx in (2, 13): segs.append((top, right) if idx == 2 else (right, top))
            elif idx in (4, 11): segs.append((right, bottom) if idx == 4 else (bottom, right))
            elif idx in (8, 7):  segs.append((bottom, left) if idx == 8 else (left, bottom))
            elif idx == 3:       segs.append((left, right))
            elif idx == 12:      segs.append((right, left))
            elif idx == 6:       segs.append((top, bottom))
            elif idx == 9:       segs.append((bottom, top))
            else:                                       # 5 / 10 saddles
                centre = (a + b + c + d) / 4.0
                if idx == 5:
                    if centre > level: segs += [(left, top), (right, bottom)]
                    else:              segs += [(left, bottom), (right, top)]
                else:
                    if centre > level: segs += [(top, right), (bottom, left)]
                    else:              segs += [(top, left), (bottom, right)]
    return segs


def link(segs):
    """Join directed segments end-to-end into closed loops."""
    Q = 1e-6
    key = lambda p: (round(p[0] / Q), round(p[1] / Q))
    starts = {}
    for s in segs:
        starts.setdefault(key(s[0]), []).append(s)
    loops = []
    used = set()
    for s0 in segs:
        if id(s0) in used:
            continue
        loop = [s0[0]]
        cur = s0
        while True:
            used.add(id(cur))
            loop.append(cur[1])
            nxts = [t for t in starts.get(key(cur[1]), []) if id(t) not in used]
            if not nxts:
                break
            cur = nxts[0]
            if key(cur[0]) == key(loop[0]) and len(loop) > 2 and key(cur[1]) == key(loop[1]):
                break
        if len(loop) > 6:
            if key(loop[0]) == key(loop[-1]):
                loop = loop[:-1]
            loops.append(loop)
    return loops


def rdp(pts, tol):
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        ax, ay = pts[i]; bx, by = pts[j]
        dx, dy = bx - ax, by - ay
        den = math.hypot(dx, dy)
        best, bi = -1.0, -1
        for k in range(i + 1, j):
            px, py = pts[k]
            d = abs(dx * (ay - py) - (ax - px) * dy) / den if den else math.hypot(px - ax, py - ay)
            if d > best:
                best, bi = d, k
        if best > tol:
            keep[bi] = True
            stack += [(i, bi), (bi, j)]
    return [p for p, k in zip(pts, keep) if k]


def simplify_closed(poly, tol):
    n = len(poly)
    def turn(k):
        a, b, c = poly[(k - 1) % n], poly[k], poly[(k + 1) % n]
        v1 = (b[0] - a[0], b[1] - a[1]); v2 = (c[0] - b[0], c[1] - b[1])
        return abs(math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1]))
    s = max(range(n), key=turn)
    rot = poly[s:] + poly[:s]
    out = rdp(rot + [rot[0]], tol)
    return out[:-1] if out[0] == out[-1] else out


def to_path(poly, scale, ox, oy):
    p = [((x - ox) * scale, (y - oy) * scale) for x, y in poly]
    n = len(p)
    if n < 3:
        return ''
    def ang(k):
        a, b, c = p[(k - 1) % n], p[k], p[(k + 1) % n]
        v1 = (b[0] - a[0], b[1] - a[1]); v2 = (c[0] - b[0], c[1] - b[1])
        return abs(math.degrees(math.atan2(v1[0] * v2[1] - v1[1] * v2[0],
                                           v1[0] * v2[0] + v1[1] * v2[1])))
    corner = [ang(k) >= SMOOTH_ANGLE for k in range(n)]
    f = lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')
    d = [f'M{f(p[0][0])} {f(p[0][1])}']
    for k in range(1, n + 1):
        cur, prev = p[k % n], p[k - 1]
        if corner[k % n] or corner[(k - 1) % n]:
            d.append(f'L{f(cur[0])} {f(cur[1])}')
        else:
            mid = ((prev[0] + cur[0]) / 2, (prev[1] + cur[1]) / 2)
            d.append(f'Q{f(prev[0])} {f(prev[1])} {f(mid[0])} {f(mid[1])}')
    d.append('Z')
    return ''.join(d)


def trace_region(mask, x0, x1, name):
    f = field(mask[:, x0:x1 + 1])
    loops = [simplify_closed(l, TOL) for l in link(marching_squares(f))]
    loops = [l for l in loops if len(l) >= 3]
    d = ''.join(to_path(l, 1.0 / UP, 2, 2) for l in loops)
    print(f'  {name}: {len(loops)} contours, {sum(len(l) for l in loops)} pts')
    return d


if __name__ == '__main__':
    red, gold = masks()
    LETTERS = [('T', 0, 160), ('E1', 186, 330), ('R1', 359, 513), ('R2', 534, 689),
               ('A', 700, 867), ('N', 1104, 1259), ('E2', 1286, 1430),
               ('X', 1454, 1615), ('U', 1632, 1784), ('S', 1806, 1959)]
    out = {'capHeight': 219, 'capTop': 35, 'baseline': 254, 'glyphs': {}, 'x': {}}
    print('tracing letters...')
    for nm, a, b in LETTERS:
        out['glyphs'][nm] = trace_region(red, a, b, nm)
        out['x'][nm] = a
    print('tracing star...')
    out['glyphs']['STAR'] = trace_region(gold, 858, 1083, 'STAR')
    out['x']['STAR'] = 858
    json.dump(out, open(OUT, 'w'))
    print('wrote glyphs.json')
