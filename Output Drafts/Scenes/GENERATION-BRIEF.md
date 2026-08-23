# Story scene generation brief — full regeneration, Rev B branding

Everything an image generator needs to regenerate the story set with the
correct patch and jacket branding **baked in**, instead of composited on
afterward. Fourteen shots, each with its own prompt and its own reference
files. Run them in the order below — several depend on the character identity
lock and the collage assembly at the end depends on every hero shot existing.

Drop results in `generated/` using the shot IDs as filenames (see the list at
the end), then run the assembly step to build the two collage scenes.

---

## 0. Before you generate anything

### The identity lock

If `Output Drafts/Character/plates/generated/id-face-front.png` does not exist
yet, go run `Output Drafts/Character/GENERATION-BRIEF.md` shot 1 first and
save the pick there. Every shot below that shows her face or full figure
attaches that file as a reference. Shots that are back-only, hands-only, or
prop-only (most of this set) don't need it, but generate it before you hit the
first shot that does — re-picking a face partway through is how identity drift
starts.

### Reference files, what each establishes

**Who she is and what she wears** — attach to every shot that shows her:

| File | Establishes |
| --- | --- |
| `Output Drafts/Character/character-sheet.png` | Identity, styling, how she photographs from the angles the story set actually uses |
| `Output Drafts/Character/plates/generated/id-face-front.png` | Locked face (once it exists) |
| `Output Drafts/Jacket/jacket-flat-back.png` | Jacket back: yoke, princess seams, scooped hem — the story set is back/three-quarter-back throughout |
| `Output Drafts/Jacket/jacket-colourways.png` | Glacier Blue, precisely |

**The patch** — attach to every shot that shows the pack:

| File | Establishes |
| --- | --- |
| `Output Drafts/Patch/patch-embroidered-red-worn.png` | The Deep Red patch, worn/faded treatment — the exact artwork, not an approximation |
| `Output Drafts/Patch/patch-colourways-on-bag.png` | Scale and placement on the pack, true to size |

**The world** — attach where noted per shot:

| File | Establishes |
| --- | --- |
| `Ouput Pictures - Updated Images/1. Opening Scene - FINAL.png` | Golden-hour grade, alpine backdrop, valley/river/peak layout to match |
| `Ouput Pictures - Updated Images/9. Story 6 - FINAL.png` | The pack in a full-figure back shot, for continuity of colour and wear |
| `Branding/Screenshot of Extended Colors for Branding.png` | Brand palette, for any UI/prop colour (map ink, device screens) |

### Technical

| | |
| --- | --- |
| Long edge | 2048 px minimum |
| Aspect | see per shot — landscape 3:2 for wide scenes, portrait 2:3 for verticals, per the original set |
| Lens look | 35–50 mm equivalent, photographic, golden-hour unless noted |
| Format | PNG |

---

## 1. The base block

Paste this **verbatim into every shot that shows her**, then add that shot's
own line. Do not paraphrase between shots.

```
A woman in her late twenties, athletic build, about 168 cm, mid-brown hair
pulled into a mid-height ponytail with loose flyaway strands at the crown.
[SAME FACE AS id-face-front.png IF THE SHOT SHOWS IT]. She wears the Terra
Nexus wind shell: a slim, close-fitting single-layer hooded shell in glacier
blue (#5A90BE), raglan sleeves, princess seams giving a nipped waist, hood worn
down and bunched behind the neck, full-length front zip closed. Long shaped
cuffs with thumbholes, lying flat. Block capitals wrap the cuffs: TERRA around
the left wrist, NEXUS around the right, printed in white. The jacket carries no
other marking of any kind — nothing on the shoulder, upper arm or chest. Slim
dark charcoal technical trousers, low brown approach boots. She carries a
rust-orange hiking backpack; a rectangular embroidered patch, dark red
(#6A1B32), lightly worn and faded, reading TERRA NEXUS with a small star
between the words, sits centred on the pack's upper front panel, just below
the lid seam — no mountain graphic, no other patch anywhere. Golden hour alpine
light, photographic, natural skin texture.
```

## 2. Hard rules — negative prompt, every shot

```
patch, logo or mark on the shoulder, upper arm or chest of the jacket; mountain
graphic on the pack patch; starless pack patch; second sewn patch anywhere;
boxy or oversized jacket fit; gathered or elasticated cuffs; hood worn up;
misspelled or garbled cuff text; misspelled or garbled patch text; "For
Auditor" (must read "ISO Auditor"); illegible or garbled sticker/label text;
second person in frame unless the shot calls for one; text overlay; watermark
```

---

## 3. The shots

### Shot A — `1-opening-scene` · generate before B, N, O
Landscape, 16:9. Golden-hour ridge overlook.
Prompt: `Seen from behind and slightly to the side, she stands on a rocky alpine ridge at golden hour, pointing with her right arm outstretched toward a distant snow-capped peak with a small flag at its summit. A river winds through a forested valley below between her and the mountain. Sun low near the horizon, dramatic clouds.` + base block.
References: `character-sheet.png`, `Ouput Pictures - Updated Images/1. Opening Scene - FINAL.png` (for backdrop layout to match, not for her branding).
Notes: this becomes the top panel of both collage scenes (2, 3) — get it right once.

### Shot B — `checklist-notebook`
Landscape, 3:2. Flatlay, no figure.
Prompt: `Overhead flatlay on dark rock: an open spiral-bound field notebook, left page a handwritten checklist reading "YOU ARE HERE / PLANNED PATH: 8 HOURS / ALTERNATE PATH: +4 HOURS (TOTAL: 12) / EQUIPMENT PACKED: 36 HOURS OF SUPPLIES / AREAS TO AVOID: KNOWN", signed "ISO Auditor" in a cursive signature with "valid: Aug. 2026 - July. 2028" beneath it and a small stamp reading "CLIMATE" above legible smaller text — right page a hand-drawn topographic map with a compass rose, a green "START (YOU ARE HERE)" marker, a dashed red "PLANNED PATH (8 HOURS)" line to a red triangle "DESTINATION" marker, a dashed blue "ALTERNATE PATH (+4 HOURS)" line, and a hatched red "DANGER — DO NOT ENTER" zone. Surrounding props: a steel camp mug, a red multi-tool knife, a coiled paracord, a steel insulated bottle. Warm directional light, photographic.` 
References: `Branding/climate-sticker-03-sunfaded-vintage.png` (for the stamp graphic), `Branding/Screenshot of Extended Colors for Branding.png`.
Notes: **every word above must render legibly and exactly as written** — this is the single most text-dense shot in the set and the one most likely to need hand-correction. "ISO Auditor" specifically corrects the original set's "For Auditor." Becomes the bottom panel of collages 2 and 3.

### Shot C — `4-story-1-compass`
Portrait, 2:3.
Prompt: `First-person point of view, her right hand holding an open brass compass at chest height, the needle pointing toward camera-left. Beyond the compass, an alpine valley at golden hour with a winding river and a flagged summit in the distance. Her forearm in the lower frame wears the glacier-blue jacket sleeve; the cuff reading NEXUS is visible near the wrist.` + base block (cuff line only, no face needed).
References: `character-sheet.png` (for jacket fabric/colour only).

### Shot D — `5-story-2-rangefinder`
Portrait, 2:3.
Prompt: `Seen from behind, over her shoulder, both hands raised holding a rugged handheld GPS rangefinder device toward the valley. The device screen shows coordinates "45.7821° N  121.5234° W", a radar-style distance graphic, and "DISTANCE: 9 MILES". Below in the valley, a small orange tent and a campfire with rising smoke are visible among the trees. Golden-hour ridge setting matching shot A.` + base block.
References: shot A output, `character-sheet.png`.

### Shot E — `5a-story-2-rangefinder-alt`
Portrait, 2:3. Alternate angle of D.
Prompt: same as D but `Seen from directly in front and slightly below, both hands raised holding the device toward camera height, both jacket cuffs visible — TERRA on her left wrist, NEXUS on her right — the mountain and flagged summit framed behind the device.` + base block.
References: shot A output, `character-sheet.png`, `Output Drafts/Patch/lockup-stacked.png` (letterform reference for both cuffs in one frame).
Notes: this is the shot most likely to need the cuff wordmarks hand-corrected afterward — see the acceptance checklist.

### Shot F — `6-story-3-gear`
Portrait, 2:3. Still life, no figure.
Prompt: `Close still-life on rocky ground at golden hour: a rust-orange hiking backpack standing upright, a rectangular dark red embroidered patch centred on its upper front panel reading TERRA NEXUS with a small star between the words. Beside it, a steel insulated water bottle, a steel camp mug, a red multi-tool knife, and the same open field notebook as the checklist shot, closed to show only its cover edge. A coiled rope rests against the pack.`
References: `Output Drafts/Patch/patch-embroidered-red-worn.png`, `Output Drafts/Patch/patch-colourways-on-bag.png`.
Notes: the patch is the entire subject of this shot — check it against the reference pixel-for-pixel before accepting.

### Shot G — `7-story-4-map-planned`
Portrait, 2:3.
Prompt: `Seen from behind and to the side, she holds up a folded paper topographic map at chest height with both hands, examining it. Hand-drawn on the map in blue ink: the word "eta" and "8 hours" near the top-left, a dashed blue route line curving up to an arrow near the top-right. Golden-hour valley and mountain visible past the map. Backpack over shoulders, TERRA NEXUS patch visible on its upper front panel where the strap doesn't cover it.` + base block.
References: shot A output, `character-sheet.png`.

### Shot H — `8-story-5-map-altroute`
Portrait, 2:3. Same setup as G, updated map.
Prompt: same as G but `the map now reads "alt route" and "+4 hours" in red ink near the top-left, with both a dashed red route line and a dashed blue route line converging toward a red triangle marker near the top-right.` + base block.
References: shot A output, `character-sheet.png`, shot G output (for consistent map paper/hand pose).

### Shot I — `9-story-6-hazard`
Portrait, 2:3.
Prompt: `Seen from behind, she stands facing an erupting volcano across a blackened lava field at golden hour — thick dark ash plume rising from the crater, glowing lava visible at the vent and in cracks running down the slope. To her right, a weathered wooden trail sign reads "FOAK SHORTCUT" in white block letters on rust-red metal. Backpack over shoulders, TERRA NEXUS patch visible on its upper front panel.` + base block.
References: `character-sheet.png`, `Output Drafts/Patch/patch-embroidered-red-worn.png`.

### Shot J — `10-outro-stargaze`
Landscape, 16:9. Dusk-to-night, not golden hour.
Prompt: `Wide shot from behind and above, she stands alone on a rocky outcrop at dusk, backpack on, looking out over a moonlit valley with a winding river toward two distant flagged peaks. Sky transitions from a fading orange horizon into deep blue-purple with visible stars.` + base block (drop "golden hour," use "dusk, fading light, stars emerging" instead).
References: `character-sheet.png`, shot A output (for terrain continuity).

### Shot K — `10a-outro-stargaze-alt`
Landscape, 16:9. Same setup as J, closer/different angle.
Prompt: same as J but framed closer, three-quarter back instead of directly behind, a third distant flagged peak visible at frame right.
References: shot J output, `character-sheet.png`.

### Shot L — `vignette-taking-photo` (trellis row-2 panel only)
Square-ish, 4:3.
Prompt: `Seen from behind and to the side, she holds a small handheld device up to eye level with both hands as if photographing the valley view — the device screen shows a preview of the mountain and river landscape. Golden-hour ridge setting matching shot A. Backpack over shoulders, TERRA NEXUS patch visible on its upper front panel.` + base block.
References: shot A output, `character-sheet.png`.

### Shot M — `vignette-writing-map-planned` (trellis row-2 panel only)
Square-ish, 4:3.
Prompt: `Seen from behind and to the side, she holds the folded topographic map from shot G against her forearm, marking it with a pencil. The visible route text reads "eta" and "8 hours."` + base block.
References: shot G output (same map, same pose family).

### Shot N — `vignette-writing-map-altroute` (trellis row-2 panel only)
Square-ish, 4:3. Same setup as M, updated map.
Prompt: same as M but the map reads "alt. route" and "+4 hours" as in shot H.
References: shot H output.

---

## 4. Check every image before you keep it

Reject and regenerate if any of these fail:

- [ ] Same face as `id-face-front.png` in every shot that shows it — not a lookalike
- [ ] Jacket fitted through the waist (princess seams visible), not boxy
- [ ] Hood down in every shot
- [ ] Shoulders, upper arm and chest **completely clean** — no patch, no logo
- [ ] Where cuffs are visible: TERRA left, NEXUS right, spelled correctly, reading the right way round
- [ ] Jacket reads Glacier Blue `#5A90BE` — not teal, not navy
- [ ] Pack patch has the star, reads "TERRA NEXUS," dark red, no mountain graphic, no second patch on the pack
- [ ] Pack patch is the same **apparent real-world size** as the other scenes at a comparable camera distance — not a fixed pixel size, a fixed physical one
- [ ] Notebook signature reads "ISO Auditor," not "For Auditor"
- [ ] All handwritten/printed text in shot B and on both map versions is legible and spelled as written above
- [ ] No watermark, no stray text overlay, no second person unless the shot calls for one

Text is the most likely failure across this whole brief — the notebook shot
(B) and both map shots (G, H) carry the most of it. If the generator can't
render it cleanly after a few tries, generate the shot with the props blank or
blurred and composite the text in afterward from a clean vector source, the
same way `Output Drafts/Character/GENERATION-BRIEF.md` handles cuff text that
won't resolve.

---

## 5. Hand it back

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

That's twelve numbered-scene deliverables covered by eleven hero generations
(A–K) plus three collage-only vignettes (L–N); scenes 2 and 3 are not
generated directly — they're assembled from A, B, L, M, N and crops of D/I
(see `../README.md`). Once everything above exists, the assembly script (see
`build/`, following the compositing approach in
`Output Drafts/Patch/build/compose.py`) lays out scenes 2 and 3 and the full
set replaces `Input Pictures - Story Based/` as the package's source.
