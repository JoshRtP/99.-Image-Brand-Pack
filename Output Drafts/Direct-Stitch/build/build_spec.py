"""Specification sheet for the direct raised stitch."""
import os, re
import build_stitch as S

OUT = S.OUT
INK, PAPER, RULE = '#061927', '#F4F2EC', '#7C8493'
FONT = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
MONO = "'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"
W, H = 396.0, 236.0
MARGIN, COL2 = 20.0, 232.0
ART_K = 1.35
AX, AY = 28.0, 58.0


def txt(x, y, s, size=3.0, fill=INK, anchor='start', weight='400', family=FONT,
        spacing=0, opacity=1):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" opacity="{opacity}">{s}</text>')


def block(x, y, title, rows, w=144, keyw=40, lead=3.9, size=2.7):
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


def dim_h(x1, x2, y, label):
    return (f'<g stroke="{RULE}" stroke-width="0.22" fill="none">'
            f'<line x1="{x1:.2f}" y1="{y-2:.2f}" x2="{x1:.2f}" y2="{y+2:.2f}"/>'
            f'<line x1="{x2:.2f}" y1="{y-2:.2f}" x2="{x2:.2f}" y2="{y+2:.2f}"/>'
            f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}"/></g>'
            + txt((x1 + x2) / 2, y - 1.6, label, 3.0, INK, 'middle', '500', MONO))


def dim_v(y1, y2, x, label):
    return (f'<g stroke="{RULE}" stroke-width="0.22" fill="none">'
            f'<line x1="{x-2:.2f}" y1="{y1:.2f}" x2="{x+2:.2f}" y2="{y1:.2f}"/>'
            f'<line x1="{x-2:.2f}" y1="{y2:.2f}" x2="{x+2:.2f}" y2="{y2:.2f}"/>'
            f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}"/></g>'
            + txt(x - 2.4, (y1 + y2) / 2 + 1.1, label, 3.0, INK, 'end', '500', MONO))


def chip(x, y, colour, name, hexv, note, rec=False):
    return f'''<g>
    <rect x="{x}" y="{y}" width="10" height="10" rx="1.2" fill="{colour}"
          stroke="{INK}" stroke-opacity="0.3" stroke-width="0.3"/>
    {txt(x + 13, y + 4.0, name + (' — recommended' if rec else ''), 2.95, INK, 'start', '700' if rec else '600')}
    {txt(x + 13, y + 8.2, hexv + '   ' + note, 2.6, INK, 'start', '400', MONO, 0, 0.7)}
  </g>'''


def build():
    art = open(os.path.join(OUT, 'stitch-flat.svg')).read()
    art = re.sub(r'^.*?</desc>', '', art, flags=re.S).rsplit('</svg>', 1)[0]
    aw, ah = S.WORD_W * ART_K, S.WORD_H * ART_K

    threads = '\n  '.join(
        chip(COL2, 44 + i * 15, S.THREADS[k][1], S.THREADS[k][0], S.THREADS[k][1],
             f'{S.THREADS[k][2]:.2f}:1 shade  {S.THREADS[k][3]:.2f}:1 sun', k == S.PRIMARY)
        for i, k in enumerate(['deep-red', 'warm-charcoal', 'olive', 'slate-purple', 'ink']))

    cons, y2 = block(MARGIN, AY + ah + 26, 'CONSTRUCTION', [
        ('Method', ['3D foam satin - 2 mm foam laid under the columns,',
                    'stitched through and trimmed. This is what makes it raised.']),
        ('Columns', ['Satin, running across each stroke']),
        ('Underlay', ['Centre-run plus edge-walk, 0.25 mm inset']),
        ('Density', ['0.38 mm stitch pitch, 45 deg column angle on the diagonals']),
        ('Minimum', [f'Narrowest stroke {S.BAR_MM:.2f} mm - clears the 2.0 mm foam',
                     'minimum with margin']),
        ('Backing', ['Cut-away, 50 g, behind the panel before assembly']),
        ('Placement', ['Centred on the upper front panel, top of the wordmark',
                       '40 mm below the lid seam']),
    ], w=196, keyw=32)

    notes, ny = block(COL2, 138, 'ARRANGEMENT', [
        ('', ['TERRA directly over NEXUS, left edges aligned, both lines',
              'tracked to the same width. This is NOT the approved lockup,',
              'which indents NEXUS by 0.592 cap heights - squared off, the',
              'block is far easier to specify and to check.']),
    ], w=144, keyw=0)
    notes2, _ = block(COL2, ny + 5, 'WHY LETTERS ONLY', [
        ('', ['The compass star cannot be foamed. Its minor rays taper',
              'below 1 mm and foam needs 2 mm to hold an edge - it would',
              'come out as a blob. If the star has to appear, run it as',
              'flat satin beside the foamed letters, not through them.']),
    ], w=144, keyw=0)
    notes = notes + '\n  ' + notes2

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm">
  <title>Terra Nexus direct raised stitch - specification</title>
  <rect width="{W}" height="{H}" fill="{PAPER}"/>
  <line x1="{MARGIN}" y1="30" x2="{W - MARGIN}" y2="30" stroke="{INK}" stroke-width="0.5"/>
  {txt(MARGIN, 22, 'TERRA NEXUS', 8.0, INK, 'start', '700', FONT, 2.1)}
  {txt(MARGIN, 27.5, 'DIRECT RAISED STITCH - PACK PANEL', 3.2, INK, 'start', '500', FONT, 1.5, 0.75)}
  {txt(W - MARGIN, 22, 'REV A', 4.0, INK, 'end', '600', MONO)}
  {txt(W - MARGIN, 27.5, 'millimetres, artwork shown at {0:.0%}'.format(ART_K), 2.7, INK, 'end', '400', FONT, 0, 0.65)}

  {txt(MARGIN, 42, 'ARTWORK — NO GROUND, NO PATCH', 3.2, INK, 'start', '700', FONT, 0.6)}
  <line x1="{MARGIN}" y1="43.8" x2="{MARGIN + 196}" y2="43.8" stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>
  <g transform="translate({AX},{AY}) scale({ART_K})">{art}</g>
  {dim_h(AX, AX + aw, AY + ah + 10, f'{S.WORD_W:.0f} mm')}
  {dim_v(AY, AY + ah, AX - 8, f'{S.WORD_H:.1f}')}
  {txt(AX + aw + 8, AY + 8, f'cap {S.CAP_MM:.2f} mm', 2.9, INK, 'start', '500', MONO)}
  {txt(AX + aw + 8, AY + 14, f'stem {S.STEM_MM:.2f} mm', 2.9, INK, 'start', '500', MONO)}
  {txt(AX + aw + 8, AY + 20, f'bar {S.BAR_MM:.2f} mm', 2.9, INK, 'start', '500', MONO)}

  {txt(COL2, 38, 'THREAD — RANKED BY HOW QUIETLY IT SITS', 3.2, INK, 'start', '700', FONT, 0.6)}
  <line x1="{COL2}" y1="39.8" x2="{COL2 + 144}" y2="39.8" stroke="{INK}" stroke-opacity="0.2" stroke-width="0.3"/>
  {threads}
  {txt(COL2, 122, 'Contrast against the pack fabric measured off the story set:', 2.6, INK, 'start', '400', FONT, 0, 0.7)}
  {txt(COL2, 125.6, '#AA642F sunlit, #662B09 mid, #441801 shadow.', 2.6, INK, 'start', '400', MONO, 0, 0.7)}
  {cons}
  {notes}

  <line x1="{MARGIN}" y1="{H - 14}" x2="{W - MARGIN}" y2="{H - 14}" stroke="{INK}" stroke-opacity="0.25" stroke-width="0.3"/>
  {txt(MARGIN, H - 8.5, 'Production artwork: Output Drafts/Direct-Stitch/stitch-flat.svg', 2.6, INK, 'start', '400', MONO, 0, 0.6)}
  {txt(W - MARGIN, H - 8.5, 'Tone on tone: the wordmark reads as relief, not as colour.', 2.6, INK, 'end', '400', FONT, 0, 0.6)}
</svg>
'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'stitch-spec-sheet.svg'), 'w').write(build())
    print('wrote stitch-spec-sheet.svg')
