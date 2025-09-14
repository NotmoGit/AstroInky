import astro_constants
import astro_functions
import requests
from PIL import Image, ImageOps

# Initialise display
inky_display, base_img, display_height, display_width, draw = astro_functions.init_display()

# Get image info from API
while True:
    response = requests.get(astro_functions.config['picture']['nasa_api_url'], params={'api_key': astro_functions.config['picture']['nasa_api_key'], 'count': 1})
    response.raise_for_status()
    data = response.json()[0]

    if data['media_type'] == 'image':
        image_url = data['url']
        title = data['title']
        explanation = data['explanation']
        break  # exit loop if it's an image

# Download image
response = requests.get(image_url)
response.raise_for_status()
with open(astro_functions.config['picture']['pic_save_path'], 'wb') as f:
    f.write(response.content)

# Process the image for Inky
apod = Image.open(astro_functions.config['picture']['pic_save_path']).convert("RGBA")
apod_crop = ImageOps.contain(apod, (display_width, display_width))  # resize to max width x width
image_frame = Image.new("RGBA", (display_width, apod_crop.height), (255, 255, 255, 255))
x = (display_width - apod_crop.width) // 2
y = 0
image_frame.paste(apod_crop, (x, y))  # <-- paste resized image here

# Write title text onto base image
margin = 10
title_y = astro_constants.nav_y + astro_constants.icon_size_sm[1] + margin
title_x = (display_width - draw.textlength(title.replace('\n', ' '), font=astro_constants.font)) // 2
draw.text((title_x, title_y), title.replace('\n', ' '), astro_constants.RED, font=astro_constants.font)

# Place downloaded image on base image
image_x = (display_width - image_frame.width) // 2
image_y = title_y + astro_constants.font_height + margin # margin + space for title
base_img.paste(image_frame, (image_x, image_y))

# Work out padding for the text supplied by NASA
text_block_width = display_width - 40
text_block_height = display_height - image_frame.height - title_y - astro_constants.nav_y - margin
max_lines = text_block_height // astro_constants.font_height - 1
lines = astro_functions.wrap_text(explanation, astro_constants.font, draw, text_block_width, max_lines)
max_text_start_y = display_height - text_block_height - 20
text_start_y = image_y + image_frame.height + margin

# Write out the text supplied by NASA onto the base image
for line in lines:
    line_width = draw.textlength(line, font=astro_constants.font)
    x = (display_width - line_width) // 2
    draw.text((x, text_start_y), line, astro_constants.GREEN, font=astro_constants.font)
    text_start_y += astro_constants.font_height


# Final Display
astro_functions.astro_display(base_img, inky_display)

# --- DEBUG INFO ---
print(f"URL: {image_url}")

