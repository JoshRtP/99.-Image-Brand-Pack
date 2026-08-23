# Output Drafts

Everything in this folder is **generated work**, not source material. It is
drafts: review it, mark it up, and it gets rebuilt.

The source material it is built from stays outside this folder and is never
written to:

- `Branding/` — the official logos, favicon, sticker and colour palette
- `Input Pictures - Story Based/` — the original story set
- `People/` — reference photography

| Folder | What it is |
| --- | --- |
| `Patch/` | The embroidered backpack patch — production artwork, embroidered and worn renders, spec sheet, three colourways. |
| `Jacket/` | The wind shell — technical flats, spec sheet, three colourways. |
| `Story Set - Deep Red Patch/` | The full story package with the Deep Red patch on the pack, same filenames and numbering as the input set. |
| `Direct-Stitch/` | The alternative to the patch — the wordmark stitched straight onto the pack in a tone-on-tone thread, so it reads as relief rather than a label. |
| `Character/` | Costume turnaround — the main character in the wind shell at five angles, plus the prompt kit for regenerating her consistently. |
| `Scenes/` | **Start here for a full re-render.** The generation brief that regenerates all twelve story scenes with the patch and jacket branding baked in, instead of composited on afterward. |

Each folder has its own README and a `build/` directory that regenerates it from
the source material. Nothing here is hand-edited output — change a script, run
its `make.sh`, and the whole folder comes back.
