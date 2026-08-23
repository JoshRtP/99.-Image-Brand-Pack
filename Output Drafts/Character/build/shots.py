"""The generation shot list, machine readable.

Single source of truth for the prompts in ../GENERATION-BRIEF.md. Run with
--json to emit ../shots.json for scripting against an image API.
"""
import json, os, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..'))
REPO_RAW = 'https://raw.githubusercontent.com/JoshRtP/99.-Image-Brand-Pack/main/'


def url(path):
    """Repo-relative path -> fetchable raw URL. Folder names contain spaces."""
    return REPO_RAW + quote(path)

FACE = ("Late twenties to early thirties. Oval face with a defined jaw and a straight "
        "nose. Fair skin with a warm undertone, light freckling across the nose and "
        "cheekbones, weathered slightly by sun and wind. Grey-green eyes, mid-brown "
        "eyebrows. No makeup beyond what survives a day outdoors. Calm, focused "
        "expression - attentive rather than smiling.")

BASE = f"""A woman in her late twenties, athletic build, about 168 cm tall. Mid-brown hair
with warm highlights, pulled into a mid-height ponytail, loose flyaway strands at the
crown. {FACE}

She wears the Terra Nexus wind shell: a slim, close-fitting single-layer hooded shell in
glacier blue (#5A90BE). Raglan sleeves. Princess seams front and back running from the
raglan seam through the waist to the hem, giving a clearly nipped waist. Hood worn down,
bunched behind the neck. Full-length front zip, closed, with a small red zip pull. Two
zipped hand pockets. Long shaped cuffs with thumbholes, lying flat - not gathered or
elasticated. Hem falls to the hip and is scooped slightly lower at centre back.

Block capitals wrap the cuffs: TERRA around the left wrist, NEXUS around the right,
printed in white. The jacket carries no other marking of any kind.

Below: slim dark charcoal technical trousers and low brown approach boots.

Photographic, sharp, natural skin texture."""

JACKET_BASE = """A single lightweight hooded wind shell photographed as a product shot on an
invisible mannequin - no visible person, no head, no hands, no face. Slim, close-fitting cut
in glacier blue (#5A90BE). Raglan sleeves. Princess seams front and back running from the
raglan seam through the waist to the hem, giving a clearly nipped waist. Hood worn down,
bunched behind the neck. Full-length front zip, closed, with a small red zip pull. Two zipped
hand pockets. Long shaped cuffs with thumbholes, lying flat - not gathered or elasticated. Hem
falls to the hip and is scooped slightly lower at centre back.

Block capitals wrap the cuffs: TERRA around the left wrist, NEXUS around the right, printed in
white. The jacket carries no other marking of any kind - nothing on the shoulder, upper arm or
chest.

Plain mid-grey seamless background, soft even studio light. Sharp, photographic, catalogue
quality."""

NEGATIVE = ("patch or logo on the shoulder, upper arm or chest; mountain graphic; any text "
            "other than TERRA and NEXUS on the cuffs; boxy, oversized or loose fit; parka; "
            "hood worn up; gathered or elasticated cuffs; hair loose or braided; sunglasses; "
            "hat; gloves; second person in frame; visible brand names other than Terra Nexus; "
            "text overlay; watermark")

STUDIO = 'plain mid-grey seamless background, soft even studio light'
P = 'Output Drafts/Character/plates/'
J = 'Output Drafts/Jacket/'
PATCH = 'Output Drafts/Patch/'
SCENES = 'Ouput Pictures - Updated Images/'

SHOTS = [
    dict(id='id-face-front', order=1, aspect='1:1', lock=True,
         add=f'Head and shoulders portrait, facing camera directly, neutral expression, {STUDIO}.',
         refs=[P + 'near-profile.png', P + 'd-head.png'],
         note='Generate several, pick one. That image becomes the identity reference '
              'attached to every later shot.'),
    dict(id='id-face-tq', order=2, aspect='1:1',
         add=f'Head and shoulders portrait, turned about 40 degrees from camera, {STUDIO}.',
         refs=['@id-face-front', P + 'd-head.png', P + 'd-collar.png']),
    dict(id='full-front', order=3, aspect='2:3',
         add=f'Full figure standing square to camera, arms relaxed at her sides, {STUDIO}.',
         refs=['@id-face-front', J + 'jacket-flat-front.png',
               'Output Drafts/Character/character-turnaround.png']),
    dict(id='full-tq-front', order=4, aspect='2:3',
         add=f'Full figure turned about 40 degrees from camera, arms relaxed, {STUDIO}.',
         refs=['@id-face-front', J + 'jacket-flat-front.png']),
    dict(id='full-side', order=5, aspect='2:3',
         add=f'Full figure in full profile, side on, arms relaxed, {STUDIO}.',
         refs=['@id-face-front', 'Output Drafts/Character/character-turnaround.png']),
    dict(id='full-tq-back', order=6, aspect='2:3',
         add=f'Full figure turned about 140 degrees, seen mostly from behind, {STUDIO}.',
         refs=['@id-face-front', J + 'jacket-flat-back.png', P + 'tq-back-left.png']),
    dict(id='full-back', order=7, aspect='2:3',
         add=f'Full figure seen directly from behind, arms relaxed, {STUDIO}.',
         refs=[J + 'jacket-flat-back.png', P + 'back.png']),
    dict(id='cuff-left-terra', order=8, aspect='3:2',
         add='Close detail of her left wrist and cuff, arm relaxed at her side. The word '
             'TERRA in white block capitals wraps around the cuff. Thumbhole visible. '
             'Plain mid-grey background, soft even light.',
         refs=[PATCH + 'lockup-stacked.png', J + 'jacket-spec-sheet.png']),
    dict(id='cuff-right-nexus', order=9, aspect='3:2',
         add='Close detail of her right wrist and cuff. The word NEXUS in white block '
             'capitals wraps around the cuff. Thumbhole visible. Plain mid-grey '
             'background, soft even light.',
         refs=[PATCH + 'lockup-stacked.png', J + 'jacket-spec-sheet.png']),
    dict(id='hood-down-collar', order=10, aspect='3:2',
         add='Close detail from behind of the hood worn down and bunched behind the neck, '
             'showing the raglan seams and back yoke. Plain mid-grey background, soft '
             'even light.',
         refs=[P + 'd-collar.png', J + 'jacket-flat-back.png']),
    dict(id='with-pack-back', order=11, aspect='2:3',
         add='Full figure from behind wearing a rust-orange hiking pack over the shell. A '
             'dark red rectangular embroidered patch reading TERRA NEXUS sits centred on '
             "the pack's upper front panel. Golden hour, low sun, alpine ridge.",
         refs=[P + 'back.png', PATCH + 'patch-colourways-on-bag.png',
               SCENES + '9. Story 6 - FINAL.png']),
    dict(id='in-world-action', order=12, aspect='2:3',
         add='Standing on an alpine ridge at golden hour, looking out across a valley, '
             'wearing the pack. Warm rim light on hair and shoulders. Matches the look of '
             'the existing story set.',
         refs=[SCENES + '1. Opening Scene - FINAL.png', '@id-face-front']),
]

JACKET_SHOTS = [
    dict(id='jacket-front', order=13, aspect='2:3', base='jacket',
         add='Front view, straight on, sleeves hanging naturally.',
         refs=[J + 'jacket-flat-front.png', J + 'jacket-spec-sheet.png',
               'Output Drafts/Character/character-turnaround.png']),
    dict(id='jacket-back', order=14, aspect='2:3', base='jacket',
         add='Back view, straight on, showing the back yoke, the princess seams and the '
             'scooped centre back hem.',
         refs=[J + 'jacket-flat-back.png', J + 'jacket-spec-sheet.png']),
    dict(id='jacket-three-quarter', order=15, aspect='2:3', base='jacket',
         add='Turned about 40 degrees, three-quarter view, so the side seam and the waist '
             'shaping read.',
         refs=[J + 'jacket-flat-front.png', J + 'jacket-flat-back.png']),
    dict(id='jacket-cuff-terra', order=16, aspect='3:2', base='jacket',
         add='Close detail of the left cuff only. The word TERRA in white block capitals '
             'wraps around the cuff. Thumbhole visible. The cuff lies flat.',
         refs=[J + 'cuff-terra.png', PATCH + 'lockup-stacked.png']),
    dict(id='jacket-cuff-nexus', order=17, aspect='3:2', base='jacket',
         add='Close detail of the right cuff only. The word NEXUS in white block capitals '
             'wraps around the cuff. Thumbhole visible. The cuff lies flat.',
         refs=[J + 'cuff-nexus.png', PATCH + 'lockup-stacked.png']),
    dict(id='jacket-hood', order=18, aspect='3:2', base='jacket',
         add='Close detail from behind of the hood worn down and bunched behind the neck, '
             'showing the raglan seams meeting the back yoke.',
         refs=[J + 'jacket-flat-back.png', P + 'd-collar.png']),
    dict(id='jacket-navy', order=19, aspect='2:3', base='jacket',
         add='Front view, but the shell is Terra Nexus Navy #131F48 instead of glacier '
             'blue. Cuff wordmarks stay white.',
         refs=[J + 'jacket-flat-front-navy.png', J + 'jacket-colourways.png']),
    dict(id='jacket-deep-red', order=20, aspect='2:3', base='jacket',
         add='Front view, but the shell is Terra Nexus Deep Red #6A1B32 instead of glacier '
             'blue. Cuff wordmarks stay white.',
         refs=[J + 'jacket-flat-front-red.png', J + 'jacket-colourways.png']),
]

SHOTS = SHOTS + JACKET_SHOTS

CHECKS = [
    'Same face as shot 1, not a lookalike',
    'Ponytail present, mid-height, loose strands at the crown',
    'Jacket fitted through the waist, not boxy',
    'Hood down',
    'Shoulders and chest completely clean - no patch, no logo, no mark',
    'Cuffs lie flat, thumbholes present',
    'Cuff wording spelled correctly and reading the right way round',
    'Jacket blue matches #5A90BE - not teal, not navy',
    'One person in frame, no text overlay',
]


def payload():
    return {
        'base_prompt': BASE,
        'negative_prompt': NEGATIVE,
        'face_is_a_proposal': True,
        'output_dir': 'Output Drafts/Character/plates/generated',
        'rebuild_command': 'sh "Output Drafts/Character/build/make.sh"',
        'reference_note': "Paths are from the repository root. '@id' means attach the "
                          'image generated by that earlier shot.',
        'jacket_base_prompt': JACKET_BASE,
        'base_url': REPO_RAW,
        'shots': [
            dict(
                s,
                group='jacket' if s.get('base') == 'jacket' else 'character',
                prompt=(JACKET_BASE if s.get('base') == 'jacket' else BASE) + '\n\n' + s['add'],
                references=[
                    {'kind': 'shot', 'shot': r[1:]} if r.startswith('@')
                    else {'kind': 'url', 'path': r, 'url': url(r)}
                    for r in s['refs']
                ],
            )
            for s in SHOTS
        ],
        'acceptance_checks': CHECKS,
    }


def check():
    """Every reference the brief names must actually be in the repo."""
    root = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
    ids = {s['id'] for s in SHOTS}
    bad = []
    for s in SHOTS:
        for r in s['refs']:
            if r.startswith('@'):
                if r[1:] not in ids:
                    bad.append((s['id'], r, 'unknown shot'))
            elif not os.path.isfile(os.path.join(root, r)):
                bad.append((s['id'], r, 'missing file'))
    for shot, ref, why in bad:
        print(f'  BAD  {shot}: {ref}  ({why})')
    print(f'{len(SHOTS)} shots, '
          f'{sum(len(s["refs"]) for s in SHOTS)} references, {len(bad)} broken')
    return 1 if bad else 0


if __name__ == '__main__':
    if '--check' in sys.argv:
        sys.exit(check())
    if '--json' in sys.argv:
        path = os.path.join(OUT, 'shots.json')
        json.dump(payload(), open(path, 'w'), indent=2)
        print(f'wrote {os.path.relpath(path, OUT)}')
    else:
        for s in SHOTS:
            g = 'jacket' if s.get('base') == 'jacket' else 'character'
            print(f"{s['order']:2d}  {s['id']:<20} {g:<9} {s['aspect']:<4} "
                  f"{len(s['refs'])} refs{'  [LOCK]' if s.get('lock') else ''}")
