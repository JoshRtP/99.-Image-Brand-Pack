# Handoff prompt — for a Claude session with image generation

Paste the block below into a Claude session that can generate images and fetch
URLs. It is self-contained: everything else it needs, it fetches.

---

```
I need you to generate a set of reference images for a brand called Terra Nexus —
a character and a jacket. Everything you need is in one file. Start by fetching it:

https://raw.githubusercontent.com/JoshRtP/99.-Image-Brand-Pack/main/Output%20Drafts/Character/shots.json

That file gives you 20 shots. Each one has an `id`, a full `prompt` already
assembled, an `aspect`, and a `references` list. Every reference is a public raw
GitHub URL you can fetch and look at before you generate — flats of the garment,
photographs of the character, the exact letterforms for the wordmark. Look at
them. They are the whole point: this is an existing character in an existing
garment, not a fresh invention.

There are two groups:

  • group "character" — shots 1 to 12. A woman in the jacket, five angles plus
    identity portraits, garment details and two in-world frames.
  • group "jacket" — shots 13 to 20. The garment alone as a product shot on an
    invisible mannequin, plus two alternate colourways.

Run them in `order`. One rule matters more than the rest:

  SHOT 1 (`id-face-front`) LOCKS HER FACE. No photograph of her face exists —
  every frame in the source set is shot from behind. So shot 1 invents it.
  Generate several, show me the options, and wait for me to pick one. Whichever
  I pick becomes the identity reference you attach to every later character
  shot. Do not run shots 2 to 12 before I have picked.

The jacket shots (13 to 20) have no such dependency — you can run those any time.

Use `negative_prompt` from the JSON on every shot. Then check each image against
`acceptance_checks`, also in the JSON, and regenerate anything that fails. The
checks that fail most often:

  • the jacket coming out boxy or oversized — it is a slim, close-fitting cut
  • something appearing on the shoulder or chest — it must be completely clean
  • the cuff wording misspelled or mirrored — it is TERRA on the left wrist and
    NEXUS on the right, and nothing else anywhere on the garment

If you cannot get the cuff lettering to spell correctly, say so rather than
shipping it — the wordmark can be composited afterwards from the artwork in the
references.

Give me the images named by their shot `id`, and tell me which ones you had to
regenerate and why.
```

---

## What the other session will pull

| | |
| --- | --- |
| Shot list, prompts, references | `Output Drafts/Character/shots.json` |
| Long-form brief, if it wants context | `Output Drafts/Character/GENERATION-BRIEF.md` |
| Character photography | `Output Drafts/Character/plates/*.png` |
| Garment flats and spec | `Output Drafts/Jacket/*.png` |
| Letterforms, patch, pack | `Output Drafts/Patch/*.png` |
| Direct-stitch threads | `Output Drafts/Direct-Stitch/threads.json` |

All under `https://raw.githubusercontent.com/JoshRtP/99.-Image-Brand-Pack/main/`,
URL-encoded — the folder names contain spaces, so `Output%20Drafts`.

## When the images come back

Drop them into `Output Drafts/Character/plates/generated/`, named by shot id,
then:

```sh
sh "Output Drafts/Character/build/make.sh"
```

The character sheet folds them in and stops reporting that her face has no
reference.
