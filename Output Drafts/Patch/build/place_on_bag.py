"""Composite the approved patch onto scene 6 as a placement reference.

The existing scene carries a non-conforming patch (mountain graphic, no star).
This removes it, then lays the approved patch back at true physical scale,
following the panel's perspective and picking up the scene's own lighting.
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SCENE = os.path.join(ROOT, 'Input Pictures - Story Based', '6. Story 3.png')

# corners of the patch currently in the scene, clockwise from top-left
OLD = np.array([[568., 489.], [663., 499.], [654., 577.], [554., 566.]])
PANEL_W = 420.          # visible width of the pack's front panel, px
PATCH_MM = 63.          # true finished width of the patch
PANEL_MM = 300.         # the pack panel is roughly 30 cm across
BLEED_MM = 2.           # patch-embroidered.svg carries 2 mm of bleed per side


def homography(src, dst):
    """3x3 mapping src (4x2) -> dst (4x2)."""
    A, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    h = np.linalg.solve(np.array(A), np.array(b))
    return np.append(h, 1).reshape(3, 3)


def apply_h(H, pts):
    p = np.hstack([pts, np.ones((len(pts), 1))]) @ H.T
    return p[:, :2] / p[:, 2:3]


def inpaint(img, mask, iters=900):
    """Laplace fill: smooth the masked region in from its boundary."""
    a = img.astype(np.float64).copy()
    m = mask.astype(bool)
    for c in range(3):
        ch = a[..., c]
        ch[m] = ch[~m].mean()
        for _ in range(iters):
            nb = np.zeros_like(ch)
            nb[1:-1, 1:-1] = (ch[:-2, 1:-1] + ch[2:, 1:-1] + ch[1:-1, :-2] + ch[1:-1, 2:]) / 4
            ch[m] = nb[m]
        a[..., c] = ch
    return a


def quad_mask(shape, quad, grow=0.0):
    c = quad.mean(axis=0)
    q = c + (quad - c) * (1 + grow)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    inside = np.ones(shape, bool)
    for i in range(4):
        p, nxt = q[i], q[(i + 1) % 4]
        e = nxt - p
        inside &= (e[0] * (yy - p[1]) - e[1] * (xx - p[0])) >= 0
    return inside


def warp_onto(patch, H, shape):
    """Inverse-warp an RGBA patch (unit square domain) into image space."""
    ph, pw = patch.shape[:2]
    Hi = np.linalg.inv(H)
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    pts = np.stack([xx.ravel(), yy.ravel(), np.ones(xx.size)])
    src = Hi @ pts
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


def build(patch_png, out_crop, mode='ba'):
    scene = Image.open(SCENE).convert('RGB')
    base = np.asarray(scene).astype(np.float64)
    H, W = base.shape[:2]

    # 1. lift the scene's own lighting over the patch area, before anything changes
    lum = np.asarray(Image.fromarray(base.astype(np.uint8)).convert('L')
                     .filter(ImageFilter.GaussianBlur(26))).astype(np.float64)

    # 2. take the old patch out
    old_mask = quad_mask((H, W), OLD, grow=0.30)
    # inpaint only a window around the patch - Laplace over the full frame is needless
    ys, xs = np.nonzero(old_mask)
    wy0, wy1 = ys.min() - 40, ys.max() + 41
    wx0, wx1 = xs.min() - 40, xs.max() + 41
    clean = base.copy()
    clean[wy0:wy1, wx0:wx1] = inpaint(base[wy0:wy1, wx0:wx1],
                                      old_mask[wy0:wy1, wx0:wx1], iters=1400)
    # put the fabric's grain back as synthetic noise matched to the panel's own
    # high-frequency statistics - borrowing real pixels drags seams in with them
    soft = np.asarray(Image.fromarray(base.astype(np.uint8))
                      .filter(ImageFilter.GaussianBlur(3))).astype(np.float64)
    ring = quad_mask((H, W), OLD, grow=0.85) & ~old_mask
    sigma = (base - soft)[ring].std(axis=0) if ring.any() else np.full(3, 3.0)
    rng = np.random.default_rng(7)
    noise = rng.standard_normal((wy1 - wy0, wx1 - wx0, 1)) * np.ones(3)
    noise = np.asarray(Image.fromarray(
        np.clip(noise * 40 + 128, 0, 255).astype(np.uint8)
    ).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float64)
    noise = (noise - noise.mean(axis=(0, 1))) / 40.0 * sigma
    win = clean[wy0:wy1, wx0:wx1]
    wm = old_mask[wy0:wy1, wx0:wx1]
    win[wm] = np.clip(win + noise, 0, 255)[wm]
    clean[wy0:wy1, wx0:wx1] = win

    # 3. place the approved patch at true scale, on the old patch's perspective
    Hq = homography(np.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.]]), OLD)
    old_w = np.linalg.norm(OLD[1] - OLD[0])
    old_h = np.linalg.norm(OLD[3] - OLD[0])
    patch = np.asarray(Image.open(patch_png).convert('RGBA')).astype(np.float64)
    ar = patch.shape[1] / patch.shape[0]
    # the source render includes bleed, so scale the whole image up by that ratio
    # to land the patch itself at its true physical width
    bleed = (PATCH_MM + 2 * BLEED_MM) / PATCH_MM
    new_w = PANEL_W * PATCH_MM / PANEL_MM * bleed  # px, true physical scale
    new_h = new_w / ar
    du, dv = new_w / old_w / 2, new_h / old_h / 2
    unit = np.array([[.5 - du, .5 - dv], [.5 + du, .5 - dv],
                     [.5 + du, .5 + dv], [.5 - du, .5 + dv]])
    quad = apply_h(Hq, unit)

    Hp = homography(np.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.]]), quad)
    warped = warp_onto(patch, Hp, (H, W))
    rgb, alpha = warped[..., :3], warped[..., 3:4] / 255.0

    # 4. make it sit in the scene: local light level, plus the sunset's warmth
    shade = np.clip(lum / 88.0, 0.55, 1.60)[..., None]
    warm = np.array([1.05, 0.99, 0.92])
    rgb = np.clip(rgb * shade * warm, 0, 255)

    out = clean * (1 - alpha) + rgb * alpha

    # 5. a before / after crop of the panel
    box = (int(quad[:, 0].min()) - 70, int(quad[:, 1].min()) - 60,
           int(quad[:, 0].max()) + 70, int(quad[:, 1].max()) + 60)
    before = scene.crop(box)
    after = Image.fromarray(out.astype(np.uint8)).crop(box)
    if mode == 'after':
        after = after.resize((after.width * 3, after.height * 3), Image.LANCZOS)
        after.save(out_crop)
    else:
        w, h = before.size
        sheet = Image.new('RGB', (w * 2 + 24, h), (244, 242, 236))
        sheet.paste(before, (0, 0)); sheet.paste(after, (w + 24, 0))
        sheet = sheet.resize((sheet.width * 3, sheet.height * 3), Image.LANCZOS)
        sheet.save(out_crop)
    print('quad', np.round(quad, 1).tolist(),
          f'| patch {new_w / bleed:.1f} x {new_h * 36 / 40:.1f} px on a {PANEL_W:.0f}px panel')


if __name__ == '__main__':
    import sys
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'ba')
