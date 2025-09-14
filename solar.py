import astro_constants
import astro_functions
import ephem
import math
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont # Font import still needed for Image, but not used for text drawing

# --- Configuration ---
# Location
latitude, longitude, elevation, tztext, timezone = astro_functions.get_location()

# Time
now_utc = datetime.utcnow()
now_local = datetime.now()

# Initialise display
inky_display, base_img, display_height, display_width, draw = astro_functions.init_display()

#region DIAGRAM PARAMETERS

# --- Diagram Parameters ---
CENTER_X, CENTER_Y = display_width // 2, display_height // 2
SUN_OUTER_RADIUS = 10
SUN_INNER_RADIUS = 6
PLANET_DOT_SIZE = 6 # Radius of planet dots

#ORBIT RINGS
ORBIT_RADII = {
    "Mercury": 20,
    "Venus": 32,
    "Earth": 48,
    "Mars": 70,
    "Jupiter": 133,
    "Saturn": 165,
    "Uranus": 199,
    "Neptune": 221,
}

#PLANETS
PLANETS_TO_DRAW = {
    "Mercury": ephem.Mercury(),
    "Venus": ephem.Venus(),
    "Earth": None,
    "Mars": ephem.Mars(),
    "Jupiter": ephem.Jupiter(),
    "Saturn": ephem.Saturn(),
    "Uranus": ephem.Uranus(),
    "Neptune": ephem.Neptune(),
}

#PLANET COLORS



PLANET_COLORS = {
    "Mercury": astro_constants.RED,
    "Venus":   astro_constants.YELLOW,
    "Earth":   astro_constants.GREEN,
    "Mars":    astro_constants.RED,
    "Jupiter": astro_constants.RED,
    "Saturn":  astro_constants.YELLOW,
    "Uranus":  astro_constants.BLUE,
    "Neptune": astro_constants.BLUE,
}

#endregion

#region DRAWING

# Write title text onto base image
margin = 10
title = "Solar display for your current location"
title_y = astro_constants.nav_y + astro_constants.icon_size_sm[1] + margin
title_x = (display_width - draw.textlength(title, font=astro_constants.font)) // 2
draw.text((title_x, title_y), title, astro_constants.RED, font=astro_constants.font)

date=now_local

if date is None:
    observer_date = datetime.utcnow()
else:
    observer_date = date

obs = ephem.Observer()
obs.lat = str(latitude)
obs.lon = str(longitude)
obs.elevation = elevation
obs.date = observer_date

# --- 1. Draw the Sun ---
draw.ellipse(
(CENTER_X - SUN_OUTER_RADIUS, CENTER_Y - SUN_OUTER_RADIUS,
    CENTER_X + SUN_OUTER_RADIUS, CENTER_Y + SUN_OUTER_RADIUS),
fill=inky_display.YELLOW
)
draw.ellipse(
(CENTER_X - SUN_INNER_RADIUS, CENTER_Y - SUN_INNER_RADIUS,
    CENTER_X + SUN_INNER_RADIUS, CENTER_Y + SUN_INNER_RADIUS),
fill=inky_display.YELLOW
)

# --- 2. Draw Orbital Rings and Planets ---
for name, planet_obj in PLANETS_TO_DRAW.items():
    if name not in ORBIT_RADII:
        continue

    orbit_radius = ORBIT_RADII[name]
    dot_color = PLANET_COLORS.get(name, inky_display.WHITE)

    # Draw the orbital rings in the planet's color
    if (CENTER_X - orbit_radius >= 0 and CENTER_Y - orbit_radius >= 0 and
        CENTER_X + orbit_radius <= display_width and CENTER_Y + orbit_radius <= display_height):
        RING_THICKNESS = 3  # change to 2, 4, etc. if desired
        for offset in range(-(RING_THICKNESS // 2), (RING_THICKNESS // 2) + 1):
            draw.ellipse(
                (CENTER_X - orbit_radius - offset, CENTER_Y - orbit_radius - offset,
                CENTER_X + orbit_radius + offset, CENTER_Y + orbit_radius + offset),
                outline=dot_color
            )

    # Compute planet's heliocentric position
    if name == "Earth":
        sun = ephem.Sun(obs)
        sun_hlon = float(sun.hlon)
        planet_h_lon = (sun_hlon + math.pi) % (2 * math.pi)
    else:
        planet_obj.compute(obs)
        planet_h_lon = float(planet_obj.hlon)

    # Calculate planet's (x, y) coordinates on its ring
    planet_x = CENTER_X + int(orbit_radius * math.cos(planet_h_lon))
    planet_y = CENTER_Y + int(orbit_radius * math.sin(planet_h_lon))

    # Draw the planet dot
    draw.ellipse(
        (planet_x - PLANET_DOT_SIZE, planet_y - PLANET_DOT_SIZE,
        planet_x + PLANET_DOT_SIZE, planet_y + PLANET_DOT_SIZE),
        fill=dot_color
    )
#endregion

#FINAL DISPLAY
astro_functions.astro_display(base_img, inky_display)



