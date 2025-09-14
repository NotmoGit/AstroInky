from inky.eeprom import read_eeprom
from PIL import Image,ImageFont

# Colour stuff
# There are 2 versions of the 7.3" Inky Impression
# Work out which one we have and what colours it supports
display = read_eeprom()
if display is None:
  print("Could not detect your Inky Impression")
  exit()
if display.get_color() == "spectra6":
  INKY_COLORS = {
      "BLACK":  (0, 0, 0),
      "WHITE":  (255, 255, 255),
      "YELLOW":    (255, 255, 0),
      "RED":  (255, 0, 0),
      "BLUE":   (0, 0, 255),
      "GREEN": (0, 255, 0)
  }
  BLACK  = INKY_COLORS["BLACK"]
  WHITE  = INKY_COLORS["WHITE"]
  RED    = INKY_COLORS["RED"]
  GREEN  = INKY_COLORS["GREEN"]
  BLUE   = INKY_COLORS["BLUE"]
  YELLOW = INKY_COLORS["YELLOW"]
  color_palette = [
      0, 0, 0,         # 0: Black
      255, 255, 255,   # 1: White
      255, 0, 0,       # 2: Red
      0, 255, 0,       # 3: Green
      0, 0, 255,       # 4: Blue
      255, 255, 0,     # 5: Yellow
  ] + [0, 0, 0]        # Fill the rest with black
elif display.get_color() == "7colour":
  INKY_COLORS = {
      "BLACK":  (0, 0, 0),
      "WHITE":  (255, 255, 255),
      "YELLOW":    (255, 255, 0),
      "RED":  (255, 0, 0),
      "BLUE":   (0, 0, 255),
      "GREEN": (0, 255, 0),
      "ORANGE": (255, 128, 0)
  }
  BLACK  = INKY_COLORS["BLACK"]
  WHITE  = INKY_COLORS["WHITE"]
  RED    = INKY_COLORS["RED"]
  GREEN  = INKY_COLORS["GREEN"]
  BLUE   = INKY_COLORS["BLUE"]
  YELLOW = INKY_COLORS["YELLOW"]
  ORANGE = INKY_COLORS["ORANGE"]
  color_palette = [
      0, 0, 0,         # 0: Black
      255, 255, 255,   # 1: White
      255, 0, 0,       # 2: Red
      0, 255, 0,       # 3: Green
      0, 0, 255,       # 4: Blue
      255, 255, 0,     # 5: Yellow
      255, 128, 0      # 6: Orange
  ] + [0, 0, 0]        # Fill the rest with black
else:
  print("Could not detect what colour palette your Inky Impression supports")
  exit()

bw_palette = [
    0, 0, 0,         # Black
    255, 255, 255    # White
] + [0, 0, 0]
bw_palette_img = Image.new("P", (16, 16))
bw_palette_img.putpalette(bw_palette)
color_palette_img = Image.new("P", (16, 16))
color_palette_img.putpalette(color_palette)
#endregion
#region TEXT, FONT & ICON SETTINGS
#FONTS
font = ImageFont.truetype("fonts/Merriweather-VariableFont_opsz,wdth,wght.ttf", 18)
font_path = "fonts/Merriweather-VariableFont_opsz,wdth,wght.ttf"
font_large = ImageFont.truetype("fonts/Merriweather-VariableFont_opsz,wdth,wght.ttf", 24)
font_small = ImageFont.truetype("fonts/Merriweather-VariableFont_opsz,wdth,wght.ttf", 12)
ascent, descent = font.getmetrics()                                                 #gets the height (ascent and descent) of the font
font_height = ascent + descent
line_spacing = font_height * 2
#ICONS
icon_size_lg = (font_height * 2, font_height * 2)
icon_size_sm = (font_height, font_height)
icon_size_xl = (font_height * 10, font_height * 10)
#TEXTWRAPPING
nav_y = 10
