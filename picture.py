"""
picture.py — NASA Astronomy Picture of the Day screen.

Fetches a random APOD image, downloads it, and displays it alongside
the title and a wrapped excerpt of the explanation.
"""

import requests
from PIL import Image, ImageOps

from astro_utils import wrap_text
from display_utils import (
    new_canvas, draw_nav, show,
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    font, font_height,
    icon_sm,
    RED, GREEN, ICON,
)
from config import NASA_API_KEY, APOD_CACHE

# ── Fetch a random APOD image (retry until we get an image, not a video) ─────
APOD_URL = "https://api.nasa.gov/planetary/apod"

while True:
    response = requests.get(APOD_URL, params={"api_key": NASA_API_KEY, "count": 1}, timeout=10)
    response.raise_for_status()
    data = response.json()[0]
    if data["media_type"] == "image":
        image_url   = data["url"]
        title       = data["title"]
        explanation = data["explanation"]
        break

# Download and cache image
image_data = requests.get(image_url, timeout=10)
image_data.raise_for_status()
APOD_CACHE.write_bytes(image_data.content)

# ── Process image ─────────────────────────────────────────────────────────────
apod        = Image.open(APOD_CACHE).convert("RGBA")
apod_fitted = ImageOps.contain(apod, (DISPLAY_WIDTH, DISPLAY_WIDTH))
frame       = Image.new("RGBA", (DISPLAY_WIDTH, apod_fitted.height), (255, 255, 255, 255))
frame.paste(apod_fitted, ((DISPLAY_WIDTH - apod_fitted.width) // 2, 0))

# ── Drawing ───────────────────────────────────────────────────────────────────
img, draw = new_canvas()

margin  = 10
title_y = margin + icon_sm[1] + margin
title_x = (DISPLAY_WIDTH - draw.textlength(title.replace("\n", " "), font=font)) // 2
draw.text((title_x, title_y), title.replace("\n", " "), RED, font=font)

image_y = title_y + font_height + margin
image_x = (DISPLAY_WIDTH - frame.width) // 2
img.paste(frame, (image_x, image_y))

# Explanation text below image
text_y      = image_y + frame.height + margin
text_w      = DISPLAY_WIDTH - 40
available_h = DISPLAY_HEIGHT - text_y - margin
max_lines   = available_h // font_height
lines       = wrap_text(explanation, font, draw, text_w, max_lines)

for line in lines:
    line_x = (DISPLAY_WIDTH - draw.textlength(line, font=font)) // 2
    draw.text((line_x, text_y), line, GREEN, font=font)
    text_y += font_height

# Navigation bar
draw_nav(img, [ICON["moon"], ICON["planet"], ICON["solar"], ICON["nose"]])

show(img)

print(f"APOD: {image_url}")
