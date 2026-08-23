# Generated plates go here

Drop the outputs from `../../GENERATION-BRIEF.md` in this folder, named by shot
ID — `id-face-front.png`, `full-front.png`, `cuff-left-terra.png` and so on.

Then run:

```sh
sh "Output Drafts/Character/build/make.sh"
```

The character sheet picks up whatever is present and adds it as a generated row.
Partial sets are fine. Once `id-face-front` is here, the sheet stops saying her
face has no reference and starts saying it is canon.
