"""Clean reference plates of the pack for an image generator.

Everything an image generator is given as a reference has to be unambiguous.
The story frames all carry either the old mountain patch or the sewn Deep Red
patch, and the existing on-bag test is a two-up before/after - hand any of those
to a generator and it will happily reproduce the wrong half. So the references
are rebuilt here: the patch is taken out, the direct stitch is put on, and the
pack is cropped out of the scene on its own.
"""
import os, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OUT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, 'Output Drafts', 'Patch', 'build')))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, 'Output Drafts', 'Direct-Stitch', 'build')))
import compose, detect_patch as D                                  # noqa: E402
import build_stitch as S                                           # noqa: E402

SCENE = os.path.join(ROOT, 'Input Pictures - Story Based', '6. Story 3.png')
ALPHA = os.path.join(ROOT, 'Output Drafts', 'Direct-Stitch', 'stitch-deep-red-alpha.png')
BOX = (520, 460, 720, 610)          # the old patch's footprint in scene 6
PANEL_W_PX, PANEL_MM = 420.0, 300.0
PACK = (352, 358, 962, 1032)        # the pack alone, straps and side pockets included


def reshade(base, clean, quad, grow):
    """Level the removal's footprint against the fabric around it.

    The texture transplant keeps the donor's shading at scales coarser than its
    own high-pass cut, so the rebuilt fabric can sit a little brighter than what
    surrounds it - a faint rectangle where the patch used to be. Harmless in a
    before/after, but a reference plate handed to an image generator must not
    show a rectangle on the panel at all, or the generator draws one back in.

    A constant per-channel offset is the right correction here, not a solved
    shading field: extrapolating the surrounding shading across the hole pulls
    the bright fold above the patch down into it and washes the area out, which
    is a more obvious rectangle than the one being removed.
    """
    shape = base.shape[:2]
    inner = compose.quad_mask(shape, quad, grow=grow)
    band_in = inner & ~compose.quad_mask(shape, quad, grow=grow - 0.16)
    band_out = compose.quad_mask(shape, quad, grow=grow + 0.16) & ~inner
    off = base[band_out].mean(axis=0) - clean[band_in].mean(axis=0)
    soft = compose._blur(np.repeat(inner[..., None] * 255.0, 3, axis=2), 9) / 255.0
    return np.clip(clean + off * soft, 0, 255)


def stitched():
    """Scene 6 with the sewn patch removed and the Deep Red stitch put on."""
    base = np.asarray(Image.open(SCENE).convert('RGB')).astype(np.float64)
    quad = D.find(SCENE, BOX)
    clean, _ = compose.remove(base, quad, grow=0.34)
    clean = reshade(base, clean, quad, 0.34)
    plate = np.asarray(Image.open(ALPHA).convert('RGBA')).astype(np.float64)
    bleed = (S.WORD_W + 20.0) / S.WORD_W          # the alpha plate carries 10mm each side
    width = PANEL_W_PX * S.WORD_W / PANEL_MM * bleed
    out, _ = compose.place(base, clean, quad, plate, width, lum_ref=96.0)
    return Image.fromarray(out.astype(np.uint8))


def save(img, box, name, scale=2):
    c = img.crop(box)
    c = c.resize((c.width * scale, c.height * scale), Image.LANCZOS)
    p = os.path.join(OUT, name)
    c.save(p)
    print(f'  {name}  {c.width}x{c.height}')


if __name__ == '__main__':
    save(stitched(), PACK, 'pack-ref-front-stitched.png')
