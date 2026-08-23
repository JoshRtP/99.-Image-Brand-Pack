"""Direct raised embroidery on the pack panel - block letters, tone on tone.

No patch ground: the wordmark is stitched straight onto the fabric in a thread
close enough in value to the panel that it reads as texture rather than as a
label. What you see is the relief, not the colour.

Letterforms come from the same trace the patch is built from.
"""
import colorsys, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
GLYPHS = os.path.abspath(os.path.join(HERE, '..', '..', 'Patch', 'build', 'glyphs.json'))
G = json.load(open(GLYPHS))

CAP_SRC, BASELINE = 219.0, 254.0
TERRA = ['T', 'E1', 'R1', 'R2', 'A']
NEXUS = ['N', 'E2', 'X', 'U', 'S']
DX = 129.6 - G['x']['N']          # NEXUS indent, from the approved lockup
DY = 1.125 * CAP_SRC              # line advance

# ---- pack fabric, measured off the story frames ----------------------------
FABRIC_LIT = '#AA642F'
FABRIC_MID = '#662B09'
FABRIC_SHADOW = '#441801'

# ---- thread options, ranked by how quietly they sit on that fabric ---------
THREADS = {
    'deep-red':      ('Terra Nexus Deep Red', '#6A1B32', 1.06, 2.51),
    'warm-charcoal': ('Warm Charcoal',        '#53494B', 1.26, 1.88),
    'olive':         ('Olive',                '#425316', 1.29, 1.84),
    'slate-purple':  ('Slate Purple',         '#49475B', 1.22, 1.95),
    'ink':           ('Terra Nexus Ink',      '#061927', 1.63, 3.88),
    'sand':          ('Terra Nexus Sand',     '#E8D77E', 7.54, 3.17),
}
PRIMARY = 'deep-red'

# ---- geometry, millimetres -------------------------------------------------
WORD_W = 85.0                     # finished width of the stacked wordmark
NEXUS_RIGHT = DX + G['x']['S'] + 154.0    # S ends at 1959 in the source
BBOX = (0.0, 35.0, max(868.0, NEXUS_RIGHT), 256.0 + DY)   # letters only, no star
BW = BBOX[2] - BBOX[0]
BH = BBOX[3] - BBOX[1]
K = WORD_W / BW                   # mm per source unit
CAP_MM = CAP_SRC * K
WORD_H = BH * K
STEM_MM = 0.192 * CAP_MM
BAR_MM = 0.164 * CAP_MM

NUM = re.compile(r'[MLQZ]|-?\d+(?:\.\d+)?')


def bake(d, k, tx, ty):
    out, i = [], 0
    for t in NUM.findall(d):
        if t in 'MLQZ':
            out.append(t); i = 0; continue
        v = float(t) * k + (tx if i % 2 == 0 else ty)
        s = f'{v:.4f}'.rstrip('0').rstrip('.')
        out.append(' ' + (s if s else '0')); i += 1
    return ''.join(out)


def glyph(name, k, ox, oy, dx=0.0, dy=0.0):
    tx = ox + (G['x'][name] + dx - BBOX[0]) * k
    ty = oy + (dy - BBOX[1]) * k
    return f'<path d="{bake(G["glyphs"][name], k, tx, ty)}"/>'


def wordmark(k, ox, oy):
    return ('\n        '.join(glyph(n, k, ox, oy) for n in TERRA) + '\n        ' +
            '\n        '.join(glyph(n, k, ox, oy, DX, DY) for n in NEXUS))


def _rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(r):
    return '#' + ''.join(f'{max(0, min(255, round(c * 255))):02X}' for c in r)


def shade(colour, lmul=1.0, ladd=0.0, smul=1.0):
    h, l, s = colorsys.rgb_to_hls(*_rgb(colour))
    l = max(0.0, min(1.0, l * lmul + ladd))
    return _hex(colorsys.hls_to_rgb(h, l, max(0.0, min(1.0, s * smul))))


# ---- production artwork ----------------------------------------------------
def build_flat():
    pad = 0.0
    W, H = WORD_W + 2 * pad, WORD_H + 2 * pad
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.2f}mm" height="{H:.2f}mm">
  <title>Terra Nexus direct stitch - production artwork</title>
  <desc>Block wordmark for direct embroidery on the pack panel. 1 user unit = 1 mm.
        Finished width {WORD_W} mm, cap height {CAP_MM:.2f} mm, stem {STEM_MM:.2f} mm.
        Letters only - no star, no ground.</desc>
  <g id="wordmark" fill="#000000" fill-rule="evenodd">
        {wordmark(K, pad, pad)}
  </g>
</svg>
'''
    open(os.path.join(OUT, 'stitch-flat.svg'), 'w').write(svg)


# ---- raised stitch on fabric ----------------------------------------------
def defs(v, thread, puff=True):
    hi = shade(thread, ladd=0.055, smul=0.97)
    lo = shade(thread, lmul=0.58)
    mid = thread
    f_hi = shade(FABRIC_LIT, ladd=0.02)
    f_lo = shade(FABRIC_MID, lmul=0.72)
    surf, blur = (5.2, 0.42) if puff else (3.0, 0.26)
    return f'''
  <defs>
    <linearGradient id="fab-{v}" x1="0.05" y1="0" x2="0.95" y2="1">
      <stop offset="0"    stop-color="{f_hi}"/>
      <stop offset="0.30" stop-color="{FABRIC_LIT}"/>
      <stop offset="0.66" stop-color="{FABRIC_MID}"/>
      <stop offset="1"    stop-color="{FABRIC_SHADOW}"/>
    </linearGradient>
    <pattern id="weave-{v}" width="0.7" height="0.7" patternUnits="userSpaceOnUse"
             patternTransform="rotate(38)">
      <rect width="0.7" height="0.35" fill="#000000" opacity="0.05"/>
      <rect y="0.35" width="0.35" height="0.35" fill="#FFFFFF" opacity="0.035"/>
    </pattern>
    <filter id="fabtex-{v}" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="4" seed="6" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0" result="g"/>
      <feComponentTransfer in="g" result="grain">
        <feFuncA type="linear" slope="0.16"/>
      </feComponentTransfer>
      <feComposite in="grain" in2="SourceAlpha" operator="in" result="gc"/>
      <feBlend in="SourceGraphic" in2="gc" mode="soft-light"/>
    </filter>

    <linearGradient id="rib-{v}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="{lo}"/>
      <stop offset="0.32" stop-color="{hi}"/>
      <stop offset="0.58" stop-color="{mid}"/>
      <stop offset="1"    stop-color="{lo}"/>
    </linearGradient>
    <pattern id="satin-{v}" width="1" height="0.52" patternUnits="userSpaceOnUse">
      <rect width="1" height="0.52" fill="url(#rib-{v})"/>
    </pattern>

    <!-- foam-backed satin: the letters stand off the panel, so the read is the
         relief and the shadow it throws, not the colour -->
    <filter id="puff-{v}" color-interpolation-filters="sRGB"
            x="-25%" y="-25%" width="150%" height="160%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="{blur}" result="b"/>
      <feSpecularLighting in="b" surfaceScale="{surf}" specularConstant="0.46"
                          specularExponent="14" lighting-color="#FFF6E8" result="sp">
        <feDistantLight azimuth="228" elevation="42"/>
      </feSpecularLighting>
      <feComposite in="sp" in2="SourceAlpha" operator="in" result="spc"/>
      <feComposite in="SourceGraphic" in2="spc" operator="arithmetic"
                   k1="0" k2="1" k3="0.48" k4="0" result="lit"/>
      <feDropShadow in="lit" dx="0.42" dy="0.62" stdDeviation="0.34"
                    flood-color="#1A0A02" flood-opacity="0.62"/>
    </filter>

    <!-- needle penetrations pull the fabric in tight around each column -->
    <filter id="pucker-{v}" color-interpolation-filters="sRGB"
            x="-30%" y="-30%" width="160%" height="160%">
      <feMorphology in="SourceAlpha" operator="dilate" radius="0.5" result="d"/>
      <feGaussianBlur in="d" stdDeviation="0.75" result="db"/>
      <feComposite in="db" in2="SourceAlpha" operator="out" result="ring"/>
      <feFlood flood-color="#2A1206" flood-opacity="0.5" result="c"/>
      <feComposite in="c" in2="ring" operator="in"/>
    </filter>
  </defs>'''


def stitch_group(v, x, y, k=None):
    k = k or K
    return f'''
    <g filter="url(#pucker-{v})" fill="#000">{wordmark(k, x, y)}</g>
    <g id="stitch" fill="url(#satin-{v})" fill-rule="evenodd" filter="url(#puff-{v})">
        {wordmark(k, x, y)}
    </g>'''


def build_panel(key, puff=True):
    name, thread, c_mid, c_lit = THREADS[key]
    v = key
    PW, PH = 150.0, 108.0
    x = (PW - WORD_W) / 2
    y = (PH - WORD_H) / 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}mm" height="{PH}mm">
  <title>Terra Nexus direct stitch - {name} on pack fabric</title>
  <desc>Raised block wordmark stitched straight onto the panel. Thread {thread}.
        Contrast against the fabric mid-tone {c_mid}:1, against sunlit fabric {c_lit}:1.</desc>
  {defs(v, thread, puff)}
  <g filter="url(#fabtex-{v})">
    <rect width="{PW}" height="{PH}" fill="url(#fab-{v})"/>
    <rect width="{PW}" height="{PH}" fill="url(#weave-{v})"/>
  </g>
  {stitch_group(v, x, y)}
</svg>
'''
    open(os.path.join(OUT, f'stitch-{key}.svg'), 'w').write(svg)


def build_alpha(key, puff=True):
    """The stitching alone on transparent, for compositing onto a real pack."""
    name, thread, _, _ = THREADS[key]
    v = key + '-a'
    pad = 10.0
    W, H = WORD_W + 2 * pad, WORD_H + 2 * pad
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}" width="{W:.2f}mm" height="{H:.2f}mm">
  <title>Terra Nexus direct stitch - {name} - transparent ground</title>
  <desc>Stitching only, for compositing onto photography of the pack.</desc>
  {defs(v, thread, puff)}
  {stitch_group(v, pad, pad)}
</svg>
'''
    open(os.path.join(OUT, f'stitch-{key}-alpha.svg'), 'w').write(svg)


if __name__ == '__main__':
    build_flat()
    for k in THREADS:
        build_panel(k)
        build_alpha(k)
    print(f'wordmark {WORD_W} x {WORD_H:.1f} mm | cap {CAP_MM:.2f} | stem {STEM_MM:.2f} '
          f'| bar {BAR_MM:.2f} mm')
    print('wrote stitch-flat.svg,', len(THREADS), 'fabric panels and', len(THREADS), 'alpha plates')
