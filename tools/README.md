# Profile asset generators

Scripts that generate the animated SVGs used in the profile README (`../assets`).

| Script | Output |
|--------|--------|
| `banner.py` | `banner-{dark,light}.svg` (header with neural network and rotating roles) and `divider-{dark,light}.svg` |
| `sections.py` | `cards-*`, `timeline-*` and `strip-*` SVGs |
| `embed_fonts.py` | Subsets Space Grotesk and JetBrains Mono to the glyphs each SVG uses and embeds them as base64 |
| `fetch_fonts.sh` | Downloads the font files from [Fontsource](https://fontsource.org) |

## Rebuild everything

```sh
./tools/build.sh
```

The first run creates a virtualenv with `fonttools` and downloads the fonts.

## Common edits

- **Rotating roles or tagline in the banner** — `ROLES` and the `tag` text in `banner.py`.
- **Cards** — `CARDS` in `sections.py` (icon, title, accent color, body).
- **Timeline** — `TIMELINE` in `sections.py`.
- **Stats strip** — `STATS` in `sections.py`.
- **Colors** — `VIOLET`, `CYAN`, `PINK` and `THEMES` in both generators.

SVGs rendered as images cannot load external fonts, which is why the fonts are embedded. Always run `embed_fonts.py` (or `build.sh`) after regenerating.
