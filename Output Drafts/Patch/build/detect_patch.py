"""Locate the existing sewn patch inside a search box and return its corners.

The patch is the dark, compact blob on the pack. Its outline is fitted with a
minimum-area rectangle, which tracks the patch's roll on the panel far more
reliably than reading corners off a screenshot.
"""
import math
import numpy as np
from PIL import Image


def dark_blob(rgb, thresh, warm=30):
    """Largest connected component of patch-like pixels.

    The patch is dark AND neutral; the pack around it is orange, so a small
    red-minus-blue difference separates the two far better than brightness,
    which is unreliable in a backlit sunset frame.
    """
    m = (rgb.mean(axis=2) < thresh) & ((rgb[..., 0] - rgb[..., 2]) < warm)
    h, w = m.shape
    seen = np.zeros_like(m)
    best, best_n = None, 0
    for sy in range(h):
        for sx in range(w):
            if not m[sy, sx] or seen[sy, sx]:
                continue
            stack, pts = [(sy, sx)], []
            seen[sy, sx] = True
            while stack:
                y, x = stack.pop()
                pts.append((x, y))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            if len(pts) > best_n:
                best, best_n = pts, len(pts)
    return best or []


def hull(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts
    def half(ps):
        out = []
        for p in ps:
            while len(out) >= 2:
                (ax, ay), (bx, by) = out[-2], out[-1]
                if (bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax) <= 0:
                    out.pop()
                else:
                    break
            out.append(p)
        return out
    return half(pts)[:-1] + half(pts[::-1])[:-1]


def edge_angle(sub, mask):  # noqa: kept for manual angle probing
    """Dominant edge direction, modulo 90 degrees.

    A rounded square's minimum-area rectangle can lock onto a diagonal, so the
    patch's roll is taken from its own edges instead: Sobel gradients inside the
    blob, binned by direction mod 90, weighted by magnitude.
    """
    g = sub.mean(axis=2)
    gx = np.zeros_like(g); gy = np.zeros_like(g)
    gx[:, 1:-1] = g[:, 2:] - g[:, :-2]
    gy[1:-1, :] = g[2:, :] - g[:-2, :]
    mag = np.hypot(gx, gy)
    grow = mask.copy()
    for _ in range(3):
        p = np.pad(grow, 1)
        grow = p[1:-1, 1:-1] | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    sel = grow & (mag > np.percentile(mag[grow], 75))
    if sel.sum() < 30:
        return None
    ang = (np.degrees(np.arctan2(gy[sel], gx[sel])) % 90.0)
    w = mag[sel]
    # circular mean on the 90-degree wrap
    t = np.radians(ang * 4)
    a = math.degrees(math.atan2((w * np.sin(t)).sum(), (w * np.cos(t)).sum())) / 4
    return a % 90.0


def rect_at(pts, deg):
    """Axis-aligned box in a frame rotated by `deg`, mapped back, clockwise."""
    P = np.array(pts, float)
    r = math.radians(deg)
    c, s = math.cos(-r), math.sin(-r)
    R = np.array([[c, -s], [s, c]])
    Q = P @ R.T
    lo, hi = Q.min(axis=0), Q.max(axis=0)
    box = np.array([[lo[0], lo[1]], [hi[0], lo[1]], [hi[0], hi[1]], [lo[0], hi[1]]])
    q = box @ np.linalg.inv(R).T
    start = min(range(4), key=lambda i: q[i][0] + q[i][1])
    return np.roll(q, -start, axis=0)


def min_area_rect(pts):
    """Corners of the smallest-area rectangle enclosing the hull, clockwise."""
    H = hull(pts)
    if len(H) < 3:
        raise ValueError('degenerate blob')
    P = np.array(H, float)
    best = None
    for i in range(len(H)):
        ax, ay = H[i]
        bx, by = H[(i + 1) % len(H)]
        ang = math.atan2(by - ay, bx - ax)
        c, s = math.cos(-ang), math.sin(-ang)
        R = np.array([[c, -s], [s, c]])
        Q = P @ R.T
        lo, hi = Q.min(axis=0), Q.max(axis=0)
        area = (hi[0] - lo[0]) * (hi[1] - lo[1])
        if best is None or area < best[0]:
            corners = np.array([[lo[0], lo[1]], [hi[0], lo[1]],
                                [hi[0], hi[1]], [lo[0], hi[1]]])
            best = (area, corners @ np.linalg.inv(R).T)
    q = best[1]
    # order clockwise from the top-left-most corner
    c = q.mean(axis=0)
    order = sorted(range(4), key=lambda i: math.atan2(q[i][1] - c[1], q[i][0] - c[0]))
    q = q[order]
    start = min(range(4), key=lambda i: q[i][0] + q[i][1])
    return np.roll(q, -start, axis=0)


def find(path, box, thresh=110, warm=30, angle=None):
    """Corners of the patch in `path`, searched within box=(x0,y0,x1,y1).

    `angle` forces the patch's roll in degrees when the automatic fit picks a
    diagonal - a near-square blob has no unique minimum-area rectangle.
    """
    im = Image.open(path).convert('RGB')
    x0, y0, x1, y1 = box
    sub = np.asarray(im.crop(box)).astype(int)
    pts = dark_blob(sub, thresh, warm)
    if len(pts) < 80:
        raise ValueError(f'{path}: no patch-sized dark blob in {box} at thresh {thresh}')
    m = np.zeros(sub.shape[:2], bool)
    m[[p[1] for p in pts], [p[0] for p in pts]] = True
    if m.sum() > 0.85 * m.size:
        raise ValueError(f'{path}: blob fills the search box in {box} - no patch there')
    q = rect_at(pts, angle) if angle is not None else min_area_rect(pts)
    q[:, 0] += x0
    q[:, 1] += y0
    return q


if __name__ == '__main__':
    import sys
    p, *rest = sys.argv[1:]
    box = tuple(int(v) for v in rest[:4])
    th = int(rest[4]) if len(rest) > 4 else 110
    wm = int(rest[5]) if len(rest) > 5 else 30
    q = find(p, box, th, wm)
    w = (np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3])) / 2
    h = (np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / 2
    print(np.round(q, 1).tolist(), f'| {w:.1f} x {h:.1f} px, aspect {w/h:.2f}')
