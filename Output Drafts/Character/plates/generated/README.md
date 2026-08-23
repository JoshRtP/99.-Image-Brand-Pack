# Generated plates go here

Named by shot ID from `../../shots.json` — `full-front.png`,
`series-holding-pack.png`, `jacket-back.png` and so on. Then:

```sh
sh "Output Drafts/Character/build/make.sh"
```

The character sheet picks up whatever is present. Partial sets are fine.

## One file is required, not generated

```
id-face-front.png
```

This is the **locked identity portrait** — a real front-facing photograph of the
character, supplied rather than generated. Every other character and series shot
matches its face to this one.

Until it is here, `shots.py --check` reports it as PENDING and the generation
handoff has nothing to anchor her to. It is the first thing to add.
