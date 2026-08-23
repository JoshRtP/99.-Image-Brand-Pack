"""Technical flat for the Terra Nexus wind shell, front and back.

Garment scale: 1 user unit = 1 mm, size M, slim athletic fit. The silhouette is
authored as a right-hand half and reflected, so the two sides cannot drift apart.
The cuff wordmarks are set from the same traced letterforms the patch is built
from, laid on an arc so they read as wrapping the wrist.
"""
import colorsys, json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
GLYPHS = os.path.abspath(os.path.join(HERE, '..', '..', 'Patch', 'build', 'glyphs.json'))

COLOURWAYS = {
    'glacier': ('Glacier Blue', '#5A90BE'),   # white-balanced off the story set
    'navy':    ('Terra Nexus Navy', '#131F48'),
    'red':     ('Terra Nexus Deep Red', '#6A1B32'),
}
PRIMARY = 'glacier'
ACCENT = '#E63D2F'   # Terra Nexus red - pulls and toggles
BONE = '#FFFFFF'
TRIM = '#16222F'


def _rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(rgb):
    return '#' + ''.join(f'{max(0, min(255, round(c * 255))):02X}' for c in rgb)


def shade(colour, lmul=1.0, ladd=0.0, smul=1.0):
    h, l, sat = colorsys.rgb_to_hls(*_rgb(colour))
    l = max(0.0, min(1.0, l * lmul + ladd))
    return _hex(colorsys.hls_to_rgb(h, l, max(0.0, min(1.0, sat * smul))))


# ---- size M, slim athletic fit, millimetres --------------------------------
NECK_F, NECK_B = 86.0, 26.0
CHEST, WAIST, HEM = 240.0, 208.0, 236.0     # half widths
WAIST_Y, SIDE_HEM = 430.0, 610.0
LEN_F, LEN_B = 622.0, 668.0                 # centre front / scooped centre back
UNDERARM = 285.0
CUFF_O, CUFF_I = (578.0, 511.0), (514.0, 565.0)
CUFF_BAND = 66.0                            # long cuff, carries the thumbhole
SLEEVE_U = (0.643, 0.766)                   # sleeve axis on the flat, 40 degrees
CAP_MM = 12.5                               # cuff wordmark cap height

G = json.load(open(GLYPHS))
CAP_SRC, BASELINE = 219.0, 254.0
WORDS = {'TERRA': ['T', 'E1', 'R1', 'R2', 'A'],
         'NEXUS': ['N', 'E2', 'X', 'U', 'S']}


def f(p):
    return f'{p[0]:.1f} {p[1]:.1f}'


def mx(p):
    return (-p[0], p[1])


def outline(p0, segs):
    pts = [p0] + [s[2] for s in segs]
    d = [f'M{f(p0)}'] + [f'C{f(c1)} {f(c2)} {f(p)}' for c1, c2, p in segs]
    for i in range(len(segs) - 1, -1, -1):
        c1, c2, _ = segs[i]
        d.append(f'C{f(mx(c2))} {f(mx(c1))} {f(mx(pts[i]))}')
    return ''.join(d) + 'Z'


def half(view):
    neck = NECK_F if view == 'front' else NECK_B
    hem = LEN_F if view == 'front' else LEN_B
    hem_c1 = (198.0, SIDE_HEM + 14) if view == 'front' else (190.0, SIDE_HEM + 40)
    hem_c2 = (92.0, hem + 3)
    return (0.0, neck), [
        ((32.0, neck - 16), (60.0, 12.0), (96.0, 2.0)),            # neckline
        ((250.0, 4.0), (430.0, 226.0), CUFF_O),                    # shoulder + sleeve top
        ((566.0, 534.0), (534.0, 552.0), CUFF_I),                  # cuff opening
        ((416.0, 452.0), (320.0, 358.0), (233.0, UNDERARM)),       # sleeve underside
        ((240.0, 330.0), (WAIST + 3, 386.0), (WAIST, WAIST_Y)),    # side seam into the waist
        ((WAIST - 1, 480.0), (HEM - 5, 562.0), (HEM, SIDE_HEM)),   # waist out to the hem
        (hem_c1, hem_c2, (0.0, hem + 3)),                          # hem
    ]


def hood(view):
    if view == 'front':
        return ('M-118 26C-148 -50 -100 -116 0 -116C100 -116 148 -50 118 26'
                'C96 138 -96 138 -118 26Z')
    return ('M-134 40C-178 -62 -112 -160 0 -160C112 -160 178 -62 134 40'
            'C88 128 -88 128 -134 40Z')


def hood_face(view):
    if view == 'front':
        return 'M-98 4C-120 -48 -80 -96 0 -96C80 -96 120 -48 98 4'
    return 'M-112 12C-144 -58 -92 -138 0 -138C92 -138 144 -58 112 12'


def raglan(mirror=False):
    pts = [(96.0, 2.0), (136.0, 88.0), (190.0, 196.0), (233.0, UNDERARM)]
    if mirror:
        pts = [mx(p) for p in pts]
    return f'M{f(pts[0])}C{f(pts[1])} {f(pts[2])} {f(pts[3])}'


def princess(view, mirror=False):
    hem = SIDE_HEM + (6 if view == 'front' else 22)
    pts = [(142.0, 100.0), (154.0, 224.0), (140.0, 336.0), (142.0, WAIST_Y),
           (144.0, 510.0), (152.0, 572.0), (154.0, hem)]
    if mirror:
        pts = [mx(p) for p in pts]
    return (f'M{f(pts[0])}C{f(pts[1])} {f(pts[2])} {f(pts[3])}'
            f'C{f(pts[4])} {f(pts[5])} {f(pts[6])}')


def cuff(mirror=False):
    ux, uy = SLEEVE_U
    a, b = CUFF_O, CUFF_I
    q = [a, b, (b[0] - ux * CUFF_BAND, b[1] - uy * CUFF_BAND),
         (a[0] - ux * CUFF_BAND, a[1] - uy * CUFF_BAND)]
    if mirror:
        q = [mx(p) for p in q]
    return 'M' + 'L'.join(f(p) for p in q) + 'Z'


def thumbhole(mirror=False):
    """Slot on the underside of the cuff, on the thumb side."""
    ux, uy = SLEEVE_U
    vx, vy = (CUFF_O[0] - CUFF_I[0]), (CUFF_O[1] - CUFF_I[1])
    n = math.hypot(vx, vy)
    vx, vy = vx / n, vy / n
    base = (CUFF_I[0] + vx * 13, CUFF_I[1] + vy * 13)
    a = (base[0] - ux * 14, base[1] - uy * 14)
    b = (base[0] - ux * 40, base[1] - uy * 40)
    if mirror:
        a, b = mx(a), mx(b)
    return f'M{f(a)}L{f(b)}'


# ---- cuff wordmarks --------------------------------------------------------
def gbox(name):
    xs, ys, i = [], [], 0
    for t in re.findall(r'[MLQZ]|-?\d+(?:\.\d+)?', G['glyphs'][name]):
        if t in 'MLQZ':
            i = 0
            continue
        (xs if i % 2 == 0 else ys).append(float(t))
        i += 1
    return min(xs), max(xs)


def word_on_cuff(word, mirror=False, fill=BONE):
    """Set `word` along the cuff on a shallow arc, so it reads as wrapping."""
    names = WORDS[word]
    boxes = {n: gbox(n) for n in names}
    left = min(G['x'][n] + boxes[n][0] for n in names)
    right = max(G['x'][n] + boxes[n][1] for n in names)
    wsrc = right - left
    k = CAP_MM / CAP_SRC
    span = wsrc * k

    ux, uy = SLEEVE_U
    o, i_ = (mx(CUFF_O), mx(CUFF_I)) if mirror else (CUFF_O, CUFF_I)
    u = (-ux, uy) if mirror else (ux, uy)
    # mid-band, then run the baseline so the word always reads left to right
    mo = (o[0] - u[0] * CUFF_BAND * 0.50, o[1] - u[1] * CUFF_BAND * 0.50)
    mi = (i_[0] - u[0] * CUFF_BAND * 0.50, i_[1] - u[1] * CUFF_BAND * 0.50)
    A, B = (mi, mo) if not mirror else (mo, mi)

    cx, cy = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    dx, dy = B[0] - A[0], B[1] - A[1]
    dn = math.hypot(dx, dy)
    dx, dy = dx / dn, dy / dn
    A = (cx - dx * span / 2, cy - dy * span / 2)
    B = (cx + dx * span / 2, cy + dy * span / 2)

    sag = span * 0.075                      # bulge toward the cuff opening
    apex = (cx + u[0] * sag, cy + u[1] * sag)
    R = (span * span) / (8 * sag) + sag / 2
    C = (apex[0] - u[0] * R, apex[1] - u[1] * R)
    a0 = math.atan2(A[1] - C[1], A[0] - C[0])
    a1 = math.atan2(B[1] - C[1], B[0] - C[0])
    if a1 - a0 > math.pi:
        a1 -= 2 * math.pi
    if a0 - a1 > math.pi:
        a1 += 2 * math.pi

    out = []
    for n in names:
        x0, x1 = boxes[n]
        centre = (G['x'][n] + (x0 + x1) / 2 - left) / wsrc
        a = a0 + (a1 - a0) * centre
        px, py = C[0] + R * math.cos(a), C[1] + R * math.sin(a)
        s = 1.0 if a1 >= a0 else -1.0
        deg = math.degrees(math.atan2(s * math.cos(a), -s * math.sin(a)))
        out.append(f'<g transform="translate({px:.2f},{py:.2f}) rotate({deg:.2f}) '
                   f'scale({k:.5f}) translate({-(x0 + x1) / 2:.2f},{-BASELINE})">'
                   f'<path d="{G["glyphs"][n]}"/></g>')
    return (f'<g class="cuff-mark" fill="{fill}" fill-rule="evenodd">'
            f'{"".join(out)}</g>')


def build(view, key=None):
    key = key or PRIMARY
    name, SHELL = COLOURWAYS[key]
    HOODIN = shade(SHELL, lmul=0.76)
    LINE = shade(SHELL, lmul=0.34)
    SEAM = shade(SHELL, lmul=0.62)
    W, H = 1420.0, 960.0
    ox, oy = W / 2, 230.0
    hem = LEN_F if view == 'front' else LEN_B
    p0, segs = half(view)

    # TERRA on the wearer's left wrist, NEXUS on the right. On the front view the
    # wearer's left is the viewer's right; on the back it is the viewer's left.
    left_is_mirrored = (view == 'back')
    marks = (word_on_cuff('TERRA', mirror=left_is_mirrored) +
             word_on_cuff('NEXUS', mirror=not left_is_mirrored))

    if view == 'front':
        detail = f'''
    <g id="front-zip-{key}-{view}">
      <line x1="0" y1="{NECK_F - 24}" x2="0" y2="{hem + 1}" stroke="{TRIM}" stroke-width="7"/>
      <line x1="0" y1="{NECK_F - 24}" x2="0" y2="{hem + 1}" stroke="#8FB4D0"
            stroke-width="2.4" stroke-dasharray="3.5 4.5" opacity="0.7"/>
      <rect x="-8" y="{NECK_F - 22}" width="16" height="30" rx="4" fill="{TRIM}"/>
      <rect x="-4" y="{NECK_F + 4}" width="8" height="40" rx="4" fill="{ACCENT}"/>
    </g>
    <g id="pockets-{key}-{view}" fill="none" stroke="{TRIM}" stroke-width="5"
       stroke-linecap="round">
      <path d="M92 402L188 342"/><path d="M-92 402L-188 342"/>
    </g>
    <g id="hood-cord-{key}-{view}" stroke="{TRIM}" stroke-width="4" fill="none"
       stroke-linecap="round">
      <path d="M-54 90C-48 124 -44 152 -46 176"/><path d="M54 90C48 124 44 152 46 176"/>
    </g>
    <g fill="{ACCENT}">
      <rect x="-52" y="174" width="12" height="20" rx="6"/>
      <rect x="40" y="174" width="12" height="20" rx="6"/>
      <rect x="-58" y="{hem - 32:.0f}" width="11" height="19" rx="5.5"/>
      <rect x="47" y="{hem - 32:.0f}" width="11" height="19" rx="5.5"/>
    </g>'''
    else:
        detail = f'''
    <path id="back-yoke-{key}-{view}" d="M-214 240C-112 202 112 202 214 240"
          fill="none" stroke="{SEAM}" stroke-width="3.5"/>
    <line id="hood-cb-{key}-{view}" x1="0" y1="-160" x2="0" y2="50"
          stroke="{SEAM}" stroke-width="3"/>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">
  <title>Terra Nexus wind shell - technical flat, {view} - {name}</title>
  <desc>Size M, slim athletic fit. 1 user unit = 1 mm. Shell {SHELL} ({name}).
        TERRA wraps the left cuff, NEXUS the right.</desc>
  <g transform="translate({ox},{oy})" stroke-linejoin="round">
    <path id="hood-{key}-{view}" d="{hood(view)}" fill="{HOODIN}" stroke="{LINE}" stroke-width="4.5"/>
    <path id="body-{key}-{view}" d="{outline(p0, segs)}" fill="{SHELL}" stroke="{LINE}" stroke-width="4.5"/>
    <g id="raglan-{key}-{view}" fill="none" stroke="{LINE}" stroke-width="3.5">
      <path d="{raglan()}"/><path d="{raglan(True)}"/>
    </g>
    <g id="princess-{key}-{view}" fill="none" stroke="{SEAM}" stroke-width="3.2">
      <path d="{princess(view)}"/><path d="{princess(view, True)}"/>
    </g>
    <g id="cuffs-{key}-{view}" fill="{SHELL}" stroke="{LINE}" stroke-width="3.5">
      <path d="{cuff()}"/><path d="{cuff(True)}"/>
    </g>
    <g id="thumbholes-{key}-{view}" fill="none" stroke="{LINE}" stroke-width="5"
       stroke-linecap="round">
      <path d="{thumbhole()}"/><path d="{thumbhole(True)}"/>
    </g>
    <path id="hood-face-{key}-{view}" d="{hood_face(view)}" fill="none" stroke="{SEAM}" stroke-width="3"/>
    <path id="hem-band-{key}-{view}" d="M-{HEM - 6:.0f} {SIDE_HEM - 30:.0f}
          C-120 {hem - 22:.0f} 120 {hem - 22:.0f} {HEM - 6:.0f} {SIDE_HEM - 30:.0f}"
          fill="none" stroke="{SEAM}" stroke-width="3.5"/>
    {detail}
    {marks}
  </g>
</svg>
'''


def flat_name(view, key=None):
    key = key or PRIMARY
    stem = f'jacket-flat-{view}'
    return f'{stem}.svg' if key == PRIMARY else f'{stem}-{key}.svg'


if __name__ == '__main__':
    for key in COLOURWAYS:
        for v in ('front', 'back'):
            open(os.path.join(OUT, flat_name(v, key)), 'w').write(build(v, key))
    print('wrote technical flats for', ', '.join(COLOURWAYS))
