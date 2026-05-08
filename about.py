"""
about.py — About screen.

Displays a heart and a custom message.
"""

from display_utils import (
    new_canvas, draw_nav, load_icon, show,
    DISPLAY_WIDTH, DISPLAY_HEIGHT,
    font, font_height,
    icon_lg, icon_xl,
    BLACK, RED, ICON,
)

# ── Drawing ───────────────────────────────────────────────────────────────────
img, draw = new_canvas()

# Large heart centred on screen
heart_x = (DISPLAY_WIDTH  // 2) - (icon_xl[0] // 2)
heart_y = (DISPLAY_HEIGHT // 2) - (icon_xl[1] // 2)
img.paste(load_icon(ICON["heart"], icon_xl), (heart_x, heart_y))

# Smaller heart layered on top
small_heart_x = (DISPLAY_WIDTH  // 2) - (icon_lg[0] // 2)
small_heart_y = (DISPLAY_HEIGHT // 2) - (icon_lg[1] // 2)
img.paste(load_icon(ICON["heart"], icon_lg), (small_heart_x, small_heart_y))

# Messages
cx = DISPLAY_WIDTH // 2

def _centred(text, y, color):
    x = cx - draw.textlength(text, font=font) // 2
    draw.text((x, y), text, color, font=font)

_centred("Custom message line 1", 200, RED)
_centred("Custom message line 2",             550, RED)
_centred("Custom message line 3",
         DISPLAY_HEIGHT - font_height * 2,                      BLACK)

# Navigation bar
draw_nav(img, [ICON["moon"], ICON["planet"], ICON["solar"], ICON["refresh"]])

show(img)
