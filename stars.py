"""
stars.py — Visible stars and planets screen.

Lists all named stars and solar system planets currently above the horizon,
showing magnitude, altitude, and azimuth for each.
"""

import math

import ephem

from astro_utils import make_observer, local_now
from display_utils import (
    new_canvas, draw_nav, show,
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    font, font_large, font_height, line_spacing,
    icon_sm,
    BLACK, RED, GREEN, BLUE, ICON,
)

# ── Named stars to check ──────────────────────────────────────────────────────
STAR_NAMES = [
    "Sirius", "Canopus", "Arcturus", "Vega", "Capella",
    "Rigel", "Procyon", "Betelgeuse", "Altair", "Aldebaran",
    "Spica", "Antares", "Pollux", "Fomalhaut", "Deneb", "Regulus",
]

PLANET_BODIES = {
    "Mercury": ephem.Mercury(),
    "Venus":   ephem.Venus(),
    "Mars":    ephem.Mars(),
    "Jupiter": ephem.Jupiter(),
    "Saturn":  ephem.Saturn(),
    "Uranus":  ephem.Uranus(),
    "Neptune": ephem.Neptune(),
    "Pluto":   ephem.Pluto(),
}

# ── Astronomy (always UTC) ────────────────────────────────────────────────────
observer = make_observer()

visible_planets: list[tuple] = []
for name, planet in PLANET_BODIES.items():
    planet.compute(observer)
    if planet.alt > 0:
        visible_planets.append((name, planet.alt, planet.az, planet.mag))

visible_stars: list[tuple] = []
for name in STAR_NAMES:
    star = ephem.star(name)
    star.compute(observer)
    if star.alt > 0:
        visible_stars.append((name, star.alt, star.az, star.mag))

# ── Column x positions ────────────────────────────────────────────────────────
col_half = (DISPLAY_WIDTH // 4) // 2
x_name   = 10
x_mag    = col_half * 3  - icon_sm[0] // 2
x_alt    = col_half * 5  - icon_sm[0] // 2
x_az     = col_half * 7  - icon_sm[0] // 2

# ── Drawing ───────────────────────────────────────────────────────────────────
img, draw = new_canvas()

# Title row
title_y = icon_sm[0] * 2
draw.text((x_name, title_y), "Stars and Planets", BLACK, font=font_large)

date_str   = local_now().strftime("%a %-d/%m/%y %H:%M")
date_width = draw.textlength(date_str, font=font)
draw.text((DISPLAY_WIDTH - date_width - 10, title_y + font_height // 2), date_str, RED, font=font)

# Column headers
header_y = icon_sm[0] * 3 + 30
draw.text((x_name, header_y), "Name", BLACK, font=font)
draw.text((x_mag,  header_y), "Mag",  GREEN, font=font)
draw.text((x_alt,  header_y), "Alt",  RED,   font=font)
draw.text((x_az,   header_y), "Az",   BLUE,  font=font)

def _draw_rows(items, start_y):
    for i, (name, alt, az, mag) in enumerate(items):
        y = start_y + i * line_spacing
        draw.text((x_name, y), name,                          BLACK, font=font)
        draw.text((x_mag,  y), f"{mag:.1f}",                  GREEN, font=font)
        draw.text((x_alt,  y), f"{math.degrees(alt):.1f}°",   RED,   font=font)
        draw.text((x_az,   y), f"{math.degrees(az):.1f}°",    BLUE,  font=font)

_draw_rows(visible_planets, icon_sm[0] * 4 + 40)
_draw_rows(visible_stars,   DISPLAY_HEIGHT // 2 + 10)

# Navigation bar
draw_nav(img, [ICON["moon"], ICON["refresh"], ICON["solar"], ICON["nose"]])

show(img)
