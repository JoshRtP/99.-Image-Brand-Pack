# Story set — Deep Red patch

The full story package with the approved Terra Nexus patch on the pack, in the
**Deep Red** colourway (`#6A1B32`). Same filenames, same numbering, same image
roles as `Input Pictures - Story Based/`, so this folder drops in as a
replacement.

Regenerate, or switch colourway, from the repo root:

```sh
cd Branding/Patch/build
python3 apply_to_scene.py ../patch-embroidered-red.png "../../../Story Set - Deep Red Patch"
```

Point it at `../patch-embroidered.png` (navy), `../patch-embroidered-ink.png`, or
any `-worn` render to produce the set in a different colourway.

---

## What changed

Five scenes carry a visible sewn patch on the pack. In each, the existing patch
was removed and the approved Deep Red patch laid back in its place, following
the panel's roll and picking up the scene's own light and colour cast.

| Scene | Old patch | New patch |
| --- | --- | --- |
| `1. Opening Scene` | 55 px wide | 47 px |
| `2. Transition to trellis` | 67 px | 57 px |
| `3. Example story trellis` | 27 px | 23 px |
| `6. Story 3` | 104 px | 89 px |
| `9. Story 6` | 44 px | 38 px |

Everything else — framing, maps, screens, props, text, grading — is untouched.
The other seven files are copied through byte-identical so the package stays
complete.

### How the size was set

Each new patch is **0.85 × the old patch's width**. That ratio comes from scene
6, the one scene where the pack's front panel is square enough to the camera to
measure against: the panel reads about 420 px across and a real pack panel is
roughly 300 mm, which puts the 63 mm patch at 88 px. The old patch there was
104 px — about 74 mm, noticeably oversized.

Using a ratio preserves the framing the original artist chose. It does **not**
fix inconsistent physical sizing between scenes: if the old patches were not all
the same real-world size, the new ones inherit that. Getting the patch to a
genuinely constant 63 mm across the set needs a physical reference measured
per scene, which is a separate pass.

---

## What was deliberately not changed

Four things in the set conflict with the rules in the package README. None of
them are the patch on the pack, so none were touched here.

1. **Jacket patches are still there** — scenes 1, 2, 3, 5, 7, 8 and 9 all carry a
   sewn patch on the jacket's upper arm, and the package rule is bags only, no
   jacket patches. Every one of them also shows the mountain graphic. Scene 9's
   reads **"TERRA PEAK"**, not Terra Nexus.
2. **Scene 5's pack logo is printed, not sewn** — it is a screen-printed mountain
   and wordmark straight on the fabric, not a patch, so there was nothing to
   swap. It still shows the forbidden mountain graphic.
3. **Scenes 7, 8, 10 and 10a** show the pack but not its patch — it is turned
   away or out of frame. Nothing to place.
4. **"For Auditor" is still "For Auditor"** in scenes 2 and 3. The package README
   asks for "ISO Auditor", keeping the handwritten treatment.

## Known limits

- In `3. Example story trellis` the patch lands at 23 px across. The ground
  colour and the star read; the wordmark cannot resolve at that size. That is a
  property of the collage, not of the composite.
- These are composites, not regenerated frames. They are correct and consistent
  and can ship, but if the set is ever re-rendered from prompts, use the prompt
  block in `Branding/Patch/README.md` instead and let the patch come out of the
  generator.
