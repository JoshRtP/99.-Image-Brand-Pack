"""Photographic character sheet: real frames of the character, by angle.

The story set is the only photography of her that exists, so the sheet is cut
from it rather than illustrated. Plates come from the corrected frames in
'Ouput Pictures - Updated Images', which already carry the Deep Red bag patch
and have the shoulder patch removed.
"""
import os, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
PLATES = os.path.join(OUT, 'plates')
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SRC = os.path.join(ROOT, 'Ouput Pictures - Updated Images')

CUTS = [
    ('back',          '9. Story 6 - FINAL.png',       (28, 610, 505, 1536)),
    ('tq-back-left',  '1. Opening Scene - FINAL.png',  (52, 140, 640, 941)),
    ('tq-back-right', '7. Story 4 - FINAL.png',        (0, 300, 470, 1270)),
    ('near-profile',  '5. Story 2 - FINAL.png',        (430, 410, 941, 1160)),
    ('tq-back-map',   '8. Story 5 - FINAL.png',        (0, 300, 500, 1290)),
    ('d-head',        '7. Story 4 - FINAL.png',        (60, 320, 400, 660)),
    ('d-collar',      '9. Story 6 - FINAL.png',        (120, 640, 470, 960)),
    ('d-pack',        '9. Story 6 - FINAL.png',        (30, 830, 340, 1160)),
    ('d-sleeve',      '8. Story 5 - FINAL.png',        (250, 820, 545, 1105)),
    ('d-hem',         '9. Story 6 - FINAL.png',        (60, 1060, 400, 1330)),
]

MAIN = [('back', 'BACK', 'scene 9'),
        ('tq-back-left', 'THREE-QUARTER BACK, LEFT', 'scene 1'),
        ('tq-back-map', 'THREE-QUARTER BACK', 'scene 8'),
        ('tq-back-right', 'THREE-QUARTER BACK, RIGHT', 'scene 7'),
        ('near-profile', 'NEAREST TO PROFILE', 'scene 5')]
DETAIL = [('d-head', 'HAIR — MID-HEIGHT PONYTAIL, LOOSE CROWN STRANDS'),
          ('d-collar', 'HOOD WORN DOWN, BUNCHED BEHIND THE NECK'),
          ('d-pack', 'PACK OVER THE SHELL — PATCH ON THE PACK, NOT THE JACKET'),
          ('d-sleeve', 'UPPER ARM — CLEAN. NO SHOULDER MARK, NO PATCH'),
          ('d-hem', 'HEM SITS AT THE HIP, BELOW THE PACK')]


def cut():
    os.makedirs(PLATES, exist_ok=True)
    for name, f, box in CUTS:
        im = Image.open(os.path.join(SRC, f)).convert('RGB')
        b = (max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3]))
        im.crop(b).save(os.path.join(PLATES, name + '.png'))
    return {n: Image.open(os.path.join(PLATES, n + '.png')).size for n, _, _ in CUTS}


def html(sizes):
    def plate(name, h):
        w, hh = sizes[name]
        return f'<img src="plates/{name}.png" width="{round(w * h / hh)}" height="{h}">'

    main = ''.join(
        f'<figure class="p"><div class="frame">{plate(n, 760)}</div>'
        f'<figcaption><b>{label}</b><span>{src}</span></figcaption></figure>'
        for n, label, src in MAIN)
    det = ''.join(
        f'<figure class="d"><div class="frame">{plate(n, 300)}</div>'
        f'<figcaption>{label}</figcaption></figure>' for n, label in DETAIL)

    return f'''<!doctype html><meta charset="utf-8">
<style>
  @page {{ margin:0 }}
  body {{ margin:0; background:#F4F2EC; color:#061927;
         font-family:"Liberation Sans",Helvetica,Arial,sans-serif; width:2480px; }}
  .wrap {{ padding:56px 60px 48px }}
  h1 {{ font-size:52px; font-weight:700; letter-spacing:13px; margin:0 }}
  .sub {{ font-size:20px; letter-spacing:9px; margin:8px 0 0; opacity:.75 }}
  .rev {{ float:right; text-align:right; font-size:26px; font-weight:700;
          letter-spacing:3px; font-family:"DejaVu Sans Mono",monospace }}
  .rev span {{ display:block; font-size:15px; font-weight:400; letter-spacing:0;
               opacity:.65; font-family:inherit; margin-top:6px }}
  hr {{ border:0; border-top:3px solid #061927; margin:22px 0 34px }}
  .lbl {{ font-size:17px; font-weight:700; letter-spacing:5px; opacity:.65;
          margin:0 0 14px }}
  .row {{ display:flex; gap:20px; align-items:flex-end }}
  .frame {{ background:#0d1520; line-height:0; border:1px solid rgba(6,25,39,.25) }}
  figure {{ margin:0 }}
  figcaption {{ margin-top:12px; font-size:16px; letter-spacing:2px }}
  .p figcaption b {{ display:block; font-weight:700; font-size:17px; letter-spacing:2.5px }}
  .p figcaption span {{ display:block; font-size:14px; opacity:.6; letter-spacing:1px;
                        margin-top:4px; font-family:"DejaVu Sans Mono",monospace }}
  .d figcaption {{ font-size:14px; opacity:.72; letter-spacing:1.4px; max-width:330px;
                   line-height:1.45 }}
  .cols {{ display:flex; gap:52px; margin-top:44px }}
  .col {{ flex:1 }}
  h2 {{ font-size:19px; font-weight:700; letter-spacing:4px; margin:0 0 8px }}
  .rule {{ border-top:1px solid rgba(6,25,39,.22); margin-bottom:14px }}
  table {{ border-collapse:collapse; width:100% }}
  td {{ padding:7px 0; vertical-align:baseline; font-size:16px; line-height:1.5 }}
  td.k {{ width:150px; font-weight:700; padding-right:16px }}
  .warn td.k {{ color:#B23A28 }}
  .foot {{ margin-top:40px; border-top:1px solid rgba(6,25,39,.25); padding-top:14px;
           font-size:14px; opacity:.6; letter-spacing:.6px }}
</style>
<div class="wrap">
  <div class="rev">REV A<span>plates cut from the corrected story frames</span></div>
  <h1>TERRA NEXUS</h1>
  <p class="sub">MAIN CHARACTER — PHOTOGRAPHIC REFERENCE</p>
  <hr>
  <p class="lbl">ANGLES THAT EXIST</p>
  <div class="row">{main}</div>
  <p class="lbl" style="margin-top:46px">DETAIL</p>
  <div class="row">{det}</div>
  <div class="cols">
    <div class="col">
      <h2>LOCKED</h2><div class="rule"></div>
      <table>
        <tr><td class="k">Build</td><td>Athletic, approximately 168 cm. Jacket size M.</td></tr>
        <tr><td class="k">Hair</td><td>Mid-brown with warm highlights, mid-height ponytail,
            loose flyaway strands at the crown. Never loose, never braided.</td></tr>
        <tr><td class="k">Jacket</td><td>Terra Nexus wind shell, Glacier Blue #5A90BE.
            Hood worn down and bunched behind the neck. Zipped.</td></tr>
        <tr><td class="k">Below</td><td>Slim dark charcoal technical trouser.
            Low brown approach boot.</td></tr>
        <tr><td class="k">Pack</td><td>Rust orange, worn over the shell. Deep Red patch on
            the pack's upper front panel — never on the jacket.</td></tr>
        <tr><td class="k">Light</td><td>Golden hour, low sun behind or beside her, warm rim
            on hair and shoulders.</td></tr>
      </table>
    </div>
    <div class="col">
      <h2>WHAT REV B CHANGES</h2><div class="rule"></div>
      <table>
        <tr><td class="k">Fit</td><td>These plates are the Rev A cut — loose through the
            waist. Rev B is slim athletic: princess seams, 6.4 cm of waist suppression,
            hem scooped at centre back. See the turnaround.</td></tr>
        <tr><td class="k">Cuffs</td><td>TERRA wraps the left wrist, NEXUS the right. The
            cuffs are out of frame in every plate here.</td></tr>
        <tr><td class="k">Shoulder</td><td>Already correct — the shoulder patch has been
            removed from these frames.</td></tr>
      </table>
      <h2 style="margin-top:30px">NO REFERENCE EXISTS</h2><div class="rule"></div>
      <table class="warn">
        <tr><td class="k">Her face</td><td>Every frame in the set is shot from behind or
            over the shoulder. It has never been seen. Choose one and lock it before the
            next generation pass, or it will drift.</td></tr>
        <tr><td class="k">Front, side</td><td>No frame shows either. The turnaround
            specifies them; nothing observes them.</td></tr>
      </table>
    </div>
  </div>
  <p class="foot">Plates cut unretouched from Ouput Pictures - Updated Images. This is the
    character as she has actually been rendered — not an illustration of her.</p>
</div>
'''


def render(path_html, out_png, width=2480):
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', 'Patch', 'build')))
    import render_png as R
    if not R.CHROME:
        sys.exit('no Chromium binary found; set CHROME=/path/to/chrome')
    subprocess.run([R.CHROME, '--headless', '--disable-gpu', '--no-sandbox',
                    '--hide-scrollbars', '--force-device-scale-factor=1',
                    f'--window-size={width},4000',
                    f'--screenshot={out_png}', 'file://' + path_html],
                   check=True, capture_output=True)
    im = Image.open(out_png).convert('RGB')
    a = im.load()
    bg = a[5, 5]
    bottom = im.height
    for y in range(im.height - 1, 0, -1):
        if any(a[x, y] != bg for x in range(0, im.width, 17)):
            bottom = min(im.height, y + 46)
            break
    im.crop((0, 0, im.width, bottom)).save(out_png)
    print(f'  {os.path.basename(out_png)}  {im.width}x{bottom}')


if __name__ == '__main__':
    sizes = cut()
    page = os.path.join(OUT, 'character-sheet.html')
    open(page, 'w').write(html(sizes))
    render(page, os.path.join(OUT, 'character-sheet.png'))
