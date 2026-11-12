"""Build the ASCII kitty and static profile headers from the authorised photo."""

import argparse
from html import escape
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
FONT = ROOT / "assets/fonts/JetBrainsMono-Regular.ttf"
SYSTEM_FONT = (
    '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, '
    'Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji"'
)
INK = "#E6EDF3"
BACKGROUND = "#0D1117"
PURPLE = "#7C3AED"
LAVENDER = "#C4B5FD"
DISPLAY_NAME = "Diogo M. Pires"


def kitty_ascii(source):
    with Image.open(source) as photo:
        photo = ImageOps.exif_transpose(photo).convert("RGB")
    if photo.size != (1200, 1600):
        raise ValueError(f"photo must be 1200 x 1600 pixels, got {photo.size}")

    # This outline follows the supplied cat, excluding the basket and tiled wall.
    mask = Image.new("L", photo.size)
    ImageDraw.Draw(mask).polygon(
        [
            (425, 244),
            (449, 259),
            (488, 286),
            (529, 309),
            (565, 299),
            (605, 293),
            (645, 290),
            (684, 290),
            (721, 264),
            (762, 232),
            (801, 204),
            (796, 231),
            (790, 261),
            (787, 286),
            (791, 311),
            (785, 336),
            (781, 363),
            (780, 395),
            (786, 425),
            (781, 454),
            (774, 485),
            (763, 514),
            (752, 540),
            (766, 565),
            (781, 600),
            (795, 636),
            (803, 673),
            (805, 710),
            (461, 710),
            (466, 677),
            (475, 645),
            (485, 610),
            (499, 578),
            (518, 554),
            (517, 532),
            (498, 506),
            (488, 477),
            (484, 449),
            (475, 408),
            (462, 373),
            (450, 347),
            (442, 314),
            (433, 284),
        ],
        fill=255,
    )
    crop = (404, 192, 836, 710)
    mask = mask.crop(crop)
    grey = ImageOps.autocontrast(photo.crop(crop).convert("L"), cutoff=1, mask=mask)
    grey = ImageEnhance.Contrast(grey).enhance(1.22)
    # A cell is 0.6 em wide and 1 em high, preserving photographic proportions.
    grey = grey.resize((72, 52), Image.Resampling.LANCZOS)
    mask = mask.resize(grey.size, Image.Resampling.LANCZOS)
    ramp = " .:-=+*#%@"
    rows = []
    for y in range(grey.height):
        row = []
        for x in range(grey.width):
            character = " "
            if mask.getpixel((x, y)) >= 128:
                tone = grey.getpixel((x, y))
                character = ramp[round(tone / 255 * (len(ramp) - 1))]
            row.append(character)
        rows.append("".join(row))
    return rows


def glyph_paths(rows):
    with TTFont(FONT) as font:
        glyphs = font.getGlyphSet()
        cmap = font.getBestCmap()
        paths = []
        for character in sorted(set("".join(rows)) - {" "}):
            pen = SVGPathPen(glyphs)
            glyphs[cmap[ord(character)]].draw(pen)
            paths.append(f'<path id="glyph-{ord(character)}" d="{pen.getCommands()}"/>')
        return "\n".join(paths), font["head"].unitsPerEm


def header(rows, paths, units_per_em, mobile):
    width, height = (600, 750) if mobile else (960, 432)
    kitty_x, kitty_y, size = (84, 27, 10) if mobile else (32, 23, 7.6)
    text_x, name_y = (64, 604) if mobile else (400, 166)
    body_y, language_y = (647, 729) if mobile else (213, 293)
    name_size, body_size, language_size = (32, 27, 26) if mobile else (30, 22, 21)
    line_height = 34 if mobile else 30
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">'
        ),
        f'<title id="title">{escape(DISPLAY_NAME)}</title>',
        (
            '<desc id="description">An ASCII portrait of my kitty beside my name, '
            "research software introduction and programming languages.</desc>"
        ),
        f'<rect width="{width}" height="{height}" fill="{BACKGROUND}"/>',
        f"<defs>\n{paths}\n</defs>",
        f'<g fill="{INK}" aria-hidden="true">',
    ]
    scale = size / units_per_em
    for y, row in enumerate(rows):
        for x, character in enumerate(row):
            if character != " ":
                parts.append(
                    f'<use href="#glyph-{ord(character)}" transform="translate('
                    f"{kitty_x + x * size * 0.6:.3f} {kitty_y + y * size:.3f}) "
                    f'scale({scale:.6f} {-scale:.6f})"/>'
                )
    parts.extend(
        [
            "</g>",
            f'<g font-family="{escape(SYSTEM_FONT, quote=True)}" fill="{INK}" font-weight="400">',
            (
                f'<text x="{text_x}" y="{name_y}" font-size="{name_size}" '
                f'font-weight="500">{escape(DISPLAY_NAME)}</text>'
            ),
            f'<text x="{text_x}" y="{body_y}" font-size="{body_size}">',
            f'<tspan x="{text_x}">I build research software for sensing,</tspan>',
            f'<tspan x="{text_x}" dy="{line_height}"> machine learning and simulation.</tspan>',
            "</text>",
            f'<text x="{text_x}" y="{language_y}" font-size="{language_size}" fill="{LAVENDER}">',
            f'Python <tspan fill="{PURPLE}">·</tspan> TypeScript <tspan fill="{PURPLE}">·</tspan> JavaScript',
            "</text>",
            "</g>",
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("photo", type=Path, help="the authorised original kitty photo")
    rows = kitty_ascii(parser.parse_args().photo)
    paths, units_per_em = glyph_paths(rows)
    (ROOT / "assets/kitty.txt").write_text(
        "\n".join(rows) + "\n", encoding="ascii", newline="\n"
    )
    for filename, mobile in [("profile.svg", False), ("profile-mobile.svg", True)]:
        (ROOT / "assets" / filename).write_text(
            header(rows, paths, units_per_em, mobile), encoding="utf-8", newline="\n"
        )


if __name__ == "__main__":
    main()
