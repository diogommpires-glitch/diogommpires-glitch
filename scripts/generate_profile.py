"""Build the static desktop and phone dashboards from public snapshot data."""

import base64
import json
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT = "'Segoe UI', Arial, sans-serif"
INK = "#f3efff"
MUTED = "#a9a1bb"
PURPLE = "#b99aff"
RULE = "#302840"
COLOURS = ["#8954f5", "#b18afa", "#d4bdfc", "#625372"]


def text(x, y, value, size=18, fill=INK, weight=400):
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}">{escape(str(value))}</text>'
    )


def rule(x, y, width):
    return f'<path d="M{x} {y}h{width}" stroke="{RULE}"/>'


def dashboard(data, portrait, mobile):
    width, height = (600, 1460) if mobile else (1200, 820)
    x, right_width = (40, 520) if mobile else (398, 754)
    title_y = 670 if mobile else 128
    date = datetime.fromisoformat(data["checked_at_utc"]).strftime("%d %B %Y")
    metrics = data["metrics"]
    languages = data["languages"]
    commits = metrics["project_public_commits"]
    total_bytes = metrics["project_language_bytes_total"]
    groups = [
        *languages[:3],
        {"name": "Other", "bytes": sum(item["bytes"] for item in languages[3:])},
    ]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">'
        ),
        '<title id="title">diogommpires-glitch | public project dashboard</title>',
        (
            f'<desc id="description">A photographic kitty portrait beside public project '
            f"facts. {metrics['project_repositories']} project repositories, {commits} "
            f"public snapshot commits and {metrics['distinct_project_languages']} "
            f"GitHub-classified languages. Data checked on {date}. "
            "PolyForm Noncommercial licence.</desc>"
        ),
        f'<g font-family="{FONT}">',
        (
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="24" '
            'fill="#0e0c15" stroke="#35274d" stroke-width="2"/>'
        ),
        '<path d="M28 34v22" stroke="#8954f5" stroke-width="5" stroke-linecap="round"/>',
        text(44, 51, "PUBLIC WORK", 16, PURPLE, 600),
        text(width - 254, 51, date, 16, MUTED),
        rule(28, 78, width - 56),
    ]
    portrait_x, portrait_y, portrait_width, portrait_height = (
        (112, 106, 376, 502) if mobile else (32, 112, 332, 444)
    )
    parts.extend(
        [
            (
                f'<circle cx="{width // 2 if mobile else 198}" '
                f'cy="{302 if mobile else 296}" r="{180 if mobile else 156}" '
                'fill="#1c1230" stroke="#483066"/>'
            ),
            (
                f'<image x="{portrait_x}" y="{portrait_y}" width="{portrait_width}" '
                f'height="{portrait_height}" preserveAspectRatio="xMidYMid meet" '
                f'href="data:image/png;base64,{portrait}"/>'
            ),
        ]
    )
    if not mobile:
        parts.extend(
            [
                text(42, 600, "SENSING", 22, PURPLE, 600),
                text(42, 631, "BIOMETRICS", 22, PURPLE, 600),
                text(42, 662, "NUMERICAL METHODS", 22, PURPLE, 600),
                rule(42, 698, 290),
                text(42, 730, "Python · TypeScript · JavaScript", 15, MUTED),
            ]
        )
    parts.extend(
        [
            text(x, title_y, "diogommpires-glitch", 29 if mobile else 34, INK, 600),
            text(x, title_y + 51, "Applied ML + simulation", 31, PURPLE, 500),
            text(x, title_y + 88, "Research software for sensing,", 22, MUTED),
            text(x, title_y + 120, "biometrics and numerical methods.", 22, MUTED),
            rule(x, title_y + 151, right_width),
        ]
    )
    metric_y = title_y + 208
    labels = [
        (metrics["project_repositories"], "Projects"),
        (commits, "Snapshot commits"),
        (metrics["distinct_project_languages"], "Languages"),
    ]
    for index, (value, label) in enumerate(labels):
        column_x = x + index * (right_width / 3)
        parts.append(text(column_x, metric_y, value, 43, INK, 600))
        if mobile and label == "Snapshot commits":
            parts.append(text(column_x, metric_y + 31, "Snapshot", 21, MUTED))
            parts.append(text(column_x, metric_y + 57, "commits", 21, MUTED))
        else:
            parts.append(text(column_x, metric_y + 31, label, 21, MUTED))
    chart_y = metric_y + (126 if mobile else 104)
    parts.extend(
        [
            rule(x, chart_y - 40, right_width),
            text(x, chart_y, "SOURCE LANGUAGES", 22, PURPLE, 600),
        ]
    )
    bar_x = x
    for group, colour in zip(groups, COLOURS, strict=True):
        bar_width = right_width * group["bytes"] / total_bytes
        parts.append(
            f'<rect x="{bar_x:.3f}" y="{chart_y + 24}" width="{bar_width:.3f}" '
            f'height="16" fill="{colour}"/>'
        )
        bar_x += bar_width
    for index, (group, colour) in enumerate(zip(groups, COLOURS, strict=True)):
        column_x = x + (index % 2) * 265 if mobile else x + index * 190
        row_y = chart_y + 88 + (index // 2) * 69 if mobile else chart_y + 82
        parts.extend(
            [
                f'<circle cx="{column_x + 4}" cy="{row_y - 7}" r="4" fill="{colour}"/>',
                text(column_x + 16, row_y, group["name"], 22, MUTED),
                text(
                    column_x + 16,
                    row_y + 30,
                    f"{100 * group['bytes'] / total_bytes:.1f}%",
                    24 if mobile else 22,
                ),
            ]
        )
    caption_y = chart_y + (219 if mobile else 151)
    parts.append(
        text(
            x,
            caption_y,
            "GitHub-classified source bytes across eight projects.",
            20,
            MUTED,
        )
    )
    activity_y = caption_y + 65
    parts.extend(
        [
            rule(x, activity_y - 29, right_width),
            text(x, activity_y, "PUBLIC SNAPSHOT ACTIVITY", 22, PURPLE, 600),
            text(
                x,
                activity_y + 42,
                f"{commits} commits in the linked snapshots",
                23 if mobile else 22,
            ),
            text(
                x,
                activity_y + 75,
                "Snapshot history only. Private activity excluded.",
                20,
                MUTED,
            ),
            rule(28, height - 66, width - 56),
            text(40, height - 33, "PolyForm Noncommercial", 19, MUTED),
            text(
                width - 196,
                height - 33,
                f"{metrics['project_repositories']} public projects",
                19,
                PURPLE,
            ),
            "</g>",
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def main():
    data = json.loads((ROOT / "data/public-metrics.json").read_text(encoding="utf-8"))
    portrait = base64.b64encode((ROOT / "assets/kitty.png").read_bytes()).decode(
        "ascii"
    )
    for filename, mobile in [("profile.svg", False), ("profile-mobile.svg", True)]:
        (ROOT / "assets" / filename).write_text(
            dashboard(data, portrait, mobile), encoding="utf-8", newline="\n"
        )


if __name__ == "__main__":
    main()
