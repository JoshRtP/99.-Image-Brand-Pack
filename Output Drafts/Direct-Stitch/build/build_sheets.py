"""Colourway comparison and the on-bag test for the direct-stitch treatment."""
import os, re, sys
import numpy as np
from PIL import Image

import build_stitch as S

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = S.OUT
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'Patch', 'build')))
import compose, detect_patch as D                                  # noqa: E402

INK, PAPER = '#061927', '#F4F2EC'
FONT = "'Helvetica Neue', Helvetica, Arial, 'Liberation Sans', sans-serif"
MONO = "'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"

ORDER = ['deep-red', 'warm-charcoal', 'olive', 'slate-purple', 'ink', 'sand']
TILE_W, GAP, MARGIN = 150.0, 12.0, 20.0
TILE_H = 108.0
COLS = 3
TITLE_Y, SUB_Y, RULE_Y, HEAD = 15.0, 21.5, 27.0, 46.0
ROW_LABEL = 21.0
W = 2 * MARGIN + COLS * TILE_W + (COLS - 1) * GAP
ROWS = (len(ORDER) + COLS - 1) // COLS
FOOT = HEAD + ROWS * (TILE_H + ROW_LABEL) + (ROWS - 1) * GAP + 12
H = FOOT + 26


def txt(x, y, s, size=3.0, fill=INK, anchor='start', weight='400', family=FONT,
        spacing=0, opacity=1):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" opacity="{opacity}">{s}</text>')


def inner(path):
    s = open(path).read()
    s = re.sub(r'^.*?<svg\b[^>]*>', '', s, flags=re.S)
    return s.rsplit('</svg>', 1)[0]


def colourways():
    parts = []
    for i, key in enumerate(ORDER):
        name, thread, c_mid, c_lit = S.THREADS[key]
        r, c = divmod(i, COLS)
        x = MARGIN + c * (TILE_W + GAP)
        y = HEAD + r * (TILE_H + ROW_LABEL + GAP)
        parts.append(f'<g transform="translate({x:.2f},{y:.2f})">'
                     f'{inner(os.path.join(OUT, f"stitch-{key}.svg"))}</g>')
        parts.append(f'<rect x="{x}" y="{y}" width="{TILE_W}" height="{TILE_H}" fill="none" '
                     f'stroke="{INK}" stroke-opacity="0.25" stroke-width="0.3"/>')
        tag = ' — recommended' if key == S.PRIMARY else ''
        parts.append(txt(x, y + TILE_H + 6.5, name.upper() + tag, 3.2, INK, 'start', '700',
                         FONT, 0.3))
        parts.append(txt(x, y + TILE_H + 11.5,
                         f'{thread}   {c_mid:.2f}:1 on shade   {c_lit:.2f}:1 in sun',
                         2.7, INK, 'start', '400', MONO, 0, 0.7))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.2f} {H:.2f}"
     width="{W:.2f}mm" height="{H:.2f}mm">
  <title>Terra Nexus direct stitch - thread options on pack fabric</title>
  <desc>One wordmark, six threads. Each panel runs from sunlit fabric at top left to
        shadow at bottom right, so you can see the thread appear and disappear.</desc>
  <rect width="{W:.2f}" height="{H:.2f}" fill="{PAPER}"/>
  {txt(MARGIN, TITLE_Y, 'TERRA NEXUS', 6.6, INK, 'start', '700', FONT, 1.8)}
  {txt(MARGIN, SUB_Y, 'DIRECT RAISED STITCH ON THE PACK PANEL - THREAD OPTIONS', 3.0, INK, 'start', '500', FONT, 1.3, 0.7)}
  {txt(W - MARGIN, TITLE_Y, 'REV A', 3.6, INK, 'end', '600', MONO)}
  <line x1="{MARGIN}" y1="{RULE_Y}" x2="{W - MARGIN}" y2="{RULE_Y}" stroke="{INK}" stroke-width="0.4"/>
  {txt(MARGIN, RULE_Y + 8, 'Each panel runs sunlit at top left to shadow at bottom right. Contrast is against the pack fabric measured off the story set: #AA642F sunlit, #662B09 mid, #441801 shadow.', 2.7, INK, 'start', '400', FONT, 0, 0.72)}
  {''.join(parts)}
  <line x1="{MARGIN}" y1="{FOOT}" x2="{W - MARGIN}" y2="{FOOT}" stroke="{INK}" stroke-opacity="0.25" stroke-width="0.3"/>
  {txt(MARGIN, FOOT + 5.5, 'Tone on tone: the wordmark reads as relief, not as colour. Sand is included as the control - it is what NOT blending looks like.', 2.7, INK, 'start', '400', FONT, 0, 0.65)}
</svg>
'''


# ---------------------------------------------------------------- on the bag
# The direct stitch replaces the patch, so the demonstration starts from the
# original frame - the one that still carries the old sewn patch - takes that
# patch out, and stitches the wordmark straight onto the panel instead.
SCENE = os.path.join(ROOT, 'Input Pictures - Story Based', '6. Story 3.png')
BOX = (520, 460, 720, 610)          # the old patch's footprint in scene 6
PANEL_W_PX, PANEL_MM = 420.0, 300.0


def on_bag(key, out_png, alpha_png):
    base = np.asarray(Image.open(SCENE).convert('RGB')).astype(np.float64)
    quad = D.find(SCENE, BOX)
    clean, _ = compose.remove(base, quad, grow=0.34)
    plate = np.asarray(Image.open(alpha_png).convert('RGBA')).astype(np.float64)
    bleed = (S.WORD_W + 20.0) / S.WORD_W          # the alpha plate carries 10mm each side
    width = PANEL_W_PX * S.WORD_W / PANEL_MM * bleed
    out, _ = compose.place(base, clean, quad, plate, width, lum_ref=96.0)
    img = Image.fromarray(out.astype(np.uint8))
    b = (int(quad[:, 0].min()) - 110, int(quad[:, 1].min()) - 95,
         int(quad[:, 0].max()) + 110, int(quad[:, 1].max()) + 95)
    before = Image.open(SCENE).convert('RGB').crop(b)
    after = img.crop(b)
    w, h = before.size
    sheet = Image.new('RGB', (w * 2 + 20, h), (244, 242, 236))
    sheet.paste(before, (0, 0)); sheet.paste(after, (w + 20, 0))
    sheet = sheet.resize((sheet.width * 3, sheet.height * 3), Image.LANCZOS)
    sheet.save(out_png)
    print(f'  {os.path.basename(out_png)}  {sheet.size[0]}x{sheet.size[1]}')


if __name__ == '__main__':
    open(os.path.join(OUT, 'stitch-colourways.svg'), 'w').write(colourways())
    print('wrote stitch-colourways.svg')
