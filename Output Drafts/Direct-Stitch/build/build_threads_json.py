"""Emit threads.json - one file an agent can fetch to use the thread patterns.

Generated from build_stitch.THREADS so the published data cannot drift from the
artwork it describes.
"""
import json, os
import build_stitch as S

RAW = ('https://raw.githubusercontent.com/JoshRtP/99.-Image-Brand-Pack/'
       'main/Output%20Drafts/Direct-Stitch/')

PHRASE = {
    'deep-red': 'a deep oxblood red only slightly darker than the rust-orange fabric',
    'warm-charcoal': 'a warm dark charcoal, close in value to the rust-orange fabric',
    'olive': 'a deep olive green, close in value to the rust-orange fabric',
    'slate-purple': 'a muted slate purple, close in value to the rust-orange fabric',
    'ink': 'a near-black ink blue, darker than the rust-orange fabric',
    'sand': 'a pale sand yellow that contrasts clearly against the rust-orange fabric',
}
NOTE = {
    'deep-red': 'Recommended. Effectively invisible as colour on shaded fabric; '
                'stays warm so it never reads as a stain; ties to the Deep Red patch.',
    'warm-charcoal': 'Most consistent - contrast barely moves between shade and full sun.',
    'olive': 'Quietest overall across all lighting.',
    'slate-purple': 'Quiet, but casts cooler than the fabric.',
    'ink': 'Quiet in shade, reads clearly dark in direct sun.',
    'sand': 'Control. This is what NOT blending looks like - do not use to blend.',
}

BASE = ('On the pack\'s upper front panel, the words TERRA and NEXUS are embroidered '
        'directly into the fabric in heavy block capitals - TERRA on the first line, '
        'NEXUS directly beneath it, both lines the same width with their left edges '
        'aligned, forming a squared-off block about {width:.0f} mm wide. The thread is '
        '{thread}, so the lettering reads mostly as raised texture and catches the light '
        'along its top edges. The stitching stands proud of the panel and casts a soft '
        'shadow. There is no patch, no border, no background panel behind the letters, '
        'and no other graphic.')


def payload():
    return {
        'name': 'Terra Nexus direct raised stitch',
        'summary': 'Block wordmark embroidered straight onto the pack panel, tone on '
                   'tone. Replaces the sewn patch - do not run both.',
        'arrangement': {
            'stack': 'TERRA directly over NEXUS',
            'alignment': 'left edges aligned, both lines tracked to the same width',
            'note': 'This is NOT the approved lockup, which indents NEXUS by 0.592 cap '
                    'heights and carries the star. Squared off for reliable generation.',
            'star': 'omitted - the star cannot be foamed at this size',
        },
        'geometry_mm': {
            'width': round(S.WORD_W, 2), 'height': round(S.WORD_H, 2),
            'cap_height': round(S.CAP_MM, 2), 'stem': round(S.STEM_MM, 2),
            'narrowest_bar': round(S.BAR_MM, 2), 'minimum_width': 55,
        },
        'fabric_reference': {
            'sunlit': S.FABRIC_LIT, 'mid': S.FABRIC_MID, 'shadow': S.FABRIC_SHADOW,
            'source': 'sampled from the story set',
        },
        'construction': {
            'method': '3D foam satin, 2 mm foam under the columns',
            'underlay': 'centre-run plus edge-walk, 0.25 mm inset',
            'pitch_mm': 0.38,
            'backing': 'cut-away, 50 g',
            'placement': 'centred on the upper front panel, top of the wordmark 40 mm '
                         'below the lid seam',
        },
        'production_artwork': RAW + 'stitch-flat.svg',
        'comparison_sheet': RAW + 'stitch-colourways.png',
        'spec_sheet': RAW + 'stitch-spec-sheet.png',
        'recommended': S.PRIMARY,
        'threads': [
            {
                'id': k,
                'name': S.THREADS[k][0],
                'hex': S.THREADS[k][1],
                'contrast_on_shaded_fabric': S.THREADS[k][2],
                'contrast_in_sunlight': S.THREADS[k][3],
                'note': NOTE[k],
                'prompt_phrase': PHRASE[k],
                'scene_prompt': BASE.format(width=S.WORD_W, thread=PHRASE[k]),
                'swatch_on_fabric': RAW + f'stitch-{k}.png',
                'transparent_plate': RAW + f'stitch-{k}-alpha.png',
            }
            for k in ['deep-red', 'warm-charcoal', 'olive', 'slate-purple', 'ink', 'sand']
        ],
    }


if __name__ == '__main__':
    path = os.path.join(S.OUT, 'threads.json')
    json.dump(payload(), open(path, 'w'), indent=2)
    print('wrote threads.json')
