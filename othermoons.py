import astro_constants
import astro_functions
import json
import random

# Initialise display
inky_display, base_img, display_height, display_width, draw = astro_functions.init_display()

# Load JSON data
with open("moons.json", "r", encoding="utf-16") as f:
    moons = json.load(f)

# Pick a random moon entry
moon = random.choice(moons)
moon_name = moon["moon"]
planet_name = moon.get("planet", "Unknown planet")


# Pick 3 random fact pairs (or fewer if not enough)
fact_items = list(moon["facts"].items()) if moon["facts"] else []
selected_facts = random.sample(fact_items, min(3, len(fact_items))) if fact_items else [("Fact", "N/A")]

# Combine the selected facts into a single string with line breaks
facts_text = "\n".join(f"{key}: {val}" for key, val in selected_facts)

# Pick a random extra fact string
extra_fact = random.choice(moon["extra_facts"]) if moon["extra_facts"] else "No extra facts available."

# Measure heights for centering
moon_name_height = astro_constants.font.getbbox(moon_name)[3] - astro_constants.font.getbbox(moon_name)[1]
facts_lines = facts_text.split('\n')
facts_height = len(facts_lines) * astro_constants.font_height
planet_height = astro_constants.font.getbbox(planet_name)[3] - astro_constants.font.getbbox(planet_name)[1]
total_height = moon_name_height + planet_height + facts_height + astro_constants.font_height  # extra for spacing
start_y = (display_height - total_height) // 2

# Draw moon name centered horizontally
moon_name_x = (display_width - draw.textlength(moon_name, font=astro_constants.font)) // 2
draw.text((moon_name_x, start_y), moon_name, astro_constants.GREEN, font=astro_constants.font)
planet_y = start_y + moon_name_height + astro_constants.font_height // 2
planet_x = (display_width - draw.textlength(planet_name, font=astro_constants.font)) // 2
draw.text((planet_x, planet_y), planet_name, astro_constants.BLUE, font=astro_constants.font)

# Draw the combined facts block centered horizontally, stacked lines
facts_y = planet_y + planet_height + astro_constants.font_height // 2
for i, line in enumerate(facts_lines):
    line_x = (display_width - draw.textlength(line, font=astro_constants.font)) // 2
    line_y = facts_y + i * astro_constants.font_height
    draw.text((line_x, line_y), line, astro_constants.BLACK, font=astro_constants.font)

# Wrap and draw extra fact below the facts block
extra_start_y = facts_y + facts_height + astro_constants.font_height // 2
max_width = display_width - 10  # leave some margin
max_lines = 4                   # how many lines to show for extra_fact
wrapped_lines = astro_functions.wrap_text(extra_fact, astro_constants.font, draw, max_width, max_lines)

y = extra_start_y
for line in wrapped_lines:
    draw.text((5, y), line, astro_constants.RED, font=astro_constants.font)  # small left margin of 5px
    y += astro_constants.font_height

#FINAL DISPLAY
astro_functions.astro_display(base_img, inky_display)
