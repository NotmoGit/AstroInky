"""
moon.py — Moon phase screen.

Shows the current phase image, date, azimuth, altitude,
and next moonrise / moonset times.
"""

import ephem
from PIL import Image

from astro_utils import make_observer, moon_phase_name, phase_image_path, rise_set_times, local_now
from display_utils import (
    new_canvas, draw_nav, load_icon, show,
    BW_PALETTE, COLOR_PALETTE,
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    font, font_large, font_height, line_spacing,
    icon_sm, icon_lg,
    BLACK, GREEN, ICON,
)

# ── Astronomy ─────────────────────────────────────────────────────────────────
observer    = make_observer()
moon        = ephem.Moon()
moon.compute(observer)

phase       = moon_phase_name(observer)
phase_img   = phase_image_path(phase)
azimuth     = float(moon.az)  * (180.0 / ephem.pi)
altitude    = float(moon.alt) * (180.0 / ephem.pi)
rise, sset  = rise_set_times(observer, moon)

# ── Drawing ───────────────────────────────────────────────────────────────────
img, draw = new_canvas()

# Moon phase image — black & white dithered
square     = (DISPLAY_WIDTH - 10, DISPLAY_WIDTH - 10)
phase_pil  = Image.open(phase_img).convert("RGBA").resize(square)
bg         = Image.new("RGBA", phase_pil.size, (255, 255, 255, 255))
flat       = Image.alpha_composite(bg, phase_pil)
moon_bw    = flat.convert("RGB").quantize(palette=BW_PALETTE, dither=Image.Dither.FLOYDSTEINBERG)
moon_x     = (DISPLAY_WIDTH  // 2) - (moon_bw.width  // 2)
moon_y     = font_height * 3 + icon_sm[0]
img.paste(moon_bw.convert("RGB"), (moon_x, moon_y))

# Date heading
date_str   = local_now().strftime("%A %d %B %Y")
date_w     = draw.textlength(date_str, font=font_large)
draw.text(((DISPLAY_WIDTH - date_w) // 2, icon_lg[0] + 10), date_str, GREEN, font=font_large)

# Left and right data columns
bottom     = DISPLAY_HEIGHT - 10 - font_height
left_col   = [
    (phase,                  ICON["phase"]),
    (f"{azimuth:.2f}°",      ICON["azimuth"]),
    (rise,                   ICON["moonrise"]),
]
right_col  = [
    ("",                     ICON["blank"]),
    (f"{altitude:.2f}°",     ICON["height"]),
    (sset,                   ICON["moonset"]),
]

for col, x_icon in [(left_col, 10), (right_col, DISPLAY_WIDTH // 2)]:
    for i, (text, icon_path) in enumerate(col):
        y    = bottom - (i * line_spacing) - icon_lg[0]
        x_text = x_icon + icon_lg[0] + 20
        img.paste(load_icon(icon_path, icon_lg), (x_icon, y))
        draw.text((x_text, y + font_height // 2), text, GREEN, font=font)

# Navigation bar
draw_nav(img, [ICON["moon"], ICON["planet"], ICON["solar"], ICON["nose"]])

show(img)
