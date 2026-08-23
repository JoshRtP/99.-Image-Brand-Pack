"""PNG exports for the direct-stitch assets, using the patch pipeline's renderer."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'Patch', 'build')))
import render_png as R                                        # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, '..'))
JOBS = [('stitch-colourways.svg', 2400), ('stitch-flat.svg', 1600)]
JOBS += [(n, 1600) for n in sorted(os.listdir(OUT))
         if n.startswith('stitch-') and n.endswith('.svg')
         and n not in ('stitch-colourways.svg', 'stitch-flat.svg')]

if __name__ == '__main__':
    if not R.CHROME:
        sys.exit('no Chromium binary found; set CHROME=/path/to/chrome')
    print(f'rendering with {R.CHROME}')
    for name, w in JOBS:
        # alpha plates carry 10 mm of padding for their own relief shadow, so
        # their content deliberately does not fill the viewBox
        R.render(os.path.join(OUT, name), os.path.join(OUT, name[:-4] + '.png'), w,
                 verify_aspect='-alpha' not in name)
