"""
display_utils.py — everything to do with the Inky display.

Import this instead of repeating 80 lines of boilerplate in every screen.
Provides: colors, palettes, fonts, icon loader, nav bar drawer, show().
"""

import io
from pathlib import Path

import cairosvg
from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

from config import FONT_FILE, FONT_SIZE, FONT_SIZE_LARGE, ICONS_DIR

# ── Display init ─────────────────────────────────────────────────────────────
inky = auto()
DISPLAY_HEIGHT, DISPLAY_WIDTH = inky.resolution

# ── Colors (RGB values — these feed into the quantize palette below) ─────────
BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255, 0,   0)
GREEN  = (0,   255, 0)
BLUE   = (0,   0,   255)
YELLOW = (255, 255, 0)

# ── Quantize palettes ────────────────────────────────────────────────────────
# PIL's quantize() maps each RGB pixel to the nearest entry in this palette.
# The palette image is a throwaway 16×16 "P" mode image — PIL just uses it
# as a lookup table, the actual pixels don't matter.

_color_palette_data = [
    0,   0,   0,    # 0 Black
    255, 255, 255,  # 1 White
    255, 0,   0,    # 2 Red
    0,   255, 0,    # 3 Green
    0,   0,   255,  # 4 Blue
    255, 255, 0,    # 5 Yellow
] + [0, 0, 0] * 250

_bw_palette_data = [
    0,   0,   0,    # 0 Black
    255, 255, 255,  # 1 White
] + [0, 0, 0] * 254

COLOR_PALETTE = Image.new("P", (16, 16))
COLOR_PALETTE.putpalette(_color_palette_data)

BW_PALETTE = Image.new("P", (16, 16))
BW_PALETTE.putpalette(_bw_palette_data)

# ── Fonts ────────────────────────────────────────────────────────────────────
font       = ImageFont.truetype(str(FONT_FILE), FONT_SIZE)
font_large = ImageFont.truetype(str(FONT_FILE), FONT_SIZE_LARGE)

ascent, descent = font.getmetrics()
font_height  = ascent + descent
line_spacing = font_height * 2

# ── Icon sizes ───────────────────────────────────────────────────────────────
icon_sm = (font_height,      font_height)
icon_lg = (font_height * 2,  font_height * 2)
icon_xl = (font_height * 10, font_height * 10)


# ── Helpers ──────────────────────────────────────────────────────────────────

def new_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    """Return a blank white RGB canvas and its draw object."""
    img  = Image.new("RGB", (DISPLAY_WIDTH, DISPLAY_HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    return img, draw


def load_icon(path: Path | str, size: tuple[int, int]) -> Image.Image:
    """Render an SVG icon to a palette-quantized RGBA image at the given size."""
    png  = cairosvg.svg2png(url=str(path), output_width=size[0], output_height=size[1])
    rgba = Image.open(io.BytesIO(png)).convert("RGBA")
    bg   = Image.new("RGBA", size, (255, 255, 255, 255))
    flat = Image.alpha_composite(bg, rgba)
    quantized = flat.convert("RGB").quantize(palette=COLOR_PALETTE)
    result = Image.new("RGBA", rgba.size)
    result.paste(quantized)
    return result


def draw_nav(img: Image.Image, icons: list[Path | str]) -> None:
    """
    Draw four navigation icons across the top of the canvas.

    icons: list of exactly 4 SVG paths, left to right.
    """
    assert len(icons) == 4, "draw_nav expects exactly 4 icons"
    nav_y     = 10
    col_half  = (DISPLAY_WIDTH // 4) // 2
    x_offsets = [col_half * (2 * i + 1) - icon_sm[0] // 2 for i in range(4)]
    for x, path in zip(x_offsets, icons):
        img.paste(load_icon(path, icon_sm), (x, nav_y))


def show(img: Image.Image) -> None:
    """Rotate, quantize, and push the image to the Inky display."""
    final = img.rotate(90, expand=True).quantize(palette=COLOR_PALETTE)
    inky.set_image(final)
    inky.show()


# ── Convenience icon paths ───────────────────────────────────────────────────
# Import these rather than spelling out the path string every time.
ICON = {
    name: ICONS_DIR / f"{name}.svg"
    for name in [
        "refresh", "solar", "planet", "nose",
        "moon", "phase", "azimuth", "height",
        "moonrise", "moonset", "blank", "eye",
        "star", "heart",
    ]
}
