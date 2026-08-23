"""Render the patch SVGs to PNG with headless Chromium.

Point CHROME at a Chromium/Chrome binary if it is not on PATH:
  CHROME=/path/to/chrome python3 render_png.py
"""
import os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))

CANDIDATES = [os.environ.get('CHROME'), 'chromium', 'chromium-browser',
              'google-chrome', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome']
CHROME = next((c for c in CANDIDATES if c and (os.path.isfile(c) or shutil.which(c))), None)

JOBS = [('lockup-stacked.svg',    2000),
        ('patch-flat.svg',        2000),
        ('patch-embroidered.svg', 2000),
        ('patch-spec-sheet.svg',  2400)]


def render(svg_path, png_path, width):
    svg = open(svg_path).read()
    vb = re.search(r'viewBox="([\d.\- ]+)"', svg).group(1).split()
    vw, vh = float(vb[2]), float(vb[3])
    height = round(width * vh / vw)
    svg = re.sub(r'(<svg[^>]*?)\s(width|height)="[^"]*"', r'\1', svg)
    svg = svg.replace('<svg ', f'<svg width="{width}" height="{height}" ', 1)
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as fh:
        fh.write('<!doctype html><meta charset=utf-8>'
                 '<style>html,body{margin:0;padding:0;background:transparent}</style>' + svg)
        page = fh.name
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--no-sandbox',
                    '--hide-scrollbars', '--default-background-color=00000000',
                    '--force-device-scale-factor=1',
                    f'--window-size={width},{height}',
                    f'--screenshot={png_path}', 'file://' + page],
                   check=True, capture_output=True)
    os.unlink(page)
    print(f'  {os.path.basename(png_path)}  {width}x{height}')


if __name__ == '__main__':
    if not CHROME:
        sys.exit('no Chromium binary found; set CHROME=/path/to/chrome')
    print(f'rendering with {CHROME}')
    for name, w in JOBS:
        render(os.path.join(OUT, name), os.path.join(OUT, name[:-4] + '.png'), w)
