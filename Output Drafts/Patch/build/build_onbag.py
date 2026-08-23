"""Each colourway composited onto the pack in scene 6, side by side.

New and worn, at true physical scale, so the choice can be made on the bag
rather than on a swatch.
"""
import os
from PIL import Image, ImageDraw, ImageFont
import build_patch as B
import place_on_bag

OUT = B.OUT
TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_onbag')
PAPER, INK, MUTED = (244, 242, 236), (6, 25, 39), (110, 120, 135)


def font(size, bold=False):
    for p in ['/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf',
              '/usr/share/fonts/truetype/dejavu/DejaVu%s.ttf']:
        try:
            return ImageFont.truetype(p % ('Bold' if bold else 'Regular'), size)
        except OSError:
            try:
                return ImageFont.truetype(p % ('Sans-Bold' if bold else 'Sans'), size)
            except OSError:
                pass
    return ImageFont.load_default()


def build():
    os.makedirs(TMP, exist_ok=True)
    rows = [('New', False), ('Worn', True)]
    tiles = {}
    for key in B.COLOURWAYS:
        for label, worn in rows:
            src = os.path.join(OUT, B.emb_name(key, worn))
            png = os.path.join(OUT, B.emb_name(key, worn)[:-4] + '.png')
            dst = os.path.join(TMP, f'{key}-{label.lower()}.png')
            place_on_bag.build(png, dst, mode='after')
            tiles[(key, worn)] = Image.open(dst).convert('RGB')

    w, h = next(iter(tiles.values())).size
    pad, head, rowlab = 18, 74, 96
    W = rowlab + 3 * w + 4 * pad
    H = head + 2 * h + 3 * pad + 46
    sheet = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(sheet)
    d.text((pad + 6, 20), 'TERRA NEXUS', font=font(30, True), fill=INK)
    d.text((pad + 6, 52), 'COLOURWAYS ON THE PACK  ·  SCENE 6  ·  TRUE PHYSICAL SCALE',
           font=font(15), fill=MUTED)
    d.line([(pad + 6, head - 4), (W - pad - 6, head - 4)], fill=INK, width=2)

    for ci, key in enumerate(B.COLOURWAYS):
        name, ground = B.COLOURWAYS[key]
        x = rowlab + pad + ci * (w + pad)
        d.text((x, head + 6), name.replace('Terra Nexus ', '').upper(), font=font(19, True), fill=INK)
        d.text((x + 170, head + 8), ground, font=font(15), fill=MUTED)
        for ri, (label, worn) in enumerate(rows):
            y = head + 32 + ri * (h + pad)
            sheet.paste(tiles[(key, worn)], (x, y))
            if ci == 0:
                d.text((pad + 6, y + h // 2 - 8), label.upper(), font=font(15, True), fill=MUTED)
    sheet.save(os.path.join(OUT, 'patch-colourways-on-bag.png'))
    for f in os.listdir(TMP):
        os.unlink(os.path.join(TMP, f))
    os.rmdir(TMP)
    print(f'wrote patch-colourways-on-bag.png {sheet.size[0]}x{sheet.size[1]}')


if __name__ == '__main__':
    build()
