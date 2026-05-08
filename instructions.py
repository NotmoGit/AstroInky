"""
instructions.py — Button reference screen.

Shows the face photo and a label for each button's short and long press action.
Uses a smaller font so four columns fit comfortably.
"""

from PIL import Image, ImageFont, ImageOps

from display_utils import (
    new_canvas, show,
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    COLOR_PALETTE,
    RED,
)
from config import FONT_FILE, FACE_IMAGE

# Smaller font so four columns fit side by side
font        = ImageFont.truetype(str(FONT_FILE), 12)
ascent, descent = font.getmetrics()
font_height = ascent + descent

# ── Button labels — ordered left to right as they appear on the display ───────
# Each tuple: (short press label, long press label)
BUTTONS = [
    ("Moon",  "Instructions"),
    ("Stars", "Other Moons"),
    ("Solar", "AstroPic"),
    ("About", "Shutdown"),
]

# ── Drawing ───────────────────────────────────────────────────────────────────
img, draw = new_canvas()

# Face photo at the bottom of the screen
face        = Image.open(FACE_IMAGE).convert("RGBA")
face_fitted = ImageOps.contain(face, (DISPLAY_WIDTH, DISPLAY_WIDTH))
frame       = Image.new("RGBA", (DISPLAY_WIDTH, face_fitted.height), (255, 255, 255, 255))
frame.paste(face_fitted, ((DISPLAY_WIDTH - face_fitted.width) // 2, 0))
img.paste(frame, ((DISPLAY_WIDTH - frame.width) // 2, DISPLAY_HEIGHT - frame.height))

# Button labels across the top
col_w = DISPLAY_WIDTH // 4
for i, (short, long_press) in enumerate(BUTTONS):
    col_x = i * col_w

    short_w = draw.textbbox((0, 0), short,      font=font)[2]
    long_w  = draw.textbbox((0, 0), long_press, font=font)[2]

    x_short = col_x + (col_w - short_w) // 2
    x_long  = col_x + (col_w - long_w)  // 2

    draw.text((x_short, 10),                  short,      RED, font=font)
    draw.text((x_long,  10 + font_height + 5), long_press, RED, font=font)

show(img)
