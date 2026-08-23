# Character generation brief — main character, wind shell Rev B

Everything an image generator needs to produce the character sheet. Twelve shots,
each with its own prompt and its own reference files. Run them in the order
below — shot 1 locks her face, and every shot after it depends on that lock.

Drop the results in `plates/generated/` using the shot IDs as filenames, then run
`sh "Output Drafts/Character/build/make.sh"` and the sheet rebuilds itself around
them.

---

## 0. Before you generate anything

### Where the generator should look

All paths are from the repository root. Attach these as image references — most
tools call this "reference image", "style reference" or "image prompt".

**Who she is** — hair, build, styling, how she photographs:

| File | What it establishes |
| --- | --- |
| `Output Drafts/Character/plates/back.png` | Full figure from behind, build and proportion |
| `Output Drafts/Character/plates/tq-back-left.png` | Three-quarter back, shoulder line |
| `Output Drafts/Character/plates/near-profile.png` | The closest thing to a profile that exists — jaw, ear, hairline |
| `Output Drafts/Character/plates/d-head.png` | Hair: mid-height ponytail, loose crown strands |
| `Output Drafts/Character/plates/d-collar.png` | Hood worn down and bunched behind the neck |

**What she wears** — the Rev B garment, which no photograph shows yet:

| File | What it establishes |
| --- | --- |
| `Output Drafts/Jacket/jacket-flat-front.png` | Front: zip, pockets, raglan, princess seams, cuffs |
| `Output Drafts/Jacket/jacket-flat-back.png` | Back: yoke, princess seams, scooped hem |
| `Output Drafts/Jacket/jacket-spec-sheet.png` | Dimensions, and the cuff wordmarks at legible size |
| `Output Drafts/Character/character-turnaround.png` | The slim cut on a body, all five angles |
| `Output Drafts/Jacket/jacket-colourways.png` | Glacier Blue against the alternates |

**Letterforms and marks** — so the type is right, not approximated:

| File | What it establishes |
| --- | --- |
| `Output Drafts/Patch/lockup-stacked.png` | The exact TERRA / NEXUS block capitals |
| `Output Drafts/Patch/patch-embroidered-red.png` | The Deep Red pack patch |
| `Output Drafts/Patch/patch-colourways-on-bag.png` | How the patch sits on the pack at true scale |

**The pack and the world** — only for the in-world shots (11–12):

| File | What it establishes |
| --- | --- |
| `Ouput Pictures - Updated Images/9. Story 6 - FINAL.png` | The pack, and the grade of the set |
| `Ouput Pictures - Updated Images/1. Opening Scene - FINAL.png` | Golden-hour light, alpine setting |
| `Branding/Example of star logo on jacket.png` | The pack in close-up |
| `Branding/Screenshot of Extended Colors for Branding.png` | The brand palette |

> `Branding/Backpack-LogoPatch.png` is the same pack photograph and exists on
> `main`, but not on this branch. Either is fine.

### Her face does not exist yet

No frame in the set shows it. Below is a **proposal**, not a fact — edit it
before you run shot 1, because whatever comes out of shot 1 becomes canon.

```
Late twenties to early thirties. Oval face with a defined jaw and a straight
nose. Fair skin with a warm undertone, light freckling across the nose and
cheekbones, weathered slightly by sun and wind. Grey-green eyes, mid-brown
eyebrows. No makeup beyond what survives a day outdoors. Calm, focused
expression — attentive rather than smiling.
```

### Two lighting setups

- **Studio** (shots 1–10): plain mid-grey seamless background, soft even light,
  no coloured cast. These are costume and identity references — the garment has
  to read, so nothing dramatic.
- **In-world** (shots 11–12): golden hour, low sun behind or beside her, warm rim
  on hair and shoulders, alpine setting. These match the story set.

### Technical

| | |
| --- | --- |
| Long edge | 2048 px minimum |
| Aspect | 2:3 portrait for full figure, 1:1 for head, 3:2 for detail |
| Lens look | 50 mm equivalent, mild subject separation, no wide-angle distortion |
| Format | PNG |

---

## 1. The base block

Paste this **verbatim into every shot**, then add that shot's own line. Do not
paraphrase it between shots — drift starts here.

```
A woman in her late twenties, athletic build, about 168 cm tall. Mid-brown hair
with warm highlights, pulled into a mid-height ponytail, loose flyaway strands
at the crown. [FACE DESCRIPTION FROM ABOVE].

She wears the Terra Nexus wind shell: a slim, close-fitting single-layer hooded
shell in glacier blue (#5A90BE). Raglan sleeves. Princess seams front and back
running from the raglan seam through the waist to the hem, giving a clearly
nipped waist. Hood worn down, bunched behind the neck. Full-length front zip,
closed, with a small red zip pull. Two zipped hand pockets. Long shaped cuffs
with thumbholes, lying flat — not gathered or elasticated. Hem falls to the hip
and is scooped slightly lower at centre back.

Block capitals wrap the cuffs: TERRA around the left wrist, NEXUS around the
right, printed in white. The jacket carries no other marking of any kind.

Below: slim dark charcoal technical trousers and low brown approach boots.

Photographic, sharp, natural skin texture.
```

## 2. Hard rules — put these in the negative prompt

```
patch or logo on the shoulder, upper arm or chest; mountain graphic; any text
other than TERRA and NEXUS on the cuffs; boxy, oversized or loose fit; parka;
hood worn up; gathered or elasticated cuffs; hair loose or braided; sunglasses;
hat; gloves; second person in frame; visible brand names other than Terra Nexus;
text overlay; watermark
```

---

## 3. The shots

Generate in this order. **Do not skip the lock step.**

### Shot 1 — `id-face-front` · LOCK THIS FIRST
Head and shoulders, front, square to camera. 1:1.
Add: `Head and shoulders portrait, facing camera directly, neutral expression, plain mid-grey background, soft even studio light.`
References: `plates/near-profile.png`, `plates/d-head.png`

> Generate four or five. Pick one. **That image is now the identity reference for
> every remaining shot** — attach it to all of them. Save your pick as
> `plates/generated/id-face-front.png` before continuing.

### Shot 2 — `id-face-tq`
Head and shoulders, turned 40°. 1:1.
Add: `Head and shoulders portrait, turned about 40 degrees from camera, plain mid-grey background, soft even studio light.`
References: shot 1, `plates/d-head.png`, `plates/d-collar.png`

### Shot 3 — `full-front`
Full figure, front. 2:3.
Add: `Full figure standing square to camera, arms relaxed at her sides, plain mid-grey seamless background, soft even studio light.`
References: shot 1, `Output Drafts/Jacket/jacket-flat-front.png`, `Output Drafts/Character/character-turnaround.png`

### Shot 4 — `full-tq-front`
Full figure, turned 40°. 2:3.
Add: `Full figure turned about 40 degrees from camera, arms relaxed, plain mid-grey seamless background, soft even studio light.`
References: shot 1, `Output Drafts/Jacket/jacket-flat-front.png`

### Shot 5 — `full-side`
Full figure, profile. 2:3.
Add: `Full figure in full profile, side on, arms relaxed, plain mid-grey seamless background, soft even studio light.`
References: shot 1, `Output Drafts/Character/character-turnaround.png`

### Shot 6 — `full-tq-back`
Full figure, turned 140°. 2:3.
Add: `Full figure turned about 140 degrees, seen mostly from behind, plain mid-grey seamless background, soft even studio light.`
References: shot 1, `Output Drafts/Jacket/jacket-flat-back.png`, `plates/tq-back-left.png`

### Shot 7 — `full-back`
Full figure, back. 2:3.
Add: `Full figure seen directly from behind, arms relaxed, plain mid-grey seamless background, soft even studio light.`
References: `Output Drafts/Jacket/jacket-flat-back.png`, `plates/back.png`

### Shot 8 — `cuff-left-terra`
Detail. 3:2.
Add: `Close detail of her left wrist and cuff, arm relaxed at her side. The word TERRA in white block capitals wraps around the cuff. Thumbhole visible. Plain mid-grey background, soft even light.`
References: `Output Drafts/Patch/lockup-stacked.png`, `Output Drafts/Jacket/jacket-spec-sheet.png`

### Shot 9 — `cuff-right-nexus`
Detail. 3:2.
Add: `Close detail of her right wrist and cuff. The word NEXUS in white block capitals wraps around the cuff. Thumbhole visible. Plain mid-grey background, soft even light.`
References: `Output Drafts/Patch/lockup-stacked.png`, `Output Drafts/Jacket/jacket-spec-sheet.png`

### Shot 10 — `hood-down-collar`
Detail. 3:2.
Add: `Close detail from behind of the hood worn down and bunched behind the neck, showing the raglan seams and back yoke. Plain mid-grey background, soft even light.`
References: `plates/d-collar.png`, `Output Drafts/Jacket/jacket-flat-back.png`

### Shot 11 — `with-pack-back`
Full figure with the pack. 2:3.
Add: `Full figure from behind wearing a rust-orange hiking pack over the shell. A dark red rectangular embroidered patch reading TERRA NEXUS sits centred on the pack's upper front panel. Golden hour, low sun, alpine ridge.`
References: `plates/back.png`, `Output Drafts/Patch/patch-colourways-on-bag.png`, `Ouput Pictures - Updated Images/9. Story 6 - FINAL.png`

### Shot 12 — `in-world-action`
In-scene. 2:3.
Add: `Standing on an alpine ridge at golden hour, looking out across a valley, wearing the pack. Warm rim light on hair and shoulders. Matches the look of the existing story set.`
References: `Ouput Pictures - Updated Images/1. Opening Scene - FINAL.png`, shot 1

---

## 4. Check every image before you keep it

Reject and regenerate if any of these fail:

- [ ] Same face as shot 1 — not a lookalike
- [ ] Ponytail present, mid-height, loose strands at the crown
- [ ] Jacket is **fitted through the waist**, not boxy
- [ ] Hood is **down**
- [ ] Shoulders and chest are **completely clean** — no patch, no logo, no mark
- [ ] Cuffs lie flat, thumbholes present
- [ ] On cuff shots, the word is spelled correctly and reads the right way round
- [ ] Jacket blue matches `#5A90BE` — not teal, not navy
- [ ] One person in frame, no text overlay

Cuff text is the shot most likely to fail. If the generator cannot spell it, take
the best cuff shape and say so — the wordmark can be composited from
`Output Drafts/Patch/lockup-stacked.png` afterwards.

---

## 5. Hand it back

```
Output Drafts/Character/plates/generated/
    id-face-front.png
    id-face-tq.png
    full-front.png
    full-tq-front.png
    full-side.png
    full-tq-back.png
    full-back.png
    cuff-left-terra.png
    cuff-right-nexus.png
    hood-down-collar.png
    with-pack-back.png
    in-world-action.png
```

Then:

```sh
sh "Output Drafts/Character/build/make.sh"
```

The sheet picks up whatever is present, adds a generated row, and drops the
"no reference exists" panel for the angles you have covered. Partial sets are
fine — it builds with whatever is there.
