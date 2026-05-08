"""
solar.py — Heliocentric solar system diagram.

Draws the sun at centre, orbital rings, and each planet's current position
calculated from its heliocentric longitude.
"""

import math

import ephem
from PIL import Image

from astro_utils import make_observer, utc_now
from display_utils import (
    new_canvas, draw_nav, show,
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    BLACK, RED, GREEN, BLUE, YELLOW,
    COLOR_PALETTE, ICON,
)

# ── Diagram constants ─────────────────────────────────────────────────────────
CX, CY         = DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2
SUN_RADIUS     = 10
SUN_CORE       = 6
PLANET_RADIUS  = 6
RING_THICKNESS = 3

# Orbital radii in pixels — tuned to fit the display
ORBIT_RADII = {
    "Mercury": 20,
    "Venus":   32,
    "Earth":   48,
    "Mars":    70,
    "Jupiter": 133,
    "Saturn":  165,
    "Uranus":  199,
    "Neptune": 221,
}

PLANET_COLORS = {
    "Mercury": RED,
    "Venus":   YELLOW,
    "Earth":   GREEN,
    "Mars":    RED,
    "Jupiter": RED,
    "Saturn":  YELLOW,
    "Uranus":  BLUE,
    "Neptune": BLUE,
}

PLANET_BODIES = {
    "Mercury": ephem.Mercury(),
    "Venus":   ephem.Venus(),
    "Earth":   None,           # derived from the Sun's position
    "Mars":    ephem.Mars(),
    "Jupiter": ephem.Jupiter(),
    "Saturn":  ephem.Saturn(),
    "Uranus":  ephem.Uranus(),
    "Neptune": ephem.Neptune(),
}

# ── Astronomy (always UTC) ────────────────────────────────────────────────────
observer = make_observer()

# ── Drawing ───────────────────────────────────────────────────────────────────
img, draw = new_canvas()

# Sun
for r, color in [(SUN_RADIUS, YELLOW), (SUN_CORE, YELLOW)]:
    draw.ellipse((CX - r, CY - r, CX + r, CY + r), fill=color)

# Planets
for name, body in PLANET_BODIES.items():
    orbit_r = ORBIT_RADII[name]
    color   = PLANET_COLORS[name]

    # Orbital ring (only if it fits on screen)
    if (CX - orbit_r >= 0 and CY - orbit_r >= 0 and
            CX + orbit_r <= DISPLAY_WIDTH and CY + orbit_r <= DISPLAY_HEIGHT):
        half = RING_THICKNESS // 2
        for offset in range(-half, half + 1):
            draw.ellipse(
                (CX - orbit_r - offset, CY - orbit_r - offset,
                 CX + orbit_r + offset, CY + orbit_r + offset),
                outline=color,
            )

    # Heliocentric longitude → (x, y) on ring
    if name == "Earth":
        sun      = ephem.Sun(observer)
        sun.compute(observer)
        h_lon    = (float(sun.hlon) + math.pi) % (2 * math.pi)
    else:
        body.compute(observer)
        h_lon    = float(body.hlon)

    px = CX + int(orbit_r * math.cos(h_lon))
    py = CY + int(orbit_r * math.sin(h_lon))

    r = PLANET_RADIUS
    draw.ellipse((px - r, py - r, px + r, py + r), fill=color)

# Navigation bar
draw_nav(img, [ICON["moon"], ICON["planet"], ICON["refresh"], ICON["nose"]])

show(img)
