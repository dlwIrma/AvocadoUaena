#!/usr/bin/env python3
"""Render social-media previews from a validated Codex v2 pet atlas."""

from __future__ import annotations

import argparse
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


CELL_WIDTH = 192
CELL_HEIGHT = 208
CANVAS_SIZE = (1080, 1440)

STATES = [
    ("01-idle", "待机", 0, 6, 0),
    ("02-running-right", "向右移动", 1, 8, 2),
    ("03-running-left", "向左移动", 2, 8, 2),
    ("04-waving", "挥手", 3, 4, 1),
    ("05-jumping", "跳跃", 4, 5, 2),
    ("06-failed", "失败", 5, 8, 4),
    ("07-waiting", "等待你", 6, 6, 2),
    ("08-running", "执行任务", 7, 6, 2),
    ("09-review", "审查", 8, 6, 2),
]


def font(size: int) -> ImageFont.FreeTypeFont:
    candidates = (
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
    )
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


@lru_cache(maxsize=1)
def make_background() -> Image.Image:
    width, height = CANVAS_SIZE
    image = Image.new("RGB", CANVAS_SIZE)
    pixels = image.load()
    top = (255, 252, 244)
    bottom = (238, 247, 204)
    for y in range(height):
        t = y / max(1, height - 1)
        color = tuple(round(a * (1 - t) + b * t) for a, b in zip(top, bottom))
        for x in range(width):
            pixels[x, y] = color

    decor = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(decor)
    draw.ellipse((-180, 980, 420, 1580), fill=(194, 224, 66, 38))
    draw.ellipse((780, -120, 1260, 360), fill=(230, 205, 255, 42))
    draw.ellipse((850, 1060, 1210, 1420), fill=(255, 226, 86, 35))
    image = Image.alpha_composite(image.convert("RGBA"), decor)
    return image


def render_frame(
    cell: Image.Image, label: str, content_box: tuple[int, int, int, int]
) -> Image.Image:
    canvas = make_background().copy()
    draw = ImageDraw.Draw(canvas)

    title_font = font(72)
    subtitle_font = font(34)
    title_box = draw.textbbox((0, 0), label, font=title_font)
    title_width = title_box[2] - title_box[0]
    pill_left = (CANVAS_SIZE[0] - title_width) // 2 - 52
    pill_right = (CANVAS_SIZE[0] + title_width) // 2 + 52
    draw.rounded_rectangle(
        (pill_left, 118, pill_right, 228),
        radius=55,
        fill=(255, 255, 255, 214),
        outline=(181, 211, 58, 150),
        width=3,
    )
    draw.text(
        ((CANVAS_SIZE[0] - title_width) // 2, 130),
        label,
        font=title_font,
        fill=(95, 112, 35, 255),
    )

    sprite = cell.crop(content_box)
    scale = min(720 / sprite.width, 820 / sprite.height)
    sprite = sprite.resize(
        (round(sprite.width * scale), round(sprite.height * scale)),
        Image.Resampling.LANCZOS,
    )
    x = (CANVAS_SIZE[0] - sprite.width) // 2
    y = 310 + (824 - sprite.height) // 2
    canvas.alpha_composite(sprite, (x, y))

    subtitle = "牛油果爱娜  ·  AvocadoUaena"
    subtitle_box = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_box[2] - subtitle_box[0]
    draw.text(
        ((CANVAS_SIZE[0] - subtitle_width) // 2, 1260),
        subtitle,
        font=subtitle_font,
        fill=(107, 91, 71, 220),
    )
    return canvas.convert("RGB")


def crop(atlas: Image.Image, row: int, column: int) -> Image.Image:
    left = column * CELL_WIDTH
    top = row * CELL_HEIGHT
    return atlas.crop((left, top, left + CELL_WIDTH, top + CELL_HEIGHT))


def save_state(
    atlas: Image.Image,
    output: Path,
    work: Path,
    slug: str,
    label: str,
    cells: list[Image.Image],
    cover_index: int,
) -> None:
    boxes = [
        cell.getchannel("A").point(lambda value: 255 if value >= 24 else 0).getbbox()
        for cell in cells
    ]
    visible_boxes = [box for box in boxes if box is not None]
    if not visible_boxes:
        raise ValueError(f"No visible pixels for {slug}")
    left = max(0, min(box[0] for box in visible_boxes) - 6)
    top = max(0, min(box[1] for box in visible_boxes) - 6)
    right = min(CELL_WIDTH, max(box[2] for box in visible_boxes) + 6)
    bottom = min(CELL_HEIGHT, max(box[3] for box in visible_boxes) + 6)
    content_box = (left, top, right, bottom)
    rendered = [render_frame(cell, label, content_box) for cell in cells]

    gif_frames = [frame.resize((540, 720), Image.Resampling.LANCZOS) for frame in rendered]
    gif_path = output / "gif" / f"{slug}.gif"
    gif_path.parent.mkdir(parents=True, exist_ok=True)
    gif_frames[0].save(
        gif_path,
        save_all=True,
        append_images=gif_frames[1:],
        duration=140,
        loop=0,
        optimize=True,
        disposal=2,
    )

    cover_path = output / "covers" / f"{slug}.jpg"
    cover_path.parent.mkdir(parents=True, exist_ok=True)
    rendered[cover_index % len(rendered)].save(cover_path, quality=95, subsampling=0)

    frame_dir = work / slug
    frame_dir.mkdir(parents=True, exist_ok=True)
    for index, frame in enumerate(rendered):
        frame.save(frame_dir / f"frame-{index:03d}.png", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("atlas", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()

    atlas = Image.open(args.atlas).convert("RGBA")
    if atlas.size != (1536, 2288):
        raise SystemExit(f"Expected a 1536x2288 v2 atlas, got {atlas.size}")

    args.output.mkdir(parents=True, exist_ok=True)
    args.work.mkdir(parents=True, exist_ok=True)

    for slug, label, row, count, cover_index in STATES:
        cells = [crop(atlas, row, column) for column in range(count)]
        save_state(atlas, args.output, args.work, slug, label, cells, cover_index)

    look_cells = [crop(atlas, 9, column) for column in range(8)]
    look_cells.extend(crop(atlas, 10, column) for column in range(8))
    save_state(
        atlas,
        args.output,
        args.work,
        "10-look-around",
        "环顾四周",
        look_cells,
        4,
    )


if __name__ == "__main__":
    main()
