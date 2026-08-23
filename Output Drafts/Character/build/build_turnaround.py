"""Costume turnaround: the main character in the wind shell, five angles.

The figure is built from horizontal elliptical cross-sections. Each section has
a half-width and a half-depth; rotating it about the vertical axis and
projecting gives both the silhouette and the position of any seam, so all five
views come from one model and cannot disagree with each other.

Scale: figure height 1000 units = 1680 mm, so 1 unit = 1.68 mm. Garment
measurements are taken straight from the jacket spec.
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'Jacket', 'build')))
import build_jacket as J                                       # noqa: E402

MM = 1.68                                    # mm per figure unit
SHELL = J.COLOURWAYS['glacier'][1]
HOODIN = J.shade(SHELL, lmul=0.76)
LINE = J.shade(SHELL, lmul=0.34)
SEAM = J.shade(SHELL, lmul=0.62)
TRIM = '#16222F'
ACCENT = '#E63D2F'
SKIN = '#C6A088'
SKIN_L = '#D6B49C'
HAIR = '#6A4830'
HAIR_L = '#8A6242'
TROUSER = '#2C313A'
TROUSER_L = '#3A404B'
BOOT = '#463A2C'
BONE = '#FFFFFF'

# ---- vertical landmarks, fraction of height x 1000 -------------------------
HEAD_TOP, CHIN = 0.0, 134.0
HPS, BUST, WAIST_Y, HIP, CROTCH = 167.0, 268.0, 387.0, 506.0, 548.0
KNEE, ANKLE, FLOOR = 726.0, 940.0, 1000.0

# ---- garment profile, from the jacket spec ---------------------------------
def u(mm):
    return mm / MM


def worn_half(flat_half_mm, k):
    """Laid-flat half width -> worn half width.

    A flat half width of h means a tube of circumference 4h. Worn, that tube
    takes an elliptical section with semi-axes a and ka; inverting Ramanujan's
    perimeter gives a. Using the flat width directly is what turns a slim shell
    into a parka on the figure.
    """
    C = 4.0 * flat_half_mm
    denom = math.pi * (3 * (1 + k) - math.sqrt((3 + k) * (1 + 3 * k)))
    return C / denom


JACKET = [                     # (y, worn half width in figure units, depth ratio)
    (HPS + 2,             u(worn_half(J.CHEST * 0.80, 0.78)), 0.78),
    (HPS + 48,            u(210.0),                           0.74),
    (HPS + 112,           u(worn_half(J.CHEST * 1.03, 0.76)), 0.76),
    (HPS + u(J.UNDERARM), u(worn_half(J.CHEST, 0.75)),        0.75),
    (HPS + u(J.WAIST_Y),  u(worn_half(J.WAIST, 0.80)),        0.80),
    (HPS + u(J.SIDE_HEM), u(worn_half(J.HEM, 0.74)),          0.74),
]
HEM_SIDE = HPS + u(J.SIDE_HEM)
HEM_CB = HPS + u(J.LEN_B)
HEM_CF = HPS + u(J.LEN_F)

LEGS = [(HIP, 92.0, 0.86), (CROTCH, 88.0, 0.86), (KNEE, 46.0, 0.92),
        (ANKLE, 26.0, 0.95)]


def lerp_profile(prof, y):
    if y <= prof[0][0]:
        return prof[0][1], prof[0][1] * prof[0][2]
    if y >= prof[-1][0]:
        return prof[-1][1], prof[-1][1] * prof[-1][2]
    for (y0, w0, k0), (y1, w1, k1) in zip(prof, prof[1:]):
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            t = t * t * (3 - 2 * t)                       # smoothstep
            w = w0 + (w1 - w0) * t
            k = k0 + (k1 - k0) * t
            return w, w * k
    return prof[-1][1], prof[-1][1] * prof[-1][2]


def half_width(prof, y, th):
    w, d = lerp_profile(prof, y)
    return math.hypot(w * math.cos(th), d * math.sin(th))


def seam_x(prof, y, phi, th):
    """Image x of a feature at azimuth phi (0 = centre front, pi = centre back)."""
    w, d = lerp_profile(prof, y)
    return w * math.sin(phi) * math.cos(th) + d * math.cos(phi) * math.sin(th)


def seam_visible(prof, y, phi, th):
    w, d = lerp_profile(prof, y)
    return (-w * math.sin(phi) * math.sin(th) + d * math.cos(phi) * math.cos(th)) > -0.04


def f(p):
    return f'{p[0]:.1f} {p[1]:.1f}'


def smooth(points, close=False):
    """Catmull-Rom through points, emitted as cubics."""
    if len(points) < 2:
        return ''
    p = points
    d = [f'M{f(p[0])}']
    n = len(p)
    for i in range(n - 1):
        p0 = p[i - 1] if i > 0 else p[0]
        p1, p2 = p[i], p[i + 1]
        p3 = p[i + 2] if i + 2 < n else p[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f'C{f(c1)} {f(c2)} {f(p2)}')
    if close:
        d.append('Z')
    return ''.join(d)


def body_shape(prof, y0, y1, th, steps=22, bottom_curve=0.0):
    """Closed silhouette between two heights."""
    ys = [y0 + (y1 - y0) * i / steps for i in range(steps + 1)]
    right = [(half_width(prof, y, th), y) for y in ys]
    left = [(-x, y) for x, y in reversed(right)]
    pts = right + left
    return smooth(pts, close=True)


# ---- hem: the jacket is longer at centre back than at the side -------------
def hem_y(phi):
    a = abs(phi)
    if a <= math.pi / 2:
        t = a / (math.pi / 2)
        return HEM_CF + (HEM_SIDE - HEM_CF) * (t * t * (3 - 2 * t))
    t = (a - math.pi / 2) / (math.pi / 2)
    return HEM_SIDE + (HEM_CB - HEM_SIDE) * (t * t * (3 - 2 * t))


def tangent_phi(prof, y, th):
    w, d = lerp_profile(prof, y)
    return math.atan2(d * math.cos(th), w * math.sin(th))


def hem_points(th, n=40):
    phi_t = tangent_phi(JACKET, HEM_SIDE, th)
    out = []
    for i in range(n + 1):
        phi = phi_t - math.pi * i / n
        y = hem_y(phi)
        out.append((seam_x(JACKET, y, phi, th), y))
    return out


def jacket_outline(th):
    top = HPS + 2
    hem = hem_points(th)
    ys = [top + (HEM_SIDE - top) * i / 20 for i in range(21)]
    right = [(half_width(JACKET, y, th), y) for y in ys]
    left = [(-half_width(JACKET, y, th), y) for y in reversed(ys)]
    pts = right[:-1] + hem + left[1:]
    return smooth(pts, close=True)


# ---- seams -----------------------------------------------------------------
def seam_path(th, phi, y0, y1, prof=JACKET, steps=14):
    pts = []
    for i in range(steps + 1):
        y = y0 + (y1 - y0) * i / steps
        if not seam_visible(prof, y, phi, th):
            continue
        pts.append((seam_x(prof, y, phi, th), y))
    return smooth(pts) if len(pts) > 1 else ''


def raglan_path(th, side, back=False, steps=16):
    """Neck to underarm: the seam's azimuth swings from the neck to the side."""
    y0, y1 = HPS + 6, HPS + u(J.UNDERARM)
    a0 = math.radians(34 if not back else 146)
    a1 = math.radians(90)
    pts = []
    for i in range(steps + 1):
        t = i / steps
        y = y0 + (y1 - y0) * t
        phi = side * (a0 + (a1 - a0) * (t ** 0.75)) if not back else side * (a0 + (a1 - a0) * (t ** 0.75))
        if not seam_visible(JACKET, y, phi, th):
            continue
        pts.append((seam_x(JACKET, y, phi, th), y))
    return smooth(pts) if len(pts) > 1 else ''


def yoke_path(th, steps=30):
    y = HPS + u(240)
    pts = []
    phi_t = tangent_phi(JACKET, y, th)
    for i in range(steps + 1):
        phi = phi_t - math.pi * i / steps
        if abs(phi) < math.radians(96):        # the yoke is a back seam only
            continue
        pts.append((seam_x(JACKET, y, phi, th), y - 14 * math.cos(phi)))
    return smooth(pts) if len(pts) > 1 else ''


def hem_band(th):
    pts = [(x, y - 16) for x, y in hem_points(th, 30)]
    return smooth(pts)


# ---- arms ------------------------------------------------------------------
ARM = [(HPS + 44, 30.0), (HPS + 150, 24.0), (HPS + 280, 19.0), (HPS + 333, 16.0)]
WRIST_Y = HPS + 333
CUFF_TOP = WRIST_Y - u(J.CUFF_BAND)


def arm_axis(side, th):
    """Image x of the arm's centre line at the shoulder and at the wrist."""
    y_sh = HPS + 40
    w, d = lerp_profile(JACKET, y_sh)
    phi = side * math.pi / 2
    x_sh = (w - 4) * math.sin(phi) * math.cos(th) + d * math.cos(phi) * math.sin(th)
    depth = -(w - 4) * math.sin(phi) * math.sin(th) + d * math.cos(phi) * math.cos(th)
    x_wr = x_sh + side * 12 * math.cos(th)
    return x_sh, x_wr, depth


def arm_shape(side, th):
    x_sh, x_wr, _ = arm_axis(side, th)
    pts_r, pts_l = [], []
    for y, r in ARM:
        t = (y - ARM[0][0]) / (WRIST_Y - ARM[0][0])
        cx = x_sh + (x_wr - x_sh) * t
        pts_r.append((cx + r, y))
        pts_l.append((cx - r, y))
    outline = smooth(pts_r + list(reversed(pts_l)), close=True)
    return outline, x_sh, x_wr


def cuff_shape(side, th):
    x_sh, x_wr, _ = arm_axis(side, th)
    t0 = (CUFF_TOP - ARM[0][0]) / (WRIST_Y - ARM[0][0])
    cx0 = x_sh + (x_wr - x_sh) * t0
    r0, r1 = 18.0, 16.0
    return (f'M{cx0 - r0:.1f} {CUFF_TOP:.1f}L{cx0 + r0:.1f} {CUFF_TOP:.1f}'
            f'L{x_wr + r1:.1f} {WRIST_Y:.1f}L{x_wr - r1:.1f} {WRIST_Y:.1f}Z')


# ---- head, hair, legs ------------------------------------------------------
HEAD_W, HEAD_D, HEAD_RY = 45.0, 52.0, 67.0
HEAD_CY = 68.0


def head_group(th):
    rx = math.hypot(HEAD_W * math.cos(th), HEAD_D * math.sin(th))
    face_x = 0.46 * HEAD_D * math.sin(th)
    show_face = math.cos(th) > -0.20
    out = [f'<ellipse cx="0" cy="{HEAD_CY}" rx="{rx:.1f}" ry="{HEAD_RY}" fill="{HAIR}"/>']
    if show_face:
        fade = max(0.0, math.cos(th))
        out.append(f'<ellipse cx="{face_x:.1f}" cy="{HEAD_CY + 10:.1f}" '
                   f'rx="{rx * 0.62:.1f}" ry="{HEAD_RY * 0.72:.1f}" fill="{SKIN}"/>')
        out.append(f'<ellipse cx="{face_x * 1.15:.1f}" cy="{HEAD_CY - 4:.1f}" '
                   f'rx="{rx * 0.60:.1f}" ry="{HEAD_RY * 0.42:.1f}" fill="{HAIR}" '
                   f'opacity="{0.9:.2f}"/>')
        out.append(f'<ellipse cx="{face_x * 0.6:.1f}" cy="{HEAD_CY + 42:.1f}" '
                   f'rx="{rx * 0.30:.1f}" ry="{10:.1f}" fill="{SKIN_L}" opacity="{fade * 0.5:.2f}"/>')
    # neck
    nw = 20 + 6 * abs(math.sin(th))
    out.append(f'<path d="M{-nw:.1f} {CHIN - 4:.1f}L{nw:.1f} {CHIN - 4:.1f}'
               f'L{nw * 0.9:.1f} {HPS + 10:.1f}L{-nw * 0.9:.1f} {HPS + 10:.1f}Z" fill="{SKIN}"/>')
    return ''.join(out)


def ponytail(th):
    x = -HEAD_D * math.sin(th) * 0.92
    lean = 6 * math.cos(th)
    pts = [(x, HEAD_CY + 4), (x - lean * 0.4, HEAD_CY + 52), (x - lean, HEAD_CY + 104),
           (x - lean * 1.3, HEAD_CY + 148)]
    w = [26, 30, 22, 8]
    r = [(px + ww * 0.5, py) for (px, py), ww in zip(pts, w)]
    l = [(px - ww * 0.5, py) for (px, py), ww in zip(reversed(pts), reversed(w))]
    return (f'<path d="{smooth(r + l, close=True)}" fill="{HAIR}"/>'
            f'<path d="{smooth([(px, py) for px, py in pts])}" fill="none" '
            f'stroke="{HAIR_L}" stroke-width="3" opacity="0.6"/>')


LEG_R = [(HIP, 40.0), (CROTCH, 38.0), (KNEE, 26.0), (ANKLE, 16.0)]


def leg_shape(side, th):
    x0 = side * 36.0 * math.cos(th)
    pts_r, pts_l = [], []
    for y, r in LEG_R:
        cx = x0 * (1 - 0.25 * (y - HIP) / (ANKLE - HIP))
        pts_r.append((cx + r, y)); pts_l.append((cx - r, y))
    return smooth(pts_r + list(reversed(pts_l)), close=True)


def boot_shape(side, th):
    x0 = side * 36.0 * math.cos(th) * 0.75
    toe = 20 * math.cos(th)
    return (f'M{x0 - 20:.1f} {ANKLE - 6:.1f}L{x0 + 20:.1f} {ANKLE - 6:.1f}'
            f'L{x0 + 23 + max(0, toe):.1f} {FLOOR - 6:.1f}'
            f'Q{x0 + 24 + max(0, toe):.1f} {FLOOR:.1f} {x0 + 18 + max(0, toe):.1f} {FLOOR:.1f}'
            f'L{x0 - 18 + min(0, toe):.1f} {FLOOR:.1f}'
            f'Q{x0 - 24 + min(0, toe):.1f} {FLOOR:.1f} {x0 - 23 + min(0, toe):.1f} {FLOOR - 6:.1f}Z')


# ---- one view --------------------------------------------------------------
PHI_PRINCESS = math.radians(54)
PHI_SIDE = math.radians(90)
PHI_PRINCESS_B = math.radians(126)


def view(th_deg, label):
    th = math.radians(th_deg)
    far, near = (1, -1) if math.sin(th) > 0 else (-1, 1)
    if abs(math.sin(th)) < 0.05:
        far, near = 1, -1

    def arm_block(side):
        outline, x_sh, x_wr = arm_shape(side, th)
        word = 'TERRA' if side > 0 else 'NEXUS'
        return f'''<g class="arm">
      <path d="{outline}" fill="{SHELL}" stroke="{LINE}" stroke-width="2.6"/>
      <path d="{cuff_shape(side, th)}" fill="{SHELL}" stroke="{LINE}" stroke-width="2.6"/>
      <path d="{cuff_shape(side, th)}" fill="{BONE}" opacity="0.9"
            transform="translate(0,0)" clip-path="none" style="display:none"/>
      <g class="cuff-mark" fill="{BONE}" opacity="0.95">
        <rect x="{x_wr - 13:.1f}" y="{(CUFF_TOP + WRIST_Y) / 2 - 5:.1f}" width="26" height="7" rx="3"/>
      </g>
      <ellipse cx="{x_wr:.1f}" cy="{WRIST_Y + 26:.1f}" rx="13" ry="26" fill="{SKIN}"/>
    </g>'''

    parts = [arm_block(far),
             f'<path d="{leg_shape(far, th)}" fill="{TROUSER}"/>',
             f'<path d="{leg_shape(near, th)}" fill="{TROUSER_L}"/>',
             f'<path d="{boot_shape(far, th)}" fill="{BOOT}"/>',
             f'<path d="{boot_shape(near, th)}" fill="{BOOT}" stroke="{TRIM}" stroke-width="2"/>',
             f'<path d="{jacket_outline(th)}" fill="{SHELL}" stroke="{LINE}" stroke-width="3"/>']

    seams = []
    for phi in (PHI_PRINCESS, -PHI_PRINCESS, PHI_PRINCESS_B, -PHI_PRINCESS_B):
        d = seam_path(th, phi, HPS + u(J.UNDERARM) - 30, hem_y(phi) - 6)
        if d:
            seams.append(f'<path d="{d}" fill="none" stroke="{SEAM}" stroke-width="2.2"/>')
    for phi in (PHI_SIDE, -PHI_SIDE):
        d = seam_path(th, phi, HPS + u(J.UNDERARM), hem_y(phi) - 6)
        if d:
            seams.append(f'<path d="{d}" fill="none" stroke="{SEAM}" stroke-width="1.8" opacity="0.7"/>')
    for side in (1, -1):
        for back in (False, True):
            d = raglan_path(th, side, back)
            if d:
                seams.append(f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="2.4"/>')
    d = yoke_path(th)
    if d:
        seams.append(f'<path d="{d}" fill="none" stroke="{SEAM}" stroke-width="2.2"/>')
    seams.append(f'<path d="{hem_band(th)}" fill="none" stroke="{SEAM}" stroke-width="2"/>')

    if math.cos(th) > 0.12:                      # centre-front zip
        zip_pts = [(seam_x(JACKET, y, 0.0, th), y)
                   for y in [HPS + 30 + i * 22 for i in range(int((HEM_CF - HPS - 30) / 22) + 1)]]
        seams.append(f'<path d="{smooth(zip_pts)}" fill="none" stroke="{TRIM}" stroke-width="3.4"/>')
        zx, zy = zip_pts[0]
        seams.append(f'<rect x="{zx - 4:.1f}" y="{zy - 6:.1f}" width="8" height="20" rx="4" fill="{ACCENT}"/>')

    # hood, worn down behind the neck
    hw = math.hypot(60 * math.cos(th), 72 * math.sin(th))
    hx = -84 * math.sin(th) * 0.35
    hood = (f'<ellipse cx="{hx:.1f}" cy="{HPS + 4:.1f}" rx="{hw:.1f}" ry="40" '
            f'fill="{HOODIN}" stroke="{LINE}" stroke-width="2.6"/>')

    body = ''.join(parts[:-1]) + hood + parts[-1] + ''.join(seams)
    pt = ponytail(th)
    head = head_group(th)
    front_tail = math.cos(th) < 0.35
    inner = (body + arm_block(near) +
             ('' if front_tail else pt) + head + (pt if front_tail else ''))
    return f'<g class="fig" data-view="{label}">{inner}</g>'


# ---- sheet -----------------------------------------------------------------
INK, PAPER = '#061927', '#F4F2EC'
FONT = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
MONO = "'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"
SW, SH = 420.0, 348.0
MARGIN = 20.0
FIG_TOP, FIG_K = 54.0, 0.170
VIEWS = [(0, 'FRONT', '0°'), (40, 'THREE-QUARTER FRONT', '40°'), (90, 'SIDE', '90°'),
         (140, 'THREE-QUARTER BACK', '140°'), (180, 'BACK', '180°')]


def txt(x, y, s, size=3.0, fill=INK, anchor='start', weight='400', family=FONT,
        spacing=0, opacity=1):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" opacity="{opacity}">{s}</text>')


def word_arc(word, cx, cy, width, cap, bulge=0.10, fill=INK):
    names = J.WORDS[word]
    boxes = {n: J.gbox(n) for n in names}
    left = min(J.G['x'][n] + boxes[n][0] for n in names)
    right = max(J.G['x'][n] + boxes[n][1] for n in names)
    wsrc = right - left
    k = cap / J.CAP_SRC
    span = wsrc * k
    sag = span * bulge
    R = (span * span) / (8 * sag) + sag / 2
    C = (cx, cy - R + sag)
    a0 = math.atan2(cy - C[1], cx - span / 2 - C[0])
    a1 = math.atan2(cy - C[1], cx + span / 2 - C[0])
    out = []
    for n in names:
        x0, x1 = boxes[n]
        t = (J.G['x'][n] + (x0 + x1) / 2 - left) / wsrc
        a = a0 + (a1 - a0) * t
        px, py = C[0] + R * math.cos(a), C[1] + R * math.sin(a)
        deg = math.degrees(a) - 90
        out.append(f'<g transform="translate({px:.2f},{py:.2f}) rotate({deg:.2f}) '
                   f'scale({k:.5f}) translate({-(x0 + x1) / 2:.2f},{-J.BASELINE})">'
                   f'<path d="{J.G["glyphs"][n]}"/></g>')
    return f'<g fill="{fill}" fill-rule="evenodd">{"".join(out)}</g>'


def cuff_detail(x, y, w):
    """Enlarged left and right cuffs, so the wordmarks are legible."""
    bw, bh = (w - 10) / 2, 30.0
    out = [txt(x, y - 4, 'CUFF DETAIL', 3.2, INK, 'start', '700', FONT, 0.6),
           f'<line x1="{x}" y1="{y - 2.2}" x2="{x + w}" y2="{y - 2.2}" '
           f'stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>']
    for i, (word, side) in enumerate((('TERRA', 'LEFT'), ('NEXUS', 'RIGHT'))):
        bx = x + i * (bw + 10)
        out.append(f'<rect x="{bx}" y="{y + 4}" width="{bw}" height="{bh}" rx="2.5" '
                   f'fill="{SHELL}" stroke="{LINE}" stroke-width="0.5"/>')
        out.append(word_arc(word, bx + bw / 2, y + 4 + bh * 0.62, bw * 0.78, 9.0,
                            0.10, BONE))
        out.append(txt(bx + bw / 2, y + bh + 10, f'{side} WRIST', 2.6, INK, 'middle',
                       '700', FONT, 0.16, 0.6))
    return '\n  '.join(out)


def block(x, y, title, rows, w=118, keyw=30, lead=3.9, size=2.7):
    out = [txt(x, y, title, 3.2, INK, 'start', '700', FONT, 0.6),
           f'<line x1="{x}" y1="{y + 1.8}" x2="{x + w}" y2="{y + 1.8}" '
           f'stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>']
    yy = y + 6.8
    for k, v in rows:
        out.append(txt(x, yy, k, size, INK, 'start', '600', FONT, 0, 0.9))
        for i, line in enumerate(v):
            out.append(txt(x + keyw, yy + i * lead, line, size, INK, 'start', '400',
                           FONT, 0, 0.78))
        yy += max(1, len(v)) * lead + 1.5
    return '\n  '.join(out), yy


def build():
    slot = (SW - 2 * MARGIN) / len(VIEWS)
    figs, labels = [], []
    for i, (deg, name, ang) in enumerate(VIEWS):
        cx = MARGIN + slot * (i + 0.5)
        figs.append(f'<g transform="translate({cx:.2f},{FIG_TOP}) scale({FIG_K})">'
                    f'{view(deg, name)}</g>')
        base = FIG_TOP + 1000 * FIG_K
        labels.append(txt(cx, base + 8, name, 2.8, INK, 'middle', '700', FONT, 0.16))
        labels.append(txt(cx, base + 12.6, ang, 2.8, INK, 'middle', '500', MONO, 0, 0.6))

    base = FIG_TOP + 1000 * FIG_K + 22
    notes, _ = block(MARGIN, base + 6, 'WARDROBE - LOCKED', [
        ('Jacket', ['Terra Nexus wind shell, Glacier Blue #5A90BE, slim athletic fit.',
                    'Hood worn down. Zipped. TERRA wraps the left cuff, NEXUS the right.',
                    'No shoulder mark, no sewn patch anywhere on the garment.']),
        ('Below', ['Dark charcoal technical trouser, slim. Low brown approach boot.']),
        ('Hair', ['Mid-brown, mid-height ponytail, loose flyaway strands at the crown.']),
        ('Build', ['Athletic, approx. 168 cm. Jacket is size M.']),
    ], w=232, keyw=26, lead=3.7, size=2.65)

    ctx, _ = block(MARGIN, base + 46, 'HOW SHE READS IN THE STORY SET', [
        ('Angles used', ['Back and three-quarter back in every character scene -',
                         'scenes 1, 2, 3, 5, 7, 8 and 9. Nothing face-on.']),
        ('With the pack', ['The pack rides over the shell. Its shoulder straps cross',
                           'the front princess seams; the Deep Red patch sits centred',
                           'on the upper front panel of the pack, not on the jacket.']),
        ('Do not', ['put a patch or any mark on the shoulder or upper arm -',
                    'the cuffs carry the wordmark now.']),
    ], w=232, keyw=26, lead=3.7, size=2.65)

    open_q, oy = block(MARGIN + 242, base + 6, 'NOT ESTABLISHED', [
        ('Face', ['The story set never shows it - every frame is', 'from behind. Left deliberately unresolved here.']),
        ('Front', ['No front-facing reference exists. The front of', 'both the figure and the garment is specified.']),
    ], w=138, keyw=20, lead=3.7, size=2.65)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SW} {SH}" width="{SW}mm" height="{SH}mm">
  <title>Terra Nexus - character costume turnaround</title>
  <desc>The main character in the wind shell at five angles, built from one
        cross-section model so the views agree with each other.</desc>
  <rect width="{SW}" height="{SH}" fill="{PAPER}"/>
  <line x1="{MARGIN}" y1="30" x2="{SW - MARGIN}" y2="30" stroke="{INK}" stroke-width="0.5"/>
  {txt(MARGIN, 22, 'TERRA NEXUS', 8.0, INK, 'start', '700', FONT, 2.1)}
  {txt(MARGIN, 27.5, 'CHARACTER COSTUME TURNAROUND - WIND SHELL', 3.2, INK, 'start', '500', FONT, 1.5, 0.75)}
  {txt(SW - MARGIN, 22, 'REV A', 4.0, INK, 'end', '600', MONO)}
  {txt(SW - MARGIN, 27.5, 'figure 168 cm, garment size M', 2.7, INK, 'end', '400', FONT, 0, 0.65)}
  {''.join(figs)}
  {''.join(labels)}
  {cuff_detail(MARGIN + 242, oy + 10, 138)}
  {notes}
  {ctx}
  {open_q}
  <line x1="{MARGIN}" y1="{SH - 13}" x2="{SW - MARGIN}" y2="{SH - 13}" stroke="{INK}" stroke-opacity="0.25" stroke-width="0.3"/>
  {txt(MARGIN, SH - 7.5, 'Costume reference only - not a likeness. Garment geometry is taken from Output Drafts/Jacket.', 2.6, INK, 'start', '400', FONT, 0, 0.6)}
</svg>
'''


def single(deg, name):
    """One angle on its own, for dropping into an image model as a reference."""
    W, H = 420.0, 1120.0
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <title>Terra Nexus character - wind shell - {name.lower()}</title>
  <rect width="{W}" height="{H}" fill="{PAPER}"/>
  <g transform="translate({W / 2},40) scale(1.02)">{view(deg, name)}</g>
  {txt(W / 2, H - 26, name, 22, INK, 'middle', '700', FONT, 1.6)}
</svg>
'''


SLUG = {0: 'front', 40: 'three-quarter-front', 90: 'side',
        140: 'three-quarter-back', 180: 'back'}

if __name__ == '__main__':
    open(os.path.join(OUT, 'character-turnaround.svg'), 'w').write(build())
    for deg, name, _ in VIEWS:
        open(os.path.join(OUT, f'character-{SLUG[deg]}.svg'), 'w').write(single(deg, name))
    print('wrote character-turnaround.svg and 5 single-angle files')
