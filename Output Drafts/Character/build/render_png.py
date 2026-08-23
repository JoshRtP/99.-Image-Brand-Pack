"""PNG exports for the character sheets, using the patch pipeline's renderer."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'Patch', 'build')))
import render_png as R                                        # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, '..'))
JOBS = [('character-turnaround.svg', 2600)]
JOBS += [(n, 900) for n in sorted(os.listdir(OUT))
         if n.startswith('character-') and n.endswith('.svg') and 'turnaround' not in n]

if __name__ == '__main__':
    if not R.CHROME:
        sys.exit('no Chromium binary found; set CHROME=/path/to/chrome')
    print(f'rendering with {R.CHROME}')
    for name, w in JOBS:
        R.render(os.path.join(OUT, name), os.path.join(OUT, name[:-4] + '.png'), w)
