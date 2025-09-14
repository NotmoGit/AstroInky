import astro_constants
import cairosvg
import io
import re
import configparser
import time
import datetime

from zoneinfo import ZoneInfo
from timezonefinder import timezone_at
from PIL import Image, ImageDraw
from inky.auto import auto

config = configparser.ConfigParser()
config.read('config.ini')

yes_words = ('y', 'Y','yes','Yes','YES',1,'true','True',True)

# Init display
def init_display():
  inky_display = auto()
  display_height, display_width = inky_display.resolution                             #defines a canvas
  base_img = Image.new("RGB", (display_width, display_height), (255, 255, 255))           #creates the initial background object (img) - mode, size, color
  draw = ImageDraw.Draw(base_img)
  nav_about = load_svg_icon("icons/refresh.svg", size=astro_constants.icon_size_sm)
  nav_solar = load_svg_icon("icons/solar.svg", size=astro_constants.icon_size_sm)
  nav_star = load_svg_icon("icons/planet.svg", size=astro_constants.icon_size_sm)
  nav_phase = load_svg_icon("icons/moon.svg", size=astro_constants.icon_size_sm)
  nav_y = 10
  xA = ((display_width // 4) // 2) - (astro_constants.icon_size_sm[0] // 2) -1
  xB = ((display_width // 4) // 2) * 3 - (astro_constants.icon_size_sm[0] // 2) -1
  xC = ((display_width // 4) // 2) * 5 - (astro_constants.icon_size_sm[0] // 2) -1
  xD = ((display_width // 4) // 2) * 7 - (astro_constants.icon_size_sm[0] // 2) -1
  base_img.paste(nav_phase, (xA, nav_y))
  base_img.paste(nav_star, (xB, nav_y))
  base_img.paste(nav_solar, (xC, nav_y))
  base_img.paste(nav_about, (xD, nav_y))
  if config['global']['use_battery'] in yes_words:
    import ina219
    # Create an INA219 instance.
    ups_hat = ina219.ina219(addr=0x43)
    bus_voltage = ups_hat.getBusVoltage_V()             # voltage on V- (load side)
    current = ups_hat.getCurrent_mA()                   # current in mA
    power = ups_hat.getPower_W()                        # power in W
    p = (bus_voltage - 3)/1.2*100
    if(p > 100):p = 100
    if(p < 0):p = 0
    # Work out which icon to display
    xBat = display_width - astro_constants.icon_size_sm[0] - 4
    if (current > 0):
      battery = load_svg_icon("icons/battery-charging.svg", size=astro_constants.icon_size_sm)
    elif (int(p) > 75):
      battery = load_svg_icon("icons/battery-full.svg", size=astro_constants.icon_size_sm)
    elif (int(p) > 25):
      battery = load_svg_icon("icons/battery-half.svg", size=astro_constants.icon_size_sm)
    elif (int(p) > 10):
      battery = load_svg_icon("icons/battery-low.svg", size=astro_constants.icon_size_sm)
    else:
      battery = load_svg_icon("icons/battery.svg", size=astro_constants.icon_size_sm)
    base_img.paste(battery, (xBat, nav_y))
  if config['global']['show_timestamp'] in yes_words:
    message_timestamp = "Updated: " + datetime.datetime.now().strftime("%H:%M:%S %Z")
    ascent, descent = astro_constants.font_small.getmetrics()
    font_height = ascent + descent
    timestamp_x = display_width - draw.textlength(message_timestamp, font=astro_constants.font_small)
    timestamp_y = display_height - font_height
    draw.text((timestamp_x, timestamp_y), message_timestamp, astro_constants.BLUE, font=astro_constants.font_small)

  return (inky_display, base_img, display_height, display_width, draw)


def wrap_text(text, font, draw, max_width, max_lines):
    words = text.split()
    lines = []
    line = ""

    for word in words:
        test_line = line + word + " "
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line.rstrip())
            line = word + " "
        if len(lines) >= max_lines:
            break

    if line and len(lines) < max_lines:
        lines.append(line.rstrip())
    elif len(lines) == max_lines:
        # Join all visible lines so far
        full_text = " ".join(lines) + " " + line

        # Find the last full sentence ending
        match = list(re.finditer(r'([.!?])\s+', full_text))
        if match:
            last_end = match[-1].end()
            clean_text = full_text[:last_end].strip()
        else:
            clean_text = full_text.strip()

        # Re-wrap from clean_text
        lines = []
        line = ""
        for word in clean_text.split():
            test_line = line + word + " "
            if draw.textlength(test_line, font=font) <= max_width:
                line = test_line
            else:
                lines.append(line.rstrip())
                line = word + " "
                if len(lines) >= max_lines - 1:
                    break
        if line:
            lines.append(line.rstrip())

        # Append ellipsis if the original text was longer
        if not full_text.strip().endswith(clean_text.strip()):
            lines[-1] = lines[-1].rstrip(".!? ") + "..."

    return lines

# endregion
#region SVG Handler

def load_svg_icon(svg_path, size=(24, 24)):
    # Render SVG to PNG in memory
    png_data = cairosvg.svg2png(url=svg_path, output_width=size[0], output_height=size[1])
    icon_rgba = Image.open(io.BytesIO(png_data)).convert("RGBA")
    icon_bg = Image.new("RGBA", size, (255, 255, 255, 255))
    icon_flat = Image.alpha_composite(icon_bg, icon_rgba)
    icon_final = icon_flat.convert("RGB").quantize(palette=astro_constants.color_palette_img)
    icon = Image.new("RGBA", icon_rgba.size)
    icon.paste(icon_final)
    return icon
#endregion

# Display finished output
def astro_display(base_img, inky_display):
    final_img = base_img.rotate(90, expand=True)
    final_img = final_img.quantize(palette=astro_constants.color_palette_img)
    inky_display.set_image(final_img)
    inky_display.show()

# Handle location info
def get_location():
  # To GPS or not to GPS
  if config['location']['use_gps'] in yes_words:
    from pa1010d import PA1010D
    gps = PA1010D()
    try:
      result = gps.update()
    except OSError as error:
      # GPS wasn't found
      # Initialise display
      inky_display, base_img, display_height, display_width, draw = init_display()
      align_center = display_width // 2
      message_top = "GPS enabled in config.ini but device not found"
      top_center = align_center - (draw.textlength(message_top, font=astro_constants.font) / 2)
      draw.text((top_center, 100), message_top, astro_constants.RED, font=astro_constants.font)
      draw.text((top_center, 200), str(error), astro_constants.RED, font=astro_constants.font)

      # Error Display
      astro_display(base_img, inky_display)
      exit()
    # Wait for GPS to stabilise
    latitude = None
    i = 0
    while True:
      if (gps.data['latitude'] != None) and (str(gps.data['latitude']) != "0.0"):
        if latitude == gps.data['latitude']:
          latitude = float(gps.data['latitude'])
          longitude = float(gps.data['longitude'])
          elevation = int(round(gps.data['altitude']))
          break
      latitude = gps.data['latitude']
      # Count how many times we've been in this loop
      i += 1
      # If it's too many, show a message on screen
      if i == 6: # 1 minute
        # Initialise display
        inky_display, base_img, display_height, display_width, draw = init_display()
        align_center = display_width // 2
        message_top = "Waiting for GPS"
        top_center = align_center - (draw.textlength(message_top, font=astro_constants.font) / 2)
        draw.text((top_center, 100), message_top, astro_constants.RED, font=astro_constants.font)
        # Display
        astro_display(base_img, inky_display)
      # If it's waaaaaay too many, give up and revert to config.ini
      if i == 90: # 15 minutes
        # Initialise display
        inky_display, base_img, display_height, display_width, draw = init_display()
        align_center = display_width // 2
        message_top = "GPS cannot locate us, use static config"
        top_center = align_center - (draw.textlength(message_top, font=astro_constants.font) / 2)
        draw.text((top_center, 100), message_top, astro_constants.RED, font=astro_constants.font)
        # Display
        astro_display(base_img, inky_display)
        # Quit out of this loop
        break
      result = gps.update()
      time.sleep(10)
  else:
    latitude = float(config['location']['latitude'])
    longitude = float(config['location']['longitude'])
    elevation = float(config['location']['elevation'])

  gps = None

  tztext = timezone_at(lng=longitude,lat=latitude)
  timezone = ZoneInfo(tztext)
  return(latitude, longitude, elevation, tztext, timezone)
