"""
othermoons.py — Random moon facts screen.

Picks a random moon from moons.json and displays its name, parent planet,
three random facts, and one random extended fact.
"""

import json
import random

from astro_utils import wrap_text
from display_utils import (
    new_canvas, draw_nav, show,
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    font, font_height, line_spacing,
    BLACK, GREEN, BLUE, RED, ICON,
)
from config import MOONS_JSON

# ── Load data ─────────────────────────────────────────────────────────────────
with open(MOONS_JSON, encoding="utf-16") as f:
    all_moons = json.load(f)

moon        = random.choice(all_moons)
moon_name   = moon["moon"]
planet_name = moon.get("planet", "Unknown planet")

fact_pairs     = list(moon["facts"].items()) if moon["facts"] else []
selected_facts = random.sample(fact_pairs, min(3, len(fact_pairs))) if fact_pairs else [("Fact", "N/A")]
extra_fact     = random.choice(moon["extra_facts"]) if moon["extra_facts"] else "No extra facts available."

# ── Layout ────────────────────────────────────────────────────────────────────
facts_lines  = [f"{k}: {v}" for k, v in selected_facts]
facts_height = len(facts_lines) * font_height
name_h       = font.getbbox(moon_name)[3]   - font.getbbox(moon_name)[1]
planet_h     = font.getbbox(planet_name)[3] - font.getbbox(planet_name)[1]
total_h      = name_h + planet_h + facts_height + font_height
start_y      = (DISPLAY_HEIGHT - total_h) // 2

# ── Drawing ───────────────────────────────────────────────────────────────────
img, draw = new_canvas()

# Moon name
name_x = (DISPLAY_WIDTH - draw.textlength(moon_name, font=font)) // 2
draw.text((name_x, start_y), moon_name, GREEN, font=font)

# Planet name
planet_y = start_y + name_h + font_height // 2
planet_x = (DISPLAY_WIDTH - draw.textlength(planet_name, font=font)) // 2
draw.text((planet_x, planet_y), planet_name, BLUE, font=font)

# Facts block
facts_y = planet_y + planet_h + font_height // 2
for i, line in enumerate(facts_lines):
    line_x = (DISPLAY_WIDTH - draw.textlength(line, font=font)) // 2
    draw.text((line_x, facts_y + i * font_height), line, BLACK, font=font)

# Extra fact (wrapped)
extra_y    = facts_y + facts_height + font_height // 2
max_width  = DISPLAY_WIDTH - 10
max_lines  = 4
wrapped    = wrap_text(extra_fact, font, draw, max_width, max_lines)
for line in wrapped:
    draw.text((5, extra_y), line, RED, font=font)
    extra_y += font_height

# Navigation bar
draw_nav(img, [ICON["moon"], ICON["planet"], ICON["solar"], ICON["nose"]])

show(img)
