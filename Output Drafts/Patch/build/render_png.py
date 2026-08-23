"""Render the patch SVGs to PNG with headless Chromium.

Headless Chromium's layout viewport is shorter than --window-size (the window
frame is still accounted for), so a tall page is silently clipped at the bottom.
Every render therefore asks for extra height and crops back, then verifies the
result against the SVG's own viewBox aspect before writing it.

Point CHROME at a Chromium/Chrome binary if it is not on PATH:
  CHROME=/path/to/chrome python3 render_png.py
"""
import os, re, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
SLACK = 200          # extra window height to clear the frame

CANDIDATES = [os.environ.get('CHROME'), 'chromium', 'chromium-browser',
              'google-chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome']
CHROME = next((c for c in CANDIDATES if c and (os.path.isfile(c) or shutil.which(c))), None)


def viewbox(svg):
    tag = re.search(r'<svg\b[^>]*>', svg, re.S).group(0)
    return [float(v) for v in re.search(r'viewBox="([\d.\- ]+)"', tag).group(1).split()]


def render(svg_path, png_path, width):
    svg = open(svg_path).read()
    _, _, vw, vh = viewbox(svg)
    height = round(width * vh / vw)

    tag = re.search(r'<svg\b[^>]*>', svg, re.S).group(0)
    fixed = re.sub(r'\s(width|height)="[^"]*"', '', tag, flags=re.S)
    fixed = fixed.replace('<svg', f'<svg width="{width}" height="{height}"', 1)
    svg = svg.replace(tag, fixed, 1)

    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as fh:
        fh.write('<!doctype html><meta charset=utf-8>'
                 '<style>html,body{margin:0;padding:0;background:transparent;'
                 'overflow:hidden}svg{display:block}</style>' + svg)
        page = fh.name
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-sandbox',
                    '--hide-scrollbars', '--default-background-color=00000000',
                    '--force-device-scale-factor=1',
                    f'--window-size={width},{height + SLACK}',
                    f'--screenshot={png_path}', 'file://' + page],
                   check=True, capture_output=True)
    os.unlink(page)

    im = Image.open(png_path).convert('RGBA')
    if im.size != (width, height):
        im = im.crop((0, 0, width, height))
        im.save(png_path)

    verify(png_path, vw / vh)
    print(f'  {os.path.basename(png_path)}  {width}x{height}')


def verify(png_path, want, tol=0.02):
    """The drawn content must still carry the viewBox's aspect ratio."""
    a = np.asarray(Image.open(png_path).convert('RGBA'))
    solid = a[..., 3] > 200
    rows, cols = solid.sum(axis=1), solid.sum(axis=0)
    ys, xs = np.nonzero(rows > 8), np.nonzero(cols > 8)
    if not len(ys[0]) or not len(xs[0]):
        raise SystemExit(f'{png_path}: rendered empty')
    h = ys[0].max() - ys[0].min() + 1
    w = xs[0].max() - xs[0].min() + 1
    got = w / h
    # content may be inset by bleed, so compare against the viewBox aspect loosely
    if abs(got - want) / want > tol + 0.06:
        raise SystemExit(f'{png_path}: content aspect {got:.3f} vs viewBox {want:.3f} '
                         '- the page was clipped, raise SLACK')


def jobs():
    out = [('lockup-stacked.svg', 2000), ('patch-spec-sheet.svg', 2400)]
    for name in sorted(os.listdir(OUT)):
        if name.startswith('patch-') and name.endswith('.svg') and 'spec-sheet' not in name:
            out.append((name, 2000))
    return out


if __name__ == '__main__':
    if not CHROME:
        sys.exit('no Chromium binary found; set CHROME=/path/to/chrome')
    print(f'rendering with {CHROME}')
    for name, w in jobs():
        render(os.path.join(OUT, name), os.path.join(OUT, name[:-4] + '.png'), w)
