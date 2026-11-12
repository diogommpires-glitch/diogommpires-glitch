# Profile notes

## Portrait and rendering

The ASCII kitty portrait comes directly from an original photograph supplied by the owner. The photograph is retained outside this repository. The local conversion uses a fixed mask and head-and-shoulders crop matched to that photograph, producing a 72-column portrait in [assets/kitty.txt](../assets/kitty.txt).

The [desktop](../assets/profile.svg) and [phone](../assets/profile-mobile.svg) headers are self-contained SVGs. The ASCII portrait uses JetBrains Mono Regular and the ordinary header text uses STIX Two Text. Both are rendered as glyph outlines, so their appearance does not depend on the viewer's installed fonts. The native project links keep GitHub's own text styling. Viewing the headers requires no external requests, font downloads or scripts.

## Regeneration

Use Python with Pillow and fontTools available in the local environment. From the repository root, supply the authorised original photograph explicitly:

```sh
python scripts/generate_profile.py /path/to/authorised-kitty-photo
```

The generator writes the plain-text portrait and both SVG layouts. A different photograph requires reviewing the fixed mask and crop in [the generator](../scripts/generate_profile.py). Review the complete README at desktop and phone widths before updating the GitHub profile. Regeneration does not publish anything.

Keep project links and their descriptions in the README. Regenerate both headers together when changing the portrait, introduction or language line.

## Licensing and provenance

[LICENSING.md](../LICENSING.md) explains the non-commercial scope of the original project code, links to the full [project licence](../LICENSE), and preserves earlier grants and third-party terms.

The vendored font is [JetBrains Mono Regular 2.304](https://raw.githubusercontent.com/JetBrains/JetBrainsMono/v2.304/fonts/ttf/JetBrainsMono-Regular.ttf). It retains the SIL Open Font License 1.1, including its [vendored notice](../assets/fonts/OFL.txt) and [upstream licence](https://raw.githubusercontent.com/JetBrains/JetBrainsMono/v2.304/OFL.txt). The project's non-commercial terms do not replace or restrict the font's licence.

STIX Two Text retains its separate [SIL Open Font License notice](../assets/fonts/STIXTwoText-OFL.txt). The unmodified variable font comes from [this recorded Google Fonts revision](https://github.com/google/fonts/tree/718c7ee0e83f5e301cc96bbc081c9bb5ade9ed92/ofl/stixtwotext). Header names use medium weight and body text uses regular weight.
