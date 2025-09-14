import astro_constants
import astro_functions
import ephem
import math
from datetime import datetime, timedelta

# --- Configuration ---
# Location
latitude, longitude, elevation, tztext, timezone = astro_functions.get_location()

# Initialise display
inky_display, base_img, display_height, display_width, draw = astro_functions.init_display()

# Time
now_utc = datetime.utcnow()
now_local = datetime.now()

#endregion
#region EMPHEM
#POSITION
observer = ephem.Observer()
observer.lat = str(latitude)
observer.lon = str(longitude)
observer.elevation = int(elevation)
observer.date = now_utc

#STARS
stars = [
    'Sirius', 'Canopus', 'Arcturus', 'Vega', 'Capella', 'Rigel',
    'Procyon', 'Betelgeuse', 'Altair', 'Aldebaran', 'Spica',
    'Antares', 'Pollux', 'Fomalhaut', 'Deneb', 'Regulus'
]

visible_stars = []

for name in stars:
    star = ephem.star(name)
    star.compute(observer)
    if star.alt > 0:  
        visible_stars.append((name, star.alt, star.az, star.mag))

#PLANETS
planets = {
    'Mercury': ephem.Mercury(),
    'Venus': ephem.Venus(),
    'Mars': ephem.Mars(),
    'Jupiter': ephem.Jupiter(),
    'Saturn': ephem.Saturn(),
    'Uranus': ephem.Uranus(),
    'Neptune': ephem.Neptune(),
    'Pluto': ephem.Pluto()
}
visible_planets = []

for name, planet in planets.items():
    planet.compute(observer)
    
    if planet.alt > 0:  # Above the horizon
        visible_planets.append((name, planet.alt, planet.az, planet.mag))

#endregion

#DATE TITLE
date_short = datetime.now(timezone).strftime('%a %-d/%m/%y %H:%M')
title = "Stars and Planets"
date_width = draw.textlength(date_short, font=astro_constants.font)
x_title = (astro_constants.icon_size_sm[0] // 2)
y_title = (astro_constants.icon_size_sm[0] * 2)
x_date = display_width - date_width - 10
y_date = (astro_constants.icon_size_sm[0] * 2) + (astro_constants.font_height // 2)

draw.text((x_title, y_title), title, astro_constants.BLACK, font=astro_constants.font_large) 
draw.text((x_date, y_date), date_short, astro_constants.RED, font=astro_constants.font) 

#GRID TITLE
title_Name = "Name"
title_Mag = "Mag"
title_Alt = "Alt"
title_Az = "Az"
x_Name = 10
x_Mag = ((display_width // 4) // 2) * 3 - (astro_constants.icon_size_sm[0] // 2)
x_Alt = ((display_width // 4) // 2) * 5 - (astro_constants.icon_size_sm[0] // 2)
x_Az = ((display_width // 4) // 2) * 7 - (astro_constants.icon_size_sm[0] // 2)
y_Name = (astro_constants.icon_size_sm[0] * 3) + 30
y_Mag = (astro_constants.icon_size_sm[0] * 3) + 30
y_Alt = (astro_constants.icon_size_sm[0] * 3) + 30
y_Az = (astro_constants.icon_size_sm[0] * 3) + 30
draw.text((x_Name, y_Name), title_Name, astro_constants.BLACK, font=astro_constants.font) 
draw.text((x_Mag, y_Mag), title_Mag, astro_constants.GREEN, font=astro_constants.font) 
draw.text((x_Alt, y_Alt), title_Alt, astro_constants.RED, font=astro_constants.font) 
draw.text((x_Az, y_Az), title_Az, astro_constants.BLUE, font=astro_constants.font) 

#LIST PLANETS
x_offset = 10
y_offset = (astro_constants.icon_size_sm[0] * 4) + 40
for i, (name, alt, az, mag) in enumerate(visible_planets):
    y = y_offset + i * astro_constants.line_spacing
    draw.text((x_Name, y), f"{name}", astro_constants.BLACK, font=astro_constants.font) 
    draw.text((x_Mag, y), f"{mag:.1f}", astro_constants.GREEN, font=astro_constants.font) 
    draw.text((x_Alt, y), f"{math.degrees(alt):.1f}°", astro_constants.RED, font=astro_constants.font) 
    draw.text((x_Az, y), f"{math.degrees(az):.1f}°", astro_constants.BLUE, font=astro_constants.font) 

#LIST STARS
x_offset = 10
y_offset = (display_height // 2) + 10
for i, (name, alt, az, mag) in enumerate(visible_stars):
    y = y_offset + i * astro_constants.line_spacing
    draw.text((x_Name, y), f"{name}", astro_constants.BLACK, font=astro_constants.font) 
    draw.text((x_Mag, y), f"{mag:.1f}", astro_constants.GREEN, font=astro_constants.font) 
    draw.text((x_Alt, y), f"{math.degrees(alt):.1f}°", astro_constants.RED, font=astro_constants.font) 
    draw.text((x_Az, y), f"{math.degrees(az):.1f}°", astro_constants.BLUE, font=astro_constants.font) 

#FINAL DISPLAY
astro_functions.astro_display(base_img, inky_display)
