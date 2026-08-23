"""Build the Terra Nexus embroidered backpack patch from the traced glyph set.

Emits into Branding/Patch/:
  lockup-stacked.svg       approved stacked lockup, normalised to cap height 100
  patch-flat*.svg          production artwork, 1 user unit = 1 mm
  patch-embroidered*.svg   rendering treatment for photo / reference use

Three colourways share one geometry; every tone in a render is derived from that
colourway's single ground colour. The worn variants are rendering treatments
only - production artwork is never worn.

Glyph coordinates are baked into millimetres so that stroke widths, patterns
and filter primitives all read in real-world units.
"""
import colorsys, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
G = json.load(open(os.path.join(HERE, 'glyphs.json')))

# ---------------------------------------------------------------- brand colours
NAVY = '#131F48'   # Terra Nexus navy - the approved ground
BONE = '#FFFFFF'   # wordmark
SAND = '#E8D77E'   # star
DUST = '#D9CDB4'   # trail dust, used only by the worn renders

# ------------------------------------------------------- source-space constants
# Trasnparent-StdLogo.png: cap height 219, cap top y=35, baseline y=254.
CAP   = 219.0
TERRA = ['T', 'E1', 'R1', 'R2', 'A']
NEXUS = ['N', 'E2', 'X', 'U', 'S']
DX    = 129.6 - G['x']['N']    # NEXUS indent, +0.592 cap  (measured off approved art)
DY    = 1.125 * CAP            # line advance, +1.125 cap
BBOX  = (0.0, 1.0, 1084.0, 256.0 + DY)      # x0 y0 x1 y1, source px
BW    = BBOX[2] - BBOX[0]
BH    = BBOX[3] - BBOX[1]

# ------------------------------------------------------------ patch geometry, mm
PW, PH = 63.0, 36.0    # finished size, 2.48in x 1.42in
RAD    = 4.0           # corner radius
MERROW = 2.5           # merrowed overlock edge width
ARTW   = 50.0          # artwork width - leaves an even 6.5mm margin all round
CLEAR  = (PW - ARTW) / 2 - MERROW
K      = ARTW / BW     # mm per source px
ARTH   = BH * K
ARTX   = (PW - ARTW) / 2
ARTY   = (PH - ARTH) / 2
CAPMM  = CAP * K
KNOCK  = 0.45          # colour-break gap around the star, mm

NUM = re.compile(r'-?\d+(?:\.\d+)?')


def bake(d, k, tx, ty):
    """Apply scale+translate to an absolute M/L/Q/Z path, emitting mm coords."""
    out, i = [], 0
    for token in re.findall(r'[MLQZ]|-?\d+(?:\.\d+)?', d):
        if token in 'MLQZ':
            out.append(token); i = 0
            continue
        v = float(token)
        v = v * k + (tx if i % 2 == 0 else ty)
        s = f'{v:.4f}'.rstrip('0').rstrip('.')
        out.append(' ' + (s if s else '0'))
        i += 1
    return ''.join(out)


def glyph(name, k, ox, oy, dx=0.0, dy=0.0):
    """One glyph, placed in the target (mm) space."""
    tx = ox + (G['x'][name] + dx - BBOX[0]) * k
    ty = oy + (dy - BBOX[1]) * k
    return f'<path d="{bake(G["glyphs"][name], k, tx, ty)}"/>'


def wordmark_paths(k, ox, oy):
    return ('\n        '.join(glyph(n, k, ox, oy) for n in TERRA) + '\n        ' +
            '\n        '.join(glyph(n, k, ox, oy, DX, DY) for n in NEXUS))


def star_path(k, ox, oy, name='STAR'):
    return glyph(name, k, ox, oy)



def flat_name(key):
    return 'patch-flat.svg' if key == PRIMARY else f'patch-flat-{key}.svg'


def emb_name(key, worn=False):
    stem = 'patch-embroidered' if key == PRIMARY else f'patch-embroidered-{key}'
    return f'{stem}-worn.svg' if worn else f'{stem}.svg'


# ------------------------------------------------------------------- colourways
COLOURWAYS = {
    'navy': ('Terra Nexus Navy',    '#131F48'),
    'red':  ('Terra Nexus Deep Red', '#6A1B32'),
    'ink':  ('Terra Nexus Ink',      '#061927'),
}
PRIMARY = 'navy'


def _rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _hex(rgb):
    return '#' + ''.join(f'{max(0, min(255, round(c * 255))):02X}' for c in rgb)


def shade(colour, lmul=1.0, ladd=0.0, smul=1.0):
    """Move a colour in HLS: scale lightness, then offset it, then scale saturation."""
    h, l, s = colorsys.rgb_to_hls(*_rgb(colour))
    l = max(0.0, min(1.0, l * lmul + ladd))
    s = max(0.0, min(1.0, s * smul))
    return _hex(colorsys.hls_to_rgb(h, l, s))


def mix(a, b, t):
    ra, rb = _rgb(a), _rgb(b)
    return _hex(tuple(x + (y - x) * t for x, y in zip(ra, rb)))


def palette(ground, worn=False):
    """Every tone the render needs, derived from the one ground colour."""
    p = {
        'ground':      ground,
        'bone':        BONE,
        'sand':        SAND,
        'twillDark':   shade(ground, lmul=0.50),
        'twillLight':  shade(ground, ladd=0.048),
        'merrowDark':  shade(ground, lmul=0.42),
        'merrowLight': shade(ground, ladd=0.100),
        'dashDark':    shade(ground, lmul=0.36),
        'dashLight':   shade(ground, ladd=0.160),
        'stitchDark':  shade(ground, lmul=0.26),
        'boneLow':     '#9DA2AD',
        'boneHigh':    '#FFFFFF',
        'sandLow':     shade(SAND, lmul=0.58, smul=0.9),
        'sandHigh':    shade(SAND, ladd=0.10, smul=0.85),
    }
    if worn:
        # sun and trail dust: everything lifts, dulls and warms a little
        p['ground']      = shade(mix(ground, DUST, 0.06), ladd=0.012, smul=0.92)
        p['bone']        = mix(BONE, DUST, 0.18)
        p['sand']        = shade(mix(SAND, DUST, 0.12), smul=0.88)
        p['twillDark']   = shade(p['ground'], lmul=0.60)
        p['twillLight']  = shade(p['ground'], ladd=0.040)
        p['merrowDark']  = shade(p['ground'], lmul=0.52)
        p['merrowLight'] = shade(p['ground'], ladd=0.090)
        p['dashDark']    = shade(p['ground'], lmul=0.46)
        p['dashLight']   = shade(p['ground'], ladd=0.140)
        p['stitchDark']  = shade(p['ground'], lmul=0.34)
        p['boneLow']     = mix('#9DA2AD', DUST, 0.22)
        p['boneHigh']    = mix(BONE, DUST, 0.10)
        p['sandLow']     = shade(mix(SAND, DUST, 0.18), lmul=0.62, smul=0.80)
        p['sandHigh']    = shade(mix(SAND, DUST, 0.08), ladd=0.08, smul=0.76)
    return p


# ------------------------------------------------------------------- 1. lockup
def build_lockup():
    k = 100.0 / CAP
    w, h = BW * k, BH * k
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.3f} {h:.3f}" width="{w:.3f}" height="{h:.3f}">
  <title>Terra Nexus stacked lockup</title>
  <desc>Approved stacked lockup vectorised from Trasnparent-StdLogo.png. Cap height = 100 units.
        NEXUS is indented 59.2 and dropped 112.5 from TERRA.</desc>
  <g id="wordmark" fill="{BONE}" fill-rule="evenodd">
        {wordmark_paths(k, 0, 0)}
  </g>
  <g id="star" fill="{SAND}" fill-rule="evenodd">{star_path(k, 0, 0)}</g>
</svg>
'''
    open(os.path.join(OUT, 'lockup-stacked.svg'), 'w').write(svg)


# --------------------------------------------------------------- 2. flat patch
def build_flat(key):
    name, ground = COLOURWAYS[key]
    i = MERROW / 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}mm" height="{PH}mm">
  <title>Terra Nexus backpack patch - flat production artwork - {name}</title>
  <desc>Finished size {PW} x {PH} mm. 1 user unit = 1 mm. Ground {ground} ({name}),
        wordmark {BONE}, star {SAND}. Cap height {CAPMM:.2f} mm.
        Star is knocked out of the wordmark by {KNOCK} mm.</desc>
  <rect id="patch-body" x="0" y="0" width="{PW}" height="{PH}" rx="{RAD}" fill="{ground}"/>
  <rect id="merrow-edge" x="{i}" y="{i}" width="{PW - MERROW}" height="{PH - MERROW}"
        rx="{RAD - i}" fill="none" stroke="{ground}" stroke-width="{MERROW}"/>
  <g id="wordmark" fill="{BONE}" fill-rule="evenodd">
        {wordmark_paths(K, ARTX, ARTY)}
  </g>
  <g id="star-knockout" fill="{ground}" stroke="{ground}" stroke-width="{2 * KNOCK}"
     stroke-linejoin="round">{star_path(K, ARTX, ARTY)}</g>
  <g id="star" fill="{SAND}" fill-rule="evenodd">{star_path(K, ARTX, ARTY)}</g>
</svg>
'''
    open(os.path.join(OUT, flat_name(key)), 'w').write(svg)


# --------------------------------------------------------- 3. embroidered patch
def defs(v, p, worn):
    """Every gradient, pattern and filter, keyed to this variant."""
    fuzz = ('''
      <feTurbulence type="fractalNoise" baseFrequency="1.7 1.1" numOctaves="2"
                    seed="23" result="fz"/>
      <feDisplacementMap in="SourceGraphic" in2="fz" scale="0.075"
                         xChannelSelector="R" yChannelSelector="G" result="src"/>''' if worn else '')
    src = 'src' if worn else 'SourceGraphic'
    alpha = 'srcA' if worn else 'SourceAlpha'
    alpha_def = ('<feColorMatrix in="src" type="matrix" result="srcA" '
                 'values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"/>') if worn else ''
    # worn stitching sits lower and catches less light
    surf, spec, expo = (2.2, 0.70, 15) if worn else (2.6, 0.8, 17)
    blur = 0.175 if worn else 0.16

    dust = f'''
    <filter id="dust-{v}" color-interpolation-filters="sRGB"
            x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="fractalNoise" baseFrequency="0.62 0.78" numOctaves="5" seed="31"/>
      <feColorMatrix type="matrix" values="
        0 0 0 0 {_rgb(DUST)[0]:.3f}
        0 0 0 0 {_rgb(DUST)[1]:.3f}
        0 0 0 0 {_rgb(DUST)[2]:.3f}
        0 0 0 0.90 -0.34"/>
    </filter>
    <filter id="grit-{v}" color-interpolation-filters="sRGB"
            x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="9"/>
      <feColorMatrix type="matrix" values="
        0 0 0 0 {_rgb(DUST)[0]:.3f}
        0 0 0 0 {_rgb(DUST)[1]:.3f}
        0 0 0 0 {_rgb(DUST)[2]:.3f}
        0 0 0 1.6 -1.12"/>
    </filter>
    <filter id="scuff-{v}" color-interpolation-filters="sRGB"
            x="-6%" y="-6%" width="112%" height="112%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85 1.15" numOctaves="3" seed="17" result="n"/>
      <feColorMatrix in="n" type="matrix" result="m" values="
        0 0 0 0 1  0 0 0 0 0.99  0 0 0 0 0.95  0 0 0 2.2 -1.32"/>
      <feComposite in="m" in2="SourceAlpha" operator="in"/>
    </filter>
    <linearGradient id="settle-{v}" x1="0" y1="0" x2="0.25" y2="1">
      <stop offset="0"    stop-color="{DUST}" stop-opacity="0"/>
      <stop offset="0.60" stop-color="{DUST}" stop-opacity="0.025"/>
      <stop offset="1"    stop-color="{DUST}" stop-opacity="0.13"/>
    </linearGradient>''' if worn else ''

    return f'''
  <defs>
    <linearGradient id="twillRib-{v}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="{p['twillDark']}"/>
      <stop offset="0.42" stop-color="{p['twillLight']}"/>
      <stop offset="1"    stop-color="{p['twillDark']}"/>
    </linearGradient>
    <pattern id="twill-{v}" width="1" height="0.30" patternUnits="userSpaceOnUse"
             patternTransform="rotate(45)">
      <rect width="1" height="0.30" fill="url(#twillRib-{v})"/>
    </pattern>

    <linearGradient id="ribBone-{v}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="{p['boneLow']}"/>
      <stop offset="0.34" stop-color="{p['boneHigh']}"/>
      <stop offset="0.58" stop-color="{mix(p['boneHigh'], p['boneLow'], 0.10)}"/>
      <stop offset="1"    stop-color="{p['boneLow']}"/>
    </linearGradient>
    <pattern id="satinBone-{v}" width="1" height="0.42" patternUnits="userSpaceOnUse">
      <rect width="1" height="0.42" fill="url(#ribBone-{v})"/>
    </pattern>

    <linearGradient id="ribSand-{v}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="{p['sandLow']}"/>
      <stop offset="0.34" stop-color="{p['sandHigh']}"/>
      <stop offset="0.58" stop-color="{p['sand']}"/>
      <stop offset="1"    stop-color="{p['sandLow']}"/>
    </linearGradient>
    <pattern id="satinSand-{v}" width="1" height="0.42" patternUnits="userSpaceOnUse"
             patternTransform="rotate(72)">
      <rect width="1" height="0.42" fill="url(#ribSand-{v})"/>
    </pattern>

    <linearGradient id="merrowRib-{v}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="{p['merrowDark']}"/>
      <stop offset="0.5" stop-color="{p['merrowLight']}"/>
      <stop offset="1"   stop-color="{p['merrowDark']}"/>
    </linearGradient>

    <filter id="relief-{v}" color-interpolation-filters="sRGB"
            x="-10%" y="-10%" width="120%" height="122%">{fuzz}
      {alpha_def}
      <feGaussianBlur in="{alpha}" stdDeviation="{blur}" result="blur"/>
      <feSpecularLighting in="blur" surfaceScale="{surf}" specularConstant="{spec}"
                          specularExponent="{expo}" lighting-color="#ffffff" result="spec">
        <feDistantLight azimuth="230" elevation="56"/>
      </feSpecularLighting>
      <feComposite in="spec" in2="{alpha}" operator="in" result="specClip"/>
      <feComposite in="{src}" in2="specClip" operator="arithmetic"
                   k1="0" k2="1" k3="0.85" k4="0" result="lit"/>
      <feDropShadow in="lit" dx="0.07" dy="0.13" stdDeviation="0.13"
                    flood-color="{p['stitchDark']}" flood-opacity="0.9"/>
    </filter>

    <filter id="thread-{v}" color-interpolation-filters="sRGB"
            x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9 0.4" numOctaves="2"
                    seed="11" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="{0.14 if worn else 0.10}"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>

    <filter id="groundTex-{v}" color-interpolation-filters="sRGB"
            x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="fractalNoise" baseFrequency="1.8" numOctaves="3" seed="4" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0" result="g"/>
      <feComponentTransfer in="g" result="grain">
        <feFuncA type="linear" slope="{0.12 if worn else 0.09}" intercept="0"/>
      </feComponentTransfer>
      <feComposite in="grain" in2="SourceAlpha" operator="in" result="grainClip"/>
      <feBlend in="SourceGraphic" in2="grainClip" mode="soft-light"/>
    </filter>

    <filter id="dropShadow-{v}" color-interpolation-filters="sRGB"
            x="-14%" y="-14%" width="128%" height="132%">
      <feDropShadow dx="0" dy="0.55" stdDeviation="0.6" flood-color="#02060F" flood-opacity="0.5"/>
    </filter>

    <radialGradient id="sheen-{v}" cx="0.32" cy="0.22" r="0.95">
      <stop offset="0"    stop-color="#ffffff" stop-opacity="{0.06 if worn else 0.10}"/>
      <stop offset="0.55" stop-color="#ffffff" stop-opacity="0.03"/>
      <stop offset="1"    stop-color="#000814" stop-opacity="0.15"/>
    </radialGradient>
    {dust}
    <clipPath id="bodyClip-{v}">
      <rect x="0" y="0" width="{PW}" height="{PH}" rx="{RAD}"/>
    </clipPath>
  </defs>'''


def merrow(v, p):
    i = MERROW / 2
    r = f'x="{i}" y="{i}" width="{PW - MERROW}" height="{PH - MERROW}" rx="{RAD - i}"'
    return f'''<g id="merrow-edge" filter="url(#thread-{v})">
      <rect {r} fill="none" stroke="url(#merrowRib-{v})" stroke-width="{MERROW}"/>
      <rect {r} fill="none" stroke="{p['dashDark']}" stroke-width="{MERROW}"
            stroke-dasharray="0.34 0.50" opacity="0.5"/>
      <rect {r} fill="none" stroke="{p['dashLight']}" stroke-width="{MERROW * 0.30}"
            stroke-dasharray="0.34 0.50" stroke-dashoffset="0.17" opacity="0.45"/>
    </g>'''


def build_embroidered(key, worn=False):
    name, ground = COLOURWAYS[key]
    v = key + ('-worn' if worn else '')
    p = palette(ground, worn)

    wear = f'''
    <g clip-path="url(#bodyClip-{v})">
      <rect x="0" y="0" width="{PW}" height="{PH}" filter="url(#dust-{v})" opacity="0.30"
            style="mix-blend-mode:soft-light"/>
      <rect x="0" y="0" width="{PW}" height="{PH}" filter="url(#dust-{v})" opacity="0.09"/>
      <rect x="0" y="0" width="{PW}" height="{PH}" filter="url(#grit-{v})" opacity="0.20"/>
      <rect x="0" y="0" width="{PW}" height="{PH}" fill="url(#settle-{v})"/>
    </g>''' if worn else ''

    scuff = f'''
    <g id="fibre-bloom" filter="url(#scuff-{v})" opacity="0.26"
       style="mix-blend-mode:screen" fill="#ffffff" fill-rule="evenodd">
        {wordmark_paths(K, ARTX, ARTY)}
        {star_path(K, ARTX, ARTY)}
    </g>''' if worn else ''

    title = f'{name}{" - worn" if worn else ""}'
    desc = ('Worn rendering: faded thread, trail dust in the stitch valleys and fibre '
            'bloom on the raised satin. Geometry is unchanged.' if worn else
            'Reference render: twill ground, satin-stitch wordmark and star, merrowed edge.')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 {PW + 4} {PH + 4}"
     width="{PW + 4}mm" height="{PH + 4}mm">
  <title>Terra Nexus backpack patch - embroidered render - {title}</title>
  <desc>{desc} Ground {ground} ({name}). Geometry identical to {flat_name(key)}.</desc>
  {defs(v, p, worn)}
  <g filter="url(#dropShadow-{v})">
    <g clip-path="url(#bodyClip-{v})">
      <g filter="url(#groundTex-{v})">
        <rect x="0" y="0" width="{PW}" height="{PH}" fill="{p['ground']}"/>
        <rect x="0" y="0" width="{PW}" height="{PH}" fill="url(#twill-{v})" opacity="0.9"/>
      </g>
    </g>
    {merrow(v, p)}
    <g id="wordmark" fill="url(#satinBone-{v})" fill-rule="evenodd" filter="url(#relief-{v})">
        {wordmark_paths(K, ARTX, ARTY)}
    </g>
    <g id="star-knockout" fill="{p['ground']}" stroke="{p['ground']}" stroke-width="{2 * KNOCK}"
       stroke-linejoin="round" opacity="0.97">{star_path(K, ARTX, ARTY)}</g>
    <g id="star" fill="url(#satinSand-{v})" fill-rule="evenodd" filter="url(#relief-{v})">
        {star_path(K, ARTX, ARTY)}
    </g>{scuff}{wear}
    <rect x="0" y="0" width="{PW}" height="{PH}" rx="{RAD}" fill="url(#sheen-{v})"
          style="mix-blend-mode:soft-light"/>
  </g>
</svg>
'''
    open(os.path.join(OUT, emb_name(key, worn)), 'w').write(svg)


if __name__ == '__main__':
    build_lockup()
    for key in COLOURWAYS:
        build_flat(key)
        build_embroidered(key, worn=False)
        build_embroidered(key, worn=True)
    print(f'patch {PW} x {PH} mm | art {ARTW:.2f} x {ARTH:.2f} mm | margin {ARTX:.2f} / {ARTY:.2f} mm')
    print(f'cap height {CAPMM:.3f} mm | stem {0.192*CAPMM:.2f} | bar {0.164*CAPMM:.2f} '
          f'| star ray {0.0594*CAPMM:.2f} | star body {0.543*CAPMM:.2f} mm')
    for key, (name, ground) in COLOURWAYS.items():
        print(f'  {key:5s} {ground}  {name}')
    print('wrote lockup-stacked.svg + 3 colourways x (flat, embroidered, worn)')
