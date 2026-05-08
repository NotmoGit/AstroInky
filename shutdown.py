"""
shutdown.py — Shutdown confirmation screen.

Displays a message, holds briefly so the display can refresh,
then the system shutdown is triggered by handler.py.
"""

import time

from display_utils import (
    new_canvas, show,
    DISPLAY_WIDTH,
    font,
    RED,
)

# ── Drawing ───────────────────────────────────────────────────────────────────
img, draw = new_canvas()

message = "System is shut down — reconnect power to start"
msg_x   = (DISPLAY_WIDTH - draw.textlength(message, font=font)) // 2
draw.text((msg_x, 100), message, RED, font=font)

show(img)

# Give the e-ink display time to finish refreshing before power is cut
time.sleep(3)
