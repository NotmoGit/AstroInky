import astro_constants
import astro_functions
import io
import time

# Initialise display
inky_display, base_img, display_height, display_width, draw = astro_functions.init_display()

#message
align_center = display_width // 2
message_top = "System is shut down - your battery is too low"
top_center = align_center - (draw.textlength(message_top, font=astro_constants.font) / 2)
draw.text((top_center, 100), message_top, astro_constants.RED, font=astro_constants.font) 

#FINAL DISPLAY
astro_functions.astro_display(base_img, inky_display)
time.sleep(3)
