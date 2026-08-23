# Story scenes — full regeneration, Rev B

Two rounds of compositing (patch swaps, sleeve-mark swaps, cuff wordmarks) got
the story set closer to on-brand but hit a hard ceiling: a composite can only
warp what's already in the photo. It can't fix a patch that was never drawn at
a consistent real-world size to begin with, and it can't put the actual Rev B
slim-cut jacket into a photo that was shot in the old loose one. Both of those
are still visible in `Ouput Pictures - Updated Images/` despite three rounds of
alignment fixes.

This folder is the alternative: regenerate every scene from a text-to-image
prompt with the correct branding **baked in at generation time** — patch,
jacket cut, cuff wordmarks, character identity — instead of composited on
after. Same story beats, same numbering, same roles; new pixels.

**`GENERATION-BRIEF.md` is the deliverable.** Fourteen shots — the ten numbered
story scenes plus their two alternates and two collage-only vignettes — each
with its full prompt, its reference images, and what to check before accepting
it. `scenes.json` is the same list, machine-readable.

---

## Why fourteen generations, not twelve numbered scenes

Three of the twelve numbered images are not independent photographs — they're
collages that reuse other images in the set as panels:

| Numbered scene | What it actually is |
| --- | --- |
| `2. Transition to trellis` | `1. Opening Scene` on top, the checklist/gear flatlay on the bottom |
| `3. Example story trellis` | `1. Opening Scene` as the top banner, five small panels in the middle row, the checklist/gear flatlay as the bottom banner |

Generating those two "from scratch" a second time would produce a *different*
photo of the same moment sitting right next to the real one — same character,
same pose, subtly different pixels, immediately visible as a mismatch. So this
brief generates every unique piece of photography exactly once (the ten
numbered scenes, their two alternates, and the two small vignettes that exist
only inside the trellis's middle row), then **assembles** scenes 2 and 3 from
those pieces with a compositing script, the same way a print designer lays out
a collage from finished photographs rather than re-shooting the whole page.

## What locks every shot together

- **Character** — `Output Drafts/Character/character-sheet.png` and, once run,
  `Output Drafts/Character/plates/generated/id-face-front.png`. Same person in
  every frame that shows her.
- **Jacket** — `Output Drafts/Jacket/` Rev B: slim athletic fit, Glacier Blue
  `#5A90BE`, hood down, cuffs read TERRA / NEXUS, nowhere else on the garment.
- **Patch** — `Output Drafts/Patch/`: the stacked lockup with the star, Deep
  Red `#6A1B32`, worn/faded, 63 mm finished width, centred on the pack's upper
  front panel, same real-world size in every scene it appears.
- **Copy fix** — the notebook reads "For Auditor" in the original set; every
  regenerated instance corrects this to "ISO Auditor," handwritten treatment
  kept.

None of this is guessed — it's pulled from the specs already in
`Output Drafts/Jacket/README.md`, `Output Drafts/Patch/README.md` and
`Output Drafts/Character/README.md`. This brief is what turns those specs into
per-scene prompts.

## Before you run it

Read `Output Drafts/Character/GENERATION-BRIEF.md` first if
`plates/generated/id-face-front.png` doesn't exist yet — every shot in *this*
brief that shows her face or full figure depends on that lock existing first.
Skip it if she's face-down-the-frame or back-only in every shot you're
generating (most of this set is), but the moment a front or three-quarter face
is needed, that lock has to exist.

## Hand it back

```
Output Drafts/Scenes/generated/
    1-opening-scene.png
    checklist-notebook.png
    4-story-1-compass.png
    5-story-2-rangefinder.png
    5a-story-2-rangefinder-alt.png
    6-story-3-gear.png
    7-story-4-map-planned.png
    8-story-5-map-altroute.png
    9-story-6-hazard.png
    10-outro-stargaze.png
    10a-outro-stargaze-alt.png
    vignette-taking-photo.png
    vignette-writing-map-planned.png
    vignette-writing-map-altroute.png
```

Then run the assembly script (once written — see `build/` — mirroring the
approach in `Output Drafts/Patch/build/compose.py`) to lay out scenes 2 and 3
from these pieces, and this folder replaces `Input Pictures - Story Based/` as
the source the rest of the package builds from.
