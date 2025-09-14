import astro_constants
import astro_functions
import ephem
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime, timedelta
from timezonefinder import timezone_at

# Initialise display
inky_display, base_img, display_height, display_width, draw = astro_functions.init_display()
square = ((display_width - 10), (display_width - 10))

# Time
now_utc = datetime.utcnow()
now_local = datetime.now()

# Location
latitude, longitude, elevation, tztext, timezone = astro_functions.get_location()

#endregion
#region EMPHEM
#POSITION
observer = ephem.Observer()
observer.lat = str(latitude)
observer.lon = str(longitude)
observer.elevation = int(elevation)
observer.date = now_utc

#WAX OR WANE
def get_precise_moon_phase(observer):
    moon = ephem.Moon(observer)
    sun = ephem.Sun(observer)
    illumination = moon.phase
    elongation = ephem.separation(moon, sun)  # angle between moon and sun

    # Calculate waxing or waning
    moon.compute(observer)
    sun.compute(observer)

    # Difference in ecliptic longitude (positive if waxing)
    waxing = (moon.elong > 0 and moon.elong < ephem.pi)

    if illumination == 0:
        return "New Moon"
    elif 0 < illumination < 50:
        return "Waxing Crescent" if waxing else "Waning Crescent"
    elif 50 <= illumination < 99:
        if elongation < ephem.pi:
            return "First Quarter" if waxing else "Last Quarter"
        else:
            return "Waxing Gibbous" if waxing else "Waning Gibbous"
    elif illumination >= 99.5:
        return "Full Moon"
    else:
        return "Unknown Phase"
    
#MOON IMAGE
moon_img_path = astro_functions.config['path']['astro_path'] + "/AstroInky/phases"
def get_moon_phase_img(phase):
    match phase.lower():
        case "new moon":
            return f"{moon_img_path}/new_moon.png"
        case "waxing crescent":
            return f"{moon_img_path}/waxing_crescent.png"
        case "first quarter":
            return f"{moon_img_path}/first_quarter.png"
        case "waxing gibbous":
            return f"{moon_img_path}/waxing_gibbous.png"
        case "full moon":
            return f"{moon_img_path}/full_moon.png"
        case "waning gibbous":
            return f"{moon_img_path}/waning_gibbous.png"
        case "last quarter" | "third quarter":
            return f"{moon_img_path}/last_quarter.png"
        case "waning crescent":
            return f"{moon_img_path}/waning_crescent.png"
        case _:
            return "Unknown moon phase."
    
# MOONPHASE
moon_phase = get_precise_moon_phase(observer) # Returns phase as text
moon_phase_image = get_moon_phase_img(moon_phase) # Returns the phase image path

moon = ephem.Moon()
moon.compute(observer)

#MOON FINDER
moon_azimuth = azimuth_deg = float(moon.az) * (180.0 / ephem.pi)
moon_altitude = altitude_deg = float(moon.alt) * (180.0 / ephem.pi)

#MOONRISE & SET
try:
    moonrise_time = (ephem.to_timezone(observer.next_rising(moon),timezone)).strftime('%H:%M %a')
except (ephem.AlwaysUpError, ephem.NeverUpError):
    moonrise_time = "Not visible today"
try:
    moonset_time = (ephem.to_timezone(observer.next_setting(moon),timezone)).strftime('%H:%M %a')
except (ephem.AlwaysUpError, ephem.NeverUpError):
    moonset_time = "Not visible today"
#endregion

#MOON IMAGE
moon = Image.open(moon_phase_image).convert("RGBA").resize(square)   
white_bg = Image.new("RGBA", moon.size, (255, 255, 255, 255))
flattened_moon = Image.alpha_composite(white_bg, moon)
moon_img = flattened_moon.convert("RGB").quantize(palette=astro_constants.bw_palette_img, dither=Image.Dither.FLOYDSTEINBERG)  
center_moon = (display_width // 2) - (moon_img.height // 2)
base_img.paste(moon_img.convert("RGB"), (center_moon, (astro_constants.font_height * 3 + astro_constants.icon_size_lg[0])))

#TEXTAREAS
text_area_top = (moon_img.height + astro_constants.line_spacing)                                             #defines the top of the text area (moon height + 100 padding)
text_area_bottom = (display_height - 10) - astro_constants.font_height                              #defines the top of the text area (total height - 10 padding, -font height as padding)
text_area_height = text_area_bottom - text_area_top                                 #defubes the difference between top and bottom as the total height

#DATE TITLE
date = datetime.now(timezone).strftime('%A %d %B %Y')
title_width = draw.textlength(date, font=astro_constants.font_large)
x_title = astro_constants.icon_size_lg[0] + 10
y_title = (display_width // 2) - (title_width // 2)
draw.text((y_title, x_title), date, astro_constants.GREEN, font=astro_constants.font_large) 


#LEFT COLUMN
left_icon = 10 
left_icon_text = left_icon + astro_constants.icon_size_lg[0] + 10
left_text_lines = [
    (moon_phase,"icons/phase.svg"), 
    (f"{azimuth_deg:.2f}°", "icons/azimuth.svg"),
    (moonrise_time, "icons/moonrise.svg"),
]
for i, (text_data, icon_path) in enumerate(left_text_lines):
    y = text_area_bottom - (i * astro_constants.line_spacing) - astro_constants.icon_size_lg[0]
    left_text_data = left_icon_text + 10
    icon = astro_functions.load_svg_icon(icon_path, size=astro_constants.icon_size_lg)
    base_img.paste(icon, (left_icon, y))
    draw.text((left_text_data, y + (astro_constants.font_height*0.5)), text_data, astro_constants.GREEN, font=astro_constants.font)
 
#RIGHT COLUMN
blank = ""
right_icon = (display_width // 2) 
right_icon_text = right_icon + astro_constants.icon_size_lg[0] + 10
right_text_lines = [ 
    (blank,"icons/blank.svg"),
    (f"{altitude_deg:.2f}°", "icons/height.svg"),
    (moonset_time, "icons/moonset.svg"),
]
for i, (text_data, icon_path) in enumerate(right_text_lines):
    y = text_area_bottom - (i * astro_constants.line_spacing) - astro_constants.icon_size_lg[0]
    right_text_data = right_icon_text + 10
    icon = astro_functions.load_svg_icon(icon_path, size=astro_constants.icon_size_lg)
    base_img.paste(icon, (right_icon, y))
    draw.text((right_text_data, y + (astro_constants.font_height*0.5)), text_data, astro_constants.GREEN, font=astro_constants.font)

#FINAL DISPLAY
astro_functions.astro_display(base_img, inky_display)
