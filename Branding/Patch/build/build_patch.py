"""Build the Terra Nexus embroidered backpack patch from the traced glyph set.

Emits into Branding/Patch/:
  lockup-stacked.svg      approved stacked lockup, normalised to cap height 100
  patch-flat.svg          production artwork, 1 user unit = 1 mm
  patch-embroidered.svg   rendering treatment for photo / reference use

Glyph coordinates are baked into millimetres so that stroke widths, patterns
and filter primitives all read in real-world units.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
G = json.load(open(os.path.join(HERE, 'glyphs.json')))

# ---------------------------------------------------------------- brand colours
NAVY = '#131F48'   # Terra Nexus navy - patch ground and merrowed edge
BONE = '#FFFFFF'   # wordmark
SAND = '#E8D77E'   # star

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
def build_flat():
    i = MERROW / 2
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {PH}" width="{PW}mm" height="{PH}mm">
  <title>Terra Nexus backpack patch - flat production artwork</title>
  <desc>Finished size {PW} x {PH} mm. 1 user unit = 1 mm. Ground {NAVY}, wordmark {BONE}, star {SAND}.
        Cap height {CAPMM:.2f} mm. Star is knocked out of the wordmark by {KNOCK} mm.</desc>
  <rect id="patch-body" x="0" y="0" width="{PW}" height="{PH}" rx="{RAD}" fill="{NAVY}"/>
  <rect id="merrow-edge" x="{i}" y="{i}" width="{PW - MERROW}" height="{PH - MERROW}"
        rx="{RAD - i}" fill="none" stroke="{NAVY}" stroke-width="{MERROW}"/>
  <g id="wordmark" fill="{BONE}" fill-rule="evenodd">
        {wordmark_paths(K, ARTX, ARTY)}
  </g>
  <g id="star-knockout" fill="{NAVY}" stroke="{NAVY}" stroke-width="{2 * KNOCK}"
     stroke-linejoin="round">{star_path(K, ARTX, ARTY)}</g>
  <g id="star" fill="{SAND}" fill-rule="evenodd">{star_path(K, ARTX, ARTY)}</g>
</svg>
'''
    open(os.path.join(OUT, 'patch-flat.svg'), 'w').write(svg)


# --------------------------------------------------------- 3. embroidered patch
DEFS = f'''
  <defs>
    <!-- polyester twill ground, fine 45 degree weave -->
    <linearGradient id="twillRib" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="#080C24"/>
      <stop offset="0.42" stop-color="#182548"/>
      <stop offset="1"    stop-color="#080C24"/>
    </linearGradient>
    <pattern id="twill" width="1" height="0.30" patternUnits="userSpaceOnUse"
             patternTransform="rotate(45)">
      <rect width="1" height="0.30" fill="url(#twillRib)"/>
    </pattern>

    <!-- satin columns: threads lie across the tile, 0.42mm pitch -->
    <linearGradient id="ribBone" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="#9DA2AD"/>
      <stop offset="0.34" stop-color="#FFFFFF"/>
      <stop offset="0.58" stop-color="#F6F7F9"/>
      <stop offset="1"    stop-color="#9DA2AD"/>
    </linearGradient>
    <pattern id="satinBone" width="1" height="0.42" patternUnits="userSpaceOnUse">
      <rect width="1" height="0.42" fill="url(#ribBone)"/>
    </pattern>

    <linearGradient id="ribSand" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"    stop-color="#93803A"/>
      <stop offset="0.34" stop-color="#F7ECB6"/>
      <stop offset="0.58" stop-color="#E8D77E"/>
      <stop offset="1"    stop-color="#93803A"/>
    </linearGradient>
    <pattern id="satinSand" width="1" height="0.42" patternUnits="userSpaceOnUse"
             patternTransform="rotate(72)">
      <rect width="1" height="0.42" fill="url(#ribSand)"/>
    </pattern>

    <linearGradient id="merrowRib" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0"   stop-color="#0A1030"/>
      <stop offset="0.5" stop-color="#243874"/>
      <stop offset="1"   stop-color="#0A1030"/>
    </linearGradient>

    <!-- raised thread relief plus the shadow the stitching casts on the twill -->
    <filter id="relief" color-interpolation-filters="sRGB" x="-10%" y="-10%" width="120%" height="122%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="0.16" result="blur"/>
      <feSpecularLighting in="blur" surfaceScale="2.6" specularConstant="0.8"
                          specularExponent="17" lighting-color="#ffffff" result="spec">
        <feDistantLight azimuth="230" elevation="56"/>
      </feSpecularLighting>
      <feComposite in="spec" in2="SourceAlpha" operator="in" result="specClip"/>
      <feComposite in="SourceGraphic" in2="specClip" operator="arithmetic"
                   k1="0" k2="1" k3="0.85" k4="0" result="lit"/>
      <feDropShadow in="lit" dx="0.07" dy="0.13" stdDeviation="0.13"
                    flood-color="#04091C" flood-opacity="0.9"/>
    </filter>

    <!-- nothing stitched is geometrically perfect -->
    <filter id="thread" color-interpolation-filters="sRGB" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.9 0.4" numOctaves="2"
                    seed="11" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="0.10"
                         xChannelSelector="R" yChannelSelector="G"/>
    </filter>

    <filter id="groundTex" color-interpolation-filters="sRGB" x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="fractalNoise" baseFrequency="1.8" numOctaves="3" seed="4" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0" result="g"/>
      <feComponentTransfer in="g" result="grain">
        <feFuncA type="linear" slope="0.09" intercept="0"/>
      </feComponentTransfer>
      <feComposite in="grain" in2="SourceAlpha" operator="in" result="grainClip"/>
      <feBlend in="SourceGraphic" in2="grainClip" mode="soft-light"/>
    </filter>

    <filter id="dropShadow" color-interpolation-filters="sRGB" x="-14%" y="-14%" width="128%" height="132%">
      <feDropShadow dx="0" dy="0.55" stdDeviation="0.6" flood-color="#02060F" flood-opacity="0.5"/>
    </filter>

    <radialGradient id="sheen" cx="0.32" cy="0.22" r="0.95">
      <stop offset="0"   stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="0.55" stop-color="#ffffff" stop-opacity="0.03"/>
      <stop offset="1"   stop-color="#000814" stop-opacity="0.15"/>
    </radialGradient>

    <clipPath id="bodyClip">
      <rect x="0" y="0" width="{PW}" height="{PH}" rx="{RAD}"/>
    </clipPath>
  </defs>'''


def merrow():
    i = MERROW / 2
    r = f'x="{i}" y="{i}" width="{PW - MERROW}" height="{PH - MERROW}" rx="{RAD - i}"'
    return f'''<g id="merrow-edge" filter="url(#thread)">
      <rect {r} fill="none" stroke="url(#merrowRib)" stroke-width="{MERROW}"/>
      <rect {r} fill="none" stroke="#080D26" stroke-width="{MERROW}"
            stroke-dasharray="0.34 0.50" opacity="0.5"/>
      <rect {r} fill="none" stroke="#31468A" stroke-width="{MERROW * 0.30}"
            stroke-dasharray="0.34 0.50" stroke-dashoffset="0.17" opacity="0.45"/>
    </g>'''


def build_embroidered():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 {PW + 4} {PH + 4}"
     width="{PW + 4}mm" height="{PH + 4}mm">
  <title>Terra Nexus backpack patch - embroidered render</title>
  <desc>Reference render of the approved patch: navy twill ground, satin-stitch wordmark
        and star, merrowed edge. Geometry is identical to patch-flat.svg.</desc>
  {DEFS}
  <g filter="url(#dropShadow)">
    <g clip-path="url(#bodyClip)">
      <g filter="url(#groundTex)">
        <rect x="0" y="0" width="{PW}" height="{PH}" fill="{NAVY}"/>
        <rect x="0" y="0" width="{PW}" height="{PH}" fill="url(#twill)" opacity="0.9"/>
      </g>
    </g>
    {merrow()}
    <g id="wordmark" fill="url(#satinBone)" fill-rule="evenodd" filter="url(#relief)">
        {wordmark_paths(K, ARTX, ARTY)}
    </g>
    <g id="star-knockout" fill="{NAVY}" stroke="{NAVY}" stroke-width="{2 * KNOCK}"
       stroke-linejoin="round" opacity="0.97">{star_path(K, ARTX, ARTY)}</g>
    <g id="star" fill="url(#satinSand)" fill-rule="evenodd" filter="url(#relief)">
        {star_path(K, ARTX, ARTY)}
    </g>
    <rect x="0" y="0" width="{PW}" height="{PH}" rx="{RAD}" fill="url(#sheen)"
          style="mix-blend-mode:soft-light"/>
  </g>
</svg>
'''
    open(os.path.join(OUT, 'patch-embroidered.svg'), 'w').write(svg)


if __name__ == '__main__':
    build_lockup(); build_flat(); build_embroidered()
    print(f'patch {PW} x {PH} mm | art {ARTW:.2f} x {ARTH:.2f} mm | margin {ARTX:.2f} / {ARTY:.2f} mm')
    print(f'cap height {CAPMM:.3f} mm | stem {0.192*CAPMM:.2f} | bar {0.164*CAPMM:.2f} '
          f'| star ray {0.0594*CAPMM:.2f} | star body {0.543*CAPMM:.2f} mm')
    print('wrote lockup-stacked.svg, patch-flat.svg, patch-embroidered.svg')
