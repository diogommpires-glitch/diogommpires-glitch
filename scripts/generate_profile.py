"""Build two static profile cards from an authorised local avatar."""

import argparse
from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
INK = " .,:;i1tfLCG08@"
FONT = "Consolas, 'Liberation Mono', Menlo, monospace"
FIELDS = [
    ("Focus", "applied ML + simulation"),
    ("Work", "sensors + biometrics"),
    ("", "numerical methods"),
    ("Code", "Python, TypeScript"),
    ("", "JavaScript"),
    ("CI targets", "Windows + Linux"),
    ("Projects", "8 source snapshots"),
    ("Licence", "PolyForm Noncommercial"),
]


def ascii_portrait(avatar: Path) -> list[str]:
    with Image.open(avatar) as source:
        image = ImageOps.exif_transpose(source).convert("RGB")
    if image.size != (300, 300):
        raise ValueError(f"Expected the approved 300 x 300 avatar, got {image.size}")

    # The silhouette excludes the buildings and people behind the author.
    mask = Image.new("L", image.size)
    ImageDraw.Draw(mask).polygon(
        [
            (0, 282),
            (5, 261),
            (45, 235),
            (72, 216),
            (89, 204),
            (94, 190),
            (80, 170),
            (74, 148),
            (72, 118),
            (50, 113),
            (49, 87),
            (61, 70),
            (70, 62),
            (90, 55),
            (130, 49),
            (160, 52),
            (188, 57),
            (204, 70),
            (215, 90),
            (214, 120),
            (207, 141),
            (208, 160),
            (196, 181),
            (185, 193),
            (185, 210),
            (212, 220),
            (257, 234),
            (299, 259),
            (299, 299),
            (0, 299),
        ],
        fill=255,
    )
    crop = (30, 35, 270, 300)
    luminance = ImageOps.grayscale(image).crop(crop)
    luminance = ImageOps.autocontrast(luminance, cutoff=1)
    luminance = ImageEnhance.Contrast(luminance).enhance(1.15)
    luminance = luminance.point(lambda value: round(255 * (value / 255) ** 0.65))
    luminance = luminance.filter(ImageFilter.UnsharpMask(radius=1.2, percent=130))
    luminance = luminance.resize((70, 45), Image.Resampling.LANCZOS)
    silhouette = mask.crop(crop).resize((70, 45), Image.Resampling.LANCZOS)
    return [
        "".join(
            INK[round((255 - luminance.getpixel((x, y))) / 255 * (len(INK) - 1))]
            if silhouette.getpixel((x, y)) >= 128
            else " "
            for x in range(70)
        ).rstrip()
        for y in range(45)
    ]


def text(x: int, y: int, value: str, fill: str, size: int = 19) -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}">{escape(value)}</text>'
    )


def card(portrait: list[str], mobile: bool) -> str:
    width, height = (600, 1168) if mobile else (1200, 760)
    facts_x, facts_y = (42, 785) if mobile else (576, 291)
    value_x = facts_x + (170 if mobile else 150)
    line_height = 37 if mobile else 40
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"',
        f' viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
        '<title id="title">diogommpires-glitch | applied ML and simulation</title>',
        (
            '<desc id="description">An ASCII portrait of the author beside public project facts. '
            "Python, TypeScript and JavaScript. Windows and Linux CI targets. "
            "Eight source snapshots. PolyForm Noncommercial licence.</desc>"
        ),
        f'<g font-family="{FONT}">',
        (
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="22" '
            'fill="#15191f" stroke="#303944" stroke-width="2"/>'
        ),
        '<circle cx="34" cy="35" r="6" fill="#fa7770"/>',
        '<circle cx="55" cy="35" r="6" fill="#edbe5f"/>',
        '<circle cx="76" cy="35" r="6" fill="#79c88b"/>',
        text(102, 41, "profile.sh", "#a9b2bd", 17),
        f'<path d="M 24 70 H {width - 24}" stroke="#303944"/>',
    ]
    portrait_x, portrait_y = (56, 116) if mobile else (44, 133)
    parts.append(
        f'<text x="{portrait_x}" y="{portrait_y}" fill="#c9d2dc" '
        'font-size="11" xml:space="preserve">'
    )
    for row, line in enumerate(portrait):
        parts.append(
            f'<tspan x="{portrait_x}" dy="{0 if row == 0 else 12}">{escape(line)}</tspan>'
        )
    parts.append("</text>")

    heading_y = 709 if mobile else 160
    parts.extend(
        [
            text(facts_x, heading_y - 34, "$ whoami", "#ffad5c", 18),
            text(facts_x, heading_y, "diogommpires-glitch", "#e8edf3", 25),
            f'<path d="M {facts_x} {heading_y + 26} H {width - 42}" stroke="#3a4654"/>',
        ]
    )
    for index, (label, value) in enumerate(FIELDS):
        y = facts_y + index * line_height
        if label:
            parts.append(text(facts_x, y, label, "#ffad5c", 24 if mobile else 19))
        parts.append(text(value_x, y, value, "#a6d4fa", 24 if mobile else 19))
    footer_y = height - 37
    parts.extend(
        [
            f'<path d="M 42 {footer_y - 30} H {width - 42}" stroke="#303944"/>',
            text(42, footer_y, "public work / 12 Nov 2026", "#8493a4", 16),
            "</g>",
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("avatar", type=Path, help="Authorised local 300 x 300 avatar")
    args = parser.parse_args()
    portrait = ascii_portrait(args.avatar)
    for filename, mobile in [("profile.svg", False), ("profile-mobile.svg", True)]:
        (ROOT / "assets" / filename).write_text(
            card(portrait, mobile), encoding="utf-8", newline="\n"
        )


if __name__ == "__main__":
    main()
