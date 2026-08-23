# Pack set prompt — for a normal Claude session with image generation

The companion to `../Character/PROFILE-SET-PROMPT.md`. Same shape, same reason:
written for claude.ai rather than Claude Code, so **nothing is fetched** — you
attach the references and the prompt carries everything else in text.

## Attach these — both, in this order

1. **`Output Drafts/Pack/pack-ref-front-stitched.png`** — the pack itself. This
   is the construction and colour anchor. It is the story-set pack with the old
   sewn patch taken out and the direct stitch put on, so it is the only image in
   the repo that shows the pack as it should now look.
2. **`Output Drafts/Direct-Stitch/stitch-deep-red.png`** — the wordmark alone,
   large, in Deep Red thread on pack fabric. The letterforms and the raised
   satin relief read clearly here and nowhere else at this size.

Optional, only if you want the two worn shots at the end: the eight-up character
sheet from the profile set, so she matches.

---

```
I'm building a product reference set for an outdoor brand called Terra Nexus.
The two attached images are the locked references for a backpack.

Image 1 is the pack itself — its shape, colour, hardware and wear. Image 2 is a
close-up of the branding stitched into its lid. Treat both as identity anchors,
not as loose inspiration. A similar-looking pack is a failed result.

Generate a product turnaround: the same pack, same lighting setup, rotated
through a range of angles so the set reads as one shoot. Put it on a plain
mid-grey seamless background under soft, even, shadowless studio light, with a
small contact shadow where it meets the floor. Same camera height, same
distance, same 50mm-equivalent lens look in every frame.

WHAT THE PACK IS
A technical hiking daypack, roughly 30 litres, in rust orange — a burnt, earthy,
slightly desaturated orange. Not safety orange, not tan. Matte ripstop nylon
with a low sheen. It is used, not new: faint trail dust, a few small scuffs,
softened corners.

Construction, all of it visible in image 1:
  • A rounded top lid flap over a horseshoe zip, closing over the main body.
  • A large front pocket panel below the lid, with a vertical seam down its
    centre and bar-tacked stress points.
  • Two vertical charcoal webbing compression straps down the front, each with
    a black side-release buckle.
  • Dual charcoal side compression straps, buckled.
  • Grey-olive stretch mesh side pockets, one each side.
  • Charcoal zip tape with grey cord pulls.
  • Padded charcoal shoulder straps with a sternum strap, a dark hip belt, and a
    charcoal grab handle at the top of the lid.
  • Black plastic hardware throughout. No branding on any of it.

THE BRANDING — one mark, one place
On the lid flap, on the upper front, sitting left of the lid's centre: the words
TERRA and NEXUS embroidered directly into the fabric in heavy block capitals.

  • TERRA on the first line. NEXUS directly beneath it.
  • Both lines exactly the same width, left edges flush — a squared-off block.
  • About 85 mm wide, so roughly a third of the lid's width.
  • The thread is a faded deep oxblood red (#6A1B32), only slightly darker than
    the rust-orange fabric. It reads mostly as raised texture, catching the
    light along the top edge of each stroke, not as a colour.
  • Raised satin stitch, sitting proud of the fabric, with a visible stitch
    direction across each stroke.
  • NO patch. No border. No rectangle, panel or badge of any kind behind the
    letters. The stitching goes straight into the pack fabric.

THE SHOTS — name each image by its id

  1. pack-front        square to camera, lid and branding facing the lens
  2. pack-tq-left      rotated about 40 degrees, its left side toward camera
  3. pack-tq-right     rotated about 40 degrees, its right side toward camera
  4. pack-side-left    full left profile, showing the side pocket and
                       compression straps
  5. pack-side-right   full right profile
  6. pack-back         the harness side: shoulder straps, back panel, hip belt
  7. pack-top          from above and slightly in front, looking down onto the
                       lid, branding readable
  8. pack-detail-stitch  macro of the lid, the wordmark filling most of the
                       frame, raised stitching clearly visible

RULES — this is where results usually go wrong

  • It is the SAME pack in every frame: same colour, same hardware, same scuffs
    in the same places. Not a family of similar packs.
  • The wordmark exists in exactly ONE place, on the lid. Every other surface is
    completely unbranded — the front pocket panel, both sides, the bottom, the
    back panel, the shoulder straps, the hip belt, the buckles, the zip pulls.
    If a logo, patch, badge, star, mountain or lettering appears anywhere else,
    the image is wrong — regenerate it.
  • TERRA is always ABOVE NEXUS. Never side by side, never on one line, never
    reversed.
  • Angles are described from the pack's own left and right, so in shot 2 the
    pack's left side appears on the RIGHT of your frame, and in shot 3 its right
    side appears on the LEFT. Check this before you finish each image.
  • In shots 4, 5 and 6 the branding is on the far side of the pack and should
    be partly hidden or not visible at all. Do not add a second copy to keep it
    in frame.
  • One object in frame. No props, no model, no text overlay, no watermark, no
    border, no reflection floor.

START WITH SHOT 1 ONLY. Show it to me so I can confirm the pack and the stitching
carry across before you spend effort on the rest. Once I confirm, generate 2
through 8.
```

---

## The two worn shots

Only worth doing once the eight product angles are approved and the character
profile set exists. Attach the character sheet alongside the two pack
references, and add:

```
Now two shots of her wearing it. Same woman as the attached character sheet,
same glacier blue hooded shell, same ponytail. Same grey seamless background and
studio light as the pack set.

  9. pack-worn-back  full figure from behind, wearing the pack on both
                     shoulders, the lid branding readable over her shoulders
 10. pack-worn-tq    full figure turned about 40 degrees, one strap on, the pack
                     hanging off the near shoulder

Her jacket carries no marking anywhere on it — not on the shoulder, the upper
arm, the chest or the back. The only lettering on the jacket is TERRA around her
left cuff and NEXUS around her right, and only if a cuff is in frame.
```

---

## Files

| File | What it is |
| --- | --- |
| `pack-ref-front-stitched.png` | The pack, patch removed, Deep Red stitch applied. The reference to attach. |
| `build/build_refs.py` | Rebuilds it from the untouched story frame. |

The branding geometry, thread ranking and production spec live in
`../Direct-Stitch`. This folder holds only what an image generator needs.
