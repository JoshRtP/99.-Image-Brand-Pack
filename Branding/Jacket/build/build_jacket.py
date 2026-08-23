"""Technical flat for the Terra Nexus wind shell, front and back.

Garment scale: 1 user unit = 1 mm, size M. The silhouette is authored as a
right-hand half and reflected, so the two sides cannot drift apart. The sleeve
logo is the same traced lockup the patch is built from.
"""
import colorsys, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
GLYPHS = os.path.abspath(os.path.join(HERE, '..', '..', 'Patch', 'build', 'glyphs.json'))

COLOURWAYS = {
    'glacier': ('Glacier Blue', '#5A90BE'),   # white-balanced off the story set
    'navy':    ('Terra Nexus Navy', '#131F48'),
    'red':     ('Terra Nexus Deep Red', '#6A1B32'),
}
PRIMARY = 'glacier'


def _rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(rgb):
    return '#' + ''.join(f'{max(0, min(255, round(c * 255))):02X}' for c in rgb)


def shade(colour, lmul=1.0, ladd=0.0, smul=1.0):
    h, l, sat = colorsys.rgb_to_hls(*_rgb(colour))
    l = max(0.0, min(1.0, l * lmul + ladd))
    return _hex(colorsys.hls_to_rgb(h, l, max(0.0, min(1.0, sat * smul))))


SHELL  = COLOURWAYS[PRIMARY][1]
HOODIN = shade(SHELL, lmul=0.76)   # hood interior seen through the neck opening
LINE   = shade(SHELL, lmul=0.34)   # outline
SEAM   = shade(SHELL, lmul=0.62)   # construction lines
TRIM   = '#16222F'   # zips, elastic, cord
ACCENT = '#E63D2F'   # Terra Nexus red - pulls and cord tips
BONE   = '#FFFFFF'
SAND   = '#E8D77E'

# ---- size M, millimetres ---------------------------------------------------
NECK_F, NECK_B = 92.0, 30.0        # centre neck drop
HEM_F, HEM_B = 668.0, 684.0        # HPS to hem
UNDERARM = 300.0
CUFF_O, CUFF_I = (594.0, 508.0), (506.0, 578.0)
CUFF_BAND = 52.0
G = json.load(open(GLYPHS))
CAP, BBOX = 219.0, (0.0, 1.0, 1084.0, 256.0 + 1.125 * 219.0)


def f(p):
    return f'{p[0]:.1f} {p[1]:.1f}'


def mx(p):
    return (-p[0], p[1])


def outline(p0, segs):
    """Closed outline: the right half, then the same half reflected."""
    pts = [p0] + [s[2] for s in segs]
    d = [f'M{f(p0)}'] + [f'C{f(c1)} {f(c2)} {f(p)}' for c1, c2, p in segs]
    for i in range(len(segs) - 1, -1, -1):
        c1, c2, _ = segs[i]
        d.append(f'C{f(mx(c2))} {f(mx(c1))} {f(mx(pts[i]))}')
    return ''.join(d) + 'Z'


def half(view):
    neck = NECK_F if view == 'front' else NECK_B
    hem = HEM_F if view == 'front' else HEM_B
    return (0.0, neck), [
        ((34.0, neck - 18), (64.0, 14.0), (100.0, 2.0)),          # neckline
        ((252.0, 6.0), (438.0, 232.0), CUFF_O),                   # shoulder + sleeve top
        ((570.0, 532.0), (534.0, 556.0), CUFF_I),                 # cuff
        ((404.0, 462.0), (320.0, 374.0), (250.0, UNDERARM)),      # sleeve underside
        ((274.0, 420.0), (278.0, 548.0), (274.0, hem - 12)),      # side seam
        ((208.0, hem + 4), (98.0, hem + 6), (0.0, hem + 6)),      # hem
    ]


def hood(view):
    if view == 'front':
        return ('M-126 28C-158 -48 -106 -118 0 -118C106 -118 158 -48 126 28'
                'C102 144 -102 144 -126 28Z')
    return ('M-142 42C-188 -64 -118 -164 0 -164C118 -164 188 -64 142 42'
            'C92 132 -92 132 -142 42Z')


def hood_face(view):
    if view == 'front':
        return 'M-104 6C-128 -50 -84 -100 0 -100C84 -100 128 -50 104 6'
    return 'M-118 14C-152 -62 -96 -142 0 -142C96 -142 152 -62 118 14'


def gathers():
    """Short ticks across the cuff band, both sleeves."""
    ax = (CUFF_O[0] - 250.0, CUFF_O[1] - UNDERARM)
    n = (ax[0] ** 2 + ax[1] ** 2) ** 0.5
    ux, uy = ax[0] / n, ax[1] / n
    out = []
    for t in (0.22, 0.42, 0.62, 0.82):
        a = (CUFF_O[0] + (CUFF_I[0] - CUFF_O[0]) * t,
             CUFF_O[1] + (CUFF_I[1] - CUFF_O[1]) * t)
        b = (a[0] - ux * CUFF_BAND, a[1] - uy * CUFF_BAND)
        out.append(f'<path d="M{f(a)}L{f(b)}"/>')
        out.append(f'<path d="M{f(mx(a))}L{f(mx(b))}"/>')
    return ''.join(out)


def cuff(mirror=False):
    ax = (CUFF_O[0] - 250.0, CUFF_O[1] - UNDERARM)
    n = (ax[0] ** 2 + ax[1] ** 2) ** 0.5
    ux, uy = ax[0] / n, ax[1] / n
    a, b = CUFF_O, CUFF_I
    c = (b[0] - ux * CUFF_BAND, b[1] - uy * CUFF_BAND)
    d = (a[0] - ux * CUFF_BAND, a[1] - uy * CUFF_BAND)
    q = [a, b, c, d]
    if mirror:
        q = [mx(p) for p in q]
    return 'M' + 'L'.join(f(p) for p in q) + 'Z'


def raglan(mirror=False):
    pts = [(100.0, 2.0), (142.0, 92.0), (198.0, 202.0), (250.0, UNDERARM)]
    if mirror:
        pts = [mx(p) for p in pts]
    return f'M{f(pts[0])}C{f(pts[1])} {f(pts[2])} {f(pts[3])}'


def lockup(cx, cy, width, fill, opacity=1.0, rotate=0.0):
    """The approved stacked lockup, scaled to `width` mm and centred."""
    k = width / (BBOX[2] - BBOX[0])
    h = (BBOX[3] - BBOX[1]) * k
    ox, oy = cx - width / 2, cy - h / 2
    parts = []
    for n in ['T', 'E1', 'R1', 'R2', 'A']:
        parts.append((n, 0.0, 0.0))
    for n in ['N', 'E2', 'X', 'U', 'S']:
        parts.append((n, 129.6 - G['x']['N'], 1.125 * CAP))
    body = []
    for n, dx, dy in parts:
        tx = ox + (G['x'][n] + dx - BBOX[0]) * k
        ty = oy + (dy - BBOX[1]) * k
        body.append(f'<path d="{G["glyphs"][n]}" transform="translate({tx:.2f},{ty:.2f}) scale({k:.5f})"/>')
    sx = ox + (G['x']['STAR'] - BBOX[0]) * k
    sy = oy + (-BBOX[1]) * k
    rot = f' transform="rotate({rotate:.1f} {cx:.1f} {cy:.1f})"' if rotate else ''
    return (f'<g opacity="{opacity}"{rot}><g fill="{fill}" fill-rule="evenodd">{"".join(body)}</g>'
            f'<g fill="{SAND}" fill-rule="evenodd"><path d="{G["glyphs"]["STAR"]}" '
            f'transform="translate({sx:.2f},{sy:.2f}) scale({k:.5f})"/></g></g>')


def build(view, key=None):
    key = key or PRIMARY
    name, SHELL = COLOURWAYS[key]
    HOODIN = shade(SHELL, lmul=0.76)
    LINE = shade(SHELL, lmul=0.34)
    SEAM = shade(SHELL, lmul=0.62)
    W, H = 1420.0, 960.0
    ox, oy = W / 2, 230.0
    hem = HEM_F if view == 'front' else HEM_B
    p0, segs = half(view)

    if view == 'front':
        detail = f'''
    <g id="front-zip-{key}-{view}">
      <line x1="0" y1="{NECK_F - 26}" x2="0" y2="{hem + 2}" stroke="{TRIM}" stroke-width="7"/>
      <line x1="0" y1="{NECK_F - 26}" x2="0" y2="{hem + 2}" stroke="#8FB4D0"
            stroke-width="2.4" stroke-dasharray="3.5 4.5" opacity="0.7"/>
      <rect x="-8" y="{NECK_F - 24}" width="16" height="30" rx="4" fill="{TRIM}"/>
      <rect x="-4" y="{NECK_F + 2}" width="8" height="40" rx="4" fill="{ACCENT}"/>
    </g>
    <g id="pockets-{key}-{view}" fill="none" stroke="{TRIM}" stroke-width="5.5" stroke-linecap="round">
      <path d="M76 408L214 358"/><path d="M-76 408L-214 358"/>
    </g>
    <g id="pocket-pulls-{key}-{view}" fill="{ACCENT}">
      <rect x="70" y="406" width="7" height="26" rx="3.5"/>
      <rect x="-77" y="406" width="7" height="26" rx="3.5"/>
    </g>
    <g id="hood-cord-{key}-{view}" stroke="{TRIM}" stroke-width="4" fill="none" stroke-linecap="round">
      <path d="M-58 96C-52 130 -48 158 -50 182"/><path d="M58 96C52 130 48 158 50 182"/>
    </g>
    <g fill="{ACCENT}">
      <rect x="-56" y="180" width="12" height="20" rx="6"/>
      <rect x="44" y="180" width="12" height="20" rx="6"/>
    </g>
    <g id="hem-cord-{key}-{view}" fill="{ACCENT}">
      <rect x="-64" y="{hem - 34:.0f}" width="11" height="19" rx="5.5"/>
      <rect x="53" y="{hem - 34:.0f}" width="11" height="19" rx="5.5"/>
    </g>
    {lockup(258, 166, 84, BONE, 1.0, -38)}'''
    else:
        detail = f'''
    <path id="back-yoke-{key}-{view}" d="M-232 {UNDERARM - 8:.0f}C-120 {UNDERARM - 62:.0f} 120 {UNDERARM - 62:.0f} 232 {UNDERARM - 8:.0f}"
          fill="none" stroke="{SEAM}" stroke-width="3.5"/>
    <line id="hood-cb-{key}-{view}" x1="0" y1="-164" x2="0" y2="52" stroke="{SEAM}" stroke-width="3"/>
    {lockup(-258, 166, 84, BONE, 1.0, 38)}'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">
  <title>Terra Nexus wind shell - technical flat, {view} - {name}</title>
  <desc>Size M. 1 user unit = 1 mm. Shell {SHELL} ({name}).</desc>
  <g transform="translate({ox},{oy})" stroke-linejoin="round">
    <path id="hood-{key}-{view}" d="{hood(view)}" fill="{HOODIN}" stroke="{LINE}" stroke-width="4.5"/>
    <path id="body-{key}-{view}" d="{outline(p0, segs)}" fill="{SHELL}" stroke="{LINE}" stroke-width="4.5"/>
    <g id="raglan-{key}-{view}" fill="none" stroke="{LINE}" stroke-width="3.5">
      <path d="{raglan()}"/><path d="{raglan(True)}"/>
    </g>
    <g id="cuffs-{key}-{view}" fill="{SHELL}" stroke="{LINE}" stroke-width="3.5">
      <path d="{cuff()}"/><path d="{cuff(True)}"/>
    </g>
    <g id="cuff-elastic-{key}-{view}" stroke="{SEAM}" stroke-width="2.4" opacity="0.85">
      {gathers()}
    </g>
    <path id="hood-face-{key}-{view}" d="{hood_face(view)}" fill="none" stroke="{SEAM}" stroke-width="3"/>
    <path id="hem-band-{key}-{view}" d="M-268 {hem - 40:.0f}C-120 {hem - 26:.0f} 120 {hem - 26:.0f} 268 {hem - 40:.0f}"
          fill="none" stroke="{SEAM}" stroke-width="3.5"/>
    {detail}
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
