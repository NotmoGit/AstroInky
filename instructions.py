import astro_constants
import astro_functions

# Initialise display
inky_display, base_img, display_height, display_width, draw = astro_functions.init_display()

# Calculate horizontal spacing
column_width = display_width // 4  # 4 columns

button_labels = [('D','Moon Info','Instructions'),('C','Visible\nBodies','A Random\n    Moon'),('B',' Visual\n  Solar\nSystem','Random\n  NASA\n  Image'),('A','About','Shutdown')]

for i, (button, primary, long_press) in enumerate(button_labels):
    column_x = i * column_width

    # Measure text widths
    primary_bbox = draw.textbbox((0, 0), primary, font=astro_constants.font)
    primary_width = primary_bbox[2] - primary_bbox[0]
    long_text = f"{long_press}"
    long_bbox = draw.textbbox((0, 0), long_text, font=astro_constants.font)
    long_width = long_bbox[2] - long_bbox[0]

    # Center text in column
    x_primary = column_x + (column_width - primary_width) // 2
    x_long = column_x + (column_width - long_width) // 2

    margin = 10
    y_primary = astro_constants.nav_y + astro_constants.icon_size_sm[1] + margin
    y_long = y_primary + (astro_constants.font_height * 3) + 5

    draw.text((x_primary, y_primary), primary, astro_constants.RED, font=astro_constants.font)
    draw.text((x_long, y_long), f"{long_press}", astro_constants.GREEN, font=astro_constants.font)

# The rest of the text
align_center = display_width // 2
message_top = "This is AstroInky!"
top_center = align_center - (draw.textlength(message_top, font=astro_constants.font_large) / 2)
message_mid = "Short press a button to view the page in red"
mid_center = align_center - (draw.textlength(message_mid, font=astro_constants.font) / 2)
message_footer = "Long press a button to view the page in green"
footer_center = align_center - (draw.textlength(message_footer, font=astro_constants.font) / 2)

draw.text((top_center, 300), message_top, astro_constants.BLACK, font=astro_constants.font_large)
draw.text((mid_center, 600), message_mid, astro_constants.RED, font=astro_constants.font)
draw.text((footer_center, 600 + (astro_constants.font_height * 2)), message_footer, astro_constants.GREEN, font=astro_constants.font)

# A moon icon
image = astro_functions.load_svg_icon('icons/moon.svg', size=astro_constants.icon_size_xl)
base_img.paste(image, ((display_width // 2) - (astro_constants.icon_size_xl[0] // 2), (display_height // 2) - (astro_constants.icon_size_xl[0] // 2) + 50))

#FINAL DISPLAY
astro_functions.astro_display(base_img, inky_display)
