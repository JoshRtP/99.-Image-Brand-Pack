"""Comparison sheet: the wind shell in each colourway, front and back."""
import os, re
import build_jacket as J

OUT = J.OUT
INK, PAPER = '#061927', '#F4F2EC'
FONT = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
MONO = "'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"

K = 0.088
CROP, ORG = (116.0, 62.0), (710.0, 230.0)
TW, TH = 1190.0 * K, 860.0 * K
GAP_X, GAP_Y, MARGIN = 14.0, 16.0, 20.0
TITLE_Y, SUB_Y, RULE_Y = 15.0, 21.5, 27.0
NAME_Y, HEX_Y, HEAD = 38.0, 43.5, 48.0
W = 2 * MARGIN + 3 * TW + 2 * GAP_X
BODY_END = HEAD + 2 * TH + GAP_Y
FOOT = BODY_END + 13.0
H = FOOT + 12.0


def txt(x, y, s, size=3.0, fill=INK, anchor='start', weight='400', family=FONT,
        spacing=0, opacity=1):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" opacity="{opacity}">{s}</text>')


def inner(path):
    s = open(path).read()
    s = re.sub(r'^.*?<svg\b[^>]*>', '', s, flags=re.S)
    return s.rsplit('</svg>', 1)[0]


def build():
    parts = []
    for ci, key in enumerate(J.COLOURWAYS):
        name, ground = J.COLOURWAYS[key]
        x = MARGIN + ci * (TW + GAP_X)
        parts.append(txt(x, NAME_Y, name.replace('Terra Nexus ', ''), 4.2, INK,
                         'start', '700', FONT, 0.5))
        parts.append(txt(x, HEX_Y, ground, 3.0, INK, 'start', '400', MONO, 0, 0.65))
        for ri, view in enumerate(('front', 'back')):
            y = HEAD + ri * (TH + GAP_Y)
            src = os.path.join(OUT, J.flat_name(view, key))
            parts.append(f'<g transform="translate({x:.2f},{y:.2f}) scale({K}) '
                         f'translate({-CROP[0]},{-CROP[1]})">{inner(src)}</g>')
    for ri, label in enumerate(('FRONT', 'BACK')):
        y = HEAD + ri * (TH + GAP_Y)
        parts.append(txt(MARGIN - 4, y + TH / 2, label, 3.0, INK, 'end', '700',
                         FONT, 0.18, 0.55))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}"
     width="{W:.2f}mm" height="{H:.2f}mm">
  <title>Terra Nexus wind shell - colourways</title>
  <desc>One garment, three grounds. The sleeve mark stays white with a sand star.</desc>
  <rect width="{W:.2f}" height="{H:.2f}" fill="{PAPER}"/>
  {txt(MARGIN, TITLE_Y, 'TERRA NEXUS', 6.6, INK, 'start', '700', FONT, 1.8)}
  {txt(MARGIN, SUB_Y, 'WIND SHELL COLOURWAYS', 3.0, INK, 'start', '500', FONT, 1.3, 0.7)}
  {txt(W - MARGIN, TITLE_Y, 'REV A', 3.6, INK, 'end', '600', MONO)}
  <line x1="{MARGIN}" y1="{RULE_Y}" x2="{W - MARGIN}" y2="{RULE_Y}" stroke="{INK}" stroke-width="0.4"/>
  {''.join(parts)}
  <line x1="{MARGIN}" y1="{FOOT}" x2="{W - MARGIN}" y2="{FOOT}" stroke="{INK}" stroke-opacity="0.25" stroke-width="0.3"/>
  {txt(MARGIN, FOOT + 5.5, 'Same pattern throughout. Only the shell colour changes; trims and the sleeve mark do not.', 2.8, INK, 'start', '400', FONT, 0, 0.65)}
  {txt(W - MARGIN, FOOT + 5.5, 'Glacier Blue is the colourway worn in the story set.', 2.8, INK, 'end', '400', FONT, 0, 0.65)}
</svg>
'''


if __name__ == '__main__':
    open(os.path.join(OUT, 'jacket-colourways.svg'), 'w').write(build())
    print('wrote jacket-colourways.svg')
