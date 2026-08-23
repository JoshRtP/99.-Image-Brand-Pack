# Profile set prompt — for a normal Claude session with image generation

For claude.ai rather than Claude Code. It assumes **nothing is fetched** — you
attach the reference and the prompt carries everything else in text, so it works
whether or not that session has web access.

## Attach these

**Required** — `Output Drafts/Character/plates/generated/id-face-front.png`

**Helpful, if the cuffs will be in frame** —
`Output Drafts/Jacket/jacket-flat-front.png`

---

```
I'm building a character reference set for an outdoor brand called Terra Nexus.
The attached photograph is the locked reference for the character. This is her.
Every image you generate must match this face — treat it as an identity anchor,
not as loose inspiration. A similar-looking woman is a failed result.

Generate a series of profile images: same woman, same jacket, same lighting
setup, at a range of angles, so the set reads as one shoot. Match the attached
reference's plain mid-grey seamless background and soft, even, shadowless studio
light. Same camera height, same distance, same 50mm-equivalent lens look.

WHO SHE IS
Late thirties. Athletic build, about 168 cm. Oval face with a defined jaw and a
straight nose. Sun-weathered skin with a warm undertone and clear freckling
across the nose and upper cheeks. Green-hazel eyes, strong straight mid-brown
brows, fine lines at the eyes. No makeup. Mouth closed, expression level and
unsmiling — self-possessed rather than posed. Mid-brown hair with sun-lightened
caramel highlights, pulled back off the face into a mid-height ponytail, with
loose curling strands escaping at the temples and crown.

WHAT SHE IS WEARING
A slim, close-fitting single-layer hooded wind shell in glacier blue (#5A90BE).
Raglan sleeves. Princess seams front and back running from the raglan seam
through the waist to the hem, giving a clearly nipped waist. Hood worn down and
bunched behind the neck. Full-length front zip, closed, with a small dark zip
pull. Long shaped cuffs that lie flat — not gathered, not elasticated.

THE SHOTS — name each image by its id

  1. front-portrait   head and shoulders, square to camera
  2. tq-left-portrait head and shoulders, turned about 40 degrees to her left
  3. tq-right-portrait head and shoulders, turned about 40 degrees to her right
  4. profile-left     head and shoulders, full left profile
  5. profile-right    head and shoulders, full right profile
  6. front-half       waist up, square to camera, arms relaxed at her sides
  7. tq-half          waist up, turned about 40 degrees
  8. back-head        head and shoulders from behind, showing the ponytail and
                      the hood bunched at the back of the neck

RULES — this is where results usually go wrong

  • Her face must match the attached reference in every image.
  • Hair is always a mid-height ponytail with loose strands escaping. Never
    loose, never braided, never tucked into the hood.
  • The jacket carries NO marking on the shoulder, upper arm or chest. It is
    completely clean there. If any logo, patch or badge appears, the image is
    wrong — regenerate it.
  • If a cuff comes into frame, it reads TERRA around her left wrist and NEXUS
    around her right, in white block capitals. No other lettering anywhere on
    the garment.
  • Hood always down. Never worn up.
  • One person in frame. No text overlay, no watermark, no border.

START WITH SHOT 1 ONLY. Show it to me so I can confirm the face carries across
before you spend effort on the rest. Once I confirm, generate 2 through 8.
```

---

## After the profile set

Once the face is proven consistent across angles, move to the full set — 26
shots covering the jacket as a product and the series of her carrying the pack:

`Output Drafts/Character/HANDOFF-PROMPT.md`
