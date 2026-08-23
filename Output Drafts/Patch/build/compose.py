"""Swap a sewn patch in a photographic scene.

Removes the patch that is there, then lays a rendered patch back in its place at
a chosen scale, following the panel's roll and picking up the scene's own light.
Shared by place_on_bag.py (the reference sheets) and apply_to_scene.py (the set).
"""
import numpy as np
from PIL import Image, ImageFilter

PATCH_MM = 63.0        # finished width of the patch
BLEED_MM = 2.0         # patch-embroidered.svg carries 2 mm of bleed per side
BLEED = (PATCH_MM + 2 * BLEED_MM) / PATCH_MM


def homography(src, dst):
    A, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    h = np.linalg.solve(np.array(A), np.array(b))
    return np.append(h, 1).reshape(3, 3)


def apply_h(H, pts):
    p = np.hstack([pts, np.ones((len(pts), 1))]) @ H.T
    return p[:, :2] / p[:, 2:3]


UNIT = np.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.]])


def quad_mask(shape, quad, grow=0.0):
    c = quad.mean(axis=0)
    q = c + (quad - c) * (1 + grow)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    inside = np.ones(shape, bool)
    sign = np.sign(np.cross(q[1] - q[0], q[2] - q[1]))
    for i in range(4):
        p, nxt = q[i], q[(i + 1) % 4]
        e = nxt - p
        inside &= sign * (e[0] * (yy - p[1]) - e[1] * (xx - p[0])) >= 0
    return inside


def inpaint(img, mask, iters=1400):
    """Laplace fill: smooth the masked region in from its boundary."""
    a = img.astype(np.float64).copy()
    m = mask.astype(bool)
    if not m.any():
        return a
    for c in range(3):
        ch = a[..., c]
        ch[m] = ch[~m].mean() if (~m).any() else 0
        for _ in range(iters):
            nb = np.zeros_like(ch)
            nb[1:-1, 1:-1] = (ch[:-2, 1:-1] + ch[2:, 1:-1] + ch[1:-1, :-2] + ch[1:-1, 2:]) / 4
            ch[m] = nb[m]
        a[..., c] = ch
    return a


def warp_onto(patch, H, shape):
    """Inverse-warp an RGBA patch (unit-square domain) into image space."""
    ph, pw = patch.shape[:2]
    Hi = np.linalg.inv(H)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    src = Hi @ np.stack([xx.ravel(), yy.ravel(), np.ones(xx.size)])
    u = (src[0] / src[2]).reshape(shape) * (pw - 1)
    v = (src[1] / src[2]).reshape(shape) * (ph - 1)
    ok = (u >= 0) & (u <= pw - 1) & (v >= 0) & (v <= ph - 1)
    u = np.clip(u, 0, pw - 1); v = np.clip(v, 0, ph - 1)
    x0, y0 = np.floor(u).astype(int), np.floor(v).astype(int)
    x1, y1 = np.minimum(x0 + 1, pw - 1), np.minimum(y0 + 1, ph - 1)
    fx, fy = (u - x0)[..., None], (v - y0)[..., None]
    out = (patch[y0, x0] * (1 - fx) * (1 - fy) + patch[y0, x1] * fx * (1 - fy) +
           patch[y1, x0] * (1 - fx) * fy + patch[y1, x1] * fx * fy)
    out[~ok] = 0
    return out


def _blur(a, r):
    return np.asarray(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(r))).astype(np.float64)


def remove(base, quad, grow=0.30, seed=7):
    """Take the old patch out.

    The exposed fabric is rebuilt by transplanting real texture from elsewhere on
    the same panel and re-lighting it: the donor's high-frequency detail (weave,
    folds) is kept, its own shading is subtracted, and the destination's shading -
    solved by a Laplace fill from the hole's boundary - is put back. Inventing the
    texture instead leaves a flat, obviously retouched blotch.
    """
    H, W = base.shape[:2]
    mask = quad_mask((H, W), quad, grow=grow)
    ys, xs = np.nonzero(mask)
    mh, mw = ys.max() - ys.min() + 1, xs.max() - xs.min() + 1
    pad = int(max(mh, mw) * 0.9) + 12
    wy0, wy1 = max(0, ys.min() - pad), min(H, ys.max() + pad + 1)
    wx0, wx1 = max(0, xs.min() - pad), min(W, xs.max() + pad + 1)
    win = base[wy0:wy1, wx0:wx1]
    wm = mask[wy0:wy1, wx0:wx1]

    dest_low = _blur(inpaint(win, wm, iters=2200), 9)
    ring = (quad_mask((H, W), quad, grow=grow + 0.55) & ~mask)[wy0:wy1, wx0:wx1]

    best, best_err = None, None
    step = max(8, int(max(mh, mw) * 0.45))
    for dy in range(-3 * step, 3 * step + 1, step):
        for dx in range(-3 * step, 3 * step + 1, step):
            if abs(dy) < mh * 0.9 and abs(dx) < mw * 0.9:
                continue                      # donor would overlap the hole
            sy0, sx0 = wy0 + dy, wx0 + dx
            if sy0 < 0 or sx0 < 0 or sy0 + (wy1 - wy0) > H or sx0 + (wx1 - wx0) > W:
                continue
            src = base[sy0:sy0 + (wy1 - wy0), sx0:sx0 + (wx1 - wx0)]
            if mask[sy0:sy0 + (wy1 - wy0), sx0:sx0 + (wx1 - wx0)].any():
                continue                      # donor must not contain the patch
            cand = src - _blur(src, 9) + dest_low
            err = float(((cand[ring] - win[ring]) ** 2).mean()) if ring.any() else 1e9
            if best_err is None or err < best_err:
                best, best_err = cand, err

    filled = best if best is not None else dest_low
    alpha = _blur(np.repeat(wm[..., None] * 255.0, 3, axis=2), 1.6) / 255.0
    out = base.copy()
    out[wy0:wy1, wx0:wx1] = np.clip(win * (1 - alpha) + filled * alpha, 0, 255)
    return out, mask


def frame(quad, patch_shape, width_px):
    """Corners for a patch render of `width_px` finished width, on quad's roll."""
    c = quad.mean(axis=0)
    u = (quad[1] - quad[0]) + (quad[2] - quad[3])
    v = (quad[3] - quad[0]) + (quad[2] - quad[1])
    u = u / np.linalg.norm(u)
    v = v / np.linalg.norm(v)
    W = width_px * BLEED
    Hh = W * patch_shape[0] / patch_shape[1]
    return np.array([c - u * W / 2 - v * Hh / 2, c + u * W / 2 - v * Hh / 2,
                     c + u * W / 2 + v * Hh / 2, c - u * W / 2 + v * Hh / 2])


def place(base, clean, quad, patch, width_px, lum_ref=88.0):
    """Composite `patch` (RGBA float array) onto `clean`, lit by `base`."""
    shape = base.shape[:2]
    lum = np.asarray(Image.fromarray(base.astype(np.uint8)).convert('L')
                     .filter(ImageFilter.GaussianBlur(26))).astype(np.float64)
    dst = frame(quad, patch.shape, width_px)
    warped = warp_onto(patch, homography(UNIT, dst), shape)
    rgb, alpha = warped[..., :3], warped[..., 3:4] / 255.0

    # take the ambient colour cast from the fabric immediately around the patch
    ring = quad_mask(shape, quad, grow=0.85) & ~quad_mask(shape, quad, grow=0.30)
    if ring.any():
        m = base[ring].mean(axis=0)
        warm = np.clip((m / max(m.mean(), 1e-6)) ** 0.35, 0.85, 1.15)
    else:
        warm = np.ones(3)
    shade = np.clip(lum / lum_ref, 0.55, 1.60)[..., None]
    rgb = np.clip(rgb * shade * warm, 0, 255)
    return clean * (1 - alpha) + rgb * alpha, dst
