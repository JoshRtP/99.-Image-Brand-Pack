"""Dimensioned technical sheet for the Terra Nexus wind shell."""
import math, os, re
import build_jacket as J

OUT = J.OUT
INK, PAPER, RULE = '#061927', '#F4F2EC', '#7C8493'
FONT = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
MONO = "'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"

W, H = 396.0, 250.0
COL2 = 258.0
FLAT_K = 0.086                      # garment mm -> sheet mm
FX, FY = 20.0, 50.0                 # front flat origin on the sheet
BX = 136.0                          # back flat origin
CROP = (116.0, 62.0)                # trims the flat's own margin
ORG = (710.0, 230.0)                # the flat's internal origin


def txt(x, y, s, size=3.0, fill=INK, anchor='start', weight='400', family=FONT,
        spacing=0, opacity=1):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" opacity="{opacity}">{s}</text>')


def block(x, y, title, rows, w=118, keyw=34, lead=3.9, size=2.7):
    out = [txt(x, y, title, 3.2, INK, 'start', '700', FONT, 0.6),
           f'<line x1="{x}" y1="{y + 1.8}" x2="{x + w}" y2="{y + 1.8}" '
           f'stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>']
    yy = y + 6.8
    for k, v in rows:
        out.append(txt(x, yy, k, size, INK, 'start', '600', FONT, 0, 0.9))
        for i, line in enumerate(v):
            out.append(txt(x + keyw, yy + i * lead, line, size, INK, 'start', '400',
                           MONO if line[:1].isdigit() else FONT, 0, 0.78))
        yy += max(1, len(v)) * lead + 1.5
    return '\n  '.join(out), yy


def sheet_pt(origin_x, bx, by):
    return (origin_x + FLAT_K * (ORG[0] + bx - CROP[0]),
            FY + FLAT_K * (ORG[1] + by - CROP[1]))


def callout(n, p, dark=False):
    fg, bg = ('#FFFFFF', INK) if dark else (INK, '#FFFFFF')
    return (f'<g><circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="2.5" fill="{bg}" stroke="{fg}" '
            f'stroke-width="0.3" stroke-opacity="0.45"/>'
            f'{txt(p[0], p[1] + 1.1, str(n), 3.0, fg, "middle", "700", MONO)}</g>')


def inner(path):
    s = open(path).read()
    s = re.sub(r'^.*?<svg\b[^>]*>', '', s, flags=re.S)
    return s.rsplit('</svg>', 1)[0]


def chip(x, y, colour, name, hexv, note):
    return f'''<g>
    <rect x="{x}" y="{y}" width="11" height="11" rx="1.2" fill="{colour}"
          stroke="{INK}" stroke-opacity="0.3" stroke-width="0.3"/>
    {txt(x + 14.5, y + 4.0, name, 3.0, INK, 'start', '600')}
    {txt(x + 14.5, y + 8.2, hexv + '   ' + note, 2.6, INK, 'start', '400', MONO, 0, 0.7)}
  </g>'''


def build():
    front = inner(os.path.join(OUT, J.flat_name('front')))
    back = inner(os.path.join(OUT, J.flat_name('back')))
    place = (f'translate({{x}},{FY}) scale({FLAT_K}) translate({-CROP[0]},{-CROP[1]})')

    marks = '\n  '.join([
        callout(1, sheet_pt(FX, 0, -96)),
        callout(2, sheet_pt(FX, 172, 148)),
        callout(3, sheet_pt(FX, -16, 250)),
        callout(4, sheet_pt(FX, 150, 382)),
        callout(5, sheet_pt(FX, 552, 546)),
        callout(6, sheet_pt(FX, 62, 646)),
        callout(7, sheet_pt(FX, 386, 118), dark=True),
        callout(8, sheet_pt(BX, 0, 262)),
        callout(9, sheet_pt(BX, 0, 24)),
    ])

    legend, y1 = block(FX, 128, 'CALLOUTS', [
        ('1', ['Attached hood, three panel, elastic-bound face opening, rear cord']),
        ('2', ['Raglan sleeve, single needle topstitch']),
        ('3', ['Centre front zip, full length, chin guard and zip garage']),
        ('4', ['Zipped hand pockets, welted, mesh bag']),
        ('5', ['Elasticated cuff, 20 mm knitted']),
        ('6', ['Hem drawcord with moulded toggles at the front']),
        ('7', ['Sleeve mark, wearer left upper arm']),
        ('8', ['Back yoke seam']),
        ('9', ['Woven main label, centre back neck']),
    ], w=222, keyw=8, lead=3.9, size=2.75)

    m = block(FX, y1 + 6, 'MEASUREMENTS - SIZE M, AS DRAWN', [
        ('Centre back length', [f'{J.HEM_B / 10:.1f} cm']),
        ('Chest, laid flat', [f'{268.0 * 2 / 10:.1f} cm']),
        ('Hem, laid flat', [f'{272.0 * 2 / 10:.1f} cm']),
        ('Sleeve, CB neck to cuff', [
            f'{math.hypot((J.CUFF_O[0] + J.CUFF_I[0]) / 2, (J.CUFF_O[1] + J.CUFF_I[1]) / 2) / 10:.1f} cm']),
        ('Cuff opening, relaxed', [
            f'{math.hypot(J.CUFF_O[0] - J.CUFF_I[0], J.CUFF_O[1] - J.CUFF_I[1]) / 10:.1f} cm']),
        ('Front neck drop', [f'{J.NECK_F / 10:.1f} cm']),
        ('Underarm drop from HPS', [f'{J.UNDERARM / 10:.1f} cm']),
        ('Hood height, worn up', ['36.0 cm   specified']),
    ], w=112, keyw=52, lead=3.9, size=2.75)[0]

    grade = [('XS', 49.6, 64.4), ('S', 51.6, 66.4), ('M', 53.6, 68.4),
             ('L', 55.6, 70.4), ('XL', 58.1, 72.4), ('XXL', 60.6, 74.4)]
    sr = [txt(FX + 124, y1 + 6, 'SIZE RUN', 3.2, INK, 'start', '700', FONT, 0.6),
          f'<line x1="{FX + 124}" y1="{y1 + 7.8}" x2="{FX + 236}" y2="{y1 + 7.8}" '
          f'stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>',
          txt(FX + 124, y1 + 12.8, 'SIZE', 2.5, INK, 'start', '700', FONT, 0.12, 0.6),
          txt(FX + 186, y1 + 12.8, 'CHEST', 2.5, INK, 'end', '700', FONT, 0.12, 0.6),
          txt(FX + 226, y1 + 12.8, 'CB LENGTH', 2.5, INK, 'end', '700', FONT, 0.12, 0.6)]
    for i, (sz, ch, ln) in enumerate(grade):
        yy = y1 + 18.4 + i * 4.6
        bold = '700' if sz == 'M' else '400'
        op = 1.0 if sz == 'M' else 0.8
        sr.append(txt(FX + 124, yy, sz, 2.75, INK, 'start', bold, MONO, 0, op))
        sr.append(txt(FX + 186, yy, f'{ch:.1f}', 2.75, INK, 'end', bold, MONO, 0, op))
        sr.append(txt(FX + 226, yy, f'{ln:.1f}', 2.75, INK, 'end', bold, MONO, 0, op))
    sr.append(txt(FX + 124, y1 + 18.4 + len(grade) * 4.6 + 3.5,
                  'Grade: chest +2.0 to L then +2.5, length +2.0, sleeve +1.5.',
                  2.5, INK, 'start', '400', FONT, 0, 0.7))
    size_run = '\n  '.join(sr)

    chips = '\n  '.join([
        chip(COL2, 44, J.COLOURWAYS['glacier'][1], 'Glacier Blue', '#5A90BE', 'primary'),
        chip(COL2, 60, J.COLOURWAYS['navy'][1], 'Terra Nexus Navy', '#131F48', 'alternate'),
        chip(COL2, 76, J.COLOURWAYS['red'][1], 'Terra Nexus Deep Red', '#6A1B32', 'alternate'),
    ])

    fabric, y2 = block(COL2, 100, 'FABRIC', [
        ('Shell', ['40D ripstop nylon, plain weave']),
        ('Weight', ['68 g/m2']),
        ('Finish', ['PU coating, C0 DWR']),
        ('Water column', ['5,000 mm']),
        ('Construction', ['Single layer, unlined']),
        ('Garment weight', ['285 g, size M']),
    ], w=118, keyw=32)

    trims, y3 = block(COL2, y2 + 5, 'TRIMS', [
        ('Front zip', ['YKK #5 reverse coil, auto-lock']),
        ('Pocket zips', ['YKK #3 reverse coil']),
        ('Pulls', ['Moulded, Terra Nexus Red #E63D2F']),
        ('Cord', ['3 mm flat black, red toggles']),
        ('Cuff elastic', ['20 mm knitted']),
        ('Labels', ['Woven main at CB neck,', 'care label at left side seam']),
    ], w=118, keyw=32)

    brand, _ = block(COL2, y3 + 5, 'BRANDING', [
        ('Sleeve', ['Heat transfer, stacked lockup', '84 mm wide, white with sand star']),
        ('Not a patch', ['Sewn patches are bags only', 'in this package - see', 'Branding/Patch']),
    ], w=118, keyw=32)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">
  <title>Terra Nexus wind shell - specification sheet</title>
  <rect width="{W}" height="{H}" fill="{PAPER}"/>
  <line x1="20" y1="30" x2="{W - 20}" y2="30" stroke="{INK}" stroke-width="0.5"/>
  {txt(20, 22, 'TERRA NEXUS', 8.0, INK, 'start', '700', FONT, 2.1)}
  {txt(20, 27.5, 'WIND SHELL - HOODED, RAGLAN', 3.2, INK, 'start', '500', FONT, 1.5, 0.75)}
  {txt(W - 20, 22, 'REV A', 4.0, INK, 'end', '600', MONO)}
  {txt(W - 20, 27.5, 'centimetres unless noted', 2.7, INK, 'end', '400', FONT, 0, 0.65)}

  <g transform="{place.format(x=FX)}">{front}</g>
  <g transform="{place.format(x=BX)}">{back}</g>
  {txt(FX + 4, 46, 'FRONT', 2.9, INK, 'start', '700', FONT, 0.22, 0.6)}
  {txt(BX + 4, 46, 'BACK', 2.9, INK, 'start', '700', FONT, 0.22, 0.6)}
  {marks}
  {legend}
  {m}
  {size_run}

  {txt(COL2, 38, 'COLOURWAYS', 3.2, INK, 'start', '700', FONT, 0.6)}
  <line x1="{COL2}" y1="39.8" x2="{COL2 + 118}" y2="39.8" stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>
  {chips}
  {txt(COL2, 94, 'One garment, three grounds. Sleeve mark stays white with a sand star.', 2.5, INK, 'start', '400', FONT, 0, 0.7)}
  {fabric}
  {trims}
  {brand}

  <line x1="20" y1="{H - 14}" x2="{W - 20}" y2="{H - 14}" stroke="{INK}" stroke-opacity="0.25" stroke-width="0.3"/>
  {txt(20, H - 8.5, 'Production artwork: Branding/Jacket/jacket-flat-front.svg', 2.6, INK, 'start', '400', MONO, 0, 0.6)}
  {txt(W - 20, H - 8.5, 'Care: wash 30, no softener, tumble low to revive the DWR, do not iron the print.', 2.6, INK, 'end', '400', FONT, 0, 0.6)}
</svg>
'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'jacket-spec-sheet.svg'), 'w').write(build())
    print('wrote jacket-spec-sheet.svg')
