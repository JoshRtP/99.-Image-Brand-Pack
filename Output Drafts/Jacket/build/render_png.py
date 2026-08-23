"""PNG exports for the jacket assets.

Reuses the patch pipeline's renderer, which crops back from a taller window
(headless Chromium's layout viewport is shorter than --window-size) and verifies
each export's drawn content against its viewBox aspect.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'Patch', 'build')))
import render_png as R                                        # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, '..'))
JOBS = [('jacket-spec-sheet.svg', 2400), ('jacket-colourways.svg', 2400)]
JOBS += [(n, 2000) for n in sorted(os.listdir(OUT))
         if n.startswith('jacket-flat') and n.endswith('.svg')]

if __name__ == '__main__':
    if not R.CHROME:
        sys.exit('no Chromium binary found; set CHROME=/path/to/chrome')
    print(f'rendering with {R.CHROME}')
    for name, w in JOBS:
        R.render(os.path.join(OUT, name), os.path.join(OUT, name[:-4] + '.png'), w)
