"""Dimensioned technical drawing for the Terra Nexus backpack patch."""
import os
import build_patch as B

OUT = B.OUT
INK, PAPER, RULE = '#061927', '#F4F2EC', '#7C8493'
FONT = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
MONO = "'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"

W, H = 340.0, 234.0
SC = 2.0
OX, OY = 52.0, 50.0
COL2 = 196.0


def sx(v): return OX + v * SC
def sy(v): return OY + v * SC


def txt(x, y, s, size=3.2, fill=INK, anchor='start', weight='400',
        family=FONT, spacing=0, opacity=1):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" opacity="{opacity}">{s}</text>')


def dim_h(x1, x2, y, label, tick=2.0):
    return f'''<g stroke="{RULE}" stroke-width="0.22" fill="none">
    <line x1="{x1:.2f}" y1="{y - tick:.2f}" x2="{x1:.2f}" y2="{y + tick:.2f}"/>
    <line x1="{x2:.2f}" y1="{y - tick:.2f}" x2="{x2:.2f}" y2="{y + tick:.2f}"/>
    <line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}"/>
  </g>{txt((x1 + x2) / 2, y - 1.6, label, 3.0, INK, 'middle', '500', MONO)}'''


def dim_v(y1, y2, x, label, tick=2.0):
    return f'''<g stroke="{RULE}" stroke-width="0.22" fill="none">
    <line x1="{x - tick:.2f}" y1="{y1:.2f}" x2="{x + tick:.2f}" y2="{y1:.2f}"/>
    <line x1="{x - tick:.2f}" y1="{y2:.2f}" x2="{x + tick:.2f}" y2="{y2:.2f}"/>
    <line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}"/>
  </g>{txt(x - 2.4, (y1 + y2) / 2 + 1.1, label, 3.0, INK, 'end', '500', MONO)}'''


def callout(n, x, y, dark=True):
    fg, bg = (INK, '#FFFFFF') if dark else ('#FFFFFF', INK)
    return (f'<g><circle cx="{x:.2f}" cy="{y:.2f}" r="2.6" fill="{bg}" stroke="{fg}" '
            f'stroke-width="0.3" stroke-opacity="0.4"/>'
            f'{txt(x, y + 1.15, str(n), 3.1, fg, "middle", "700", MONO)}</g>')


def block(x, y, title, rows, w=118, keyw=32):
    out = [txt(x, y, title, 3.3, INK, 'start', '700', FONT, 0.6),
           f'<line x1="{x}" y1="{y + 1.9}" x2="{x + w}" y2="{y + 1.9}" '
           f'stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>']
    yy = y + 7.2
    for k, v in rows:
        out.append(txt(x, yy, k, 2.85, INK, 'start', '600', FONT, 0, 0.9))
        for i, line in enumerate(v):
            out.append(txt(x + keyw, yy + i * 4.1, line, 2.85, INK, 'start', '400', FONT, 0, 0.78))
        yy += max(1, len(v)) * 4.1 + 1.7
    return '\n  '.join(out), yy


def chip(x, y, colour, name, hexv, rgb, use):
    return f'''<g>
    <rect x="{x}" y="{y}" width="12" height="12" rx="1.3" fill="{colour}" stroke="{INK}" stroke-opacity="0.3" stroke-width="0.3"/>
    {txt(x + 15.5, y + 4.2, name, 3.2, INK, 'start', '600')}
    {txt(x + 15.5, y + 8.5, hexv + '   ' + rgb, 2.8, INK, 'start', '400', MONO, 0, 0.72)}
    {txt(x + 15.5, y + 12.3, use, 2.8, INK, 'start', '400', FONT, 0, 0.72)}
  </g>'''


def build():
    flat = open(os.path.join(OUT, 'patch-flat.svg')).read()
    inner = flat.split('</desc>', 1)[1].rsplit('</svg>', 1)[0]

    px1, px2 = sx(0), sx(B.PW)
    py1, py2 = sy(0), sy(B.PH)
    ax1, ax2 = sx(B.ARTX), sx(B.ARTX + B.ARTW)

    dims = f'''
  {dim_h(ax1, ax2, py2 + 9, f'{B.ARTW:.0f} artwork')}
  {dim_h(px1, px2, py2 + 19, f'{B.PW:.0f} mm / 2.48 in')}
  {dim_v(py1, py2, px1 - 10, f'{B.PH:.0f} / 1.42 in')}'''

    marks = '\n  '.join([
        callout(1, sx(B.PW * 0.5), sy(B.MERROW / 2), dark=False),
        callout(2, sx(B.PW) - 4.2, sy(0) + 4.2, dark=False),
        callout(3, sx(B.ARTX - 3.4), sy(B.ARTY + 5.0), dark=False),
        callout(4, sx(B.ARTX + 48.6), sy(B.ARTY + 20.0), dark=False),
        callout(5, sx(B.ARTX / 2), sy(B.PH * 0.5), dark=False),
    ])

    legend, _ = block(52, 152, 'CALLOUTS', [
        ('1', [f'Merrowed overlock edge, {B.MERROW} mm wide, navy']),
        ('2', [f'Corner radius {B.RAD:.0f} mm']),
        ('3', [f'Cap height {B.CAPMM:.2f} mm']),
        ('4', [f'Star knocked out of the wordmark, {B.KNOCK} mm gap']),
        ('5', [f'Clear space {B.ARTX:.1f} mm to the finished edge']),
    ], w=126, keyw=8)

    art, _ = block(52, 192, 'ARTWORK', [
        ('Lockup', ['Approved stacked lockup. NEXUS is indented 0.592 and',
                    'dropped 1.125 cap heights from TERRA.']),
        ('Never', ['add a mountain or any graphic above TERRA; drop the',
                   'star; re-set the type; change the letter spacing.']),
    ], w=126, keyw=32)

    chips = '\n  '.join([
        chip(COL2, 50, B.NAVY, 'Terra Nexus Navy', B.NAVY, 'R19 G31 B72', 'ground + merrowed edge'),
        chip(COL2, 69, B.BONE, 'White', B.BONE, 'R255 G255 B255', 'wordmark'),
        chip(COL2, 88, B.SAND, 'Terra Nexus Sand', B.SAND, 'R232 G215 B126', 'star'),
    ])

    cons, _ = block(COL2, 122, 'CONSTRUCTION', [
        ('Type', ['Embroidered patch, 100% stitch coverage']),
        ('Backing', ['Navy twill; iron-on adhesive plus sew-through']),
        ('Edge', [f'Merrowed overlock, {B.MERROW} mm, navy']),
        ('Stitching', ['Wordmark and star: satin columns',
                       'Ground: tatami fill at 45 degrees']),
        ('Density', ['0.40 mm satin pitch, 0.20 mm underlay']),
        ('Tolerance', ['+/- 1.0 mm on the finished size']),
    ])

    limits, _ = block(COL2, 178, 'STITCH LIMITS AT THIS SIZE', [
        ('Letter stem', [f'{0.192 * B.CAPMM:.2f} mm - clears the 1.2 mm satin minimum']),
        ('Letter bar', [f'{0.164 * B.CAPMM:.2f} mm - clears the minimum']),
        ('Star ray', [f'{0.0594 * B.CAPMM:.2f} mm - below the 0.9 mm minimum. Digitise as',
                      'tapered satin with a 0.9 mm floor and accept slight',
                      'tip rounding, or run the patch woven instead, which',
                      'holds the star exactly as drawn.']),
    ])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">
  <title>Terra Nexus backpack patch - specification sheet</title>
  <rect width="{W}" height="{H}" fill="{PAPER}"/>
  <line x1="20" y1="30" x2="{W - 20}" y2="30" stroke="{INK}" stroke-width="0.5"/>
  {txt(20, 22, 'TERRA NEXUS', 8.4, INK, 'start', '700', FONT, 2.2)}
  {txt(20, 27.5, 'EMBROIDERED BACKPACK PATCH', 3.4, INK, 'start', '500', FONT, 1.6, 0.75)}
  {txt(W - 20, 22, 'REV A', 4.2, INK, 'end', '600', MONO)}
  {txt(W - 20, 27.5, 'all dimensions in millimetres', 2.8, INK, 'end', '400', FONT, 0, 0.65)}

  <g transform="translate({OX},{OY}) scale({SC})">{inner}</g>
  {dims}
  {marks}
  {legend}
  {art}

  {txt(COL2, 42, 'THREAD COLOURS', 3.3, INK, 'start', '700', FONT, 0.6)}
  <line x1="{COL2}" y1="43.9" x2="{COL2 + 118}" y2="43.9" stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>
  {chips}
  {txt(COL2, 108, 'Match to these RGB values from the mill thread card and supply', 2.75, INK, 'start', '400', FONT, 0, 0.72)}
  {txt(COL2, 112, 'a physical strike-off for approval before bulk production.', 2.75, INK, 'start', '400', FONT, 0, 0.72)}
  {cons}
  {limits}

  <line x1="20" y1="223" x2="{W - 20}" y2="223" stroke="{INK}" stroke-opacity="0.25" stroke-width="0.3"/>
  {txt(20, 228.5, 'Production artwork: Output Drafts/Patch/patch-flat.svg', 2.7, INK, 'start', '400', MONO, 0, 0.6)}
  {txt(W - 20, 228.5, 'Navy shown. Deep Red #6A1B32 and Ink #061927 are identical but for the ground - see patch-colourways.svg.', 2.7, INK, 'end', '400', FONT, 0, 0.6)}
</svg>
'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'patch-spec-sheet.svg'), 'w').write(build())
    print('wrote patch-spec-sheet.svg')
