"""Comparison sheet: three colourways, new and worn.

Each variant's defs are already id-suffixed by colourway, so all six renders
nest into one document without collisions.
"""
import os, re
import build_patch as B

OUT = B.OUT
INK, PAPER, RULE = '#061927', '#F4F2EC', '#7C8493'
FONT = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
MONO = "'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"

TW, TH = B.PW + 4, B.PH + 4        # one patch render, including its bleed
GAP_X, GAP_Y = 15.0, 17.0
MARGIN = 20.0
TITLE_Y, SUB_Y, RULE_Y = 15.0, 21.5, 27.0
COLNAME_Y, COLHEX_Y = 38.0, 43.5
HEAD = 48.0
ROWS = [('New', False), ('Worn', True)]
KEYS = list(B.COLOURWAYS)

W = 2 * MARGIN + 3 * TW + 2 * GAP_X
BODY_END = HEAD + len(ROWS) * TH + (len(ROWS) - 1) * GAP_Y
FOOT_RULE = BODY_END + 13.0
H = FOOT_RULE + 12.0


def txt(x, y, s, size=3.2, fill=INK, anchor='start', weight='400', family=FONT,
        spacing=0, opacity=1):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" opacity="{opacity}">{s}</text>')


def inner(path):
    """The body of an SVG file, minus its own <svg> wrapper."""
    s = open(path).read()
    s = re.sub(r'^.*?<svg\b[^>]*>', '', s, flags=re.S)
    return s.rsplit('</svg>', 1)[0]


def build():
    parts = []
    for ci, key in enumerate(KEYS):
        name, ground = B.COLOURWAYS[key]
        x = MARGIN + ci * (TW + GAP_X)
        parts.append(txt(x, COLNAME_Y, name.replace('Terra Nexus ', ''), 4.2, INK,
                         'start', '700', FONT, 0.5))
        parts.append(txt(x, COLHEX_Y, ground, 3.0, INK, 'start', '400', MONO, 0, 0.65))
        for ri, (_, worn) in enumerate(ROWS):
            y = HEAD + ri * (TH + GAP_Y)
            src = os.path.join(OUT, B.emb_name(key, worn))
            parts.append(f'<g transform="translate({x:.2f},{y:.2f}) translate(2,2)">'
                         f'{inner(src)}</g>')
    for ri, (label, _) in enumerate(ROWS):
        y = HEAD + ri * (TH + GAP_Y)
        parts.append(txt(MARGIN - 4, y + TH / 2, label.upper(), 3.0, INK, 'end', '700',
                         FONT, 0.18, 0.55))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}"
     width="{W:.2f}mm" height="{H:.2f}mm">
  <title>Terra Nexus backpack patch - colourways</title>
  <desc>One geometry, three grounds, each shown new and lightly worn.
        Worn is a rendering treatment only; production artwork is never worn.</desc>
  <rect width="{W:.2f}" height="{H:.2f}" fill="{PAPER}"/>
  {txt(MARGIN, TITLE_Y, 'TERRA NEXUS', 6.6, INK, 'start', '700', FONT, 1.8)}
  {txt(MARGIN, SUB_Y, 'BACKPACK PATCH COLOURWAYS', 3.0, INK, 'start', '500', FONT, 1.3, 0.7)}
  {txt(W - MARGIN, TITLE_Y, 'REV A', 3.6, INK, 'end', '600', MONO)}
  <line x1="{MARGIN}" y1="{RULE_Y}" x2="{W - MARGIN}" y2="{RULE_Y}"
        stroke="{INK}" stroke-width="0.4"/>
  {''.join(parts)}
  <line x1="{MARGIN}" y1="{FOOT_RULE}" x2="{W - MARGIN}" y2="{FOOT_RULE}"
        stroke="{INK}" stroke-opacity="0.25" stroke-width="0.3"/>
  {txt(MARGIN, FOOT_RULE + 5.5, 'Same geometry throughout: 63 x 36 mm, white wordmark, sand star. '
       'Only the ground changes.', 2.8, INK, 'start', '400', FONT, 0, 0.65)}
  {txt(W - MARGIN, FOOT_RULE + 5.5, 'Worn is a render treatment - production artwork is never worn.',
       2.8, INK, 'end', '400', FONT, 0, 0.65)}
</svg>
'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'patch-colourways.svg'), 'w').write(build())
    print('wrote patch-colourways.svg')
