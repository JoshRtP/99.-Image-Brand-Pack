# Handoff prompt — for a Claude session with image generation

Paste the block below into a Claude session that can generate images and fetch
URLs. It is self-contained: everything else it needs, it fetches.

> **Before you use it**, the locked face portrait must be in the repo at
> `Output Drafts/Character/plates/generated/id-face-front.png`. Until it is,
> `shots.py --check` reports it as PENDING and the other session has nothing to
> match her to.

---

```
I need you to generate a set of images for a brand called Terra Nexus — a
character, a jacket, and a series of the two together. Everything you need is in
one file. Start by fetching it:

https://raw.githubusercontent.com/JoshRtP/99.-Image-Brand-Pack/main/Output%20Drafts/Character/shots.json

That file gives you 26 shots. Each has an `id`, a full `prompt` already
assembled, an `aspect`, and a `references` list. Every reference is a public raw
GitHub URL you can fetch and look at before generating — flats of the garment,
photographs of the character, the exact letterforms, the stitching on the pack.
Look at them. This is an existing character in existing products, not a fresh
invention.

FIRST, AND BEFORE ANYTHING ELSE:

Shot 1, `id-face-front`, is marked `supplied: true`. Do NOT generate it. It is a
photograph of the character's face, and it is the locked identity reference.
Fetch it, look at it carefully, and attach it to every character and series shot
you generate. Her face must match it in every single image. If a result comes
back with a different face, that result is wrong — regenerate it.

Then three groups, which you can run in any order:

  • "character" — shots 2 to 12. Her in the jacket: angles, garment details,
    two in-world frames.
  • "jacket" — shots 13 to 20. The garment alone as a product shot on an
    invisible mannequin, plus two alternate colourways. These are the only
    shots with no face in them.
  • "series" — shots 21 to 26. Her wearing the jacket and carrying the pack,
    in world. This is the set that matters most.

Two branding rules run through everything, and they are the most common way
these come out wrong:

  1. THE JACKET carries its wordmark ONLY on the cuffs — TERRA wrapping the left
     wrist, NEXUS wrapping the right, in white block capitals. The shoulders,
     upper arms and chest are completely clean. No patch, no logo, nothing.

  2. THE PACK carries no patch at all. Its wordmark is embroidered straight into
     the rust-orange fabric in a faded deep oxblood thread only slightly darker
     than the fabric — TERRA over NEXUS, both lines the same width, left edges
     aligned, a squared-off block. It reads as raised texture catching the light,
     not as a label. No patch, no border, no panel behind the letters.

Use `negative_prompt` from the JSON on every shot. Check each image against
`acceptance_checks`, also in the JSON, and regenerate anything that fails. The
usual failures: the jacket coming out boxy instead of slim; something appearing
on the shoulder or chest; the pack getting a patch instead of stitching; cuff
lettering misspelled or mirrored.

If you cannot get the lettering to spell correctly, say so rather than shipping
it — the wordmarks can be composited afterwards from the artwork in the
references.

Give me the images named by their shot `id`, and tell me which ones you had to
regenerate and why.
```

---

## The three groups

| Group | Shots | What it is |
| --- | --- | --- |
| `character` | 2–12 | Her in the jacket — angles, details, in-world |
| `jacket` | 13–20 | The garment alone, product shots, three colourways |
| `series` | 21–26 | Her with the pack: holding it, shouldering it, wearing it, walking, hero |

## When the images come back

Drop them into `Output Drafts/Character/plates/generated/`, named by shot id,
then:

```sh
sh "Output Drafts/Character/build/make.sh"
```

The character sheet folds them in automatically.
